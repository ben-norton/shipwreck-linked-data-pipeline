# Linked Art Place - Quick Reference Card

## Core Pattern

```turtle
<https://example.org/place/id> a crm:E53_Place ;
    rdfs:label "Place Name" .
```

## Complete Property Mappings

### Identity & Classification

| Property | CIDOC-CRM | Range | Cardinality |
|----------|-----------|-------|-------------|
| `type` | `rdf:type` | `crm:E53_Place` | Required (1) |
| `_label` | `rdfs:label` | `xsd:string` | Required (1) |
| `classified_as` | `crm:P2_has_type` | `crm:E55_Type` | Optional (0-n) |

### Names & Identifiers

| Property | CIDOC-CRM | Range | Used For |
|----------|-----------|-------|----------|
| `identified_by` (Name) | `crm:P1_is_identified_by` | `crm:E41_Appellation` | Names, titles |
| `identified_by` (Identifier) | `crm:P1_is_identified_by` | `crm:E42_Identifier` | IDs, codes |

Pattern:
```turtle
crm:P1_is_identified_by [
    a crm:E41_Appellation ;
    crm:P190_has_symbolic_content "Name String"
] .
```

### Documentation

| Property | CIDOC-CRM | Range | Used For |
|----------|-----------|-------|----------|
| `referred_to_by` | `crm:P67i_is_referred_to_by` | `crm:E33_Linguistic_Object` | Descriptions, notes |
| `subject_of` | `crm:P129i_is_subject_of` | `crm:E33_Linguistic_Object` | Documents about place |

Pattern:
```turtle
crm:P67i_is_referred_to_by [
    a crm:E33_Linguistic_Object ;
    crm:P190_has_symbolic_content "Description text"@en ;
    crm:P2_has_type <http://vocab.getty.edu/aat/300080091>  # description
] .
```

### Geographic Definition

| Property | CIDOC-CRM | Range | Format |
|----------|-----------|-------|--------|
| `defined_by` | `crm:P168_place_is_defined_by` | WKT or GeoJSON | String |

Examples:
```turtle
# Point
crm:P168_place_is_defined_by "POINT(-78.6382 35.7796)"^^geo:wktLiteral .

# Polygon
crm:P168_place_is_defined_by "POLYGON((-78.7 35.7, -78.5 35.7, -78.5 35.9, -78.7 35.9, -78.7 35.7))"^^geo:wktLiteral .

# GeoJSON (as string)
crm:P168_place_is_defined_by '{"type":"Point","coordinates":[-78.6382,35.7796]}' .
```

### Relationships

| Property | CIDOC-CRM | Range | Meaning |
|----------|-----------|-------|---------|
| `part_of` | `crm:P89_falls_within` | `crm:E53_Place` | Contained within |
| `equivalent` | `skos:exactMatch` | `crm:E53_Place` | Same place, different URI |
| `member_of` | `crm:P107i_is_current_or_former_member_of` | `crm:E74_Group` | Group membership |

Patterns:
```turtle
# Hierarchy
crm:P89_falls_within <https://example.org/place/parent> .

# External equivalence
skos:exactMatch <http://www.geonames.org/4487042/> ;
skos:exactMatch <http://sws.geonames.org/4487042/> .
```

### Attribution & Evidence

| Property | CIDOC-CRM | Range | Used For |
|----------|-----------|-------|----------|
| `attributed_by` | `crm:P140i_was_attributed_by` | `crm:E13_Attribute_Assignment` | Attribution statements |

Pattern:
```turtle
crm:P140i_was_attributed_by [
    a crm:E13_Attribute_Assignment ;
    crm:P14_carried_out_by <https://example.org/actor/researcher> ;
    crm:P4_has_time-span [
        a crm:E52_Time-Span ;
        crm:P82a_begin_of_the_begin "2024-01-01"^^xsd:date
    ]
] .
```

### Media

| Property | CIDOC-CRM | Range | Used For |
|----------|-----------|-------|----------|
| `representation` | `schema:image` | `crm:E36_Visual_Item` | Images, maps |

Pattern:
```turtle
schema:image <https://example.org/image/place.jpg> .
```

## Common Type Vocabulary (Getty AAT)

| Concept | AAT URI | Usage |
|---------|---------|-------|
| city | `http://vocab.getty.edu/aat/300008347` | Urban centers |
| state | `http://vocab.getty.edu/aat/300000774` | Political subdivisions |
| county | `http://vocab.getty.edu/aat/300000771` | Administrative divisions |
| nation | `http://vocab.getty.edu/aat/300128207` | Countries |
| museum | `http://vocab.getty.edu/aat/300005768` | Museum institutions |
| building | `http://vocab.getty.edu/aat/300004792` | Built structures |
| description | `http://vocab.getty.edu/aat/300080091` | Descriptive statements |
| preferred terms | `http://vocab.getty.edu/aat/300404670` | Preferred names |

