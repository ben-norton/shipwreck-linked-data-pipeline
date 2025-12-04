# Quick Reference: CSV to Linked Art Mapping

## Visual Mapping Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    CSV SHIPWRECK RECORD                          │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ├──────────────────┐
                            ▼                  ▼
                    ┌──────────────┐   ┌──────────────┐
                    │    EVENT      │   │    PLACE     │
                    │  (Shipwreck)  │   │  (Location)  │
                    └──────────────┘   └──────────────┘
```

## EVENT Mapping (Shipwreck)

### CSV → Linked Art Event Structure

```
CSV Column(s)               →  Linked Art Property
─────────────────────────────────────────────────────────────────

IDENTIFICATION
├─ shipsName                →  _label, identified_by[Name]
├─ aka                      →  identified_by[Name] (alternative)
└─ miscInformation ID       →  identified_by[Identifier]

CLASSIFICATION  
├─ causeOfLoss              →  classified_as[Type] (cause)
└─ vesselType               →  referred_to_by[LinguisticObject]

TEMPORAL
├─ year, month, day         →  timespan[TimeSpan]
└─ dateLost                 →  timespan._label

SPATIAL
├─ locationLost             →  took_place_at[Place]
├─ latitude                 →  took_place_at → Place.defined_by
└─ longitude                →  took_place_at → Place.defined_by

DESCRIPTIVE
├─ miscInformation          →  referred_to_by[LinguisticObject]
├─ numberOfCrew             →  referred_to_by (casualty report)
├─ numPass                  →  referred_to_by (casualty report)
├─ livesLost                →  referred_to_by (casualty report)
├─ natureOfCargo            →  referred_to_by (cargo manifest)
├─ vesselType               →  referred_to_by (specifications)
├─ construction             →  referred_to_by (specifications)
├─ flag                     →  referred_to_by (specifications)
├─ length, beam, draft      →  referred_to_by (specifications)
└─ grossTonnage             →  referred_to_by (specifications)

ECONOMIC
├─ shipValue                →  attributed_by[MonetaryAmount]
└─ cargoValue               →  attributed_by[MonetaryAmount]

CAUSAL
└─ causeOfLoss              →  caused_by[Event]

RELATIONAL
└─ shipsName                →  used_specific_object[HumanMadeObject]
```

## PLACE Mapping (Locations)

### Multiple Place Types Created

```
CSV Column          →  Place Type       →  Classification
─────────────────────────────────────────────────────────────

locationLost        →  shipwreck-site   →  "shipwreck site"
                       + latitude/lon   →  defined_by (POINT)
                       + part_of        →  "New Jersey"

homeHailingPort     →  port             →  "port"
departurePort       →  port             →  "port"
destinationPort     →  port             →  "port"

whereBuilt          →  construction     →  "shipyard"

