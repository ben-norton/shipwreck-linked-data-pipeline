import pandas as pd
from datetime import date
from pathlib import Path
import globals as cfg
import csv
# Return inferred datatypes for each column in dataset

today = cfg.get_today()
root_dir = cfg.get_project_root()
datasets = cfg.get_datasets()

target_path = str(root_dir) + '/data/output/'


for dataset in datasets:
	dtype_dict = {}
	source_file = str(root_dir) + '/data/input/remapped/' + dataset
	datasetName = dataset.replace('.csv', '')
	target_file = str(target_path) + datasetName + '-col-dtypes.csv'

	df = pd.read_csv(source_file, sep=',', lineterminator='\n', encoding='utf-8')
	dtype_dict['dataset'] = df.infer_objects().dtypes
	for col in df.columns:
		inferred_type = pd.api.types.infer_dtype(df[col])
		dtype = {'column': col, 'type': inferred_type}
#		dtype_dict[col] = inferred_type

	with open(target_file, "w", newline="") as f:
		w = csv.DictWriter(f, dtype_dict.keys())
		w.writerow(dtype_dict)



