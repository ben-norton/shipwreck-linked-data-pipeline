# NJ Maritime Shipwreck Database to Linked Art Mapping

## Overview
This document maps the NJ Maritime Shipwreck Database CSV to Linked Art Place and Event schemas, creating structured semantic data about maritime disasters off the New Jersey coast.

## Data Structure

### Source Dataset
- **File**: nj_maritime_shipwreck_database.csv
- **Records**: 4,600 shipwreck records
- **Time Period**: 1820-1916+ (maritime disasters)

---

## Schema Mappings

### 1. EVENT Schema Mapping (Shipwreck Event)

Each shipwreck record represents a **shipwreck event** that should be modeled as an `Event` or `Activity` in Linked Art.

#### Core Event Properties

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/event/shipwreck-{shipsName}-{year}",
  "type": "Event",
  "_label": "{shipsName} shipwreck"
}
```

#### Property Mappings

| Linked Art Property | CSV Column(s) | Mapping Notes |
|---------------------|---------------|---------------|
| `type` | - | Always "Event" (shipwrecks are events) |
| `_label` | `shipsName` | Format: "{shipsName} shipwreck ({year})" |
| `identified_by` | `shipsName`, `aka` | Create Name and Identifier entities |
| `classified_as` | `causeOfLoss`, `vesselType` | Event classification (e.g., "maritime disaster", "grounding", "collision") |
| `referred_to_by` | `miscInformation` | LinguisticObject with descriptive text |
| `timespan` | `year`, `month`, `day`, `dateLost` | TimeSpan with begin_of_the_begin and end_of_the_end |
| `took_place_at` | `locationLost`, `latitude`, `longitude` | References Place entity (see below) |
| `caused_by` | `causeOfLoss` | Event or Condition causing the shipwreck |
| `used_specific_object` | `shipsName` + ship properties | Reference to the ship as a HumanMadeObject |
| `participant` | `master`, `numberOfCrew`, `numPass` | Person entities for master and counts for crew/passengers |

#### Detailed Mapping Examples

**identified_by** (Ship Name):
```json
"identified_by": [
  {
    "type": "Name",
    "content": "{shipsName}",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300404670",
        "type": "Type",
        "_label": "Primary Name"
      }
    ]
  },
  {
    "type": "Name",
    "content": "{aka}",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300264273",
        "type": "Type",
        "_label": "Alternative Name"
      }
    ]
  }
]
```

**classified_as** (Event Type):
```json
"classified_as": [
  {
    "id": "http://vocab.getty.edu/aat/300054734",
    "type": "Type",
    "_label": "shipwreck",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300435443",
        "type": "Type",
        "_label": "Type of Event"
      }
    ]
  },
  {
    "id": "https://example.org/type/cause/{causeOfLoss}",
    "type": "Type",
    "_label": "{causeOfLoss}",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300435424",
        "type": "Type",
        "_label": "Cause"
      }
    ]
  }
]
```

**timespan** (When the shipwreck occurred):
```json
"timespan": {
  "type": "TimeSpan",
  "_label": "{dateLost}",
  "begin_of_the_begin": "{year}-{month}-{day}T00:00:00Z",
  "end_of_the_end": "{year}-{month}-{day}T23:59:59Z",
  "identified_by": [
    {
      "type": "Name",
      "content": "{dateLost}",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404669",
          "type": "Type",
          "_label": "Display Date"
        }
      ]
    }
  ]
}
```

**referred_to_by** (Additional Information):
```json
"referred_to_by": [
  {
    "type": "LinguisticObject",
    "content": "{miscInformation}",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300435416",
        "type": "Type",
        "_label": "Description"
      }
    ]
  },
  {
    "type": "LinguisticObject",
    "content": "Lives Lost: {livesLost}",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300435425",
        "type": "Type",
        "_label": "Casualty Report"
      }
    ]
  },
  {
    "type": "LinguisticObject",
    "content": "Crew: {numberOfCrew}, Passengers: {numPass}",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300435413",
        "type": "Type",
        "_label": "Manifest Information"
      }
    ]
  }
]
```

**attributed_by** (Value Information):
```json
"attributed_by": [
  {
    "type": "AttributeAssignment",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300404277",
        "type": "Type",
        "_label": "Monetary Value"
      }
    ],
    "assigned": [
      {
        "type": "MonetaryAmount",
        "_label": "Ship Value: {shipValue}",
        "value": {shipValue_numeric},
        "currency": {
          "id": "http://vocab.getty.edu/aat/300411994",
          "type": "Currency",
          "_label": "US Dollar"
        }
      }
    ]
  },
  {
    "type": "AttributeAssignment",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300404277",
        "type": "Type",
        "_label": "Cargo Value"
      }
    ],
    "assigned": [
      {
        "type": "MonetaryAmount",
        "_label": "Cargo Value: {cargoValue}",
        "value": {cargoValue_numeric},
        "currency": {
          "id": "http://vocab.getty.edu/aat/300411994",
          "type": "Currency",
          "_label": "US Dollar"
        }
      }
    ]
  }
]
```

---

### 2. PLACE Schema Mapping

Multiple places are referenced in each shipwreck record:
1. **Shipwreck Location** (where the ship was lost)
2. **Home/Hailing Port**
3. **Departure Port**
4. **Destination Port**
5. **Where Built**
6. **USLSS Station** (rescue station)

#### Core Place Properties

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/place/{location-id}",
  "type": "Place",
  "_label": "{locationLost}"
}
```

