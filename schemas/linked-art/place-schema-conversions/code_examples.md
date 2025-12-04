# Practical Code Examples for Linked Art Place Data

This document provides working code examples for loading, querying, and transforming Place data across different programming languages and environments.

## Python Examples

### Basic Loading and Querying with RDFLib

```python
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS

# Define namespaces
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

# Load the data
g = Graph()
g.parse('place.ttl', format='turtle')

# Find all places
print("All Places:")
for place in g.subjects(RDF.type, CRM.E53_Place):
    label = g.value(place, RDFS.label)
    print(f"  {place} - {label}")

# Find places with coordinates
print("\nPlaces with coordinates:")
for s, o in g.subject_objects(CRM.P168_place_is_defined_by):
    label = g.value(s, RDFS.label)
    print(f"  {label}: {o}")

# Find hierarchical relationships
print("\nPlace hierarchy:")
for place in g.subjects(CRM.P89_falls_within, None):
    place_label = g.value(place, RDFS.label)
    for parent in g.objects(place, CRM.P89_falls_within):
        parent_label = g.value(parent, RDFS.label)
        print(f"  {place_label} is part of {parent_label}")
```

### Converting Between Formats

```python
from rdflib import Graph

# Load Turtle, export as JSON-LD
g = Graph()
g.parse('place.ttl', format='turtle')

# Export with context
context = {
    "@vocab": "http://www.cidoc-crm.org/cidoc-crm/",
    "label": "http://www.w3.org/2000/01/rdf-schema#label",
    "type": "@type",
    "id": "@id"
}

jsonld_str = g.serialize(format='json-ld', context=context, indent=2)
with open('place_custom.jsonld', 'w') as f:
    f.write(jsonld_str)
```

### SPARQL Queries

```python
from rdflib import Graph

g = Graph()
g.parse('place.ttl', format='turtle')

# Query for places and their types
query = """
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?place ?label ?type ?typeLabel
WHERE {
  ?place a crm:E53_Place ;
         rdfs:label ?label .
  OPTIONAL {
    ?place crm:P2_has_type ?type .
    ?type rdfs:label ?typeLabel .
  }
}
"""

results = g.query(query)
for row in results:
    print(f"{row.label}: {row.typeLabel if row.typeLabel else 'No type'}")
```

### Create New Place Programmatically

```python
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
AAT = Namespace("http://vocab.getty.edu/aat/")

g = Graph()
g.bind("crm", CRM)
g.bind("rdfs", RDFS)

# Create a new place
place_uri = URIRef("https://example.org/place/smithsonian-nmnh")
g.add((place_uri, RDF.type, CRM.E53_Place))
g.add((place_uri, RDFS.label, Literal("National Museum of Natural History")))
g.add((place_uri, CRM.P2_has_type, AAT["300005768"]))  # museums

# Add coordinates
g.add((place_uri, CRM.P168_place_is_defined_by, 
       Literal("POINT(-77.0260 38.8913)")))

# Add parent location
dc_uri = URIRef("https://example.org/place/washington-dc")
g.add((dc_uri, RDF.type, CRM.E53_Place))
g.add((dc_uri, RDFS.label, Literal("Washington, D.C.")))
g.add((place_uri, CRM.P89_falls_within, dc_uri))

# Serialize
print(g.serialize(format='turtle'))
```

## JavaScript/Node.js Examples

### Using rdf-ext

```javascript
const rdf = require('rdf-ext');
const ParserN3 = require('@rdfjs/parser-n3');
const fs = require('fs');

// Parse Turtle file
const parser = new ParserN3();
const quadStream = parser.import(fs.createReadStream('place.ttl'));

const dataset = rdf.dataset();

quadStream.on('data', quad => {
  dataset.add(quad);
});

quadStream.on('end', () => {
  console.log(`Loaded ${dataset.size} quads`);
  
  // Query for places
  const CRM_E53_Place = rdf.namedNode('http://www.cidoc-crm.org/cidoc-crm/E53_Place');
  const RDF_type = rdf.namedNode('http://www.w3.org/1999/02/22-rdf-syntax-ns#type');
  
  for (const quad of dataset.match(null, RDF_type, CRM_E53_Place)) {
    console.log('Place:', quad.subject.value);
  }
});
```

