from fastapi import APIRouter, HTTPException
from typesense_client import client
import logging


logger = logging.getLogger("uvicorn.info")  # or "uvicorn.error"
router = APIRouter()

@router.get("/search")
def search(
    q: str,
    query_by: str,
    sort_by: str = None,
    collection: str = "books"
):
    """
    Search for documents in a Typesense collection.
    """
    search_parameters = {
        "q": q,
        "query_by": query_by,
        "per_page": 20,  # Default to 20 results per page
    }
    if sort_by:
        search_parameters["sort_by"] = sort_by

    logger.info(f"Search parameters: {search_parameters}")

    try:
        result = client.collections[collection].documents.search(search_parameters)
        return result
    except Exception as e:
        logger.error(
            f"Search failed for collection '{collection}' with parameters {search_parameters}: {e}",
            exc_info=True
        )
        raise HTTPException(status_code=404, detail=str(e))