import trafilatura

def parse_article(url: str) -> str:
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        if not text:
            return "Не удалось извлечь текст"
        return text[:4000]
    except Exception as e:
        return f"Ошибка парсинга: {str(e)}"