import typesense
import os

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
    schema = {
        "name": "user_likes",
        "fields": [
            {"name": "user_id", "type": "string"},
            {"name": "item_id", "type": "string"},
            {"name": "score", "type": "float"}
        ],
        "default_sorting_field": "score"
    }

    try:
        client.collections.create(schema)
    except Exception:
        pass  # Collection might already exist

def import_sample_data():
    import json

    with open("sample-data.json") as f:
        records = json.load(f)

    client.collections['user_likes'].documents.import_(records, {'action': 'upsert'})
