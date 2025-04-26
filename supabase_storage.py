import os
import json
from typing import Dict, List, Any, Optional, Union
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Supabase setup
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in .env file")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_property(property_data: Dict[str, Any]) -> bool:
    """
    Insert a property record and all its related data into Supabase
    Returns True if successful, False otherwise
    """
    try:
        property_id = property_data.get('id')
        url = property_data.get('url')
        images = property_data.get('images', [])
        scraped_data_list = property_data.get('scraped_data', [])
        
        if not property_id or not url:
            print(f"Invalid property data, missing ID or URL")
            return False

        # Get the first scraped data item (if any)
        scraped_data = scraped_data_list[0] if scraped_data_list else {}
        
        # 1. Insert main property record
        property_record = {
            "id": property_id,
            "url": url,
            "scraped_at": datetime.now().isoformat()
        }
        
        # Add basic property info from scraped data
        if scraped_data:
            property_record.update({
                "project_name": scraped_data.get('project_name', ''),
                "developer_name": scraped_data.get('developer_name', ''),
                "location": scraped_data.get('location', ''),
                "price_range": scraped_data.get('price_range', ''),
                "price_per_sqft": scraped_data.get('price_per_sqft', ''),
                "configurations": scraped_data.get('configurations', ''),
                "possession_date": scraped_data.get('possession_date', ''),
                "area_range": scraped_data.get('area_range', ''),
                "project_area": scraped_data.get('project_area', ''),
                "sizes": scraped_data.get('sizes', ''),
                "project_size": scraped_data.get('project_size', ''),
                "launch_date": scraped_data.get('launch_date', ''),
                "average_price": scraped_data.get('average_price', ''),
                "rera_id": scraped_data.get('rera_id', ''),
                "project_description": scraped_data.get('project_description', '')
            })
        
        # Store the property
        response = supabase.table('properties').upsert(property_record).execute()
        
        if hasattr(response, 'error') and response.error:
            print(f"Error inserting property {property_id}: {response.error}")
            return False
            
        # 2. Insert property images
        for index, image_url in enumerate(images):
            image_record = {
                "property_id": property_id,
                "image_url": image_url,
                "image_order": index
            }
            supabase.table('property_images').upsert(image_record).execute()
        
        # 3. Insert amenities if available
        amenities = scraped_data.get('amenities', [])
        for amenity in amenities:
            if 'name' in amenity:
                amenity_record = {
                    "property_id": property_id,
                    "name": amenity['name']
                }
                supabase.table('property_amenities').upsert(amenity_record).execute()
        
        # 4. Insert specifications if available
        specifications = scraped_data.get('specifications', [])
        for spec in specifications:
            if 'key' in spec and 'value' in spec:
                spec_record = {
                    "property_id": property_id,
                    "key": spec['key'],
                    "value": spec['value']
                }
                supabase.table('property_specifications').upsert(spec_record).execute()
        
        # 5. Insert project highlights if available
        highlights = scraped_data.get('project_highlights', [])
        for highlight in highlights:
            if 'key' in highlight:
                highlight_record = {
                    "property_id": property_id,
                    "description": highlight['key']
                }
                supabase.table('property_highlights').upsert(highlight_record).execute()
        
        # 6. Insert around the project info if available
        around_project = scraped_data.get('around_the_project', [])
        for item in around_project:
            if 'key' in item:
                around_record = {
                    "property_id": property_id,
                    "description": item['key']
                }
                supabase.table('property_around').upsert(around_record).execute()

        # Store raw JSON as well in case we missed anything
        raw_data_record = {
            "property_id": property_id,
            "raw_json": json.dumps(scraped_data)
        }
        supabase.table('property_raw_data').upsert(raw_data_record).execute()
            
        print(f"Successfully stored property ID: {property_id}")
        return True
            
    except Exception as e:
        print(f"Error storing property data in Supabase: {str(e)}")
        return False

def save_metadata(metadata: Dict[str, Any]) -> bool:
    """
    Save scraping metadata to Supabase
    """
    try:
        response = supabase.table('scrape_metadata').insert(metadata).execute()
        if hasattr(response, 'error') and response.error:
            print(f"Error saving metadata: {response.error}")
            return False
        return True
    except Exception as e:
        print(f"Error saving metadata: {str(e)}")
        return False