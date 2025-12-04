import pandas as pd
import globals as cfg

# Return Dataframe Shapes as Markdown Table

# Get Source Datasets Dataframe Shapes
today = cfg.get_today()
root_dir = cfg.get_project_root()
datasets = cfg.get_datasets()
md_file = str(root_dir) + '/data/profiles/md/dataset-shapes-table.md'

shape_dict = {}
for dataset in datasets:
    source_filename = dataset
    source_file = str(root_dir) + '/data/input/remapped/' + dataset

    df = pd.read_csv(source_file, sep=',', lineterminator='\n', encoding='utf-8', encoding_errors='ignore', on_bad_lines='skip', dtype=object)
    shape_dict[dataset] = df.shape

    df_shapes = pd.DataFrame.from_dict(shape_dict, orient='index', columns=['rows', 'columns'])
    df_shapes['dataset'] = source_filename
    md = df_shapes.to_markdown()
    with open(md_file, 'w') as f:
        f.write(md)
