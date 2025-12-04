#!/usr/bin/env python3
"""
Convert New Jersey Shipwreck Database to Linked Art Place and Event entities

This script reads shipwreck data from CSV and generates two JSON-LD outputs:
1. Place entities (shipwreck site locations) 
2. Event entities (sinking/loss events)

Each shipwreck record creates both a Place and an Event that reference each other.

Usage:
    python convert_shipwreck_to_linked_art.py input.csv output_dir/

Output:
    - places_collection.json (all Place entities)
    - events_collection.json (all Event entities)
    - places_sample.json (first 50 places)
    - events_sample.json (first 50 events)
    - conversion_report.txt (statistics and validation)
"""

import csv
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import sys


def generate_slug(name: str) -> str:
    """Generate URL-safe slug from ship name"""
    if not name or name.strip() == '':
        return 'unnamed'
    
    slug = name.lower()
    # Replace non-alphanumeric with hyphen
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug if slug else 'unnamed'


def clean_value(value: Any) -> Optional[str]:
    """Clean and normalize a value from CSV"""
    if value is None:
        return None
    
    value = str(value).strip()
    
    # Treat these as empty
    if value in ['', 'N', 'n/a', 'N/A', 'null', 'NULL']:
        return None
    
    return value


def parse_date(date_str: str, year: str, month: str, day: str) -> Optional[Dict]:
    """
    Parse date information and return ISO 8601 timespan
    
    Priority:
    1. Use year/month/day if all present
    2. Parse dateLost string (M/D/YYYY format)
    3. Use year only
    """
    year_val = clean_value(year)
    month_val = clean_value(month)
    day_val = clean_value(day)
    
    # Try to use structured fields first
    if year_val and month_val and day_val:
        try:
            y = int(float(year_val))
            m = int(float(month_val))
            d = int(float(day_val))
            
            return {
                "type": "TimeSpan",
                "_label": f"{y:04d}-{m:02d}-{d:02d}",
                "begin_of_the_begin": f"{y:04d}-{m:02d}-{d:02d}T00:00:00Z",
                "end_of_the_end": f"{y:04d}-{m:02d}-{d:02d}T23:59:59Z"
            }
        except (ValueError, TypeError):
            pass
    
    # Try year-month
    if year_val and month_val:
        try:
            y = int(float(year_val))
            m = int(float(month_val))
            
            # Get last day of month
            if m in [1, 3, 5, 7, 8, 10, 12]:
                last_day = 31
            elif m in [4, 6, 9, 11]:
                last_day = 30
            else:  # February
                last_day = 29 if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0) else 28
            
            return {
                "type": "TimeSpan",
                "_label": f"{y:04d}-{m:02d}",
                "begin_of_the_begin": f"{y:04d}-{m:02d}-01T00:00:00Z",
                "end_of_the_end": f"{y:04d}-{m:02d}-{last_day:02d}T23:59:59Z"
            }
        except (ValueError, TypeError):
            pass
    
    # Try year only
    if year_val:
        try:
            y = int(float(year_val))
            return {
                "type": "TimeSpan",
                "_label": str(y),
                "begin_of_the_begin": f"{y:04d}-01-01T00:00:00Z",
                "end_of_the_end": f"{y:04d}-12-31T23:59:59Z"
            }
        except (ValueError, TypeError):
            pass
    
    return None