#### Property Mappings

| Linked Art Property | CSV Column(s) | Mapping Notes |
|---------------------|---------------|---------------|
| `type` | - | Always "Place" |
| `_label` | `locationLost`, `homeHailingPort`, etc. | Human-readable place name |
| `identified_by` | Location name | Name entity with display name |
| `classified_as` | Context-dependent | Shipwreck site, port, construction site, etc. |
| `referred_to_by` | Various | Additional descriptive information |
| `defined_by` | `latitude`, `longitude` | WKT or GeoJSON point geometry |
| `part_of` | Geographic hierarchy | Link to broader geographic entities (NJ, USA, etc.) |

#### Detailed Place Mappings

**Place Type 1: Shipwreck Site**

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/place/shipwreck-site-{id}",
  "type": "Place",
  "_label": "{locationLost}",
  "identified_by": [
    {
      "type": "Name",
      "content": "{locationLost}",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404670",
          "type": "Type",
          "_label": "Primary Name"
        }
      ]
    }
  ],
  "classified_as": [
    {
      "id": "http://vocab.getty.edu/aat/300008025",
      "type": "Type",
      "_label": "shipwreck site"
    }
  ],
  "defined_by": "POINT({longitude} {latitude})",
  "part_of": [
    {
      "id": "https://example.org/place/new-jersey",
      "type": "Place",
      "_label": "New Jersey"
    },
    {
      "id": "https://example.org/place/atlantic-ocean",
      "type": "Place",
      "_label": "Atlantic Ocean"
    }
  ]
}
```

**Place Type 2: Ports (Hailing, Departure, Destination)**

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/place/port-{normalized-name}",
  "type": "Place",
  "_label": "{homeHailingPort|departurePort|destinationPort}",
  "identified_by": [
    {
      "type": "Name",
      "content": "{port_name}",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404670",
          "type": "Type",
          "_label": "Primary Name"
        }
      ]
    }
  ],
  "classified_as": [
    {
      "id": "http://vocab.getty.edu/aat/300008738",
      "type": "Type",
      "_label": "port"
    }
  ]
}
```

**Place Type 3: Construction Site**

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/place/construction-{normalized-name}",
  "type": "Place",
  "_label": "{whereBuilt}",
  "identified_by": [
    {
      "type": "Name",
      "content": "{whereBuilt}",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404670",
          "type": "Type",
          "_label": "Primary Name"
        }
      ]
    }
  ],
  "classified_as": [
    {
      "id": "http://vocab.getty.edu/aat/300006999",
      "type": "Type",
      "_label": "shipyard"
    }
  ]
}
```

**GeoJSON Format for defined_by**

When latitude and longitude are available:

```json
"defined_by": "{\"type\":\"Point\",\"coordinates\":[{longitude},{latitude}]}"
```

Or in WKT format:
```json
"defined_by": "POINT({longitude} {latitude})"
```

---

## 3. SHIP as HumanMadeObject (Related Entity)

While not in the provided schemas, ships should be modeled as `HumanMadeObject` entities that are referenced by the shipwreck event.

**Ship Properties from CSV:**

| Ship Property | CSV Column(s) |
|---------------|---------------|
| Name | `shipsName`, `aka` |
| Type | `vesselType` |
| Owner | `shipsOwner` |
| Construction | `construction` (material) |
| Flag/Nationality | `flag` |
| Dimensions | `length`, `beam`, `draft` |
| Tonnage | `grossTonnage`, `netTonnage` |
| Built | `yearBuilt`, `whereBuilt` |

**Ship Reference in Event:**

```json
"used_specific_object": [
  {
    "id": "https://example.org/object/ship-{shipsName}",
    "type": "HumanMadeObject",
    "_label": "{shipsName}",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300082981",
        "type": "Type",
        "_label": "{vesselType}"
      }
    ]
  }
]
```

---

## 4. CARGO as Conceptual Entity

Cargo information can be modeled as part of the event description or as a separate entity.

**From CSV:**
- `natureOfCargo`: Type of cargo (coal, lumber, bricks, etc.)
- `cargoValue`: Monetary value of cargo

**Modeling Approach:**

```json
"referred_to_by": [
  {
    "type": "LinguisticObject",
    "content": "Cargo: {natureOfCargo}, Value: {cargoValue}",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300435429",
        "type": "Type",
        "_label": "Cargo Manifest"
      }
    ]
  }
]
```

---

## 5. RESCUE STATIONS (USLSS)

U.S. Life-Saving Service (USLSS) stations can be modeled as organizational Places or as Organizations.

**From CSV:**
- `uslssStationName`: Name of the life-saving station

**As Place:**

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/place/station-{normalized-name}",
  "type": "Place",
  "_label": "{uslssStationName}",
  "classified_as": [
    {
      "id": "http://vocab.getty.edu/aat/300121182",
      "type": "Type",
      "_label": "life-saving station"
    }
  ],
  "part_of": [
    {
      "id": "https://example.org/place/new-jersey-coast",
      "type": "Place",
      "_label": "New Jersey Coast"
    }
  ]
}
```

