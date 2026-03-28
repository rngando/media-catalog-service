
import os
from dotenv import load_dotenv

from scraping.client import fetch_page
from scraping.parsers import soup, extract_search
from scraping.normalizer import normalize_data_movies

from fastapi import APIRouter
from fastapi.responses import JSONResponse


load_dotenv()
search_router = APIRouter(prefix="/search", tags=["Busca"])

@search_router.get("/", summary="Buscar Filmes/Séries", response_description="Resultados de busca normalizados")
def search(query: str):
    """
        Realiza uma busca por filmes ou séries com base na query fornecida.

        Args:
            query (str): O termo de busca (ex: 'Ana').

        Returns:
            JSONResponse: Uma lista de resultados de busca normalizados ou erro 500.
    """
    url = f"{os.getenv('URL')}/busca?q={query}"
    page_content = fetch_page(url)
    if not page_content:
        return JSONResponse(
            content={"error": "Failed to fetch search results"},
            status_code=500
        )

    busca = extract_search(soup(page_content))
    normalid_data = normalize_data_movies(busca)

    if not normalid_data["collection"]:
        return JSONResponse(
            content={"message": "No results found for the given query."},
            status_code=404
        )
    
    return JSONResponse(
        content=normalid_data,
        status_code=200
    )