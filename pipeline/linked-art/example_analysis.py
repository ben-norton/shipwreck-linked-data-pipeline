#!/usr/bin/env python3
"""
Example Analysis Scripts for NJ Shipwreck Linked Art Data

Demonstrates various analytical queries and visualizations using the transformed data.
"""

import json
from collections import Counter, defaultdict
from datetime import datetime
import csv
from pathlib import Path
root_dir = Path(__file__).resolve().parents[2]

def load_data():
    """Load the Linked Art JSON files."""

    eventsJson = str(root_dir) + '/pipeline/linked-art/output/shipwreck_events.json'
    with open(eventsJson, 'r') as f:
        events = json.load(f)

    placesJson = str(root_dir) + '/pipeline/linked-art/output/shipwreck_places.json'
    with open(placesJson, 'r') as f:
        places = json.load(f)
    
    return events, places


def temporal_analysis(events):
    """Analyze shipwrecks over time."""
    print("\n" + "="*60)
    print("TEMPORAL ANALYSIS")
    print("="*60 + "\n")
    
    # Extract years
    years = []
    for event in events:
        timespan = event.get('timespan', {})
        begin = timespan.get('begin_of_the_begin', '')
        if begin:
            year = int(begin[:4])
            years.append(year)
    
    # Decade analysis
    decade_counts = Counter(y // 10 * 10 for y in years)
    
    print("Shipwrecks by Decade:")
    print("-" * 40)
    for decade in sorted(decade_counts.keys()):
        count = decade_counts[decade]
        bar = "█" * (count // 10)
        print(f"{decade}s: {count:4d} {bar}")
    
    # Century analysis
    print("\nShipwrecks by Century:")
    print("-" * 40)
    century_counts = Counter(y // 100 * 100 for y in years)
    for century in sorted(century_counts.keys()):
        count = century_counts[century]
        print(f"{century}s: {count:4d}")


def cause_analysis(events):
    """Analyze causes of loss."""
    print("\n" + "="*60)
    print("CAUSE OF LOSS ANALYSIS")
    print("="*60 + "\n")
    
    causes = []
    for event in events:
        for classification in event.get('classified_as', []):
            for meta_class in classification.get('classified_as', []):
                if 'Cause' in meta_class.get('_label', ''):
                    causes.append(classification.get('_label', 'Unknown'))
    
    cause_counts = Counter(causes)
    
    print("Top 20 Causes of Loss:")
    print("-" * 40)
    for i, (cause, count) in enumerate(cause_counts.most_common(20), 1):
        pct = count / len(events) * 100
        print(f"{i:2d}. {cause:30s} {count:4d} ({pct:4.1f}%)")


def casualty_analysis(events):
    """Analyze casualties."""
    print("\n" + "="*60)
    print("CASUALTY ANALYSIS")
    print("="*60 + "\n")
    
    total_lives_lost = 0
    events_with_casualties = 0
    total_crew = 0
    total_passengers = 0
    
    for event in events:
        for referred in event.get('referred_to_by', []):
            if any(c.get('_label') == 'Casualty Report' 
                   for c in referred.get('classified_as', [])):
                content = referred.get('content', '')
                
                # Parse lives lost
                if 'Lives Lost:' in content:
                    try:
                        lives = int(content.split('Lives Lost:')[1].split(',')[0].strip())
                        if lives > 0:
                            total_lives_lost += lives
                            events_with_casualties += 1
                    except (ValueError, IndexError):
                        pass
                
                # Parse crew
                if 'Crew:' in content:
                    try:
                        crew = int(content.split('Crew:')[1].split(',')[0].strip())
                        total_crew += crew
                    except (ValueError, IndexError):
                        pass
                
                # Parse passengers
                if 'Passengers:' in content:
                    try:
                        passengers = int(content.split('Passengers:')[1].split(',')[0].strip())
                        total_passengers += passengers
                    except (ValueError, IndexError):
                        pass
    
    print(f"Total lives lost: {total_lives_lost:,}")
    print(f"Events with casualties: {events_with_casualties} ({events_with_casualties/len(events)*100:.1f}%)")
    print(f"Average lives lost per fatal event: {total_lives_lost/events_with_casualties:.1f}")
    print(f"\nTotal crew recorded: {total_crew:,}")
    print(f"Total passengers recorded: {total_passengers:,}")
    
    # Find deadliest events
    print("\nDeadliest Shipwrecks:")
    print("-" * 60)
    
    deadly_events = []
    for event in events:
        for referred in event.get('referred_to_by', []):
            if any(c.get('_label') == 'Casualty Report' 
                   for c in referred.get('classified_as', [])):
                content = referred.get('content', '')
                if 'Lives Lost:' in content:
                    try:
                        lives = int(content.split('Lives Lost:')[1].split(',')[0].strip())
                        if lives > 0:
                            deadly_events.append({
                                'name': event.get('_label', 'Unknown'),
                                'lives': lives,
                                'year': event.get('timespan', {}).get('begin_of_the_begin', 'Unknown')[:4]
                            })
                    except (ValueError, IndexError):
                        pass
    
    for i, evt in enumerate(sorted(deadly_events, key=lambda x: x['lives'], reverse=True)[:10], 1):
        print(f"{i:2d}. {evt['name']:40s} {evt['lives']:3d} lives ({evt['year']})")


def economic_analysis(events):
    """Analyze economic losses."""
    print("\n" + "="*60)
    print("ECONOMIC ANALYSIS")
    print("="*60 + "\n")
    
    total_ship_value = 0
    total_cargo_value = 0
    ship_value_count = 0
    cargo_value_count = 0
    
    for event in events:
        for attribution in event.get('attributed_by', []):
            for classification in attribution.get('classified_as', []):
                label = classification.get('_label', '')
                
                for assigned in attribution.get('assigned', []):
                    value = assigned.get('value', 0)
                    
                    if 'Ship Value' in label:
                        total_ship_value += value
                        ship_value_count += 1
                    elif 'Cargo Value' in label:
                        total_cargo_value += value
                        cargo_value_count += 1
    
    print(f"Total ship losses recorded: {ship_value_count}")
    print(f"Total ship value lost: ${total_ship_value:,.0f}")
    print(f"Average ship value: ${total_ship_value/ship_value_count:,.0f}")
    
    print(f"\nTotal cargo losses recorded: {cargo_value_count}")
    print(f"Total cargo value lost: ${total_cargo_value:,.0f}")
    print(f"Average cargo value: ${total_cargo_value/cargo_value_count:,.0f}")
    
    print(f"\nTotal economic loss: ${total_ship_value + total_cargo_value:,.0f}")


def geographic_analysis(events, places):
    """Analyze geographic distribution."""
    print("\n" + "="*60)
    print("GEOGRAPHIC ANALYSIS")
    print("="*60 + "\n")
    
    # Location frequency
    locations = []
    for event in events:
        for place_ref in event.get('took_place_at', []):
            locations.append(place_ref.get('_label', 'Unknown'))
    
    location_counts = Counter(locations)
    
    print("Top 15 Shipwreck Locations:")
    print("-" * 60)
    for i, (location, count) in enumerate(location_counts.most_common(15), 1):
        print(f"{i:2d}. {location:45s} {count:4d}")
    
    # Coordinate coverage
    places_with_coords = sum(1 for p in places if 'defined_by' in p)
    print(f"\nPlaces with coordinates: {places_with_coords}/{len(places)} ({places_with_coords/len(places)*100:.1f}%)")


def vessel_type_analysis(events):
    """Analyze vessel types."""
    print("\n" + "="*60)
    print("VESSEL TYPE ANALYSIS")
    print("="*60 + "\n")
    
    vessel_types = []
    for event in events:
        for referred in event.get('referred_to_by', []):
            if any(c.get('_label') == 'Vessel Specifications' 
                   for c in referred.get('classified_as', [])):
                content = referred.get('content', '')
                if 'Type:' in content:
                    vessel_type = content.split('Type:')[1].split(';')[0].strip()
                    vessel_types.append(vessel_type)
    
    type_counts = Counter(vessel_types)
    
    print("Top 20 Vessel Types:")
    print("-" * 40)
    for i, (vtype, count) in enumerate(type_counts.most_common(20), 1):
        pct = count / len(vessel_types) * 100
        print(f"{i:2d}. {vtype:25s} {count:4d} ({pct:4.1f}%)")


def generate_csv_summary(events, output_path):
    """Generate a CSV summary for further analysis."""
    print("\n" + "="*60)
    print("GENERATING CSV SUMMARY")
    print("="*60 + "\n")
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Ship Name', 'Year', 'Location', 'Cause', 'Lives Lost', 
                        'Ship Value', 'Cargo Value', 'Vessel Type'])
        
        for event in events:
            name = event.get('_label', 'Unknown')
            
            # Extract year
            year = 'Unknown'
            timespan = event.get('timespan', {})
            if 'begin_of_the_begin' in timespan:
                year = timespan['begin_of_the_begin'][:4]
            
            # Extract location
            location = 'Unknown'
            if event.get('took_place_at'):
                location = event['took_place_at'][0].get('_label', 'Unknown')
            
            # Extract cause
            cause = 'Unknown'
            for classification in event.get('classified_as', []):
                for meta_class in classification.get('classified_as', []):
                    if 'Cause' in meta_class.get('_label', ''):
                        cause = classification.get('_label', 'Unknown')
            
            # Extract casualties
            lives_lost = 0
            for referred in event.get('referred_to_by', []):
                if any(c.get('_label') == 'Casualty Report' 
                       for c in referred.get('classified_as', [])):
                    content = referred.get('content', '')
                    if 'Lives Lost:' in content:
                        try:
                            lives_lost = int(content.split('Lives Lost:')[1].split(',')[0].strip())
                        except (ValueError, IndexError):
                            pass
            
            # Extract values
            ship_value = ''
            cargo_value = ''
            for attribution in event.get('attributed_by', []):
                for classification in attribution.get('classified_as', []):
                    label = classification.get('_label', '')
                    for assigned in attribution.get('assigned', []):
                        value = assigned.get('value', '')
                        if 'Ship Value' in label:
                            ship_value = value
                        elif 'Cargo Value' in label:
                            cargo_value = value
            
            # Extract vessel type
            vessel_type = 'Unknown'
            for referred in event.get('referred_to_by', []):
                if any(c.get('_label') == 'Vessel Specifications' 
                       for c in referred.get('classified_as', [])):
                    content = referred.get('content', '')
                    if 'Type:' in content:
                        vessel_type = content.split('Type:')[1].split(';')[0].strip()
            
            writer.writerow([name, year, location, cause, lives_lost, 
                           ship_value, cargo_value, vessel_type])
    
    print(f"CSV summary saved to: {output_path}")


def main():
    """Run all analyses."""
    print("\n" + "="*60)
    print("NJ SHIPWRECK LINKED ART DATA - ANALYSIS SUITE")
    print("="*60)
    
    events, places = load_data()
    
    print(f"\nLoaded {len(events):,} events and {len(places):,} places")
    
    # Run analyses
    temporal_analysis(events)
    cause_analysis(events)
    casualty_analysis(events)
    economic_analysis(events)
    geographic_analysis(events, places)
    vessel_type_analysis(events)
    
    # Generate CSV
    csv_path = str(root_dir) + '/pipeline/linked-art/output/shipwreck_summary.csv'
    generate_csv_summary(events, csv_path)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
