import typesense
import os
import logging
logger = logging.getLogger(__name__)

TYPESENSE_HOST = os.getenv("TYPESENSE_HOST", "typesense")
TYPESENSE_PORT = os.getenv("TYPESENSE_PORT", "8108")
TYPESENSE_API_KEY = os.getenv("TYPESENSE_API_KEY")

client = typesense.Client({
    "nodes": [{
        "host": TYPESENSE_HOST,
        "port": TYPESENSE_PORT,
        "protocol": "http"
    }],
    "api_key": TYPESENSE_API_KEY,
    "connection_timeout_seconds": 2
})

def init_schema():
    logger.info("Initializing Typesense schema...")
    books_schema = {
        'name': 'books',
        'fields': [
            {'name': 'title', 'type': 'string' },
            {'name': 'authors', 'type': 'string[]', 'facet': True },

            {'name': 'publication_year', 'type': 'int32', 'facet': True },
            {'name': 'ratings_count', 'type': 'int32' },
            {'name': 'average_rating', 'type': 'float' }
        ],
        'default_sorting_field': 'ratings_count'
    }

    try:
        logger.info("Creating collection 'books'...")
        client.collections.create(books_schema)
    except Exception:
        logger.warning("Collection 'books' already exists or could not be created.")
        pass
        

def import_sample_data():
    logger.info("Importing sample data into Typesense...")
    with open('books.jsonl') as jsonl_file:
        client.collections['books'].documents.import_(jsonl_file.read().encode('utf-8'))
