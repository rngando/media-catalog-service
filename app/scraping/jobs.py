# Responsável por: orquestrar o processo completo de scraping.

import os, json
from dotenv import load_dotenv

from client import fetch_page
from parsers import soup, extract_details_movie, get_link_movie



load_dotenv()

def start():
    # 1ª client
    url = f"{os.getenv('URL')}/filme/anaconda-2025"
    page_content = fetch_page(url)
    if not page_content:
        return {"status": "error", "message": "Failed to fetch the page."}
    normalid_data = extract_details_movie(soup(page_content))
    iframes = normalid_data.get("videos", [])
    
    selected_iframe = iframes[0]

    get_link = fetch_page(selected_iframe)
    
    if not get_link:
        return {"status": "error", "message": "Failed to fetch the iframe page."}
    # Apagar o campo "videos" e adicionar o campo "video_link"
    normalid_data.pop("videos", None)
    normalid_data["video_link"] = get_link_movie(soup(get_link))
    
    return json.dumps(normalid_data, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    result = start()
    print(result)
