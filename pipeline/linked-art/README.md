# NJ Maritime Shipwreck Database - Linked Art Mapping

## Project Overview

This project successfully maps the NJ Maritime Shipwreck Database (4,600 shipwreck records) to the [Linked Art](https://linked.art/) data model, creating structured semantic data about maritime disasters off the New Jersey coast from 1705-2023.

## Contents

### Documentation
- **nj_shipwreck_linked_art_mapping.md** - Comprehensive mapping specification documenting how CSV fields map to Linked Art Event and Place schemas

### Code
- **shipwreck_transformer.py** - Python script that transforms CSV data to Linked Art JSON
- **validate_linked_art.py** - Validation script to verify JSON compliance with schemas

### Output Data
- **shipwreck_events.json** - 4,600 shipwreck events in Linked Art format
- **places.json** - 3,558 unique places (shipwreck sites, ports, shipyards)
- **transformation_stats.json** - Statistical summary of the transformation

## Transformation Results

### Validation Summary
✅ **100% Valid** - All 4,600 events and 3,558 places conform to Linked Art schemas

### Data Coverage
- **Events with timespan**: 4,600 (100%)
- **Events with location**: 4,458 (96.9%)
- **Events with cause**: 4,268 (92.8%)
- **Events with monetary values**: 1,484 (32.3%)
- **Events with descriptions**: 4,575 (99.5%)
- **Places with coordinates**: 439 (12.3%)
- **Places with parent location**: 1,847 (51.9%)

### Date Range
- **Earliest**: 1705
- **Latest**: 2023

### Top Causes of Loss
1. Stranded: 1,260
2. Grounded: 399
3. Foundered: 343
4. Burned: 244
5. Wrecked: 125

### Place Types
- **Shipwreck sites**: 1,847
- **Ports**: 1,094
- **Shipyards**: 617

## Schema Mapping

### Event Schema (Shipwreck Event)

Each shipwreck is modeled as a Linked Art **Event** with the following key properties:

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/nj-shipwrecks/event/shipwreck-{name}-{year}",
  "type": "Event",
  "_label": "{Ship Name} shipwreck ({Year})",
  "identified_by": [...],        // Ship name and alternate names
  "classified_as": [...],        // Event type (shipwreck) and cause
  "timespan": {...},             // When the shipwreck occurred
  "took_place_at": [...],        // Where it occurred (Place reference)
  "referred_to_by": [...],       // Descriptions, casualties, cargo, vessel specs
  "attributed_by": [...],        // Monetary values (ship and cargo)
  "caused_by": [...],            // Weather/environmental causes
  "used_specific_object": [...]  // Reference to the ship
}
```

### Place Schema

Places are modeled with the following structure:

```json
{
  "@context": "https://linked.art/ns/v1/linked-art.json",
  "id": "https://example.org/nj-shipwrecks/place/{type}-{name}",
  "type": "Place",
  "_label": "{Place Name}",
  "identified_by": [...],        // Place name
  "classified_as": [...],        // Place type (shipwreck site, port, shipyard)
  "defined_by": "POINT(...)",    // Coordinates (when available)
  "part_of": [...]               // Broader geographic context
}
```

## Key Features

### Rich Semantic Relationships
- Events linked to places through `took_place_at`
- Hierarchical place relationships via `part_of`
- Causal relationships through `caused_by`
- Temporal precision with ISO 8601 dates
- Monetary valuations with currency specification

### Getty AAT Integration
Uses Getty Art & Architecture Thesaurus (AAT) for controlled vocabulary:
- Event types: `http://vocab.getty.edu/aat/300054734` (shipwreck)
- Names: `http://vocab.getty.edu/aat/300404670` (Primary Name)
- Ports: `http://vocab.getty.edu/aat/300008738` (port)
- Shipyards: `http://vocab.getty.edu/aat/300006999` (shipyard)

### Comprehensive Data Capture
- Ship identification (name, aka)
- Vessel specifications (type, dimensions, tonnage, construction)
- Event details (date, location, cause)
- Human impact (crew, passengers, casualties)
- Economic data (ship value, cargo value)
- Cargo manifests
- Rescue operations (USLSS stations)

## Usage Examples

### Loading and Querying Events

