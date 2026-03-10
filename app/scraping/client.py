# client.py
# Responsável por: comunicação com o site externo.

import requests
from requests.exceptions import RequestException, Timeout


def debug(content):
    with open("debug.html", "wb") as f:
        f.write(content)

def fetch_page(url, method="GET", data=None):
    headers = {
        "accept-language": "pt-BR,pt;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    try:
        if method == "GET":
            res = requests.get(url, headers=headers)
        elif method == "POST":
            res = requests.post(url, json=data, headers=headers)
        res.raise_for_status()
        return res.content
    except (RequestException, Timeout) as e:
        print(f"Erro de conexão: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
