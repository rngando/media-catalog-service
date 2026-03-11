# noralizer.py
# Responsável por: limpar e padronizar os dados extraídos.

import re


def clean_year(year_str):
    """Extrai apenas os números do ano (ex: '2024' -> 2024)"""
    if not year_str:
        return None
    match = re.search(r"\d{4}", year_str)
    return int(match.group(0)) if match else None

def clean_rating(rating_str):
    """Converte '8.5' (string) para 8.5 (float)"""
    try:
        # Remove espaços e troca vírgula por ponto se necessário
        val = rating_str.replace(",", ".").strip()
        return float(val)
    except (ValueError, AttributeError):
        return 0.0

def normalize_data_index(movie_list):
    """Percorre a lista de filmes e aplica as limpezas"""
    normalized_dict = {}
    for category, movie_list in movie_list.items():
        normalized_dict[category] = []

        for movie in movie_list:
            # Cria uma cópia para não mexer no original
            clean_movie = movie.copy()

            # Aplicar a limpeza
            clean_movie["year"] = clean_year(movie.get("year"))
            clean_movie["rating"] = clean_rating(movie.get("rating"))
            clean_movie["title"] = movie.get("title", "").title()

            # Adiciona o filme limpo na lista da categoria correspondente
            normalized_dict[category].append(clean_movie)
    
    result = {
        "total": sum(len(movies) for movies in normalized_dict.values()),
        "status": "success",
        "collection": normalized_dict
    }
    return result

def normalize_data_movies(movie_list):
    normalized_movies = []
    
    # for movie in movie_list:
    clean_data = movie_list.copy()

    clean_data["year"] = clean_year(movie_list.get("year"))
    clean_data["rating"] = clean_rating(movie_list.get("rating"))
    clean_data["title"] = movie_list.get("title", "").title()
    normalized_movies.append(clean_data)
    
    result = {
        "total": len(normalized_movies),
        "status": "success",
        "collection": normalized_movies
    }
    return result

def normalize_data_series(series_list):
    normalized_series = []

    for serie in series_list:
        clean_data = serie.copy()

        clean_data["year"] = clean_year(serie.get("year"))
        clean_data["rating"] = clean_rating(serie.get("rating"))
        clean_data["title"] = serie.get("title", "").title()
        normalized_series.append(clean_data)
    
    result = {
        "total": len(normalized_series),
        "status": "success",
        "collection": normalized_series
    }
    return result
