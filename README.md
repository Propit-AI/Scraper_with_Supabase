# 🏡 Property Scraper & Supabase Uploader

This project provides an automated pipeline for scraping detailed property listings from web sources and storing the data into a Supabase PostgreSQL database. It uses [Crawl4AI](https://github.com/Firecrawl/crawl4ai) for scraping and the official Supabase Python client for data persistence.

---

## 📁 Project Structure


---

## ⚙️ Key Features

- Custom web scraping using CSS selectors via Crawl4AI
- Outputs structured JSON files with metadata
- Automatically uploads property info, images, specifications, and metadata to Supabase
- Supports graceful error handling and detailed logs

---

## 🔧 Setup Instructions

### 1. Clone the Repository


git clone (https://github.com/Propit-AI/Scraper_with_Supabase.git)
cd your-repo-name

# Create virtual environment
python3 -m venv venv

# Activate on Unix/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

python-dotenv
supabase
crawl4ai

Create a .env file in the root directory with your Supabase URL and Key:


SUPABASE_URL=https://your-supabase-project.supabase.co
SUPABASE_KEY=your-service-role-api-key

Step 1: Scrape Property Data
Edit or use script.py to scrape a predefined list of property IDs and URLs:

python script.py
✅ This creates an output JSON like:

housing_scraped_results_mumbai_20250429_153000.json


Use the generated JSON file with import_existing_data.py:
python import_existing_data.py housing_scraped_results_mumbai_20250429_153000.json

📤 Output JSON Format
{
  "metadata": {
    "total_properties": 10,
    "successful_scrapes": 8,
    "scraped_at": "2025-04-29T15:30:00"
  },
  "properties": [
    {
      "id": "project-123",
      "url": "https://...",
      "images": ["https://img1...", "https://img2..."],
      "scraped_data": {
        "project_name": "...",
        "location": "...",
        "amenities": [...],
        ...
      }
    }
  ]
}

🧪 Development Tips
You can test the scraper with just a few URLs by editing the input list in script.py.

Always validate that your .env contains valid Supabase credentials.

You can rerun the import anytime with the generated JSON file.

 Need Help?
Feel free to open an issue or discussion on this repository if you run into any problems.



