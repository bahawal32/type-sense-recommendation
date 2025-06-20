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


@app.get("/search")
def search(
    q: str,
    query_by: str,
    sort_by: str = None,
    collection: str = "books"
):
    search_parameters = {
        "q": q,
        "query_by": query_by
    }
    if sort_by:
        search_parameters["sort_by"] = sort_by

    try:
        result = client.collections[collection].documents.search(search_parameters)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
