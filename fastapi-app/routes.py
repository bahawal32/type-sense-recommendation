from fastapi import APIRouter
from .app_init import router as init_router
from .search import router as search_router

router = APIRouter()
router.include_router(init_router)
router.include_router(search_router)