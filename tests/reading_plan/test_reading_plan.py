import pytest
from unittest.mock import patch
from tech_news.analyzer.reading_plan import (
    ReadingPlanService,
)  # noqa: F401, E261, E501

mock_result = [
    {
        "url": "https://www.google.com/",
        "title": "10 jogos para iniciantes aprenderem a programar!",
        "timestamp": "22/05/2023",
        "writer": "Nome Sobrenome",
        "reading_time": 3,
        "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "category": "Tecnologia",
    },
    {
        "url": "https://www.google.com/",
        "title": "Endless OS: por que vale a pena usar esse sistema",
        "timestamp": "18/05/2023",
        "writer": "Cairo Noleto",
        "reading_time": 4,
        "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "category": "Tecnologia",
    },
    {
        "url": "https://www.google.com/",
        "title": "CTO do Nubank revela as habilidades importantes",
        "timestamp": "15/05/2023",
        "writer": "Lucas Custódio",
        "reading_time": 10,
        "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "category": "Carreira",
    },
    {
        "url": "https://www.google.com/",
        "title": "Título de uma notícia não lida",
        "timestamp": "15/05/2023",
        "writer": "Lucas Custódio",
        "reading_time": 15,
        "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "category": "Carreira",
    },
]


def test_reading_plan_group_news():
    #  test if available_time <= 0
    with pytest.raises(ValueError):
        ReadingPlanService.group_news_for_available_time(available_time=0)

    # mock the return value from the db
    with patch(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
        return_value=mock_result,
    ):
        #  test if the unreadable key has only one news
        assert (
            len(
                ReadingPlanService.group_news_for_available_time(10)[
                    "unreadable"
                ]
            )
            == 1
        )

        #  test if the first readable group key has 3 minutes
        #  of unfilled time left
        assert (
            ReadingPlanService.group_news_for_available_time(10)["readable"][
                0
            ]["unfilled_time"]
            == 3
        )
