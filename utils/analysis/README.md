# Analysis README
Project: shipwreck-linked-data-pipeline
Created: 2025-12-03

## Contents of the Analysis Utilities
All utility scripts are run against the files in the get_datasets dictionary in globals.py

| Script | Description                                              |
| -- | -- |----------------------------------------------------------|
| detect-csv-column_type.py | Infers column datatypes and writes each to a separate file |
| generate-csvstats.py | Generates CSV statistics using the CSVKit library        |
| generate-table-schemas.py | Generate tableschema representations of the source datasets. See [https://specs.frictionlessdata.io//table-schema/](https://specs.frictionlessdata.io//table-schema/) |
| get-shapes.py | Write dataframe shapes to markdown table |
| unique-values.py | Generate a workbook where each worksheet contains the unique values for a column in a dataframe for each dataset|
