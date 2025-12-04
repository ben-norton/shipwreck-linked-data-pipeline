from datetime import date
import os
import globals as cfg
from pathlib import Path
root_dir = Path(__file__).resolve().parents[2]

# This script generates CSV stats for CSV datasets using the CSVKit Library.
# Files are specified by dataset name (see globals.py)

datasets = cfg.get_datasets()

today = date.today()
ts = today.strftime("%Y%m%d")

for dataset in datasets:
    # Set source file
    source_file = str(root_dir) + '/data/input/remapped/' + dataset
    # Set destination folder
    target_path = str(root_dir) + '/data/profiles/csvstats/'
    datasetName = dataset.replace('.csv','')
    # Set target file containing the full results
    target_full_report = str(target_path) + '/' + datasetName + '-full-csvstats.txt'
    # Set target file containing the unique value counts
    target_uniques_report = str(target_path) + '/' + datasetName + '-unique-csvstats.txt'

    f = source_file

    # Unique Counts
    os.system("csvstat -z 10000000 --unique " + f + " > " + target_uniques_report)

    # Full Stats
    os.system("csvstat -z 10000000 " + f + " > " + target_full_report)