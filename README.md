# Shipwreck Linked Data Pipeline
A proof of concept extract, transform, load (ETL) pipeline for extracting and transforming shipwreck data from various sources into Linked Data that conforms to the Linked Art Model using Python.
The goal is to leverage an external dataset for the enrichment of internal datasets. The project describes the selection process, transformation procedures, and conversion of a tabular dataset into JSON-LD that complies with the
[Linked Open Usable Data](https://linked.art/loud/) specification, [Linked Art](https://linked.art/).  

Information about shipwreck datasets including the selection criteria can be found in the [shipwreck-datasets](project-docs/shipwreck-datasets.md) README file.  

Hypothetical linkages between shipwrecks and linked resources are also described in the project documentation and illustrated in the diagram below.

![](project-docs\diagrams\ShipwreckLinkages_20251204.png)


## Project Directory Structure
```
rdf-etl-pipelines/
├── data/                   | Input and output data
│   ├── output/             | Linked Data output
│   ├── input/              | Pipeline Input data
│   │   ├── remapped/       | Remapped verbatim datasets
│   │   └── verbatim/       | Sources datasets in their verbatim form
│   ├── profiles/           | Output from the profiling utility scripts
│   │   ├── csvstats/       | CSKKit csvstats output
│   │   ├── dtypes/         | Column datatype inferences
│   │   ├── md/             | Markdown output files
│   │   ├── tableschemas/   | Tableschemes output files
│   │   └── unique-values/  | Unique value sets for source datasets
├── project-docs/           | Project documentation
├── schemas/                | Target schemas
│   ├── linked-art/         | Linked Art Schemas applicable to this project
│   └── SeaLiT/             | SeaLit Ontology - An extension of CIDOC-CRM for the modelling of Maritime History information
├── sources/                | Source files
│   └── datasets/           | Source datasets
└── utils/                  | Project Utilities
    ├── analysis/           | Analysis utilities for analyzing the structure and content of source datasets
    ├── general/            | General utility scripts 
    ├── converstion/        | Linked Data conversion scripts
    └── transformations/    | Data transformations including column remappings
```

## Source Data
All source datasets were downloaded from web-based resources listed under the sources README file and in the source metadata yaml files.


## Initialize Pipeline
To initiate the pipeline, please see [procedure.md](project-docs/procedure.md) under project-docs.


## Linkages
A diagram illustrating the hypothetical linkages between a shipwreck record and linked resources via 
the [Linked Art Model](https://linked.art/)



