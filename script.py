import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import time
from datetime import datetime

async def extract_property_data(url, property_id):
    """Extracts detailed information about a property from its URL"""
    schema = JsonCssExtractionStrategy({
        "name": "Full Project Info with Image",
        "baseSelector": "body",
        "fields": [
            {
                "name": "project_name",
                "selector": "h1.css-1hidc9c",
                "type": "text"
            },
            {
                "name": "developer_name",
                "selector": "div.css-gdymlq a",
                "type": "text"
            },
            {
                "name": "location",
                "selector": "div[data-q='address']",
                "type": "text"
            },
            {
                "name": "price_range",
                "selector": "span.css-19rl1ms",
                "type": "text"
            },
            {
                "name": "price_per_sqft",
                "selector": "span.css-124qey8",
                "type": "text"
            },
            {
                "name": "configurations",
                "selector": "div.css-c2zxhw:nth-of-type(1) > div.css-1k19e3",
                "type": "text"
            },
            {
                "name": "possession_date",
                "selector": "div.css-c2zxhw:nth-of-type(2) > div.css-1k19e3",
                "type": "text"
            },
            {
                "name": "area_range",
                "selector": "div.css-c2zxhw:nth-of-type(4) div._9s1o8l",
                "type": "text"
            },
            {
                "name": "cover_image",
                "selector": "div[data-content='Cover Image'] img.css-40aejx",
                "type": "attr",
                "attribute": "src"
            },
            {
                "name": "project_area",
                "selector": "td:has(div:contains('Project Area')) div.T_valueStyle",
                "type": "text"
            },
            {
                "name": "sizes",
                "selector": "td:has(div:contains('Sizes')) div.T_valueStyle",
                "type": "text"
            },
            {
                "name": "project_size",
                "selector": "td:has(div:contains('Project Size')) div.T_valueStyle",
                "type": "text"
            },
            {
                "name": "launch_date",
                "selector": "td:has(div:contains('Launch Date')) div.T_valueStyle",
                "type": "text"
            },
            {
                "name": "average_price",
                "selector": "td:has(div:contains('Avg. Price')) div.T_valueStyle",
                "type": "text"
            },
            {
                "name": "possession_date",
                "selector": "td:has(div:contains('Possession Starts')) div.T_valueStyle",
                "type": "text"
            },
            {
                "name": "configurations",
                "selector": "td:has(div:contains('Configurations')) div.T_valueStyle",
                "type": "text"
            },
            {
                "name": "rera_id",
                "selector": "td:has(div:contains('Rera Id')) a",
                "type": "text"
            },
            {
                "name": "amenities",
                "selector": "div.T_iconAmenityStyle div.T_cellStyle:not(:has(div.T_LestMoreStyle))",
                "type": "list",
                "fields": [
                    {
                        "name": "name",
                        "selector": "div.T_amenityLabelStyle",
                        "type": "text"
                    }
                ]
            },
            {
                "name": "specifications",
                "selector": "section._gqexct._mpcp1yer._1wuiglyw",
                "type": "list",
                "fields": [
                    {
                        "name": "key",
                        "selector": "span.T_furnishingLabelKeyStyle",
                        "type": "text"
                    },
                    {
                        "name": "value",
                        "selector": "span.T_furnishingLabelValueStyle",
                        "type": "text"
                    }
                ]
            },
            {
                "name": "project_highlights_title",
                "selector": "section#highlights h2.T_projectTitleStyle",
                "type": "text"
            },
            {
                "name": "project_highlights",
                "selector": "div[class*='T_limitHeightStyle'] div[class*='T_listItemStyle']",
                "type": "list",
                "fields": [
                    {
                        "name": "key",
                        "type": "text"
                    }
                ]
            },
            {
                "name": "around_the_project",
                "selector": "div[class*='T_limitHeightStyle'] div[class*='T_listItemStyle']",
                "type": "list",
                "fields": [
                    {
                        "name": "key",
                        "type": "text"
                    }
                ]
            },
            {
                "name": "project_description",
                "selector": "div[data-q='desc']",
                "type": "text"
            }
        ]
    }, verbose=True)

    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=schema,
    )

    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=url,
            config=config
        )

        if not result.success:
            print(f"Crawl failed for {property_id}: {result.error_message}")
            return None

        try:
            data = json.loads(result.extracted_content)
            return data
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON for {property_id}: {e}")
            return None
async def main():
    try:
        with open('scraped_property_images_noida.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading input file: {e}")
        return

    print(f"Found {len(data)} properties to process")
    
    results = []
    for i, prop in enumerate(data):
        property_id = prop.get('id')
        url = prop.get('url')
        images = prop.get('images', [])

        if not url or not property_id:
            print(f"Skipping invalid entry at index {i}")
            continue

        print(f"Processing {i+1}/{len(data)}: ID={property_id}")
        result = await extract_property_data(url, property_id)

        if result:
            results.append({
                "id": property_id,
                "url": url,
                "images": images,
                "scraped_data": result
            })

        await asyncio.sleep(2)  # polite crawling

    output_file = f'housing_scraped_results_noida_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'total_properties': len(data),
                'successful_scrapes': len(results),
                'scraped_at': datetime.now().isoformat()
            },
            'properties': results
        }, f, indent=2, ensure_ascii=False)

    print(f"Scraping complete. Results saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())