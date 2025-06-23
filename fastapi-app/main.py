from fastapi import FastAPI
from app_init import router as init_router
from search import router as search_router

app = FastAPI()
app.include_router(init_router)
app.include_router(search_router)