uslssStationName    →  station          →  "life-saving station"
```

## Complete Record Example

### CSV Input Row
```csv
A G Ropes,,Luckenbach SS Co,Schooner - Barge,1884,"Bath, ME",
12/26/1913,1913.0,12,26,Island Beach,,,Foundered in gale,Wood,
US,258.2,44.7,28.4,2438,2328,"New York, NY","Philadelphia, PA",
"Providence, RI",,5,,5,"$50,000","$9,800",Coal,,Y,Y,Y,
#106318; Total loss
```

### Linked Art Event Output
```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/.../shipwreck-a-g-ropes-1913",
  "type": "Event",
  "_label": "A G Ropes shipwreck (1913)",
  
  "identified_by": [
    {"type": "Name", "content": "A G Ropes"}
  ],
  
  "classified_as": [
    {"id": "http://vocab.getty.edu/aat/300054734",
     "type": "Type", "_label": "shipwreck"},
    {"_label": "Foundered in gale"}
  ],
  
  "timespan": {
    "type": "TimeSpan",
    "_label": "December 26, 1913",
    "begin_of_the_begin": "1913-12-26T00:00:00Z",
    "end_of_the_end": "1913-12-26T23:59:59Z"
  },
  
  "took_place_at": [
    {"id": ".../place/island-beach-nj",
     "type": "Place", "_label": "Island Beach"}
  ],
  
  "referred_to_by": [
    {"type": "LinguisticObject",
     "content": "Crew: 5, Lives Lost: 5"},
    {"type": "LinguisticObject",
     "content": "Cargo: Coal"},
    {"type": "LinguisticObject",
     "content": "Type: Schooner - Barge; ..."}
  ],
  
  "attributed_by": [
    {"type": "AttributeAssignment",
     "assigned": [{"type": "MonetaryAmount",
                   "value": 50000,
                   "currency": "US Dollar"}]}
  ]
}
```

### Linked Art Place Output
```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/.../place/island-beach-nj",
  "type": "Place",
  "_label": "Island Beach",
  
  "identified_by": [
    {"type": "Name", "content": "Island Beach"}
  ],
  
  "classified_as": [
    {"id": "http://vocab.getty.edu/aat/300008025",
     "type": "Type", "_label": "shipwreck site"}
  ],
  
  "part_of": [
    {"id": ".../place/new-jersey",
     "type": "Place", "_label": "New Jersey"}
  ]
}
```

## Entity Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│  EVENT (Shipwreck A G Ropes 1913)                           │
│  type: Event                                                 │
│  _label: "A G Ropes shipwreck (1913)"                       │
│                                                               │
│  ┌─────────────────────┐                                     │
│  │ identified_by       │ Name: "A G Ropes"                  │
│  └─────────────────────┘                                     │
│                                                               │
│  ┌─────────────────────┐                                     │
│  │ classified_as       │ shipwreck, Foundered in gale       │
│  └─────────────────────┘                                     │
│                                                               │
│  ┌─────────────────────┐                                     │
│  │ timespan           │ 1913-12-26                          │
│  └─────────────────────┘                                     │
│                                                               │
│  ┌─────────────────────┐         ┌──────────────────────┐  │
│  │ took_place_at      │────────→ │ PLACE                 │  │
│  └─────────────────────┘         │ Island Beach          │  │
│                                   │ type: Place           │  │
│                                   │ classified_as: site   │  │
│                                   │ part_of: New Jersey   │  │
│                                   └──────────────────────┘  │
│                                                               │
│  ┌─────────────────────┐                                     │
│  │ referred_to_by     │ Casualties, Cargo, Specs           │
│  └─────────────────────┘                                     │
│                                                               │
│  ┌─────────────────────┐                                     │
│  │ attributed_by      │ $50,000 ship, $9,800 cargo         │
│  └─────────────────────┘                                     │
│                                                               │
│  ┌─────────────────────┐         ┌──────────────────────┐  │
│  │ caused_by          │────────→ │ EVENT                 │  │
│  └─────────────────────┘         │ Gale                  │  │
│                                   │ type: Event           │  │
│                                   └──────────────────────┘  │
│                                                               │
│  ┌─────────────────────┐         ┌──────────────────────┐  │
│  │ used_specific_object│────────→ │ HumanMadeObject      │  │
│  └─────────────────────┘         │ Ship: A G Ropes       │  │
│                                   │ Built: 1884, Bath ME  │  │
│                                   └──────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Data Types & Formats

### Identifiers (URIs)
```
Events:    https://example.org/.../event/shipwreck-{name}-{year}
Places:    https://example.org/.../place/{type}-{name}
Ships:     https://example.org/.../object/ship-{name}
```

### Dates (ISO 8601)
```
Full:      "1913-12-26T00:00:00Z"
Year only: "1913-01-01T00:00:00Z" to "1913-12-31T23:59:59Z"
```

### Coordinates (WKT)
```
POINT(longitude latitude)
Example: POINT(-74.0 40.4)
```

### Monetary Values
```json
{
  "type": "MonetaryAmount",
  "value": 50000,
  "currency": {
    "id": "http://vocab.getty.edu/aat/300411994",
    "type": "Currency",
    "_label": "US Dollar"
  }
}
```

## Getty AAT References

```
Concept                          AAT ID
─────────────────────────────────────────────────────────────
shipwreck                        300054734
Primary Name                     300404670
Alternative Name                 300264273
port                             300008738
shipyard                         300006999
shipwreck site                   300008025
Cause                            300435424
Description                      300435416
Casualty Report                  300435425
Cargo Manifest                   300435429
Vessel Specifications            300435432
Monetary Value                   300404277
US Dollar                        300411994
```

## Field Coverage Statistics

```
Required Fields:        100.0%  ✓ All records have required fields
Temporal Data:          100.0%  ✓ All have timespans
Location Names:          96.9%  ✓ Most have location text
Coordinates:             12.3%  ⚠ Limited geocoded data
Cause Information:       92.8%  ✓ Most have causes
Casualty Data:           60.2%  ⚠ Partial coverage
Monetary Values:         32.3%  ⚠ Limited for older records
Vessel Specifications:   99.5%  ✓ Excellent coverage
```

## Validation Checklist

✓ All events have required fields (@context, id, type, _label)
✓ All places have required fields (@context, id, type, _label)
✓ Event.type is "Event" (or "Activity", "Period")
✓ Place.type is "Place"
✓ TimeSpans include begin_of_the_begin and end_of_the_end
✓ took_place_at references valid Place entities
✓ Coordinates use WKT POINT format
✓ MonetaryAmounts include value and currency
✓ Classifications use Getty AAT URIs where applicable

## Usage Examples

### Query by Date Range
```python
events_1880s = [e for e in events 
                if '188' in e['timespan']['begin_of_the_begin'][:4]]
```

### Query by Location
```python
sandy_hook = [e for e in events 
              if any('Sandy Hook' in p['_label'] 
                    for p in e.get('took_place_at', []))]
```

### Query by Cause
```python
storms = [e for e in events
          if any('storm' in c.get('_label', '').lower()
                for c in e.get('classified_as', []))]
```

### Extract Coordinates
```python
coords = []
for place in places:
    if 'defined_by' in place:
        wkt = place['defined_by']
        if wkt.startswith('POINT'):
            lon, lat = wkt.replace('POINT(','').replace(')','').split()
            coords.append((float(lon), float(lat), place['_label']))
```

## Files in This Package

```
📁 linked_art/
├── 📄 README.md                              (This overview)
├── 📄 nj_shipwreck_linked_art_mapping.md    (Detailed mapping spec)
├── 📄 shipwreck_events.json                 (4,600 Event entities)
├── 📄 places.json                            (3,558 Place entities)
├── 📄 shipwreck_summary.csv                  (Tabular summary)
├── 📄 transformation_stats.json              (Statistics)
├── 🐍 shipwreck_transformer.py               (Transformation script)
├── 🐍 validate_linked_art.py                 (Validation script)
└── 🐍 example_analysis.py                    (Analysis examples)
```

---
For detailed information, see **nj_shipwreck_linked_art_mapping.md**
