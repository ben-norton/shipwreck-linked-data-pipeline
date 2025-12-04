# Pipeline Transformation Procedure

1. Download a dataset (pipeline assumes CSV format)
2. Create a folder under the sources/datasets folder to store the source version of the dataset
3. Copy source dataset to the newly created folder
4. Capture dataset metadata by making a copy of the yaml template (source-metadata-template.yml), placing the copy inside the dataset folder, then completing the metadata fields.
5. Add dataset to the get_source_datasets dict using parent folder/filename
6. Add remapped dataset to the get_datasets dict using the snake-casing filename
7. Copy source dataset to the data/input/verbatim folder
8. Creating column mapping and add to the mappings.py file under utils/transformations to rename columns in lower camel case
9. Update remap columns with mapping (note the filename change from verbatim to snake casing)
10. Run remap-columns.py
11. Verify the file generated in the data/input/remapped folder
12. Run analysis scripts under utils\analysis. These can be run in any order.
13. Assess profile results to select the most suitable dataset for the intended purpose - Enrich internal datasets through newly established linkages between classes
14. Run conversion scripts under pipeline/linked-art. See README for more details.