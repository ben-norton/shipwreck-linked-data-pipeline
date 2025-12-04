# Pipeline Transformation Procedure

1. Indentify and download a dataset
2. Create a folder under the sources/datasets folder to store the source version of the dataset
3. Copy source dataset to the newly created folder
4. Capture dataset metadata by making a copy of the yaml template (source-metadata-template.yml), placing the copy inside the dataset folder, then completing the metadata fields.
5. Add dataset to the get_source_datasets dict using parent folder/filename
6. Copy source dataset to the data/input/verbatim folder
7. Creating column mapping and add to the mappings.py file under utils/transformations
8. Update remap columns with mapping (note the filename change from verbatim to snake casing)
9. Run remap-columns.py
10. A newly created file should be in the data/input/remapped folder
11. Run analysis scripts under utils\analysis
12. Assess profile results to select the most suitable dataset for the intended purpose - Enrich internal datasets through newly established linkages between classes
13. Run conversion scripts and document results in a dataset specific folder under project-docs.