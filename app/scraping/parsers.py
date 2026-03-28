# parsers.py
# Responsável por: extrair dados do HTML bruto.

from bs4 import BeautifulSoup


def debug(content):
    with open("debug.html", "wb") as f:
        f.write(content)

def soup(raw_html: str):
    return BeautifulSoup(raw_html, "html.parser")

def format_link(link):
    """ Corrige links que começam com "//" para "https:// """
    if link.startswith("//"):
        return "https:" + link
    return link

def extract_section(data, selector):
    """ Extrai os dados de uma seção específica usando o seletor CSS fornecido. Retorna uma lista de itens extraídos."""
    items = []

    for card in data.select(selector):
        item = extract_card(card)

        if item:
            items.append(item)

    return items

def extract_card(card):
    """ Extrai os dados de um card específico, como título, gênero, qualidade, ano, avaliação, link e imagem."""
    try:
        return {
            "title": card.find("h3", class_="card__title").text.strip(),
            "genre": card.find("span", class_="span-category").text.strip() if card.find("span", class_="span-category") else None,
            "quality": card.find("span", class_="tag-hd").text.strip() if card.find("span", class_="tag-hd") else None,
            "year": card.find("span", attrs={"class": "span-year"}).text.strip() if card.find("span", attrs={"class": "span-year"}) else None,
            "rating": card.find("span", class_="card__rate").text.strip() if card.find("span", class_="card__rate") else None,
            # "/filme/peaky-blinders-o-homem-imortal" quero apenas "peaky-blinders-o-homem-imortal"
            "id": card.find("a")["href"].split("/")[-1],
            "image": (
                card.find("img").get("data-src") or
                card.find("img").get("src")
            )
        }
    except:
        return None

def extract_index(soup_data):
    """ Extrai os dados de todas as seções da página inicial usando os seletores CSS definidos. Retorna um dicionário com as seções e seus respectivos itens extraídos."""
    sections = {
        "destaque": ".home__carousel .card",
        "assistidos": "#owl_assistidos .card",
        "adicionados": "#owl_ultimos .card",
        "lancamentos": "#lancamentos_recentes .card",
        "series": "#owl_series .card"
    }

    result = {}

    for name, selector in sections.items():
        result[name] = extract_section(soup_data, selector)

    return result


# ################################ #
#          Dados dos Filmes        #
# ################################ #
def extract_movies(soup_data):
    """ Extrai os dados de todos os filmes da página usando o seletor CSS definido. Retorna uma lista de filmes extraídos."""
    result = []
    cards = soup_data.select(".card")
    for card in cards:
        result.append({
            "title": card.find("h3", class_="card__title").text.strip(),
            "genre": card.find("span", class_="card__category").text.split(",")[0].strip(),
            "quality": card.find("div", class_="tags-top").text.strip() if card.find("div", class_="tags-top") else None,
            "year": card.find("span", class_="card__category").text.strip().split(",")[1].strip(),
            "rating": card.find("span", class_="card__rate").text.strip() if card.find("span", class_="card__rate") else None,
            "id": card.find("a")["href"].split("/")[-1],
            "image": (
                card.find("img").get("data-src") or
                card.find("img").get("src")
            )
        })
    return result

def extract_details_movie(soup_data):
    """ Extrai os detalhes de um filme específico da página usando os seletores CSS definidos. Retorna um dicionário com os detalhes extraídos, incluindo título, avaliação, imagem, gênero, ano, duração, sinopse e vídeos relacionados."""
    try:
        title = soup_data.find("h1", attrs={"class": "section__title"})
        rating = soup_data.find("span", attrs={"class": "card__rate"})
        image = soup_data.select(".card--details picture")[0].find("img")
        details = soup_data.select(".card__content .card__meta")
        meta_items = soup_data.select(".card__meta li")
        sinopse = soup_data.select(".card__description")
        videos = soup_data.select(".iframe-container iframe")

        genre = None
        year = None
        duration = None

        for item in meta_items:
            text = item.get_text(strip=True)

            if "Gênero" in text:
                genre_tag = item.find("a")
                if genre_tag:
                    genre = genre_tag.text.strip()

            elif "Ano de lançamento" in text:
                year = text.split(":")[-1].strip()

            elif "Duração" in text:
                duration = text.split(":")[-1].strip()

        return {
            "title": title.text.strip() if title else None,
            "rating": rating.text.strip() if rating else None,
            "image": image.get("data-src"),
            "genre": genre,
            "year": year,
            "duration": duration,
            "sinopse": sinopse[0].text.strip(),
            "videos": [format_link(video["src"]) for video in videos]
        }

    except Exception as e:
        print(e)
        return None

def get_link_movie(soup_data):
    """ Extrai o link do vídeo de um filme específico da página usando o seletor CSS definido. Retorna o link do vídeo extraído ou None em caso de erro."""
    try:
        video = soup_data.select("video source[src][size]")[0]["src"]
        return format_link(video)
    except Exception as e:
        print(e)
        return None

