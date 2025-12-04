import os
from datetime import date
from pathlib import Path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_project_root() -> Path:
    return os.path.dirname(os.path.abspath(__file__))

def get_data_root() -> Path:
    return Path(get_project_root(), "data")

def get_today():
    today = date.today()
    ts = today.strftime("%Y%m%d")
    return ts

def get_source_datasets():
    datasets = [
        'marine_heritage_shipwrecks_database/Marine_Heritage_Shipwrecks_Database.csv',
        'nj_maritime_shipwreck_databases/ShipwreckDatabase120924SR.csv',
        'emodnet_ha_heritage_shipwrecks_20220720/EMODnet_HA_Heritage_Shipwrecks_20220720.csv',
        'wrecks_and_obstructions_in_AWOIS/Wrecks_and_Obstructions_in_AWOIS.csv'
    ]
    return datasets

def get_datasets():
    datasets = [
        'maritime_heritage_shipwrecks_database.csv',
        'nj_maritime_shipwreck_database.csv',
        'emodnet_ha_heritage_shipwrecks.csv',
    ]
    return datasets

# Get Selected Dataset (Selected Datasets are specifically chosen for a purpose)
# Target datasets usually contains one dataset, but may contain many
def get_target_datasets():
    dataset = [
        'ShipwreckDatabase120924SR.csv'
    ]
    return dataset