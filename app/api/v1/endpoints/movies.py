
import os
from dotenv import load_dotenv

from scraping.client import fetch_page
from scraping.parsers import soup, extract_movies
from scraping.normalizer import normalize_data_movies

from fastapi import APIRouter
from fastapi.responses import JSONResponse


load_dotenv()
movies_router = APIRouter(prefix="/movies", tags=["movies"])

@movies_router.get("/")
def get_movies():
    movie_data = fetch_page(f"{os.getenv('URL')}/listaFilmes")
    if not movie_data:
        # return {"error": "Failed to fetch movie data"}, 500
        return JSONResponse(
            content={"error": "Failed to fetch movie data"},
            status_code=500
        )

    movies = extract_movies(soup(movie_data))
    normalized_movies = normalize_data_movies(movies)
    # return normalized_movies, 200
    return JSONResponse(
        content=normalized_movies,
        status_code=200
    )
