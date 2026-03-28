
import os
from dotenv import load_dotenv

from scraping.client import fetch_page
from scraping.normalizer import normalize_data_series
from scraping.parsers import soup, extract_series, extract_details_series, extract_details_season

from fastapi import Path
from fastapi import APIRouter
from fastapi.responses import JSONResponse


load_dotenv()
series_router = APIRouter(prefix="/series", tags=["series"])

@series_router.get("/", summary="Listar Séries", response_description="Lista de séries normalizada")
def get_series():
    """
        Lista todas as séries disponíveis na página de listagem.
        Realiza o scraping da rota principal de séries, extrai as informações
        dos cards e normaliza os dados (converte ratings, limpa títulos, etc).
        Returns:
            JSONResponse: Uma lista de objetos de séries formatados ou 
            um erro 500 caso a conexão com a fonte falhe.
    """
    series_data = fetch_page(f"{os.getenv('URL')}/series-todas")
    if not series_data:
        # return {"error": "Failed to fetch series data"}, 500
        return JSONResponse(
            content={"error": "Failed to fetch series data"},
            status_code=500
        )

    series = extract_series(soup(series_data))
    normalized_series = normalize_data_series(series)
    # return normalized_series, 200
    return JSONResponse(
        content=normalized_series,
        status_code=200
    )

@series_router.get("/{series_id}", summary="Obter Detalhes da Série", response_description="Detalhes da série normalizados")
def get_series_by_id(series_id):
    """
        Obtém os detalhes completos de uma série específica.

        Busca informações detalhadas como sinopse, duração e ano de lançamento 
        usando o ID (path) fornecido.

        Args:
            series_id (str): O slug ou caminho da série (ex: 'serie/stranger-things').

        Returns:
            JSONResponse: Objeto com os detalhes da série ou erro 404/500.
    """
    url = f"{os.getenv('URL')}/serie/{series_id}"
    serie_data = fetch_page(url)
    if not serie_data:
        return JSONResponse(
            content={"error": f"Series with ID {series_id} not found"},
            status_code=404
        )
    
    serie = extract_details_series(soup(serie_data))
    normalized_serie = normalize_data_series(serie)
    return JSONResponse(
        content=normalized_serie,
        status_code=200
    )

@series_router.get("/{season_id}/{season_number}", summary="Obter Detalhes Específicos da Série")
def get_series_details(season_id, season_number):
    """
        Obtém detalhes específicos de uma série, como sinopse, duração e ano de lançamento.

        Args:
            series_id (str): O slug ou caminho da série (ex: 'serie/stranger-things').

        Returns:
            JSONResponse: Objeto com os detalhes específicos da série ou erro 404/500.
    """
    url = f"{os.getenv('URL')}/serie/{season_id}/temporada-{season_number}"
    serie_data = fetch_page(url)
    if not serie_data:
        return JSONResponse(
            content={"error": f"Series with ID {season_id} not found"},
            status_code=404
        )
    
    details = extract_details_season(soup(serie_data))
    normalized_details = normalize_data_series(details)
    return JSONResponse(
        content=normalized_details,
        status_code=200
    )
