from datetime import date
from pathlib import Path
import globals as cfg
import pandas as pd
from mappings import get_nj_maritime_shipwreck_database_mappings, get_maritime_heritage_column_mappings, \
	get_emodnet_ha_heritage_shipwrecks_column_mappings, get_nj_maritime_shipwreck_database_column_subset

# Remaps Columns in Source Datasets to Columns Defined in Mappings File (mappings.py)

today = cfg.get_today()
root_dir = cfg.get_project_root()
datasets = cfg.get_datasets()

# ----------------------------------------------------------------------------------
## Maritime Heritage Shipwrecks Database
def rename_maritime_shipwreck_columns(input_file, output_file=None):
	# Column mapping dictionary
	column_mapping = get_maritime_heritage_column_mappings()
	df = pd.read_csv(input_file)
	df = df.rename(columns=column_mapping)
	if output_file:
		df.to_csv(output_file, index=False)
		print(f"Renamed CSV saved to: {output_file}")
	return df

def remap_maritime_heritage_columns():
	source_file = str(root_dir) + '/data/input/verbatim/Marine_Heritage_Shipwrecks_Database.csv'
	target_csv = str(root_dir) + '/data/input/remapped/maritime_heritage_shipwrecks_database.csv'
	df_remapped = rename_maritime_shipwreck_columns(source_file)
	df_remapped.to_csv(target_csv, index=False)

# ----------------------------------------------------------------------------------
## NJ Maritime Shipwreck Database
def rename_nj_shipwreck_database_columns(input_file, output_file=None):
	# Column mapping dictionary
	column_mapping = get_nj_maritime_shipwreck_database_mappings()
	df = pd.read_csv(input_file)
	df = df.rename(columns=column_mapping)
	if output_file:
		df.to_csv(output_file, index=False)
		print(f"Renamed CSV saved to: {output_file}")
	return df

def remap_nj_shipwreck_database_columns():
	source_file = str(root_dir) + '/data/input/verbatim/ShipwreckDatabase120924SR.csv'
	target_csv = str(root_dir) + '/data/input/remapped/nj_maritime_shipwreck_database.csv'
	df_remapped = rename_nj_shipwreck_database_columns(source_file)
	#print(df_remapped.columns.tolist())
	df_remapped.to_csv(target_csv, index=False)

# ----------------------------------------------------------------------------------
## EMODnet Heritage Shipwrecks
def rename_emodnet_heritage_shipwrecks_columns(input_file, output_file=None):
	# Column mapping dictionary
	column_mapping = get_emodnet_ha_heritage_shipwrecks_column_mappings()
	df = pd.read_csv(input_file)
	df = df.rename(columns=column_mapping)
	if output_file:
		df.to_csv(output_file, index=False)
		print(f"Renamed CSV saved to: {output_file}")
	return df

def remap_emodnet_heritage_shipwrecks_columns():
	source_file = str(root_dir) + '/data/input/verbatim/EMODnet_HA_Heritage_Shipwrecks_20220720.csv'
	target_csv = str(root_dir) + '/data/input/remapped/emodnet_ha_heritage_shipwrecks.csv'
	df_remapped = rename_emodnet_heritage_shipwrecks_columns(source_file)
	df_remapped.to_csv(target_csv, index=False)

# ----------------------------------------------------------------------------------
# Create dataset using subset of NJ Maritime Shipwreck Database
def subset_nj_shipwreck_database_columns():
	source_file = str(root_dir) + '/data/input/remapped/nj_maritime_shipwreck_database.csv'
	target_csv = str(root_dir) + '/data/input/remapped/nj_maritime_shipwreck_database_subset.csv'
	df = pd.read_csv(source_file)
	subset = get_nj_maritime_shipwreck_database_column_subset()

	# Write new dataframe with subset of columns
	df_subset = df[subset]
	# Omit records where latitude or dateLost are null
	filtered_df = df_subset[df_subset['latitude'].notnull()]
	filtered_df = df_subset[df_subset['dateLost'].notnull()]
	# Write new dataframe to file
	filtered_df.to_csv(target_csv, index=False)





# Execute Functions
if __name__ == '__main__':
	remap_maritime_heritage_columns()
	remap_nj_shipwreck_database_columns()
	remap_emodnet_heritage_shipwrecks_columns()
	subset_nj_shipwreck_database_columns()
