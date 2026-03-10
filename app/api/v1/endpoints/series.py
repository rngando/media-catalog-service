
import os
from dotenv import load_dotenv

from scraping.client import fetch_page
from scraping.parsers import soup, extract_series
from scraping.normalizer import normalize_data_series

from fastapi import APIRouter
from fastapi.responses import JSONResponse


load_dotenv()
series_router = APIRouter(prefix="/series", tags=["series"])

@series_router.get("/")
def get_series():
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