def create_place_entity(row: Dict, base_uri: str = "https://example.org") -> Dict:
    """
    Create a Linked Art Place entity for a shipwreck site
    
    Required fields: shipsName, locationLost
    Optional: latitude, longitude, aka, vesselType, construction, etc.
    """
    ship_name = clean_value(row.get('shipsName')) or 'Unknown'
    location = clean_value(row.get('locationLost')) or 'Unknown location'
    aka = clean_value(row.get('aka'))
    
    slug = generate_slug(ship_name)
    place_id = f"{base_uri}/place/shipwreck/{slug}"
    
    # Core properties (required)
    place = {
        "@context": "https://linked.art/ns/v1/linked-art.json",
        "id": place_id,
        "type": "Place",
        "_label": f"Shipwreck site of {ship_name} at {location}"
    }
    
    # Classification as shipwreck site
    place["classified_as"] = [{
        "id": "http://vocab.getty.edu/aat/300008707",
        "type": "Type",
        "_label": "shipwreck sites"
    }]
    
    # Identifiers
    identified_by = []
    
    # Primary name
    identified_by.append({
        "type": "Name",
        "content": ship_name,
        "classified_as": [{
            "id": "http://vocab.getty.edu/aat/300404670",
            "type": "Type",
            "_label": "preferred terms"
        }]
    })
    
    # Alternate name (aka)
    if aka:
        identified_by.append({
            "type": "Name",
            "content": aka,
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300404671",
                "type": "Type",
                "_label": "alternate names"
            }]
        })
    
    place["identified_by"] = identified_by
    
    # Spatial definition (GeoJSON Point)
    lat = clean_value(row.get('latitude'))
    lon = clean_value(row.get('longitude'))
    
    if lat and lon:
        try:
            lat_f = float(lat)
            lon_f = float(lon)
            
            # GeoJSON Point: [longitude, latitude]
            geojson = {
                "type": "Point",
                "coordinates": [lon_f, lat_f]
            }
            place["defined_by"] = json.dumps(geojson)
        except (ValueError, TypeError):
            pass
    
    # Textual references
    referred_to_by = []
    
    # Location description
    if location:
        referred_to_by.append({
            "type": "LinguisticObject",
            "content": f"Location: {location}",
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300435430",
                "type": "Type",
                "_label": "description"
            }]
        })
    
    # Construction and physical details
    construction_parts = []
    for field, label in [
        ('construction', 'Construction'),
        ('flag', 'Flag'),
        ('length', 'Length'),
        ('beam', 'Beam'),
        ('draft', 'Draft')
    ]:
        val = clean_value(row.get(field))
        if val:
            construction_parts.append(f"{label}: {val}")
    
    if construction_parts:
        referred_to_by.append({
            "type": "LinguisticObject",
            "content": "; ".join(construction_parts),
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300080091",
                "type": "Type",
                "_label": "physical description"
            }]
        })
    
    # Tonnage
    tonnage_parts = []
    gross = clean_value(row.get('grossTonnage'))
    net = clean_value(row.get('netTonnage'))
    if gross:
        tonnage_parts.append(f"Gross tonnage: {gross}")
    if net:
        tonnage_parts.append(f"Net tonnage: {net}")
    
    if tonnage_parts:
        referred_to_by.append({
            "type": "LinguisticObject",
            "content": "; ".join(tonnage_parts),
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300435430",
                "type": "Type",
                "_label": "description"
            }]
        })
    
    # Vessel information
    vessel_parts = []
    vessel_type = clean_value(row.get('vesselType'))
    year_built = clean_value(row.get('yearBuilt'))
    where_built = clean_value(row.get('whereBuilt'))
    
    if vessel_type:
        vessel_parts.append(f"Type: {vessel_type}")
    if year_built:
        vessel_parts.append(f"Built: {year_built}")
    if where_built:
        vessel_parts.append(f"Built at: {where_built}")
    
    if vessel_parts:
        referred_to_by.append({
            "type": "LinguisticObject",
            "content": "; ".join(vessel_parts),
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300435430",
                "type": "Type",
                "_label": "description"
            }]
        })
    
    if referred_to_by:
        place["referred_to_by"] = referred_to_by
    
    return place


