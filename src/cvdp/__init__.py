__version__ = '0.1.0'
__all__ = ['base', 'cluster', 'data_cvdp']

DESCRIPTION = ''
ARGS = [
    [
        ['-f', '--folds'],
        {
            'type': int,
            'dest': 'folds',
            'help': 'Specify the number of folds during cross-validation (default: 10).',
            'required': False,
            'default': 10
        }
    ],
    [
        ['data_path'],
        {
            'type': str,
            'help': 'Specify the file containing a series of SMILES data of the structures.',
        }
    ],
    [
        ['-n', '--n-clusters'],
        {
            'type': int,
            'dest': 'n_clusters',
            'help': 'Specify the number of clusters.',
            'required': True,
        }
    ],
    [
        ['-c', '--column-header'],
        {
            'type': str,
            'dest': 'structure_column_header',
            'help': 'Specify the column header that records the structure (default: smiles).',
            'required': False,
            'default': 'smiles'
        }
    ],
    [
        ['--et-ratio'],
        {
            'type': float,
            'dest': 'external_test_ratio',
            'help': 'Specify the external test ratio (default: 0.2).',
            'required': False,
            'default': 0.2
        }
    ],
    [
        ['-o', '--output-dir'],
        {
            'type': str,
            'dest': 'output_dir',
            'help': 'Specify a directory to save results (default: ./model_data_out).',
            'required': False,
            'default': './model_data_out'
        }
    ],
]
