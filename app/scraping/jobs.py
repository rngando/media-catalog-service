# Responsável por: orquestrar o processo completo de scraping.

import os, json
from dotenv import load_dotenv

from client import fetch_page
from parsers import soup, extract_index, extract_movies, extract_series
from normalizer import normalize_data_index, normalize_data_movies, normalize_data_series



load_dotenv()

def start():
    url = f"{os.getenv('URL')}listaFilmes"

    # 1. Coleta (client)
    raw_html = fetch_page(url)
    if not raw_html:
        return print("Falha na coleta HTML Bruta")
    
    # 2. Extração (parser)
    parser_data = soup(raw_html)
    raw_list = extract_movies(parser_data)

    # 3. Normalização (normalize)
    # final_data = normalize_data_index(raw_list)
    final_data = normalize_data_movies(raw_list)
    
    # Debug do resultado final
    # for category, movies in final_data.items():
    #     print(f"\n--- {category.upper()} ---")
    #     for item in movies:
    #         print(f"⭐ {item['rating']} | 📅 {item['year']} | 🎬 {item['title']} | {item['link']}")
    
    return json.dumps(final_data, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    result = start()
    print(result)
