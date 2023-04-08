from cvdp.base import *
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from random import shuffle

def smiles_to_mol(value):
    return Chem.MolFromSmiles(value)

class molecule():
    def calc_morgan_fp(self):
        return AllChem.GetMorganFingerprintAsBitVect(self.mol, 2, 2048)

    def apply_cluster(self, cluster_index: int, cluster_index_header: str='cluster_index') -> None:
        self.properties[cluster_index_header] = cluster_index

    def __init__(self, info: Dict[str, any], structure_header: str='smiles', convert_func: Callable=smiles_to_mol) -> None:
        structure = {structure_header: info[structure_header]}
        self.structure = structure
        self.mol = convert_func(info[structure_header])
        self.morgan_fp = self.calc_morgan_fp()
        self.properties = {**structure, **info}

class molecules():
    def __init__(self, mols: List[Dict[str, any]], structure_header: str='smiles', convert_func: Callable=smiles_to_mol) -> None:
        self.mols = []
        for mol in mols:
            self.mols.append(molecule(mol, structure_header, convert_func))

    def calc_similarity(self) -> None:
        dis_matrix = []
        for i in range(len(self.mols)):
            fp = self.mols[i].morgan_fp
            fps = []
            for j in range(i+1):
                fps.append(self.mols[j].morgan_fp)
            dis_matrix.append(DataStructs.BulkTanimotoSimilarity(fp, fps, returnDistance=True))
        for i in range(len(self.mols)):
            for j in range(len(self.mols)):
                if j>= len(dis_matrix[i]):
                    dis_matrix[i].append(dis_matrix[j][i])
        self.dis_array = np.array(dis_matrix)

    def cluster_preview(self) -> None:
        if not hasattr(self, 'dis_array'):
            self.calc_similarity()
        linked_array = hierarchy.ward(self.dis_array)
        hierarchy.dendrogram(linked_array)
        plt.show()

    def cluster(self, n_clusters: int, cluster_index_header: str='cluster_index') -> None:
        self.cluster_library = {i: [] for i in range(n_clusters)}
        ward = AgglomerativeClustering(n_clusters)
        ward.fit(self.dis_array)
        for n,j in enumerate(ward.labels_):
            self.cluster_library[j].append(self.mols[n])
            self.mols[n].apply_cluster(cluster_index=j, cluster_index_header=cluster_index_header)
    
    def output_mols(self, section=None, fold=None) -> List[Dict]:
        res = []
        if section is None:
            for mol in self.mols:
                res.append(mol.properties)
        elif section == 'train':
            if fold is None:
                for mol in self.model_data['train']:
                    res.append(mol.properties)
            elif 0 <= int(fold) < len(self.model_data['cv']):
                for i in range(len(self.model_data['cv'])):
                    if fold != i:
                        for mol in self.model_data['cv'][i]:
                            res.append(mol.properties)
        elif section == 'test':
            if fold is None:
                for mol in self.model_data['test']:
                    res.append(mol.properties)
            elif 0 <= int(fold) < len(self.model_data['cv']):
                for mol in self.model_data['cv'][fold]:
                    res.append(mol.properties)
        return res
    
    def split_data(self, folds: int=10, external_test_ratio: float=0.2):
        model_data = {
            'cv': [],
            'test': [],
            'train': []
        }
        for j in range(folds):
            model_data['cv'].append([])

        cluster = deepcopy(self.cluster_library)
        for i in range(len(cluster)):
            shuffle(cluster[i])

        cv = []
        # test
        for i in range(len(cluster)):
            pos = round(len(cluster[i]) * external_test_ratio)
            model_data['test'] += cluster[i][:pos]
            train_data = cluster[i][pos:]
            model_data['train'] += deepcopy(train_data)
            cv.append(deepcopy(train_data))

        # cross validation
        for i in cv: # i: a cluster
            fold_size = round(len(i)/folds)
            available = len(i)
            cur = 0
            for j in range(folds):
                cur_fold = []
                if available > 0:
                    if available >= fold_size:
                        cur_fold = i[cur:cur+fold_size]
                        cur += fold_size
                        available -= fold_size
                    else:
                        cur_fold = i[cur:]
                        cur = len(i)
                        available = 0
                model_data['cv'][j] += cur_fold
        self.model_data = model_data
