import cvdp
from cvdp.base import *
from cvdp import cluster
from cvdp import data_cvdp
import argparse

# 判断脚本/可执行文件
def myenv() -> tuple:
    if getattr(sys, 'frozen', False):
        home = os.path.dirname(os.path.abspath(sys.executable))
        pause_before_exit = True
    else:
        home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pause_before_exit = False
    return (refine_path(home), pause_before_exit)

# 全局常量
HOME, PAUSE_BEFORE_EXIT = myenv()

def parse_arguments():
    parser = argparse.ArgumentParser(description=cvdp.DESCRIPTION)
    for i in range(len(cvdp.ARGS)):
        parser.add_argument(*cvdp.ARGS[i][0], **cvdp.ARGS[i][1])
    args = parser.parse_args()
    return args

def check_args(args) -> Tuple(bool, str, str):
    if args.folds <= 0:
        return (False, "--folds", "")
    if args.n_clusters <= 0:
        return (False, "--n-clusters", "")
    if not (0<args.external_test_ratio<1):
        return (False, "--external_test_ratio", "")
    return (True, "", "")

def main():
    args = parse_arguments()
    check_res = check_args(args)
    if not check_res[0]:
        raise RuntimeError(f"Invalid argument: {check_res[1]}. {check_res[2]}")
    data_raw = data_cvdp.from_csv(args.data_path)
    structures = cluster.molecules(data_raw, args.structure_column_header)
    structures.calc_similarity()
    structures.cluster(n_clusters=args.n_clusters)
    structures.split_data(folds=args.folds, external_test_ratio=args.external_test_ratio)
    output_path_home = refine_path(args.output_dir)
    write_data_paras = []
    sections = ['train', 'test']
    folds = [None] + [i for i in range(args.folds)]
    for section in sections:
        for fold in folds:
            if fold is None:
                para = (section, fold, f"{output_path_home}/{section}.csv")
            else:
                os.makedirs(f"{output_path_home}/fold_{fold}", exist_ok=True)
                if section == 'test':
                    para = (section, fold, f"{output_path_home}/fold_{fold}/validate.csv")
                else:
                    para = (section, fold, f"{output_path_home}/fold_{fold}/train.csv")
            write_data_paras.append(para)
    os.makedirs(f"{output_path_home}", exist_ok=True)
    for para in write_data_paras:
        data_cvdp.to_csv(structures.output_mols(section=para[0], fold=para[1]), para[2])

if __name__ == '__main__':
    main()
    if PAUSE_BEFORE_EXIT:
        a = input()
    pass
