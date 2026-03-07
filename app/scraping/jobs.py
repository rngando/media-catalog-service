# Responsável por: orquestrar o processo completo de scraping.

import os
from dotenv import load_dotenv

from client import fetch_page
from parsers import soup, extract_itens
from normalizer import normalize_movie_data



load_dotenv()

def start():
    url = os.getenv('URL')

    # 1. Coleta (client)
    raw_html = fetch_page(url)
    if not raw_html:
        return print("Falha na coleta HTML Bruta")
    
    # 2. Extração (parser)
    parser_data = soup(raw_html)
    raw_list = extract_itens(parser_data)

    # 3. Normalização (normalize)
    final_data = normalize_movie_data(raw_list)
    
    # Debug do resultado final
    for category, movies in final_data.items():
        print(f"\n--- {category.upper()} ---")
        for item in movies:
            print(f"⭐ {item['rating']} | 📅 {item['year']} | 🎬 {item['title']} | {item['link']}")
    
    return final_data


if __name__ == "__main__":
    start()