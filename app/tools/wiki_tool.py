import requests
from urllib.parse import quote

HEADERS = {
    "User-Agent": "ai-news-agent/1.0 (educational project; contact: local-user)",
}

def _fetch_wiki(lang: str, query: str):
    search_url = f"https://{lang}.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": 3,
    }
    search_response = requests.get(search_url, params=search_params, timeout=20, headers=HEADERS)
    if search_response.status_code != 200:
        return []

    search_data = search_response.json()
    pages = search_data.get("query", {}).get("search", [])
    results = []
    for page in pages:
        title = page.get("title", "")
        if not title:
            continue
        summary_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
        summary_response = requests.get(summary_url, timeout=20, headers=HEADERS)
        if summary_response.status_code != 200:
            continue
        summary_data = summary_response.json()
        results.append(
            {
                "title": summary_data.get("title", title),
                "summary": summary_data.get("extract", ""),
                "url": summary_data.get("content_urls", {}).get("desktop", {}).get("page", ""),
            }
        )
    return results

def get_wikipedia_context(query: str):
    try:
        ru_results = _fetch_wiki("ru", query)
        if ru_results:
            return ru_results

        return _fetch_wiki("en", query)
    except Exception:
        return []