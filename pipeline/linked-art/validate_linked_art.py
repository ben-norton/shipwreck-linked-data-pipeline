#!/usr/bin/env python3
"""
Linked Art JSON Validator

This script validates the generated JSON files against the Linked Art schemas
and provides a report on compliance and data quality.
"""

import json
from typing import Dict, List, Tuple
from pathlib import Path

class LinkedArtValidator:
    """Validate Linked Art JSON entities."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_event(self, event: Dict) -> Tuple[bool, List[str], List[str]]:
        """Validate an Event entity against the schema."""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ['@context', 'id', 'type', '_label']
        for field in required_fields:
            if field not in event:
                errors.append(f"Missing required field: {field}")
        
        # Type must be Event
        if event.get('type') not in ['Event', 'Activity', 'Period']:
            errors.append(f"Invalid type: {event.get('type')} (must be Event, Activity, or Period)")
        
        # Validate timespan if present
        if 'timespan' in event:
            if not isinstance(event['timespan'], dict):
                errors.append("timespan must be an object")
            elif 'type' not in event['timespan'] or event['timespan']['type'] != 'TimeSpan':
                errors.append("timespan must have type: TimeSpan")
        
        # Validate took_place_at if present
        if 'took_place_at' in event:
            if not isinstance(event['took_place_at'], list):
                errors.append("took_place_at must be an array")
            else:
                for place_ref in event['took_place_at']:
                    if not isinstance(place_ref, dict):
                        errors.append("took_place_at items must be objects")
                    elif place_ref.get('type') != 'Place':
                        errors.append(f"took_place_at item must have type: Place")
        
        # Validate identified_by if present
        if 'identified_by' in event:
            if not isinstance(event['identified_by'], list):
                errors.append("identified_by must be an array")
            else:
                for identifier in event['identified_by']:
                    if identifier.get('type') not in ['Name', 'Identifier']:
                        warnings.append(f"identified_by type should be Name or Identifier")
        
        # Validate classified_as if present
        if 'classified_as' in event:
            if not isinstance(event['classified_as'], list):
                errors.append("classified_as must be an array")
        
        # Check for recommended fields
        recommended_fields = ['timespan', 'took_place_at', 'identified_by', 'classified_as']
        for field in recommended_fields:
            if field not in event:
                warnings.append(f"Recommended field missing: {field}")
        
        return len(errors) == 0, errors, warnings
    
    def validate_place(self, place: Dict) -> Tuple[bool, List[str], List[str]]:
        """Validate a Place entity against the schema."""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ['@context', 'id', 'type', '_label']
        for field in required_fields:
            if field not in place:
                errors.append(f"Missing required field: {field}")
        
        # Type must be Place
        if place.get('type') != 'Place':
            errors.append(f"Invalid type: {place.get('type')} (must be Place)")
        
        # Validate defined_by if present
        if 'defined_by' in place:
            if not isinstance(place['defined_by'], str):
                errors.append("defined_by must be a string (WKT or GeoJSON)")
            elif not (place['defined_by'].startswith('POINT') or 
                     place['defined_by'].startswith('{')):
                warnings.append("defined_by should be WKT (POINT) or GeoJSON format")
        
        # Validate part_of if present
        if 'part_of' in place:
            if not isinstance(place['part_of'], list):
                errors.append("part_of must be an array")
            else:
                for parent_ref in place['part_of']:
                    if not isinstance(parent_ref, dict):
                        errors.append("part_of items must be objects")
                    elif parent_ref.get('type') != 'Place':
                        errors.append(f"part_of item must have type: Place")
        
        # Validate identified_by if present
        if 'identified_by' in place:
            if not isinstance(place['identified_by'], list):
                errors.append("identified_by must be an array")
        
        # Check for recommended fields
        recommended_fields = ['identified_by', 'classified_as']
        for field in recommended_fields:
            if field not in place:
                warnings.append(f"Recommended field missing: {field}")
        
        return len(errors) == 0, errors, warnings
    
    def validate_file(self, file_path: str, entity_type: str = 'event'):
        """Validate a JSON file containing multiple entities."""
        print(f"\n{'='*60}")
        print(f"Validating {file_path}")
        print(f"{'='*60}\n")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            entities = json.load(f)
        
        if not isinstance(entities, list):
            print(f"ERROR: File must contain an array of {entity_type}s")
            return
        
        total = len(entities)
        valid = 0
        total_errors = 0
        total_warnings = 0
        
        # Sample validation (first 10 entities for detailed output)
        sample_size = min(10, total)
        
        for i, entity in enumerate(entities):
            if entity_type == 'event':
                is_valid, errors, warnings = self.validate_event(entity)
            else:
                is_valid, errors, warnings = self.validate_place(entity)
            
            if is_valid:
                valid += 1
            
            total_errors += len(errors)
            total_warnings += len(warnings)
            
            # Print details for first few entities
            if i < sample_size:
                status = "✓ VALID" if is_valid else "✗ INVALID"
                print(f"{entity_type.capitalize()} {i+1}: {entity.get('_label', 'N/A')} - {status}")
                
                if errors:
                    for error in errors:
                        print(f"  ERROR: {error}")
                
                if warnings and i < 3:  # Only show warnings for first 3
                    for warning in warnings:
                        print(f"  WARNING: {warning}")
                print()
        
        # Summary
        print(f"\n{'='*60}")
        print(f"VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"Total {entity_type}s: {total}")
        print(f"Valid: {valid} ({valid/total*100:.1f}%)")
        print(f"Invalid: {total - valid} ({(total-valid)/total*100:.1f}%)")
        print(f"Total errors: {total_errors}")
        print(f"Total warnings: {total_warnings}")
        print(f"{'='*60}\n")
        
        # Data quality insights
        self.generate_insights(entities, entity_type)
    
    def generate_insights(self, entities: List[Dict], entity_type: str):
        """Generate data quality insights."""
        print(f"\n{'='*60}")
        print(f"DATA QUALITY INSIGHTS")
        print(f"{'='*60}\n")
        
        if entity_type == 'event':
            # Event-specific insights
            with_timespan = sum(1 for e in entities if 'timespan' in e)
            with_location = sum(1 for e in entities if 'took_place_at' in e)
            with_cause = sum(1 for e in entities if 'caused_by' in e)
            with_values = sum(1 for e in entities if 'attributed_by' in e)
            with_descriptions = sum(1 for e in entities if 'referred_to_by' in e)
            
            print(f"Events with timespan: {with_timespan} ({with_timespan/len(entities)*100:.1f}%)")
            print(f"Events with location: {with_location} ({with_location/len(entities)*100:.1f}%)")
            print(f"Events with cause: {with_cause} ({with_cause/len(entities)*100:.1f}%)")
            print(f"Events with monetary values: {with_values} ({with_values/len(entities)*100:.1f}%)")
            print(f"Events with descriptions: {with_descriptions} ({with_descriptions/len(entities)*100:.1f}%)")
            
            # Classification analysis
            causes = {}
            for e in entities:
                for classification in e.get('classified_as', []):
                    if 'Cause' in str(classification.get('classified_as', [])):
                        cause = classification.get('_label', 'Unknown')
                        causes[cause] = causes.get(cause, 0) + 1
            
            print(f"\nTop 10 Causes of Loss:")
            for cause, count in sorted(causes.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {cause}: {count}")
        
        else:  # place
            # Place-specific insights
            with_coords = sum(1 for p in entities if 'defined_by' in p)
            with_parent = sum(1 for p in entities if 'part_of' in p)
            
            print(f"Places with coordinates: {with_coords} ({with_coords/len(entities)*100:.1f}%)")
            print(f"Places with parent location: {with_parent} ({with_parent/len(entities)*100:.1f}%)")
            
            # Classification analysis
            place_types = {}
            for p in entities:
                for classification in p.get('classified_as', []):
                    place_type = classification.get('_label', 'Unknown')
                    place_types[place_type] = place_types.get(place_type, 0) + 1
            
            print(f"\nPlace Types Distribution:")
            for ptype, count in sorted(place_types.items(), key=lambda x: x[1], reverse=True):
                print(f"  {ptype}: {count}")
        
        print(f"\n{'='*60}\n")


if __name__ == "__main__":

    root_dir = Path(__file__).resolve().parents[2]
    validator = LinkedArtValidator()
    
    # Validate events
    validator.validate_file(
        str(root_dir) + "/pipeline/linked-art/output/shipwreck_events.json",
        entity_type='event'
    )
    
    # Validate places
    validator.validate_file(
        str(root_dir) + "/pipeline/linked-art/output/shipwreck_places.json",
        entity_type='place'
    )
