import re
from tech_news.database import search_news


def search_by_title(title: str) -> list[tuple]:
    pattern = re.compile(r"\b" + re.escape(title) + r"\b", re.IGNORECASE)

    result = []
    for el in search_news({"title": {"$regex": pattern}}):
        result.append((el["title"], el["url"]))

    return result


# Requisito 8
def search_by_date(date):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    raise NotImplementedError
