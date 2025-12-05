# Shipwreck Linked Data Pipeline
This proof-of-concept demonstrates a Python-based ETL (Extract, Transform, Load) pipeline that converts tabular shipwreck data  into Linked Art-compliant JSON-LD, enabling their integration with and enrichment of existing internal collections.

## Project Scope
General project documentation stored under [project-docs](/project-docs) and transformation results under [/pipeline/linked-art](/pipeline/linked-art) covers three key areas:
1. **Dataset Selection** - Criteria and rationale for choosing shipwreck data sources (detailed in the [shipwreck-datasets README](sources/datasets/README.md))
2. **Transformation methodology** – Detailed procedures and transformation reports for converting tabular data into Linked Art format
3. **Data modeling** – Overview of mapping shipwreck records to [Linked Open Usable Data (LOUD)](https://linked.art/loud/) specification through [Linked Art](https://linked.art/).

## Semantic Connections
The project also explores potential semantic relationships between shipwreck records and other linked resources, with examples illustrated in the diagram below.
![](project-docs\diagrams\ShipwreckLinkages_20251204.png)

Final transformations and associated documentation generated with the aid of the Claude Sonnet 4.5 LLM Model    
  
The Shipwreck Places JSON-LD and Shipwreck Events JSON-LD are generated separately and named accordingly for illustration purposes. The two files would be merged prior to being ingested into a production environment index, the 


## Project Directory Structure
```
rdf-etl-pipelines/
├── data/                   | Input and output data
│   ├── input/              | Pipeline Input data
│   │   ├── remapped/       | Remapped verbatim datasets
│   │   └── verbatim/       | Sources datasets in their verbatim form
│   ├── profiles/           | Output from the profiling utility scripts
│   │   ├── csvstats/       | CSKKit csvstats output
│   │   ├── dtypes/         | Column datatype inferences
│   │   ├── md/             | Markdown output files
│   │   ├── tableschemas/   | Tableschemes output files
│   │   └── unique-values/  | Unique value sets for source datasets
├── pipeline/               | Pipeline output and transformation reports
│   ├── linked-art/         | Pipeline scripts for generating Linked Art complicant JSON-LD from tabular data, includes both process reports, scripts, and reference documentation
│   │   ├── output/         | Linked Art transformation output
├── project-docs/           | Project documentation
├── schemas/                | Target schemas
│   ├── linked-art/         | Linked Art Schemas applicable to this project
│   └── SeaLiT/             | SeaLit Ontology - An extension of CIDOC-CRM for the modelling of Maritime History information
├── sources/                | Source files
│   └── datasets/           | Source datasets
└── utils/                  | Project Utilities
    ├── analysis/           | Analysis utilities for analyzing the structure and content of source datasets
    ├── general/            | General utility scripts 
    └── transformations/    | Data transformations including column remappings
```
## I/O Flows
| Sequence                                                                                        | Description                              |
|-------------------------------------------------------------------------------------------------|------------------------------------------|
| source/datasets > data/input/verbatim                                                           | Copy source dataset to verbatim folder   |
| utils/transformations/remap-columns.py > data/input/remapped                                    | Apply column remappings                  |
| utils/analysis/generate-csvstats.py > data/profiles/csvstats                                    | Generate CSV Stats                       |
| utils/analysis/generate-dtypes.py > data/profiles/col-dtypes                                    | Infer column datatypes                   |
| utils/analysis/generate-tableschemas.py > data/profiles/tableschemas                            | Generate tableschemas                    |
| utils/analysis/generate-unique-values.py > data/profiles/unique-values                          | Generate unique value reports            |
| pipeline/linked-art/shipwreck_transformer.py > pipeline/linked-art/output/places.json           | Convert CSV to Linked Art JSON-LD        |
| pipeline/linked-art/shipwreck_transformer.py > pipeline/linked-art/output/shipwreck_events.json | Shipwrecks dataset as Linked Art JSON-LD |
| pipeline/linked-art/shipwreck_transformer.py > pipeline/linked-art/output/transformation_stats.json | Statistics from transformation process   |


## Source Data
All source datasets were downloaded from web-based resources listed under the sources README file and in the source metadata YAML files.

## Process
To initiate the pipeline, please refer to [procedure.md](project-docs/procedure.md) in project-docs.

## Resources
A collection of resources used in the development of this project provides further information on the project scope and methodology.  

| Title | URL                                                                                                          |
| -- |--------------------------------------------------------------------------------------------------------------|
| Project LUX Data Pipeline | [https://https://github.com/project-lux/data-pipeline](https://https://github.com/project-lux/data-pipeline) | 
| LUX: Yale Collections Discovery | [https://lux.collections.yale.edu/](https://lux.collections.yale.edu/)                                       |
| Linked Art | [https://linked.art/](https://linked.art/)                                                                       |
| SeaLit Project | [https://www.sealitproject.eu/](https://www.sealitproject.eu/) |

## Publications
* Fafalios, P., Kritsotaki, A. and Doerr, M., 2023. The SeaLiT ontology–an extension of CIDOC-CRM for the modeling and integration of maritime history information. ACM Journal on Computing and Cultural Heritage, 16(3), pp.1-21. [https://doi.org/10.1145/3586080](https://doi.org/10.1145/3586080)
* Newbury, D., 2018, September. Loud: Linked open usable data and linked.art. In 2018 CIDOC Conference (pp. 1-11). [URL](https://cidoc.mini.icom.museum/wp-content/uploads/sites/6/2021/03/CIDOC2018_paper_153.pdf)
* Raemy, J.A., 2023. Characterising the IIIF and Linked Art communities (Doctoral dissertation, University of Basel). [URL](https://hal.science/hal-04162572/document)
* Raemy, J.A., 2024. Linked Open Usable Data for cultural heritage: perspectives on community practices and semantic interoperability (Doctoral dissertation, University of Basel).  [URL](https://phd.julsraemy.ch/thesis.html)
* Sanderson, R., 2024. Implementing Linked Art in a Multi-Modal Database for Cross-Collection Discovery. Open Library of Humanities, 10(2). [https://doi.org/10.16995/olh.15407](https://doi.org/10.16995/olh.15407)

## Contact  
Ben Norton  
michaelnorton.ben@gmail.com  
Last Modified: 2025-12-04