### Using SPARQL with Oxigraph

```javascript
const oxigraph = require('oxigraph');

const store = new oxigraph.Store();
store.load('place.ttl', 'text/turtle');

const query = `
  PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  
  SELECT ?place ?label WHERE {
    ?place a crm:E53_Place ;
           rdfs:label ?label .
  }
`;

const results = store.query(query);
for (const binding of results) {
  console.log(binding.get('label').value);
}
```

## PHP/Laravel Examples

### Using EasyRDF

```php
<?php
require_once 'vendor/autoload.php';

use EasyRdf\Graph;
use EasyRdf\Namespace;

// Register namespaces
Namespace::set('crm', 'http://www.cidoc-crm.org/cidoc-crm/');

// Load the graph
$graph = new Graph();
$graph->parseFile('place.ttl', 'turtle');

// Find all places
$places = $graph->resourcesMatching('rdf:type', 'crm:E53_Place');

foreach ($places as $place) {
    echo "Place: " . $place->label() . "\n";
    
    // Get coordinates if available
    $coords = $place->get('crm:P168_place_is_defined_by');
    if ($coords) {
        echo "  Coordinates: " . $coords . "\n";
    }
    
    // Get parent locations
    $parents = $place->allResources('crm:P89_falls_within');
    foreach ($parents as $parent) {
        echo "  Part of: " . $parent->label() . "\n";
    }
}
```

### Laravel Integration

```php
<?php
namespace App\Services;

use EasyRdf\Graph;
use EasyRdf\Namespace;

class LinkedArtService
{
    protected $graph;
    
    public function __construct()
    {
        Namespace::set('crm', 'http://www.cidoc-crm.org/cidoc-crm/');
        $this->graph = new Graph();
    }
    
    public function loadPlace($uri)
    {
        $this->graph->load($uri, 'turtle');
        return $this->graph->resource($uri);
    }
    
    public function getPlaceHierarchy($placeUri)
    {
        $place = $this->graph->resource($placeUri);
        $hierarchy = [];
        
        $current = $place;
        while ($current) {
            $hierarchy[] = [
                'uri' => (string)$current->getUri(),
                'label' => $current->label(),
                'type' => $this->getPlaceType($current)
            ];
            
            $parent = $current->get('crm:P89_falls_within');
            $current = $parent ? $parent : null;
        }
        
        return array_reverse($hierarchy);
    }
    
    private function getPlaceType($place)
    {
        $type = $place->get('crm:P2_has_type');
        return $type ? $type->label() : null;
    }
}
```

## R Examples

### Using rdflib

```r
library(rdflib)
library(dplyr)

# Load the RDF data
rdf <- rdf_parse("place.ttl", format = "turtle")

# Query with SPARQL
query <- '
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?place ?label ?coords WHERE {
  ?place a crm:E53_Place ;
         rdfs:label ?label .
  OPTIONAL { ?place crm:P168_place_is_defined_by ?coords }
}
'

results <- rdf_query(rdf, query)
print(results)

# Extract coordinates for mapping
places_with_coords <- results %>%
  filter(!is.na(coords)) %>%
  mutate(
    lon = sub("POINT\\(([^ ]+) .*\\)", "\\1", coords),
    lat = sub("POINT\\([^ ]+ ([^)]+)\\)", "\\1", coords)
  )

print(places_with_coords)
```

## SQL/SPARQL Endpoint Examples

### Apache Jena Fuseki Query

```sparql
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>

# Find all places within a bounding box
SELECT ?place ?label ?coords
WHERE {
  ?place a crm:E53_Place ;
         rdfs:label ?label ;
         crm:P168_place_is_defined_by ?coords .
  
  # This would require GeoSPARQL support
  # FILTER(geof:within(?coords, "POLYGON((...))"^^geo:wktLiteral))
}
ORDER BY ?label
```

### Complex Hierarchy Query