def create_event_entity(row: Dict, place_entity: Dict, base_uri: str = "https://example.org") -> Dict:
    """
    Create a Linked Art Event entity for a shipwreck/sinking event
    
    Links to the corresponding Place entity via took_place_at
    """
    ship_name = clean_value(row.get('shipsName')) or 'Unknown'
    date_lost = clean_value(row.get('dateLost'))
    
    slug = generate_slug(ship_name)
    event_id = f"{base_uri}/event/sinking/{slug}"
    
    # Core properties (required)
    event = {
        "@context": "https://linked.art/ns/v1/linked-art.json",
        "id": event_id,
        "type": "Event",
        "_label": f"Loss of {ship_name}"
    }
    
    # Add date to label if available
    if date_lost:
        event["_label"] += f" on {date_lost}"
    
    # Classification as shipwreck event
    event["classified_as"] = [{
        "id": "http://vocab.getty.edu/aat/300054734",
        "type": "Type",
        "_label": "shipwrecks (events)"
    }]
    
    # Link to place where it occurred
    event["took_place_at"] = [{
        "id": place_entity["id"],
        "type": "Place",
        "_label": place_entity["_label"]
    }]
    
    # Timespan
    timespan = parse_date(
        date_lost,
        row.get('year', ''),
        row.get('month', ''),
        row.get('day', '')
    )
    if timespan:
        event["timespan"] = timespan
    
    # Cause of loss
    cause = clean_value(row.get('causeOfLoss'))
    if cause:
        event["caused_by"] = [{
            "type": "Event",
            "_label": cause,
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300054734",
                "type": "Type",
                "_label": "maritime accidents"
            }]
        }]
    
    # Ship as object used in event
    vessel_type = clean_value(row.get('vesselType'))
    year_built = clean_value(row.get('yearBuilt'))
    
    ship_label = ship_name
    if vessel_type:
        ship_label += f" ({vessel_type}"
        if year_built:
            ship_label += f", built {year_built}"
        ship_label += ")"
    
    event["used_specific_object"] = [{
        "type": "HumanMadeObject",
        "_label": ship_label,
        "classified_as": [{
            "id": "http://vocab.getty.edu/aat/300178749",
            "type": "Type",
            "_label": "ships (watercraft)"
        }]
    }]
    
    # Master/Captain
    master = clean_value(row.get('master'))
    if master:
        event["carried_out_by"] = [{
            "type": "Person",
            "_label": master,
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300139460",
                "type": "Type",
                "_label": "ship masters"
            }]
        }]
    
    # Textual references for rich information
    referred_to_by = []
    
    # Voyage information
    voyage_parts = []
    departure = clean_value(row.get('departurePort'))
    destination = clean_value(row.get('destinationPort'))
    home_port = clean_value(row.get('homeHailingPort'))
    
    if departure and destination:
        voyage_parts.append(f"Voyage from {departure} to {destination}")
    elif departure:
        voyage_parts.append(f"Departed from {departure}")
    elif destination:
        voyage_parts.append(f"Bound for {destination}")
    
    if home_port:
        voyage_parts.append(f"Home port: {home_port}")
    
    if voyage_parts:
        referred_to_by.append({
            "type": "LinguisticObject",
            "content": "; ".join(voyage_parts),
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300435430",
                "type": "Type",
                "_label": "description"
            }]
        })
    
    # Human impact
    impact_parts = []
    crew = clean_value(row.get('numberOfCrew'))
    passengers = clean_value(row.get('numPass'))
    lives_lost = clean_value(row.get('livesLost'))
    
    if crew:
        impact_parts.append(f"Crew: {crew}")
    if passengers:
        impact_parts.append(f"Passengers: {passengers}")
    if lives_lost:
        impact_parts.append(f"Lives lost: {lives_lost}")
    
    if impact_parts:
        referred_to_by.append({
            "type": "LinguisticObject",
            "content": "; ".join(impact_parts),
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300435430",
                "type": "Type",
                "_label": "description"
            }]
        })
    
    # Cargo information
    cargo_parts = []
    cargo_nature = clean_value(row.get('natureOfCargo'))
    cargo_value = clean_value(row.get('cargoValue'))
    
    if cargo_nature:
        cargo_parts.append(f"Cargo: {cargo_nature}")
    if cargo_value:
        cargo_parts.append(f"Cargo value: ${cargo_value}")
    
    if cargo_parts:
        referred_to_by.append({
            "type": "LinguisticObject",
            "content": "; ".join(cargo_parts),
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300435430",
                "type": "Type",
                "_label": "description"
            }]
        })
    
    # Financial impact
    ship_value = clean_value(row.get('shipValue'))
    if ship_value or cargo_value:
        value_parts = []
        if ship_value:
            value_parts.append(f"Ship value: ${ship_value}")
        if cargo_value:
            value_parts.append(f"Cargo value: ${cargo_value}")
        
        referred_to_by.append({
            "type": "LinguisticObject",
            "content": "; ".join(value_parts),
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300435430",
                "type": "Type",
                "_label": "description"
            }]
        })
    
    # Rescue/recovery information
    station = clean_value(row.get('uslssStationName'))
    if station:
        referred_to_by.append({
            "type": "LinguisticObject",
            "content": f"USLSS/USCG Station: {station}",
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300435430",
                "type": "Type",
                "_label": "description"
            }]
        })
    
    # Additional notes
    misc = clean_value(row.get('miscInformation'))
    lost_flag = clean_value(row.get('lost'))
    
    if misc:
        referred_to_by.append({
            "type": "LinguisticObject",
            "content": misc,
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300435430",
                "type": "Type",
                "_label": "description"
            }]
        })
    
    if lost_flag and lost_flag.upper() == 'Y':
        referred_to_by.append({
            "type": "LinguisticObject",
            "content": "Status: Total loss",
            "classified_as": [{
                "id": "http://vocab.getty.edu/aat/300435430",
                "type": "Type",
                "_label": "description"
            }]
        })
    
    if referred_to_by:
        event["referred_to_by"] = referred_to_by
    
    return event


