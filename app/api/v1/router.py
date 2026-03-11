# app/api/v1/router.py
# Responsável por: configurar as rotas da API.

from fastapi import APIRouter
from .endpoints import index_router, movies_router, series_router


router = APIRouter()
router.include_router(index_router, prefix="/api/v1")
router.include_router(movies_router, prefix="/api/v1")
router.include_router(series_router, prefix="/api/v1")
