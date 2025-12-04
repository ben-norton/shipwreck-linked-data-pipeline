# shipwreck-datasets.md

## Overview
Shipwreck datasets offer a unique opportunity to establish linkages between multiple Linked Art classes and LUX object types in both the 
Cultural Heritage and Natural History domains. Linked data is a powerful tool for linking data across disciplines by interlinking resources. 
The primary criteria for selection of an external dataset was based on the theoretical relationships that can be established between the 
objects in the dataset and the objects in the LUX domain. Once the general type of dataset was selected, a collection of shipwreck datasets 
was identified (see [Dataset README](../sources/datasets/README.md) and evaluated for suitability, completeness, (perceived) quality, and 
consistency. For an overview of shipwreck semantics, see the SeaLiT ontology.

## General Procedure for Dataset Selection:
1. Identify and download multiple shipwreck datasets
2. Profile each dataset using the utility scripts
3. Use the generated profiles to assess each dataset for suitability, completeness, (perceived) quality, and consistency. In general, the more complete and consistent dataset will facilitate better linkages between resources, the ultimate goal of linked data architectures. Example criteria include:
A. How complete is the dataset?
B. Does the dataset contain latitude and longitude coordinates?
C. Are the ship names clear?
D. Are the columns properly formatted (For year column, are the values integers?)?  
4. 
4. Select the dataset and convert the CSV file into a Linked Art JSON-LD file.

## Hypothetical Shipwreck Concept Linkages
![](diagrams\ShipwreckLinkages_20251204.png)