```sparql
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# Find all places and their complete hierarchy path
SELECT ?place ?label 
       (GROUP_CONCAT(?parentLabel; separator=" > ") AS ?path)
WHERE {
  ?place a crm:E53_Place ;
         rdfs:label ?label .
  
  OPTIONAL {
    ?place crm:P89_falls_within+ ?parent .
    ?parent rdfs:label ?parentLabel .
  }
}
GROUP BY ?place ?label
ORDER BY ?path ?label
```

## Database Integration Examples

### PostgreSQL with pgrdf

```sql
-- Create table from N-Triples
CREATE TABLE place_triples (
    subject TEXT,
    predicate TEXT,
    object TEXT
);

-- Load N-Triples file
\copy place_triples FROM 'place.nt' WITH (FORMAT csv, DELIMITER E'\t');

-- Query for places
SELECT DISTINCT subject, object as label
FROM place_triples
WHERE predicate = '<http://www.w3.org/2000/01/rdf-schema#label>'
  AND EXISTS (
    SELECT 1 FROM place_triples t2 
    WHERE t2.subject = place_triples.subject 
      AND t2.predicate = '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'
      AND t2.object = '<http://www.cidoc-crm.org/cidoc-crm/E53_Place>'
  );
```

### MongoDB with JSON-LD

```javascript
const { MongoClient } = require('mongodb');
const fs = require('fs');

async function loadPlaces() {
  const client = new MongoClient('mongodb://localhost:27017');
  await client.connect();
  
  const db = client.db('linked_art');
  const collection = db.collection('places');
  
  // Load JSON-LD
  const jsonld = JSON.parse(fs.readFileSync('place.jsonld', 'utf8'));
  
  // Extract Place documents (simplified)
  const places = jsonld['@graph'].filter(item => 
    item['@type'] === 'http://www.cidoc-crm.org/cidoc-crm/E53_Place'
  );
  
  // Insert into MongoDB
  await collection.insertMany(places);
  
  // Query example
  const result = await collection.find({
    'http://www.cidoc-crm.org/cidoc-crm/P168_place_is_defined_by': {
      $exists: true
    }
  }).toArray();
  
  console.log('Places with coordinates:', result.length);
  
  await client.close();
}

loadPlaces();
```

## Validation Examples

### SHACL Validation with pySHACL

```python
from pyshacl import validate
from rdflib import Graph

# Load data and shapes
data_graph = Graph()
data_graph.parse('place.ttl', format='turtle')

shapes_graph = Graph()
shapes_graph.parse('place.ttl', format='turtle')  # Contains SHACL shapes

# Validate
conforms, results_graph, results_text = validate(
    data_graph,
    shacl_graph=shapes_graph,
    inference='rdfs',
    abort_on_first=False
)

print(f"Conforms: {conforms}")
if not conforms:
    print("Validation Results:")
    print(results_text)
```

## Testing Examples

### Unit Test for Place Creation

```python
import unittest
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

class TestPlaceCreation(unittest.TestCase):
    def setUp(self):
        self.CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        self.g = Graph()
        self.g.bind("crm", self.CRM)
        
    def test_minimal_place(self):
        """Test that a minimal place has required properties"""
        place = URIRef("https://example.org/place/test")
        self.g.add((place, RDF.type, self.CRM.E53_Place))
        self.g.add((place, RDFS.label, Literal("Test Place")))
        
        # Verify required triples exist
        self.assertTrue((place, RDF.type, self.CRM.E53_Place) in self.g)
        self.assertTrue((place, RDFS.label, None) in self.g)
        
    def test_place_hierarchy(self):
        """Test that place hierarchy is correctly modeled"""
        city = URIRef("https://example.org/place/city")
        state = URIRef("https://example.org/place/state")
        
        self.g.add((city, self.CRM.P89_falls_within, state))
        
        # Verify relationship
        self.assertTrue((city, self.CRM.P89_falls_within, state) in self.g)

if __name__ == '__main__':
    unittest.main()
```

These examples should help you get started with working with Linked Art Place data in various environments!
