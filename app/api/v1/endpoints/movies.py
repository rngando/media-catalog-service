# app/api/v1/endpoints/movies.py
# Responsável por: definir as rotas relacionadas a filmes.

import os
from dotenv import load_dotenv

from scraping.client import fetch_page
from scraping.parsers import soup, extract_movies, extract_details
from scraping.normalizer import normalize_data_movies

from fastapi import Path
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

@movies_router.get("/{movies_id:path}")
def get_movies_by_id(movies_id: str = Path(...)):
    movie_data = fetch_page(f"{os.getenv('URL')}/{movies_id}")
    if not movie_data:
        return JSONResponse(
            content={"error": f"Movie with ID {movies_id} not found"}
        )
    
    movie = extract_details(soup(movie_data))
    normalized_movie = normalize_data_movies(movie)
    return JSONResponse(
        content=normalized_movie,
        status_code=200
    )