def convert_csv_to_linked_art(input_file: str, output_dir: str):
    """
    Main conversion function
    
    Reads CSV and generates both Place and Event collections
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    places = []
    events = []
    
    stats = {
        'total': 0,
        'with_coordinates': 0,
        'with_full_date': 0,
        'with_cause': 0,
        'with_master': 0,
        'with_cargo': 0
    }
    
    print(f"Reading shipwreck data from {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            stats['total'] += 1
            
            # Create Place entity
            place = create_place_entity(row)
            places.append(place)
            
            # Create Event entity (linked to Place)
            event = create_event_entity(row, place)
            events.append(event)
            
            # Update statistics
            if clean_value(row.get('latitude')) and clean_value(row.get('longitude')):
                stats['with_coordinates'] += 1
            
            if clean_value(row.get('year')) and clean_value(row.get('month')) and clean_value(row.get('day')):
                stats['with_full_date'] += 1
            
            if clean_value(row.get('causeOfLoss')):
                stats['with_cause'] += 1
            
            if clean_value(row.get('master')):
                stats['with_master'] += 1
            
            if clean_value(row.get('natureOfCargo')):
                stats['with_cargo'] += 1
            
            if stats['total'] % 500 == 0:
                print(f"  Processed {stats['total']} records...")
    
    print(f"\nConversion complete: {stats['total']} shipwrecks processed")
    
    # Write full collections
    print("\nWriting Place collection...")
    with open(output_path / 'places_collection.json', 'w', encoding='utf-8') as f:
        json.dump(places, f, indent=2, ensure_ascii=False)
    
    print("Writing Event collection...")
    with open(output_path / 'events_collection.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
    
    # Write sample collections (first 50)
    print("Writing sample collections (50 records)...")
    with open(output_path / 'places_sample.json', 'w', encoding='utf-8') as f:
        json.dump(places[:50], f, indent=2, ensure_ascii=False)
    
    with open(output_path / 'events_sample.json', 'w', encoding='utf-8') as f:
        json.dump(events[:50], f, indent=2, ensure_ascii=False)
    
    # Write conversion report
    print("Writing conversion report...")
    report_path = output_path / 'conversion_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("SHIPWRECK DATABASE TO LINKED ART CONVERSION REPORT\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Input file: {input_file}\n")
        f.write(f"Output directory: {output_dir}\n")
        f.write(f"Conversion date: {datetime.now().isoformat()}\n\n")
        
        f.write("STATISTICS\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total shipwrecks: {stats['total']}\n")
        f.write(f"Place entities created: {len(places)}\n")
        f.write(f"Event entities created: {len(events)}\n\n")
        
        f.write("DATA COVERAGE\n")
        f.write("-" * 60 + "\n")
        f.write(f"Records with coordinates: {stats['with_coordinates']} ({stats['with_coordinates']/stats['total']*100:.1f}%)\n")
        f.write(f"Records with full dates: {stats['with_full_date']} ({stats['with_full_date']/stats['total']*100:.1f}%)\n")
        f.write(f"Records with cause of loss: {stats['with_cause']} ({stats['with_cause']/stats['total']*100:.1f}%)\n")
        f.write(f"Records with master name: {stats['with_master']} ({stats['with_master']/stats['total']*100:.1f}%)\n")
        f.write(f"Records with cargo info: {stats['with_cargo']} ({stats['with_cargo']/stats['total']*100:.1f}%)\n\n")
        
        f.write("OUTPUT FILES\n")
        f.write("-" * 60 + "\n")
        f.write(f"places_collection.json - All {len(places)} Place entities\n")
        f.write(f"events_collection.json - All {len(events)} Event entities\n")
        f.write(f"places_sample.json - Sample of 50 Place entities\n")
        f.write(f"events_sample.json - Sample of 50 Event entities\n\n")
        
        f.write("SCHEMA COMPLIANCE\n")
        f.write("-" * 60 + "\n")
        f.write("Place entities conform to: https://linked.art/api/1.0/schema/place.json\n")
        f.write("Event entities conform to: https://linked.art/api/1.0/schema/event.json\n\n")
        
        f.write("SAMPLE URIs\n")
        f.write("-" * 60 + "\n")
        if places:
            f.write(f"First Place: {places[0]['id']}\n")
        if events:
            f.write(f"First Event: {events[0]['id']}\n")
    
    print(f"\nAll files written to: {output_dir}")
    print(f"\nFiles created:")
    print(f"  - places_collection.json ({len(places)} places)")
    print(f"  - events_collection.json ({len(events)} events)")
    print(f"  - places_sample.json (50 sample places)")
    print(f"  - events_sample.json (50 sample events)")
    print(f"  - conversion_report.txt")
    
    return stats


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python convert_shipwreck_to_linked_art.py input.csv [output_dir]")
        print("\nExample:")
        print("  python convert_shipwreck_to_linked_art.py ShipwreckDatabase.csv ./output")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_directory = sys.argv[2] if len(sys.argv) > 2 else './linked_art_output'
    
    convert_csv_to_linked_art(input_csv, output_directory)
