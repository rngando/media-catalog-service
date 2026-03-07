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

def normalize_movie_data(movie_list):
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
        
    return normalized_dict
