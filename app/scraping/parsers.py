# parsers.py
# Responsável por: extrair dados do HTML bruto.

from bs4 import BeautifulSoup


def debug(content):
    with open("debug.html", "wb") as f:
        f.write(content)

def soup(raw_html: str):
    return BeautifulSoup(raw_html, "html.parser")

def extract_section(data, selector):
    items = []

    for card in data.select(selector):
        item = extract_card(card)

        if item:
            items.append(item)

    return items

def extract_card(card):
    try:
        return {
            "title": card.find("h3", class_="card__title").text.strip(),
            "genre": card.find("span", class_="span-category").text.strip() if card.find("span", class_="span-category") else None,
            "quality": card.find("span", class_="tag-hd").text.strip() if card.find("span", class_="tag-hd") else None,
            "year": card.find("span", attrs={"class": "span-year"}).text.strip() if card.find("span", attrs={"class": "span-year"}) else None,
            "rating": card.find("span", class_="card__rate").text.strip() if card.find("span", class_="card__rate") else None,
            "link": card.find("a")["href"],
            "image": (
                card.find("img").get("data-src") or
                card.find("img").get("src")
            )
        }
    except:
        return None

def extract_index(soup_data):
    # Playlists (ex: Todo Mundo em Pânico) -> #carousel_playlist1 .card
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

def extract_movies(soup_data):
    result = []
    cards = soup_data.select(".card")
    for card in cards:
        result.append({
            "title": card.find("h3", class_="card__title").text.strip(),
            "genre": card.find("span", class_="card__category").text.split(",")[0].strip(),
            "quality": card.find("div", class_="tags-top").text.strip() if card.find("div", class_="tags-top") else None,
            "year": card.find("span", class_="card__category").text.strip().split(",")[1].strip(),
            "rating": card.find("span", class_="card__rate").text.strip() if card.find("span", class_="card__rate") else None,
            "link": card.find("a")["href"],
            "image": (
                card.find("img").get("data-src") or
                card.find("img").get("src")
            )
        })
    return result

def extract_series(soup_data):
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
            "link": card.find("a")["href"],
            "image": (
                card.find("img").get("data-src") or
                card.find("img").get("src")
            )
        })
    return result

def extract_details(soup_data):
    try:
        title = soup_data.find("h1", attrs={"class": "section__title"})
        rating = soup_data.find("span", attrs={"class": "card__rate"})
        image = soup_data.select(".card--details picture")[0].find("img")
        details = soup_data.select(".card__content .card__meta")
        meta_items = soup_data.select(".card__meta li")
        sinopse = soup_data.select(".card__description")

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
            "sinopse": sinopse[0].text.strip()
        }

    except Exception as e:
        print(e)
        return None
