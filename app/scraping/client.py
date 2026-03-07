# client.py
# Responsável por: comunicação com o site externo.

import os
import requests
from requests.exceptions import RequestException, Timeout
from dotenv import load_dotenv



load_dotenv()

def debug(content):
    # 'content' agora é uma string, não precisa de .text aqui
    with open("index.html", "wb") as file:
        file.write(content)

def fetch_page(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.content
    except (RequestException, Timeout) as e:
        print(f"Erro de conexão: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

