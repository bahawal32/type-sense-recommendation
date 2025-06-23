from fastapi import FastAPI, HTTPException
from typesense_client import client, init_schema, import_sample_data

app = FastAPI()
import logging
logger = logging.getLogger(__name__)

@app.get("/")
def root():
    return {"message": "Typesense Recommendation API"}

@app.post("/init")
def initialize_typesense():
    """Initialize Typesense schema and import sample data."""
    try:
        init_schema()
        import_sample_data()
        return {"message": "Typesense schema initialized and sample data imported."}
    except Exception as e:
        logger.error(f"Error initializing Typesense: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
def search(
    q: str,
    query_by: str,
    sort_by: str = None,
    collection: str = "books"
):
    """Search for documents in a Typesense collection.
    Args:
        q (str): The search query. (harry potter)
        query_by (str): The fields to query by, comma-separated. (title,authors)
        sort_by (str, optional): The field to sort by. Defaults to None. (ratings_count:desc)
        collection (str): The collection to search in. Defaults to "books".
    """
    
    search_parameters = {
        "q": q,
        "query_by": query_by
    }
    
    logger.info(f"Search parameters: {search_parameters}")

    if sort_by:
        search_parameters["sort_by"] = sort_by

    try:
        result = client.collections[collection].documents.search(search_parameters)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
