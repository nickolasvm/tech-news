from tech_news.database import db


def top_5_categories():
    categories = list(db.news.find({}, {"_id": False, "category": True}))

    for i, c in enumerate(categories):
        categories[i]["count"] = db.news.find(
            {"category": c["category"]}
        ).count()

    #  sort alphabetically
    categories = sorted(categories, key=lambda x: x["category"])
    #  sort by count
    categories = sorted(categories, key=lambda x: x["count"], reverse=True)

    result = []
    seen = set()
    for c in categories:
        if c["category"] not in seen and len(result) < 5:
            seen.add(c["category"])
            result.append(c["category"])

    return result
