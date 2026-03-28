
import os
from dotenv import load_dotenv

from scraping.client import fetch_page
from scraping.parsers import soup, extract_index
from scraping.normalizer import normalize_data_index

from fastapi import APIRouter
from fastapi.responses import JSONResponse


load_dotenv()
index_router = APIRouter(tags=["index"])

@index_router.get("/", summary="Obter Índice Principal")
def get_index():
    index_data = fetch_page(f"{os.getenv('URL')}")
    if not index_data:
        # return {"error": "Failed to fetch index data"}, 500
        return JSONResponse(
            content={"error": "Failed to fetch index data"},
            status_code=500
        )

    index = extract_index(soup(index_data))
    normalized_index = normalize_data_index(index)
    # return normalized_index, 200
    return JSONResponse(
        content=normalized_index,
        status_code=200
    )