```python
import json

# Load events
with open('shipwreck_events.json', 'r') as f:
    events = json.load(f)

# Find events by year
events_1913 = [e for e in events 
               if '1913' in e.get('timespan', {}).get('begin_of_the_begin', '')]

# Find events by cause
groundings = [e for e in events 
              if any('grounded' in c.get('_label', '').lower() 
                    for c in e.get('classified_as', []))]

# Find events with high casualty counts
high_casualties = [e for e in events 
                   if any('Lives Lost' in r.get('content', '') and 
                         int(r['content'].split('Lives Lost: ')[1].split(',')[0]) > 10
                         for r in e.get('referred_to_by', [])
                         if 'Lives Lost' in r.get('content', ''))]
```

### Spatial Queries with Places

```python
# Load places
with open('places.json', 'r') as f:
    places = json.load(f)

# Find places with coordinates
places_with_coords = [p for p in places if 'defined_by' in p]

# Extract coordinates for mapping
coords = []
for place in places_with_coords:
    if place['defined_by'].startswith('POINT'):
        lon, lat = place['defined_by'].replace('POINT(', '').replace(')', '').split()
        coords.append({
            'name': place['_label'],
            'lat': float(lat),
            'lon': float(lon)
        })
```

## Extending the Model

### Additional Entities to Consider

1. **HumanMadeObject** - Full ship records with construction details
2. **Person** - Ship masters and crew members
3. **Group** - Crew and passenger groups
4. **Organization** - Ship owners, USLSS, insurance companies
5. **DigitalObject** - Photos, maps, archival documents

### Additional Relationships

```json
// Rescue operations
"carried_out_by": [
  {
    "id": "https://example.org/organization/uslss-station-97",
    "type": "Organization",
    "_label": "USLSS Station #97"
  }
]

// Salvage attempts
"influenced": [
  {
    "id": "https://example.org/activity/salvage-{id}",
    "type": "Activity",
    "_label": "Salvage operation"
  }
]
```

## Data Quality Notes

### Strengths
- High completeness for core fields (ship name, date, location)
- Comprehensive cause of loss documentation
- Good coverage of vessel specifications
- Detailed casualty reporting

### Limitations
- Only 12.3% of places have precise coordinates
- Monetary values present for only 32.3% of events
- Some dates are approximate (year only)
- Crew/passenger counts incomplete for older records

### Recommended Enhancements
1. **Geocoding** - Add coordinates for remaining 87.7% of places
2. **Authority linking** - Connect to:
   - TGN (Getty Thesaurus of Geographic Names) for places
   - ULAN (Union List of Artist Names) for ship masters
   - VIAF for organizations
3. **Digital resources** - Link to archival photos and documents
4. **Historical context** - Add period events (wars, economic conditions)
5. **Archaeological data** - Link to modern survey/dive site information

## Technical Specifications

### URI Structure
- Events: `https://example.org/nj-shipwrecks/event/shipwreck-{name}-{year}`
- Places: `https://example.org/nj-shipwrecks/place/{type}-{normalized-name}`
- Ships: `https://example.org/nj-shipwrecks/object/ship-{name}`

### Context
All entities use the Linked Art context: `https://linked.art/ns/v1/linked-art.json`

### Date Format
ISO 8601: `YYYY-MM-DDTHH:MM:SSZ`

### Coordinate Format
Well-Known Text (WKT): `POINT(longitude latitude)`

## Integration Opportunities

This dataset can be integrated with:
- **Maritime heritage databases** - NOAA shipwrecks, state databases
- **Cultural heritage platforms** - Arches, CollectiveAccess
- **GIS systems** - QGIS, ArcGIS for spatial analysis
- **Graph databases** - Neo4j, Blazegraph for relationship queries
- **Linked Open Data** - Integration with Wikidata, DBpedia

## References

- **Linked Art**: https://linked.art/
- **Linked Art API**: https://linked.art/api/1.0/
- **Linked Art Model**: https://linked.art/model/
- **Getty AAT**: https://www.getty.edu/research/tools/vocabularies/aat/
- **CIDOC-CRM**: https://cidoc-crm.org/

## License & Attribution

This transformation maintains the original dataset's licensing. When using this data, please cite both:
1. The original NJ Maritime Shipwreck Database source
2. This Linked Art transformation

## Contact & Contributions

For questions about the mapping specification or to suggest improvements, please refer to the mapping documentation.

---

**Generated**: December 2024
**Linked Art Version**: 1.0
**Total Records**: 4,600 events, 3,558 places
**Validation Status**: ✅ 100% Valid
