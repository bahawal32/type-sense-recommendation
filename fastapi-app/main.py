from fastapi import FastAPI, HTTPException
from typesense_client import client, init_schema, import_sample_data

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_schema()
    import_sample_data()

@app.get("/")
def root():
    return {"message": "Typesense Recommendation API"}

@app.get("/recommend/{user_id}/{item_id}")
def recommend(user_id: str, item_id: str, model: str = "item-item"):
    doc_id = f"{user_id}:{item_id}"

    try:
        result = client.collections["user_likes"].documents.recommend(
            document_id=doc_id,
            model=model,
            per_page=5,
            include_fields=["item_id"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
