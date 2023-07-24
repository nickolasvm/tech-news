import re
from datetime import datetime
from tech_news.database import search_news


def search_by_title(title: str) -> list[tuple]:
    pattern = re.compile(r"\b" + re.escape(title) + r"\b", re.IGNORECASE)

    result = []
    for el in search_news({"title": {"$regex": pattern}}):
        result.append((el["title"], el["url"]))

    return result


def convert_date_format(date: str) -> str:
    input_format = "%Y-%m-%d"
    output_format = "%d/%m/%Y"

    parsed_date = datetime.strptime(date, input_format)
    converted_date = parsed_date.strftime(output_format)

    return converted_date


def search_by_date(date: str) -> list[tuple]:
    try:
        datetime.strptime(date, "%Y-%m-%d")

        result = []
        for el in search_news({"timestamp": convert_date_format(date)}):
            result.append((el["title"], el["url"]))

        return result
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    raise NotImplementedError
