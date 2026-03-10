
from fastapi import APIRouter
from .endpoints import index_router, movies_router, series_router


router = APIRouter()
router.include_router(index_router)
router.include_router(movies_router)
router.include_router(series_router)
