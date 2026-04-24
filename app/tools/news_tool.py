import requests
from app.core.config import NEWS_API_KEY

def _query_variants(query: str) -> list[str]:
    variants = [query.strip()]
    lowered = query.lower()

    simplified = (
        lowered.replace(" для ", " ")
        .replace(" про ", " ")
        .replace(" о ", " ")
        .strip()
    )
    if simplified and simplified not in variants:
        variants.append(simplified)

    unique = []
    for item in variants:
        if item and item not in unique:
            unique.append(item)
    return unique

def _request_news(query: str, language: str | None):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "pageSize": 5,
    }
    if language:
        params["language"] = language

    response = requests.get(url, params=params, timeout=20)
    if response.status_code != 200:
        return []

    data = response.json()
    articles = data.get("articles", [])
    return [
        {
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "url": item.get("url", ""),
        }
        for item in articles
    ]

def get_news(query: str):

    for query_variant in _query_variants(query):
        for language in ("ru", "en", None):
            articles = _request_news(query_variant, language)
            if articles:
                return articles
    return []