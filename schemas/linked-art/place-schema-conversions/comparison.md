# JSON-LD vs Turtle Comparison

This document shows how a Linked Art Place looks in both JSON-LD and Turtle formats.

## JSON-LD Instance

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://linked.art/example/place/raleigh-nc",
  "type": "Place",
  "_label": "Raleigh, North Carolina",
  "classified_as": [
    {
      "id": "http://vocab.getty.edu/aat/300008347",
      "type": "Type",
      "_label": "cities"
    }
  ],
  "identified_by": [
    {
      "type": "Name",
      "content": "Raleigh",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404670",
          "type": "Type",
          "_label": "preferred terms"
        }
      ]
    },
    {
      "type": "Identifier",
      "content": "4487042",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404626",
          "type": "Type",
          "_label": "identification numbers"
        }
      ]
    }
  ],
  "referred_to_by": [
    {
      "type": "LinguisticObject",
      "content": "Capital city of North Carolina, known as the City of Oaks",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300080091",
          "type": "Type",
          "_label": "description"
        }
      ]
    }
  ],
  "defined_by": "POINT(-78.6382 35.7796)",
  "part_of": [
    {
      "id": "https://linked.art/example/place/north-carolina",
      "type": "Place",
      "_label": "North Carolina"
    },
    {
      "id": "https://linked.art/example/place/wake-county-nc",
      "type": "Place",
      "_label": "Wake County, North Carolina"
    }
  ],
  "equivalent": [
    {
      "id": "http://www.geonames.org/4487042/",
      "type": "Place"
    }
  ]
}
```

## Equivalent Turtle (TTL)

```turtle
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix geosparql: <http://www.opengis.net/ont/geosparql#> .

<https://linked.art/example/place/raleigh-nc> a crm:E53_Place ;
    rdfs:label "Raleigh, North Carolina" ;
    
    # classified_as -> P2_has_type
    crm:P2_has_type <http://vocab.getty.edu/aat/300008347> ;
    
    # identified_by -> P1_is_identified_by
    crm:P1_is_identified_by [
        a crm:E41_Appellation , crm:E33_E41_Linguistic_Appellation ;
        rdfs:label "Primary Name" ;
        crm:P2_has_type <http://vocab.getty.edu/aat/300404670> ;
        crm:P190_has_symbolic_content "Raleigh"
    ] ;
    
    crm:P1_is_identified_by [
        a crm:E42_Identifier ;
        rdfs:label "GeoNames ID" ;
        crm:P2_has_type <http://vocab.getty.edu/aat/300404626> ;
        crm:P190_has_symbolic_content "4487042"
    ] ;
    
    # referred_to_by -> P67i_is_referred_to_by
    crm:P67i_is_referred_to_by [
        a crm:E33_Linguistic_Object ;
        rdfs:label "Description" ;
        crm:P2_has_type <http://vocab.getty.edu/aat/300080091> ;
        crm:P190_has_symbolic_content "Capital city of North Carolina, known as the City of Oaks"@en
    ] ;
    
    # defined_by -> P168_place_is_defined_by
    crm:P168_place_is_defined_by "POINT(-78.6382 35.7796)"^^geosparql:wktLiteral ;
    
    # part_of -> P89_falls_within
    crm:P89_falls_within <https://linked.art/example/place/north-carolina> ;
    crm:P89_falls_within <https://linked.art/example/place/wake-county-nc> ;
    
    # equivalent -> skos:exactMatch
    skos:exactMatch <http://www.geonames.org/4487042/> .

# Type Resources (referenced above)
<http://vocab.getty.edu/aat/300008347> a crm:E55_Type ;
    rdfs:label "cities" .

<http://vocab.getty.edu/aat/300404670> a crm:E55_Type ;
    rdfs:label "preferred terms" .

<http://vocab.getty.edu/aat/300404626> a crm:E55_Type ;
    rdfs:label "identification numbers" .

<http://vocab.getty.edu/aat/300080091> a crm:E55_Type ;
    rdfs:label "description" .

# Referenced Places
<https://linked.art/example/place/north-carolina> a crm:E53_Place ;
    rdfs:label "North Carolina" .

<https://linked.art/example/place/wake-county-nc> a crm:E53_Place ;
    rdfs:label "Wake County, North Carolina" .
```

## Key Differences

### JSON-LD Features
- **Inline contexts**: `@context` defines namespace mappings
- **Nested objects**: Properties can contain full objects
- **Arrays**: Multiple values naturally expressed as JSON arrays
- **String values**: Direct property-to-string mappings (like `content`, `_label`)

### Turtle Features
- **Prefix declarations**: Defined once at the top
- **Blank nodes**: Use `[ ]` syntax for anonymous resources
- **Subject grouping**: Semicolons allow multiple predicates for same subject
- **Commas**: Multiple objects for same subject-predicate pair
- **URIs**: Full URIs or prefixed names (`crm:E53_Place`)
- **Datatypes**: Explicit typing with `^^` (e.g., `^^geosparql:wktLiteral`)
- **Language tags**: Use `@en` for language-specific strings

## Property Mapping Reference

| JSON-LD | Turtle Predicate | CIDOC-CRM |
|---------|------------------|-----------|
| `type` | `rdf:type` or `a` | Class membership |
| `_label` | `rdfs:label` | Human-readable label |
| `content` | `crm:P190_has_symbolic_content` | String value |
| `classified_as` | `crm:P2_has_type` | Type classification |
| `identified_by` | `crm:P1_is_identified_by` | Appellations/Identifiers |
| `referred_to_by` | `crm:P67i_is_referred_to_by` | Linguistic objects |
| `defined_by` | `crm:P168_place_is_defined_by` | Geographic bounds |
| `part_of` | `crm:P89_falls_within` | Spatial containment |
| `equivalent` | `skos:exactMatch` | Same-as relationships |

## Serialization Trade-offs

### When to use JSON-LD
- Web APIs and REST services
- JavaScript/Node.js applications
- Document-oriented databases (MongoDB, CouchDB)
- When JSON tooling is already in use
- Human-readable data exchange

### When to use Turtle
- Triple stores and SPARQL endpoints
- Academic publications and documentation
- Human-readable RDF for review
- Teaching and learning RDF concepts
- Version control (git-friendly)

### When to use N-Triples
- Bulk loading into triple stores
- Large dataset processing
- Simple parsing requirements
- Line-by-line processing
- Streaming applications
