#!/usr/bin/env python3
"""
NJ Maritime Shipwreck Database to Linked Art Transformer

This script transforms the NJ Maritime Shipwreck Database CSV into Linked Art
Place and Event JSON entities following the mapping specification.
"""



import csv
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict
from pathlib import Path


class LinkedArtTransformer:
    """Transform shipwreck CSV data to Linked Art JSON format."""
    
    def __init__(self, base_uri: str = "https://example.org"):
        self.base_uri = base_uri
        self.context = "https://linked.art/ns/v1/linked-art.json"
        self.places_cache = {}  # Cache for created places
        
    def normalize_id(self, text: str) -> str:
        """Normalize text for use in URIs."""
        if not text:
            return "unknown"
        # Convert to lowercase, replace spaces with hyphens, remove special chars
        normalized = re.sub(r'[^\w\s-]', '', text.lower())
        normalized = re.sub(r'[-\s]+', '-', normalized)
        return normalized.strip('-')
    
    def parse_monetary_value(self, value_str: str) -> Optional[float]:
        """Parse monetary value string like '$50,000' to float."""
        if not value_str or value_str.strip() == '':
            return None
        # Remove $, commas, and whitespace
        cleaned = re.sub(r'[\$,\s]', '', value_str)
        try:
            return float(cleaned)
        except ValueError:
            return None
    
    def create_timespan(self, year: str, month: str, day: str, date_lost: str) -> Dict:
        """Create a TimeSpan object from date components."""
        timespan = {
            "type": "TimeSpan",
            "_label": date_lost or f"{year}"
        }
        
        try:
            year_int = int(float(year)) if year else None
            month_int = int(float(month)) if month else None
            day_int = int(float(day)) if day else None
            
            if year_int and month_int and day_int:
                date_str = f"{year_int:04d}-{month_int:02d}-{day_int:02d}"
                timespan["begin_of_the_begin"] = f"{date_str}T00:00:00Z"
                timespan["end_of_the_end"] = f"{date_str}T23:59:59Z"
            elif year_int:
                timespan["begin_of_the_begin"] = f"{year_int:04d}-01-01T00:00:00Z"
                timespan["end_of_the_end"] = f"{year_int:04d}-12-31T23:59:59Z"
        except (ValueError, TypeError):
            pass
        
        return timespan
    
    def create_place(self, 
                    location_name: str, 
                    latitude: str = None, 
                    longitude: str = None,
                    place_type: str = "shipwreck-site",
                    classification_label: str = "shipwreck site",
                    classification_id: str = "http://vocab.getty.edu/aat/300008025") -> Dict:
        """Create a Place entity."""
        
        if not location_name or location_name.strip() == '':
            return None
            
        normalized_name = self.normalize_id(location_name)
        place_id = f"{self.base_uri}/place/{place_type}-{normalized_name}"
        
        # Check cache
        if place_id in self.places_cache:
            return {"id": place_id, "type": "Place", "_label": location_name}
        
        place = {
            "@context": self.context,
            "id": place_id,
            "type": "Place",
            "_label": location_name,
            "identified_by": [
                {
                    "type": "Name",
                    "content": location_name,
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
                    "id": classification_id,
                    "type": "Type",
                    "_label": classification_label
                }
            ]
        }
        
        # Add coordinates if available
        if latitude and longitude:
            try:
                lat = float(latitude)
                lon = float(longitude)
                place["defined_by"] = f"POINT({lon} {lat})"
            except (ValueError, TypeError):
                pass
        
        # Add part_of for shipwreck sites
        if place_type == "shipwreck-site":
            place["part_of"] = [
                {
                    "id": f"{self.base_uri}/place/new-jersey",
                    "type": "Place",
                    "_label": "New Jersey"
                }
            ]
        
        self.places_cache[place_id] = place
        return place
    
    def create_port_place(self, port_name: str) -> Optional[Dict]:
        """Create a port Place entity."""
        if not port_name or port_name.strip() == '':
            return None
            
        return self.create_place(
            location_name=port_name,
            place_type="port",
            classification_label="port",
            classification_id="http://vocab.getty.edu/aat/300008738"
        )
    
    def create_shipwreck_event(self, row: Dict) -> Dict:
        """Transform a CSV row into a Linked Art Event (shipwreck)."""
        
        ship_name = row['shipsName']
        year = row['year']
        normalized_name = self.normalize_id(ship_name)
        
        event_id = f"{self.base_uri}/event/shipwreck-{normalized_name}-{year.split('.')[0] if year else 'unknown'}"
        
        event = {
            "@context": self.context,
            "id": event_id,
            "type": "Event",
            "_label": f"{ship_name} shipwreck ({year.split('.')[0] if year else 'unknown'})"
        }
        
        # identified_by: Name and identifiers
        identified_by = [
            {
                "type": "Name",
                "content": ship_name,
                "classified_as": [
                    {
                        "id": "http://vocab.getty.edu/aat/300404670",
                        "type": "Type",
                        "_label": "Primary Name"
                    }
                ]
            }
        ]
        
        # Add AKA if present
        if row.get('aka') and row['aka'].strip():
            identified_by.append({
                "type": "Name",
                "content": row['aka'],
                "classified_as": [
                    {
                        "id": "http://vocab.getty.edu/aat/300264273",
                        "type": "Type",
                        "_label": "Alternative Name"
                    }
                ]
            })
        
        event["identified_by"] = identified_by
        
        # classified_as: Event type and cause
        classified_as = [
            {
                "id": "http://vocab.getty.edu/aat/300054734",
                "type": "Type",
                "_label": "shipwreck"
            }
        ]
        
        if row.get('causeOfLoss') and row['causeOfLoss'].strip():
            cause_normalized = self.normalize_id(row['causeOfLoss'])
            classified_as.append({
                "id": f"{self.base_uri}/type/cause/{cause_normalized}",
                "type": "Type",
                "_label": row['causeOfLoss'],
                "classified_as": [
                    {
                        "id": "http://vocab.getty.edu/aat/300435424",
                        "type": "Type",
                        "_label": "Cause"
                    }
                ]
            })
        
        event["classified_as"] = classified_as
        
        # timespan
        event["timespan"] = self.create_timespan(
            row.get('year', ''),
            row.get('month', ''),
            row.get('day', ''),
            row.get('dateLost', '')
        )
        
        # took_place_at: Location
        if row.get('locationLost') and row['locationLost'].strip():
            location_place = self.create_place(
                row['locationLost'],
                row.get('latitude'),
                row.get('longitude')
            )
            if location_place:
                event["took_place_at"] = [
                    {
                        "id": location_place["id"],
                        "type": "Place",
                        "_label": location_place["_label"]
                    }
                ]
        
        # referred_to_by: Various descriptive information
        referred_to_by = []
        
        # Misc information
        if row.get('miscInformation') and row['miscInformation'].strip():
            referred_to_by.append({
                "type": "LinguisticObject",
                "content": row['miscInformation'],
                "classified_as": [
                    {
                        "id": "http://vocab.getty.edu/aat/300435416",
                        "type": "Type",
                        "_label": "Description"
                    }
                ]
            })
        
        # Casualty information
        crew = row.get('numberOfCrew', '')
        passengers = row.get('numPass', '')
        lives_lost = row.get('livesLost', '')
        
        casualty_parts = []
        if crew and crew.strip():
            casualty_parts.append(f"Crew: {crew}")
        if passengers and passengers.strip():
            casualty_parts.append(f"Passengers: {passengers}")
        if lives_lost and lives_lost.strip():
            casualty_parts.append(f"Lives Lost: {lives_lost}")
        
        if casualty_parts:
            referred_to_by.append({
                "type": "LinguisticObject",
                "content": ", ".join(casualty_parts),
                "classified_as": [
                    {
                        "id": "http://vocab.getty.edu/aat/300435425",
                        "type": "Type",
                        "_label": "Casualty Report"
                    }
                ]
            })
        
        # Cargo information
        if row.get('natureOfCargo') and row['natureOfCargo'].strip():
            cargo_text = f"Cargo: {row['natureOfCargo']}"
            if row.get('cargoValue') and row['cargoValue'].strip():
                cargo_text += f", Value: {row['cargoValue']}"
            
            referred_to_by.append({
                "type": "LinguisticObject",
                "content": cargo_text,
                "classified_as": [
                    {
                        "id": "http://vocab.getty.edu/aat/300435429",
                        "type": "Type",
                        "_label": "Cargo Manifest"
                    }
                ]
            })
        
        # Vessel details
        vessel_parts = []
        if row.get('vesselType') and row['vesselType'].strip():
            vessel_parts.append(f"Type: {row['vesselType']}")
        if row.get('construction') and row['construction'].strip():
            vessel_parts.append(f"Construction: {row['construction']}")
        if row.get('flag') and row['flag'].strip():
            vessel_parts.append(f"Flag: {row['flag']}")
        
        dimensions = []
        if row.get('length') and row['length'].strip():
            dimensions.append(f"Length: {row['length']}")
        if row.get('beam') and row['beam'].strip():
            dimensions.append(f"Beam: {row['beam']}")
        if row.get('draft') and row['draft'].strip():
            dimensions.append(f"Draft: {row['draft']}")
        if dimensions:
            vessel_parts.append(", ".join(dimensions))
        
        if row.get('grossTonnage') and row['grossTonnage'].strip():
            vessel_parts.append(f"Gross Tonnage: {row['grossTonnage']}")
        
        if vessel_parts:
            referred_to_by.append({
                "type": "LinguisticObject",
                "content": "; ".join(vessel_parts),
                "classified_as": [
                    {
                        "id": "http://vocab.getty.edu/aat/300435432",
                        "type": "Type",
                        "_label": "Vessel Specifications"
                    }
                ]
            })
        
        if referred_to_by:
            event["referred_to_by"] = referred_to_by
        
        # attributed_by: Value information
        attributed_by = []
        
        ship_value = self.parse_monetary_value(row.get('shipValue', ''))
        if ship_value:
            attributed_by.append({
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
                        "_label": row['shipValue'],
                        "value": ship_value,
                        "currency": {
                            "id": "http://vocab.getty.edu/aat/300411994",
                            "type": "Currency",
                            "_label": "US Dollar"
                        }
                    }
                ]
            })
        
        cargo_value = self.parse_monetary_value(row.get('cargoValue', ''))
        if cargo_value:
            attributed_by.append({
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
                        "_label": row['cargoValue'],
                        "value": cargo_value,
                        "currency": {
                            "id": "http://vocab.getty.edu/aat/300411994",
                            "type": "Currency",
                            "_label": "US Dollar"
                        }
                    }
                ]
            })
        
        if attributed_by:
            event["attributed_by"] = attributed_by
        
        # caused_by: Weather/environmental causes
        if row.get('causeOfLoss') and row['causeOfLoss'].strip():
            event["caused_by"] = [
                {
                    "type": "Event",
                    "_label": row['causeOfLoss'],
                    "classified_as": [
                        {
                            "id": "http://vocab.getty.edu/aat/300054734",
                            "type": "Type",
                            "_label": "natural phenomenon"
                        }
                    ]
                }
            ]
        
        # used_specific_object: Reference to the ship
        ship_obj_id = f"{self.base_uri}/object/ship-{normalized_name}"
        event["used_specific_object"] = [
            {
                "id": ship_obj_id,
                "type": "HumanMadeObject",
                "_label": ship_name
            }
        ]
        
        return event
    
    def transform_csv(self, csv_path: str, output_dir: str = "/pipeline/output"):
        """Transform entire CSV file to Linked Art JSON."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        events = []
        places = []
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader):
                try:
                    # Create event
                    event = self.create_shipwreck_event(row)
                    events.append(event)
                    
                    # Also track unique places for ports
                    for port_field in ['homeHailingPort', 'departurePort', 'destinationPort']:
                        if row.get(port_field) and row[port_field].strip():
                            self.create_port_place(row[port_field])
                    
                    # Construction site
                    if row.get('whereBuilt') and row['whereBuilt'].strip():
                        self.create_place(
                            row['whereBuilt'],
                            place_type="construction",
                            classification_label="shipyard",
                            classification_id="http://vocab.getty.edu/aat/300006999"
                        )
                    
                    if (i + 1) % 100 == 0:
                        print(f"Processed {i + 1} records...")
                        
                except Exception as e:
                    print(f"Error processing row {i + 1}: {e}")
                    continue
        
        # Get all places from cache
        places = list(self.places_cache.values())
        
        # Save events
        events_file = os.path.join(output_dir, "shipwreck_events.json")
        with open(events_file, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(events)} events to {events_file}")
        
        # Save places
        places_file = os.path.join(output_dir, "shipwreck_places.json")
        with open(places_file, 'w', encoding='utf-8') as f:
            json.dump(places, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(places)} places to {places_file}")
        
        # Save summary statistics
        stats = {
            "total_events": len(events),
            "total_places": len(places),
            "events_with_coordinates": sum(1 for e in events if 'took_place_at' in e),
            "events_with_casualties": sum(1 for e in events if any(
                r.get('classified_as', [{}])[0].get('_label') == 'Casualty Report'
                for r in e.get('referred_to_by', [])
            )),
            "date_range": {
                "earliest": min((e['timespan'].get('begin_of_the_begin', '')[:4] 
                               for e in events if 'timespan' in e and 'begin_of_the_begin' in e['timespan']), 
                              default="N/A"),
                "latest": max((e['timespan'].get('end_of_the_end', '')[:4] 
                              for e in events if 'timespan' in e and 'end_of_the_end' in e['timespan']),
                             default="N/A")
            }
        }
        
        stats_file = os.path.join(output_dir, "transformation_stats.json")
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        print(f"Saved statistics to {stats_file}")
        
        return events, places


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parents[2]

    transformer = LinkedArtTransformer(base_uri="https://example.org/nj-shipwrecks")
    
    csv_path = str(root_dir) + "/data/input/remapped/nj_maritime_shipwreck_database.csv"
    output_dir = str(root_dir) + "/pipeline/linked-art/output"
    
    print("Starting transformation...")
    events, places = transformer.transform_csv(csv_path, output_dir)
    print("\nTransformation complete!")
    print(f"Total events: {len(events)}")
    print(f"Total places: {len(places)}")
