from bs4 import BeautifulSoup
import requests
import time
import re
from tech_news.database import create_news

HEADER = {"user-agent": "Fake user-agent"}


def fetch(url: str) -> str | None:
    time.sleep(1)

    try:
        response = requests.get(url, headers=HEADER, timeout=2)
        if response.status_code == 200:
            return response.text

    except requests.ReadTimeout:
        return None


def scrape_updates(html_content: str) -> list[str]:
    soup = BeautifulSoup(html_content, "html.parser")

    links = []
    for post in soup.find_all("a", {"class": "cs-overlay-link"}):
        links.append(post["href"])
    return links


def scrape_next_page_link(html_content: str) -> str | None:
    soup = BeautifulSoup(html_content, "html.parser")

    next_link = soup.find("a", {"class": "next"})

    if next_link:
        return next_link["href"]
    else:
        return None


def extract_digit_from_string(string: str) -> int:
    digits = re.findall(r"\d", string)
    result = int("".join(digits))
    return result


def clean_text(text: str) -> str:
    cleaned_text = text.replace("\xa0", "")
    if cleaned_text[-1] == " ":
        cleaned_text = cleaned_text[:-1]
    return cleaned_text


def scrape_news(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, "html.parser")

    url = soup.find("link", {"rel": "canonical"})["href"]
    title = clean_text(soup.find("h1", {"class": "entry-title"}).text)
    timestamp = soup.find("li", {"class": "meta-date"}).text
    writer = soup.find("span", {"class": "author"}).a.text
    reading_time = extract_digit_from_string(
        soup.find("li", {"class": "meta-reading-time"}).text
    )
    summary = clean_text(soup.find("div", {"class": "entry-content"}).p.text)
    category_tag = soup.find("a", {"class": "category-style"})
    category = category_tag.find("span", {"class": "label"}).text

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }


def get_tech_news(amount: int) -> list[dict]:
    html = fetch("https://blog.betrybe.com/")

    news = []

    news_links = scrape_updates(html)

    while amount > len(news_links):
        html = fetch(scrape_next_page_link(html))
        news_links.extend(scrape_updates(html))

    for i in range(amount):
        news.append(scrape_news(fetch(news_links[i])))

    create_news(news)

    return news
