# Linked Art Place Schema - RDF Conversions

This directory contains conversions of the Linked Art Place JSON Schema to various RDF serialization formats.

## Files Overview

### Full Examples (with SHACL shapes and detailed instances)

1. **place.ttl** - Turtle format (human-readable)
   - SHACL shape definition for Place validation
   - Detailed example: Raleigh, NC with full hierarchy
   - Uses CIDOC-CRM predicates
   - 97 triples

2. **place.nt** - N-Triples format (machine-readable)
   - Same content as place.ttl
   - Each triple on a separate line
   - Useful for bulk processing and database imports

3. **place.jsonld** - JSON-LD format
   - JSON representation of the RDF graph
   - Compatible with JSON tools
   - Includes @context for semantic mapping

### Minimal Examples (essential properties only)

4. **place-minimal.ttl** - Minimal Turtle examples
   - Bare minimum: just URI, type, and label
   - Simple place with basic properties
   - 9 triples
   - Good starting point for quick implementations

5. **place-minimal.nt** - Minimal N-Triples
   - Same as place-minimal.ttl in N-Triples format

6. **place-minimal.jsonld** - Minimal JSON-LD
   - Same as place-minimal.ttl in JSON-LD format

## Key Mappings from JSON Schema to CIDOC-CRM

| JSON Schema Property | CIDOC-CRM Predicate | Description |
|---------------------|---------------------|-------------|
| `type: "Place"` | `rdf:type crm:E53_Place` | Entity class |
| `_label` | `rdfs:label` | Human-readable label |
| `classified_as` | `crm:P2_has_type` | Type classification |
| `identified_by` | `crm:P1_is_identified_by` | Names and identifiers |
| `referred_to_by` | `crm:P67i_is_referred_to_by` | Descriptions and statements |
| `defined_by` | `crm:P168_place_is_defined_by` | Geographic definition (WKT/GeoJSON) |
| `part_of` | `crm:P89_falls_within` | Hierarchical containment |
| `equivalent` | `skos:exactMatch` | External equivalent URIs |
| `representation` | `schema:image` | Visual representations |
| `member_of` | `crm:P107i_is_current_or_former_member_of` | Set membership |
| `subject_of` | `crm:P129i_is_subject_of` | Documents about the place |
| `attributed_by` | `crm:P140i_was_attributed_by` | Attribution statements |

## Usage Examples

### Loading with RDFLib (Python)

```python
from rdflib import Graph

# Load Turtle
g = Graph()
g.parse('place.ttl', format='turtle')

# Load N-Triples
g = Graph()
g.parse('place.nt', format='nt')

# Load JSON-LD
g = Graph()
g.parse('place.jsonld', format='json-ld')

# Query the graph
for s, p, o in g.triples((None, None, None)):
    print(f"{s} {p} {o}")
```

### SPARQL Query Example

```sparql
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?place ?label ?parent ?parentLabel
WHERE {
  ?place a crm:E53_Place ;
         rdfs:label ?label .
  OPTIONAL {
    ?place crm:P89_falls_within ?parent .
    ?parent rdfs:label ?parentLabel .
  }
}
```

### Loading into a Triple Store

```bash
# Apache Jena TDB2
tdb2.tdbloader --loc /path/to/database place.nt

# Blazegraph
curl -X POST -H 'Content-Type:text/plain' \
  --data-binary '@place.nt' \
  'http://localhost:9999/blazegraph/sparql'

# GraphDB
# Import via workbench UI or REST API
```

## Standards References

- **Linked Art API**: https://linked.art/api/1.0/endpoint/place/
- **CIDOC-CRM**: http://www.cidoc-crm.org/
- **SHACL**: https://www.w3.org/TR/shacl/
- **WKT**: http://www.opengis.net/ont/geosparql#wktLiteral
- **Getty AAT**: http://vocab.getty.edu/aat/

## Notes

- All URIs are examples and should be replaced with your actual identifiers
- Geographic coordinates use WKT format for interoperability
- The SHACL shapes provide validation constraints based on the JSON Schema
- Equivalent properties (skos:exactMatch) link to external authority files like GeoNames