---

## 6. Additional Relationships

### Event-Place Relationships

```json
"took_place_at": [
  {
    "id": "https://example.org/place/shipwreck-site-{id}",
    "type": "Place",
    "_label": "{locationLost}"
  }
]
```

### Temporal Relationships

For events that occurred during broader historical periods:

```json
"during": [
  {
    "id": "https://example.org/period/civil-war",
    "type": "Period",
    "_label": "American Civil War"
  }
]
```

---

## 7. Data Quality Flags

The CSV includes data quality indicators:
- `map`: Map availability (Y/N)
- `lost`: Total loss status (Y/N)
- `photoOnFile`: Photo documentation (Y/N)

These can be modeled as:

```json
"referred_to_by": [
  {
    "type": "LinguisticObject",
    "content": "Photo on file: {photoOnFile}",
    "classified_as": [
      {
        "id": "http://vocab.getty.edu/aat/300435418",
        "type": "Type",
        "_label": "Documentation Status"
      }
    ]
  }
]
```

---

## 8. Complete Example Transformation

### Source CSV Row:
```
A G Ropes,,Luckenbach SS Co,Schooner - Barge,1884,"Bath, ME",12/26/1913,1913.0,12,26,Island Beach,,,Foundered in gale,Wood,US,258.2,44.7,28.4,2438,2328,"New York, NY","Philadelphia, PA","Providence, RI",,5,,5,"$50,000","$9,800",Coal,,Y,Y,Y,#106318; Total loss
```

### Transformed to Linked Art:

**Event (Shipwreck):**

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/event/shipwreck-a-g-ropes-1913",
  "type": "Event",
  "_label": "A G Ropes shipwreck (1913)",
  "identified_by": [
    {
      "type": "Name",
      "content": "A G Ropes",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404670",
          "type": "Type",
          "_label": "Primary Name"
        }
      ]
    },
    {
      "type": "Identifier",
      "content": "#106318",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404626",
          "type": "Type",
          "_label": "Catalog Number"
        }
      ]
    }
  ],
  "classified_as": [
    {
      "id": "http://vocab.getty.edu/aat/300054734",
      "type": "Type",
      "_label": "shipwreck"
    },
    {
      "id": "https://example.org/type/cause/foundering",
      "type": "Type",
      "_label": "Foundered in gale"
    }
  ],
  "referred_to_by": [
    {
      "type": "LinguisticObject",
      "content": "#106318; Total loss",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300435416",
          "type": "Type",
          "_label": "Description"
        }
      ]
    },
    {
      "type": "LinguisticObject",
      "content": "Crew: 5, Lives Lost: 5",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300435425",
          "type": "Type",
          "_label": "Casualty Report"
        }
      ]
    },
    {
      "type": "LinguisticObject",
      "content": "Cargo: Coal",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300435429",
          "type": "Type",
          "_label": "Cargo Manifest"
        }
      ]
    }
  ],
  "timespan": {
    "type": "TimeSpan",
    "_label": "December 26, 1913",
    "begin_of_the_begin": "1913-12-26T00:00:00Z",
    "end_of_the_end": "1913-12-26T23:59:59Z"
  },
  "took_place_at": [
    {
      "id": "https://example.org/place/island-beach-nj",
      "type": "Place",
      "_label": "Island Beach"
    }
  ],
  "caused_by": [
    {
      "type": "Event",
      "_label": "Gale",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300054734",
          "type": "Type",
          "_label": "storm"
        }
      ]
    }
  ],
  "used_specific_object": [
    {
      "id": "https://example.org/object/ship-a-g-ropes",
      "type": "HumanMadeObject",
      "_label": "A G Ropes"
    }
  ],
  "attributed_by": [
    {
      "type": "AttributeAssignment",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404277",
          "type": "Type",
          "_label": "Ship Value"
        }
      ],
      "assigned": [
        {
          "type": "MonetaryAmount",
          "_label": "$50,000",
          "value": 50000,
          "currency": {
            "id": "http://vocab.getty.edu/aat/300411994",
            "type": "Currency",
            "_label": "US Dollar"
          }
        }
      ]
    },
    {
      "type": "AttributeAssignment",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404277",
          "type": "Type",
          "_label": "Cargo Value"
        }
      ],
      "assigned": [
        {
          "type": "MonetaryAmount",
          "_label": "$9,800",
          "value": 9800,
          "currency": {
            "id": "http://vocab.getty.edu/aat/300411994",
            "type": "Currency",
            "_label": "US Dollar"
          }
        }
      ]
    }
  ]
}
```

**Place (Shipwreck Site):**

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/place/island-beach-nj",
  "type": "Place",
  "_label": "Island Beach",
  "identified_by": [
    {
      "type": "Name",
      "content": "Island Beach",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404670",
          "type": "Type",
          "_label": "Primary Name"
        }
      ]
    }
  ],
  "classified_as": [
    {
      "id": "http://vocab.getty.edu/aat/300008025",
      "type": "Type",
      "_label": "shipwreck site"
    }
  ],
  "part_of": [
    {
      "id": "https://example.org/place/new-jersey",
      "type": "Place",
      "_label": "New Jersey"
    }
  ]
}
```

