from tableschema import Table, infer, Schema
from json_extract import GetValue2
import csv
import json
import os
from datetime import date
from pathlib import Path
import globals as cfg

analysis_type = 'column-lengths'

today = date.today()
ts = today.strftime("%Y%m%d")

root_dir = cfg.get_project_root()
datasets = cfg.get_datasets()

for dataset in datasets:
    source_filename = dataset

    source_file = str(root_dir) + '/data/input/remapped/' + dataset
    target_path = str(root_dir) + '/data/profiles/tableschemas'

    stemName = Path(dataset).stem
    stemName = str.lower(stemName)
    stemName = stemName.replace('_','-')
    table = Table(source_file)

    # Scan first 500 rows to determine datatype
    table.infer(limit=50, confidence=0.75)

    # Table Schema
    schema = table.schema.descriptor
    schema_json = json.dumps(schema, indent=4)

    # Column Names
    columns = table.headers

    # Column Schema (Name and Datatype)
    getColumns = GetValue2(schema)
    names = getColumns.get_values('name')
    datatypes = getColumns.get_values('type')
    columns_dict = dict(zip(names, datatypes))
    columns_json = json.dumps(columns_dict, indent=4)

    # Output (File + Path)
    base_filename = dataset
    outputSchema = os.path.join(dataset, target_path + '/' + base_filename + "-schema.json")
    columnsSchema = os.path.join(dataset, target_path + '/' + base_filename + "-columns.json")
    templateCsv = os.path.join(dataset, target_path + '/' + base_filename + "-template.csv")

    # Write Tableschema JSON
    with open(outputSchema, "w") as outfile:
        outfile.write(schema_json)
    table.schema.save(outputSchema)

    # Write template csv (blank with column headers only)
    with open(templateCsv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)

    # Write Column Schema JSON (Name + Datatype)
    with open(columnsSchema, "w") as outfile:
        outfile.write(columns_json)
