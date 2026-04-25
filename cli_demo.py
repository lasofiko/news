import json
import sys
from textwrap import shorten

import requests

API_URL = "http://127.0.0.1:8000/analyze"

def _print_header(title: str) -> None:
    print(f"\n {title} ")

def _get_api_fields(data: dict) -> dict:

    return {
        "result": data.get("result", ""),
        "collected_at": data.get("collected_at", ""),
        "news_items": data.get("news_items", []),
        "wiki_items": data.get("wiki_items", []),
        "warning": data.get("warning", ""),
    }

def _print_news_items(items: list[dict]) -> None:
    if not items:
        print("Нет новостей")
        return
    for idx, item in enumerate(items, start=1):
        title = item.get("title", "")
        description = item.get("description", "")
        print(f"{idx}. {title}")
        if description:
            print(f"   {shorten(description, width=140, placeholder='...')}")
        if item.get("url"):
            print(f"   {item['url']}")

def _print_wiki_items(items: list[dict]) -> None:
    if not items:
        print("Нет информации из википедии")
        return
    for idx, item in enumerate(items, start=1):
        title = item.get("title", "")
        summary = item.get("summary", "")
        print(f"{idx}. {title}")
        if summary:
            print(f"   {shorten(summary, width=180, placeholder='...')}")
        if item.get("url"):
            print(f"   {item['url']}")

def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):

        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    print("Демо версия cli новостного агента")
    print("Напишите тему или вставьте url-ссылкую Затем нажмите enter")
    query = input("Ввод: ").strip()

    if not query:
        print("Пустой запрос")
        return

    try:
        response = requests.post(API_URL, json={"query": query}, timeout=120)
    except requests.RequestException as exc:
        print(f"Ошибка запроса: {exc}")
        print("Сервер должен быть запущен: uvicorn app.main:app --reload")
        return

    if response.status_code != 200:
        print(f"Ошибка api: {response.status_code}")
        try:
            print(json.dumps(response.json(), ensure_ascii=False, indent=2))
        except Exception:
            print(response.text)
        return

    data = response.json()
    fields = _get_api_fields(data)

    _print_header("РЕЗУЛЬТАТ")
    print(fields["result"])

    _print_header("ДИАГНОСТИКА")
    print(f"время сбора: {fields['collected_at']}")
    print(f"количество новостей: {len(fields['news_items'])}")
    print(f"количество данных из википедии: {len(fields['wiki_items'])}")
    if fields["warning"]:
        print(f"предупреждение: {fields['warning']}")

    _print_header("НОВОСТИ")
    _print_news_items(fields["news_items"])

    _print_header("ВИКИПЕДИЯ")
    _print_wiki_items(fields["wiki_items"])

if __name__ == "__main__":
    main()
