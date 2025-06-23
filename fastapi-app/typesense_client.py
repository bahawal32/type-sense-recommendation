import typesense
import os
import logging
logger = logging.getLogger(__name__)

TYPESENSE_HOST = os.getenv("TYPESENSE_HOST", "localhost")
TYPESENSE_PORT = os.getenv("TYPESENSE_PORT", "8108")
TYPESENSE_API_KEY = os.getenv("TYPESENSE_API_KEY")

client = typesense.Client({
    "nodes": [{
        "host": TYPESENSE_HOST,
        "port": TYPESENSE_PORT,
        "protocol": "http"
    }],
    "api_key": TYPESENSE_API_KEY,
    "connection_timeout_seconds": 500,

})

def init_schema():
    logger.info("Initializing Typesense schema...")
    news_article_schema = {
        "name": "news_articles",
        "fields": [
            { "name": "link", "type": "string" },
            { "name": "headline", "type": "string" },
            { "name": "category", "type": "string", "facet": True },
            { "name": "short_description", "type": "string" },
            { "name": "authors", "type": "string", "facet": True },
            { "name": "date", "type": "string", "facet": True }
        ]
        }

    logger.info("Creating collection 'news_articles'...")
    client.collections.create(news_article_schema)
  
        

def import_sample_data():
    logger.info("Importing sample data into Typesense...")
    with open('News_Category_Dataset_v3.jsonl') as jsonl_file:
        client.collections['news_articles'].documents.import_(jsonl_file.read().encode('utf-8'))
