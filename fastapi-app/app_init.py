import os
import tempfile
from fastapi import APIRouter, HTTPException, Header, Depends, UploadFile, File
from typesense_client import client, init_schema, import_sample_data
from models import CollectionSchema
import typesense
import logging
# Load environment variables from .env file
logger = logging.getLogger(__name__)
router = APIRouter()

SECRET_TOKEN = os.getenv("TOKEN")

def verify_token(token: str = Header(..., alias="X-Token")):
    if SECRET_TOKEN is None or token != SECRET_TOKEN:
        logger.warning("Unauthorized access attempt with token: %s", token)
        raise HTTPException(status_code=401, detail="Invalid or missing token")

@router.post("/init")
def initialize_typesense(token: str = Depends(verify_token)):
    try:
        init_schema()
        import_sample_data()
        return {"message": "Typesense schema initialized and sample data imported."}
    except Exception as e:
        logger.error(f"Error initializing Typesense: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-collection")
async def create_collection(
    schema: CollectionSchema,
    token: str = Depends(verify_token)
):
    try:
        logger.info(f"Attempting to create collection: {schema.name}")
        schema_dict = schema.dict(exclude_none=True)
        response = client.collections.create(schema_dict)
        return {"status": "success", "data": response}
    except typesense.exceptions.ObjectAlreadyExists:
        raise HTTPException(status_code=409, detail=f"Collection '{schema.name}' already exists")
    except typesense.exceptions.RequestMalformed as e:
        raise HTTPException(status_code=400, detail=f"Invalid schema: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating collection: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/import-jsonl")
async def import_jsonl(
    collection_name: str,
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):
    try:
        logger.info(f"Received file for collection '{collection_name}': {file.filename}")

        # Ensure tmp directory exists
        os.makedirs("tmp", exist_ok=True)

        # Save the uploaded file to a temporary directory
        with tempfile.NamedTemporaryFile(delete=False, dir="tmp", suffix=".jsonl") as tmp_file:
            tmp_file.write(await file.read())
            tmp_file_path = tmp_file.name

        # Check if collection exists
        try:
            client.collections[collection_name].retrieve()
        except Exception:
            os.remove(tmp_file_path)
            raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' does not exist")

        # Import documents from the saved file
        import_sample_data(filepath=tmp_file_path, collection_name=collection_name)

        os.remove(tmp_file_path)
        logger.info(f"Successfully imported documents to collection '{collection_name}'")

        return {"status": "success", "result": "Done"}
    except Exception as e:
        logger.error(f"Error importing JSONL to collection '{collection_name}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to import JSONL data")