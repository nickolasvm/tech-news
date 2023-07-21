from bs4 import BeautifulSoup
import requests
import time

HEADER = {"user-agent": "Fake user-agent"}


def fetch(url: str) -> str:
    time.sleep(1)

    try:
        response = requests.get(url, headers=HEADER, timeout=2)
        if response.status_code == 200:
            print(type(response.text))
            print(type(url))
            return response.text

    except requests.ReadTimeout:
        return None


def scrape_updates(html_content: str) -> list[str]:
    soup = BeautifulSoup(html_content, "html.parser")

    links = []
    for post in soup.find_all("a", {"class": "cs-overlay-link"}):
        links.append(post["href"])
    return links


def test():
    html = fetch("https://blog.betrybe.com/")
    scrape_updates(html)


test()


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
