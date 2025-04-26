import json
from supabase_storage import insert_property, save_metadata

def import_json_file(filepath):
    """Import data from an existing JSON file into Supabase"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        metadata = data.get('metadata', {})
        properties = data.get('properties', [])
        
        print(f"Found {len(properties)} properties in file")
        
        successful_imports = 0
        for property_data in properties:
            if insert_property(property_data):
                successful_imports += 1
        
        # Update metadata and save
        updated_metadata = {
            'total_properties': metadata.get('total_properties', len(properties)),
            'successful_scrapes': metadata.get('successful_scrapes', len(properties)),
            'successful_db_inserts': successful_imports,
            'scraped_at': metadata.get('scraped_at'),
            'imported_at': datetime.now().isoformat()
        }
        
        save_metadata(updated_metadata)
        
        print(f"Import complete: {successful_imports}/{len(properties)} properties imported")
        
    except Exception as e:
        print(f"Error importing data: {str(e)}")

if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        import_json_file(filepath)
    else:
        print("Please provide the path to the JSON file as an argument")
        print("Example: python import_existing_data.py housing_scraped_results_noida_20250425_143928.json")