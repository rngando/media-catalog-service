
from core import URL
from scraping.client import fetch_page
from scraping.parsers import soup, extract_categories
from scraping.normalizer import normalize_data_movies

from fastapi import APIRouter
from fastapi.responses import JSONResponse


categoria_router = APIRouter(prefix="/categoria", tags=["Categoria"])
VALID_CATEGORIES = {'acao', 'animacao', 'aventura', 'comedia', 'crime', 'documentario', 'drama', 'familia', 'fantasia', 'faroeste', 'ficcao-cientifica', 'guerra', 'historia', 'misterio', 'romance', 'terror', 'thriller'}

@categoria_router.post("/{category}", summary="Buscar por categoria")
def categoria(category):
    if category not in VALID_CATEGORIES:
        return JSONResponse(
            content={"error": "Category not found"},
            status_code=404
        )

    url = f"{URL}/categoria/{category}"
    page_contente = fetch_page(url)
    if not page_contente:
        return JSONResponse(
            content={"error": "Failed to fetch external data"},
            status_code=500
        )
    
    categoria = extract_categories(soup(page_contente))
    normalized_data = normalize_data_movies(categoria)

    return JSONResponse(
        content=normalized_data,
        status_code=200
    )