# ################################ #
#          Dados dos Series        #
# ################################ #
def extract_series(soup_data):
    """ Extrai os dados de todas as séries da página usando o seletor CSS definido. Retorna uma lista de séries extraídas."""
    result = []
    cards = soup_data.select(".catalog .container .card")
    for card in cards:
        ano = card.find("span", class_="card__category").find_all("a")
        year = ano[1].text.strip() if len(ano) > 1 else ano[0].text.strip()

        result.append({
            "title": card.find("h3", class_="card__title").text.strip(),
            "genre": card.find("span", class_="card__category").find_all("a")[0].text.strip(),
            "year": year,
            "rating": card.find("span", class_="card__rate").text.strip() if card.find("span", class_="card__rate") else None,
            "id": card.find("a")["href"].split("/")[-1],
            "image": (
                card.find("img").get("data-src") or
                card.find("img").get("src")
            )
        })
    return result

def extract_details_series(soup_data):
    """ Extrai os detalhes de uma série específica da página usando os seletores CSS definidos. Retorna um dicionário com os detalhes extraídos, incluindo título, imagem, gênero, ano, temporada, sinopse e temporadas relacionadas."""
    try:
        image = soup_data.select(".card--details picture")[0].find("img")
        title = soup_data.find("h1", attrs={"class": "section__title"})
        sinopse = soup_data.select(".card__description")
        details = soup_data.select(".card__content .card__meta")
        meta_items = soup_data.select(".card__meta li")

        # genero, ano, temporada
        genre = None
        year = None
        season = None
        seasons = []

        for item in meta_items:
            text = item.get_text(strip=True)

            if "Gênero" in text:
                genre_tag = item.find("a")
                if genre_tag:
                    genre = genre_tag.text.strip()

            elif "Ano de lançamento" in text:
                year = text.split(":")[-1].strip()
            
            elif "Temp" in text:
                season = int(text.split(".")[-1].split(" ")[1].strip())
        
        if season > 1:
            for i in range(1, season + 1):
                temporadas = soup_data.find("div", attrs={"id": f"temporada-{i}"})
                seasons.append({
                    "season": temporadas.find("a")["href"][len("/serie/"):], 
                    "image": temporadas.find("img").get("data-src"),
                    "id": temporadas.find("h3", attrs={"class": "card__title"}).text.strip()
                })
        
        else:
            temporadas = soup_data.find("div", attrs={"id": f"temporada-1"})
            seasons.append({
                "season": temporadas.find("a")["href"][len("/serie/"):],
                "image": temporadas.find("img").get("data-src"),
                "title": temporadas.find("h3", attrs={"class": "card__title"}).text.strip()
            })

        return {
            "title": title.text.strip() if title else None,
            "image": image.get("data-src"),
            "genre": genre,
            "year": year,
            "season": season,
            "seasons": seasons,
            "sinopse": sinopse[0].text.strip()
        }

    except Exception as e:
        print(e)
        return None

def extract_details_season(soup_data):
    """ Extrai os detalhes de uma temporada específica da página usando os seletores CSS definidos. Retorna um dicionário com os detalhes extraídos, incluindo título, imagem, gênero, ano, temporada, sinopse e episódios relacionados."""
    try:
        image = soup_data.select(".card--details img")
        rating = soup_data.find("span", attrs={"class": "card__rate"})
        title = soup_data.find("h1", attrs={"class": "section__title"})
        sinopse = soup_data.select(".card__description")
        meta_items = soup_data.select(".card__meta li")

        # genero, status, episodes
        genre = None
        status = None
        episode = None
        episodes = []

        for item in meta_items:
            text = item.get_text(strip=True)

            if "Gênero" in text:
                genre_tag = item.find("a")
                if genre_tag:
                    genre = genre_tag.text.strip()

            elif "Status" in text:
                status = text.split(":")[-1].strip()
        
        episode_cards = soup_data.select("#listaEp .accordion__list tbody tr")
        for card in episode_cards:
            video = card["onclick"][len("reloadVideoSerie("): -len(")")]
            episode_number = card.find_all("th")[0].text.strip()
            episode_title = card.find_all("th")[-1].text.strip()

            # "reloadVideoSerie('QW1aNUF0PT0=', '12e211bf40eae5c222316f22a8d2ce2d')"
            token = video.split(",")[1].strip().strip("'").strip('"')
            id_video = video.split(",")[0].strip().strip("'").strip('"')

            episodes.append({
                "title": episode_title,
                "ep": int(episode_number),
                "link": f"https://assistir.biz/playserie/{id_video}/{token}"
            })
        
        return {
            "title": title.text.strip() if title else None,
            "image": image[0]["data-src"],
            "genre": genre,
            "episode": len(episode_cards),
            "episodes": episodes,
            "sinopse": sinopse[0].text.strip()
        }

    except Exception as e:
        print(e)
        return None

# ################################ #
#         Dados de Pesquisa        #
# ################################ #
def extract_search(soup_data):
    """ Extrai os dados de pesquisa da página usando o seletor CSS definido. Retorna uma lista de itens de pesquisa extraídos."""
    result = []
    cards = soup_data.select(".card")
    for card in cards:
        result.append({
            "title": card.find("h3", class_="card__title").text.strip(),
            "genre": card.find("span", class_="card__category").text.split(",")[0].strip(),
            "year": card.find("span", class_="card__category").text.strip().split(",")[-1].strip(),
            "id": card.find("a")["href"].split("/")[-1],
            "image": (
                card.find("img").get("data-src") or
                card.find("img").get("src")
            )
        })
    return result
