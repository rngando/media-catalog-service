# app/api/v1/endpoints/movies.py
# Responsável por: definir as rotas relacionadas a filmes.

import os
from dotenv import load_dotenv

from scraping.client import fetch_page
from scraping.normalizer import normalize_data_movies
from scraping.parsers import soup, extract_movies, extract_details_movie, get_link_movie

from fastapi import Path
from fastapi import APIRouter
from fastapi.responses import JSONResponse


load_dotenv()
movies_router = APIRouter(prefix="/movies", tags=["Filmes"])

@movies_router.get("/", summary="Listar Filmes")
def get_movies():
    """
        Lista todos os filmes disponíveis na página de listagem.

        Realiza o scraping da rota principal de filmes, extrai as informações 
        dos cards e normaliza os dados (converte ratings, limpa títulos, etc).

        Returns:
            JSONResponse: Uma lista de objetos de filmes formatados ou 
            um erro 500 caso a conexão com a fonte falhe.
    """
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

@movies_router.get("/{movies_id}", summary="Obter Detalhes do Filme")
def get_movies_by_id(movies_id: str):
    """
        Obtém os detalhes completos de um filme específico.

        Busca informações detalhadas como sinopse, duração e ano de lançamento 
        usando o ID (path) fornecido.

        Args:
            movies_id (str): O slug ou caminho do vídeo (ex: 'filme/panico-7').

        Returns:
            JSONResponse: Objeto com os detalhes do filme ou erro 404/500.
    """
    url = f"{os.getenv('URL')}/filme/{movies_id}" 
    movie_data = fetch_page(url)
    
    if not movie_data:
        return JSONResponse(content={"error": "Not found"}, status_code=404)

    movie = extract_details_movie(soup(movie_data))
    return JSONResponse(content=normalize_data_movies(movie), status_code=200)

@movies_router.get("/{movies_id:path}/video", summary="Obter Link do Vídeo")
def get_movie_video_link(movies_id: str = Path(...)):
    """
        Obtém o link direto do vídeo de um filme específico. 
    """
    url = f"{os.getenv('URL')}/filme/{movies_id.split('/')[0]}"
    page_html = fetch_page(url)

    if not page_html:
        return JSONResponse(content={"error": "Filme not found"}, status_code=404)
    
    movie_data = extract_details_movie(soup(page_html))
    
    iframe_url = movie_data.get("videos", [None])[0]
    
    if not iframe_url:
        return JSONResponse(content={"error": "Player not found"}, status_code=404)
    
    iframe_html = fetch_page(iframe_url)
    if not iframe_html:
        return JSONResponse(content={"error": "Failed to access the player"}, status_code=500)
    
    final_video_link = get_link_movie(soup(iframe_html))

    if not final_video_link:
        return JSONResponse(content={"error": "Video link not found in player"}, status_code=404)
    
    movie_data.pop("videos", None)
    movie_data["video_link"] = final_video_link
    movie_data["video_type"] = "hls" if ".m3u8" in final_video_link else "mp4"
    
    return JSONResponse(content=movie_data, status_code=200)
