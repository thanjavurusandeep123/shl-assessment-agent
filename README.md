# SHL Conversational Assessment Recommender

## Setup

### Install dependencies
pip install -r requirements.txt

### Scrape catalog
python catalog_scraper.py

### Build FAISS index
python build_index.py

### Run app
uvicorn app:app --reload
