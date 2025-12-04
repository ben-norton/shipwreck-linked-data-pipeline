from datetime import date
from pathlib import Path
import globals as cfg
import pandas as pd
from mappings import get_nj_shipwreck_database_column_subset

# Generates a file with a specific subset of columns from a remapped dataset
# Must run remap-columns.py before running this script

today = date.today()
ts = today.strftime("%Y%m%d")

root_dir = cfg.get_project_root()

## Extract subset of columns and omit records where latitude or dateLost are null
def subset_nj_shipwreck_database_columns():
	source_file = str(root_dir) + '/data/input/remapped/ShipwreckDatabase120924SR_remapped.csv'
	target_csv = str(root_dir) + '/data/input/remapped/ShipwreckDatabase120924SR_subset.csv'
	df = pd.read_csv(source_file)
	subset = get_nj_shipwreck_database_column_subset()

	# Write new dataframe with subset of columns
	df_subset = df[subset]
	# Omit records where latitude or dateLost are null
	filtered_df = df_subset[df_subset['latitude'].notnull()]
	filtered_df = df_subset[df_subset['dateLost'].notnull()]
	# Write new dataframe to file
	filtered_df.to_csv(target_csv, index=False)

subset_nj_shipwreck_database_columns()