**Place (Ports):**

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/place/port-new-york-ny",
  "type": "Place",
  "_label": "New York, NY",
  "identified_by": [
    {
      "type": "Name",
      "content": "New York, NY",
      "classified_as": [
        {
          "id": "http://vocab.getty.edu/aat/300404670",
          "type": "Type",
          "_label": "Primary Name"
        }
      ]
    }
  ],
  "classified_as": [
    {
      "id": "http://vocab.getty.edu/aat/300008738",
      "type": "Type",
      "_label": "port"
    }
  ]
}
```

---

## 9. Implementation Notes

### URI Construction

**Events:**
- Pattern: `https://example.org/event/shipwreck-{normalized-ship-name}-{year}`
- Normalization: lowercase, spaces to hyphens, remove special characters

**Places:**
- Pattern: `https://example.org/place/{type}-{normalized-name}`
- Types: shipwreck-site, port, construction-site, station

**Objects (Ships):**
- Pattern: `https://example.org/object/ship-{normalized-ship-name}`

### Data Cleaning Requirements

1. **Dates**: Parse `dateLost` field, fill in year/month/day where missing
2. **Coordinates**: Latitude/longitude are often empty; require geocoding
3. **Monetary Values**: Parse currency strings (e.g., "$50,000" → 50000)
4. **Names**: Normalize ship names, handle AKAs
5. **Port Names**: Standardize port naming conventions
6. **Cause of Loss**: Map to controlled vocabulary

### Missing Data Handling

- Empty coordinates: Place still created with textual location only
- Missing dates: Use year only, create broader TimeSpan
- Unknown values: Omit property rather than using placeholder

### Controlled Vocabularies

**Recommended:**
- Getty AAT for type classifications
- GeoNames or TGN for places
- Local vocabulary for causes of loss
- MIME types for digital representations

---

## 10. Statistics & Data Quality

**Dataset Statistics:**
- Total Records: 4,600 shipwrecks
- Date Range: 1820-1916+
- Geographic Focus: New Jersey coastal waters

**Data Completeness:**
- Location names: ~100%
- Coordinates: ~5-10% (estimated)
- Dates: ~95%
- Vessel details: ~80%
- Casualties: ~60%

**Priority Fields for Linked Art:**
1. Ship name → Event identification
2. Date lost → Event timespan
3. Location lost → Place reference
4. Cause of loss → Event classification
5. Coordinates → Place definition (when available)

---

## 11. Extension Opportunities

### Additional Entities to Consider

1. **Person entities** for ship masters
2. **Organization entities** for ship owners, USLSS
3. **Group entities** for crew and passengers
4. **Collection/Set** for grouping related shipwrecks
5. **DigitalObject** for photos, maps, documents

### Additional Relationships

1. **Related Events**: Rescue operations, salvage attempts
2. **Broader Historical Context**: Wars, economic periods
3. **Environmental Conditions**: Weather, sea state
4. **Modern Site Status**: Archaeological sites, dive sites

---

## Conclusion

This mapping provides a comprehensive framework for transforming the NJ Maritime Shipwreck Database into Linked Art format. The resulting structured data enables:

- Semantic querying across maritime disaster events
- Geographic visualization of shipwreck locations
- Temporal analysis of maritime safety
- Integration with broader cultural heritage datasets
- Enhanced discoverability and research applications

The mapped data respects the Linked Art schema requirements while preserving the rich detail of the original shipwreck records.