## Namespace Prefixes

```turtle
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix schema: <http://schema.org/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix aat: <http://vocab.getty.edu/aat/> .
```

## Minimal Valid Example

```turtle
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://example.org/place/123> a crm:E53_Place ;
    rdfs:label "Example Place" .
```

## Full-Featured Example

```turtle
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix aat: <http://vocab.getty.edu/aat/> .

<https://example.org/place/raleigh> a crm:E53_Place ;
    rdfs:label "Raleigh, North Carolina" ;
    
    # Type
    crm:P2_has_type aat:300008347 ;  # city
    
    # Name
    crm:P1_is_identified_by [
        a crm:E41_Appellation ;
        crm:P190_has_symbolic_content "Raleigh" ;
        crm:P2_has_type aat:300404670  # preferred term
    ] ;
    
    # Description
    crm:P67i_is_referred_to_by [
        a crm:E33_Linguistic_Object ;
        crm:P190_has_symbolic_content "Capital city of North Carolina"@en ;
        crm:P2_has_type aat:300080091  # description
    ] ;
    
    # Coordinates
    crm:P168_place_is_defined_by "POINT(-78.6382 35.7796)"^^geo:wktLiteral ;
    
    # Hierarchy
    crm:P89_falls_within <https://example.org/place/north-carolina> ;
    
    # External reference
    skos:exactMatch <http://www.geonames.org/4487042/> .
```

## Validation Checklist

- [ ] Has `rdf:type crm:E53_Place`
- [ ] Has `rdfs:label` with human-readable name
- [ ] All URIs are properly formed (no spaces, proper encoding)
- [ ] Language tags used for multilingual content (`@en`, `@es`, etc.)
- [ ] Datatypes specified where appropriate (`^^xsd:date`, `^^geo:wktLiteral`)
- [ ] External references use appropriate properties (`skos:exactMatch`, not custom)
- [ ] Hierarchical relationships use `crm:P89_falls_within`
- [ ] Names use `crm:E41_Appellation`, identifiers use `crm:E42_Identifier`
- [ ] All blank nodes have explicit types

## Common Patterns

### Place with Multiple Names
```turtle
<https://example.org/place/nyc> a crm:E53_Place ;
    rdfs:label "New York City" ;
    crm:P1_is_identified_by [
        a crm:E41_Appellation ;
        crm:P190_has_symbolic_content "New York City" ;
        crm:P2_has_type aat:300404670
    ] ;
    crm:P1_is_identified_by [
        a crm:E41_Appellation ;
        crm:P190_has_symbolic_content "NYC" ;
        crm:P2_has_type aat:300404671  # acronym
    ] ;
    crm:P1_is_identified_by [
        a crm:E41_Appellation ;
        crm:P190_has_symbolic_content "The Big Apple" ;
        crm:P2_has_type aat:300404674  # nickname
    ] .
```

### Place with Historical Names
```turtle
<https://example.org/place/istanbul> a crm:E53_Place ;
    rdfs:label "Istanbul" ;
    crm:P1_is_identified_by [
        a crm:E41_Appellation ;
        crm:P190_has_symbolic_content "Istanbul" ;
        crm:P2_has_type aat:300404670 ;  # current name
        crm:P4_has_time-span [
            a crm:E52_Time-Span ;
            crm:P82a_begin_of_the_begin "1930-03-28"^^xsd:date
        ]
    ] ;
    crm:P1_is_identified_by [
        a crm:E41_Appellation ;
        crm:P190_has_symbolic_content "Constantinople" ;
        crm:P2_has_type aat:300404673 ;  # historical name
        crm:P4_has_time-span [
            a crm:E52_Time-Span ;
            crm:P82a_begin_of_the_begin "330"^^xsd:gYear ;
            crm:P82b_end_of_the_end "1930-03-28"^^xsd:date
        ]
    ] .
```

### Complex Geographic Boundary
```turtle
<https://example.org/place/park> a crm:E53_Place ;
    rdfs:label "National Park" ;
    crm:P168_place_is_defined_by """
        POLYGON((
            -80.0 36.0,
            -79.0 36.0,
            -79.0 37.0,
            -80.0 37.0,
            -80.0 36.0
        ))
    """^^geo:wktLiteral .
```

---

**Pro Tips:**
- Always validate WKT syntax before adding to RDF
- Use Getty AAT for type classification when possible
- Prefer `skos:exactMatch` over custom equivalence properties
- Keep blank node structures simple and well-typed
- Use language tags for all natural language content
- Document coordinate reference systems (default: WGS84)
