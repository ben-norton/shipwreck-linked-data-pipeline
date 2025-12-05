# shipwreck-datasets.md

## Overview
Shipwreck datasets offer a unique opportunity to establish linkages between multiple Linked Art classes and LUX object types in both the 
Cultural Heritage and Natural History domains. 
The primary criterion for selection of shipwreck data as the proof of concept was a combination of personal interest and the diversity of potential linkages. Once the general type of dataset was selected, a discovery phase yielded a collection of shipwreck datasets (see [Dataset README](../sources/datasets/README.md), which were subsequently evaluated for suitability, completeness, (perceived) quality, and 
consistency. For an overview of shipwreck semantics, see the SeaLiT ontology.

## General Procedure for Dataset Selection:
1. Identify and download multiple shipwreck datasets. 
2. Profile each dataset using the utility scripts. 
3. Use the generated profiles to assess each dataset for suitability, completeness, (perceived) quality, and consistency. In general, the most complete and consistent  dataset will yield the most linkages between resources, the ultimate goal of linked data architectures. Example criteria include:  
A. What is the completeness percentage for each column? Are there empty columns?  
B. Does the dataset include a dictionary of column names? If not, do all the columns make sense?  
C. Does the dataset contain latitude and longitude coordinates or just a location description?  
D. Are the ship names clear?  
E. Are the columns properly formatted (For the year column, are the values integers?)?  
4. Select the dataset and run the pipeline to produce a final Linked Art compliant JSON-LD dataset.   

## Hypothetical Shipwreck Concept Linkages
![](https://github.com/ben-norton/shipwreck-linked-data-pipeline/blob/main/project-docs/diagrams/ShipwreckLinkages_20251204.png)

