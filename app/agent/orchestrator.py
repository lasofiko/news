from datetime import datetime, timezone

from app.agent.router import decide_tools
from app.tools.parser_tool import parse_article
from app.tools.news_tool import get_news
from app.tools.wiki_tool import get_wikipedia_context
from app.services.summarizer_service import summarize
from app.services.analyzer_service import analyze

def run_agent(query: str):
    tools = decide_tools(query)
    article_summary = ""
    wiki_data = []
    llm_warning = ""

    if "parser" in tools:
        article_text = parse_article(query)
        try:
            article_summary = summarize(article_text)
            search_query = article_summary[:200]
        except Exception as exc:
            llm_warning = f"LLM unavailable: {exc}"
            article_summary = article_text[:700]
            search_query = article_summary[:200]
        news_data = get_news(search_query)
    else:
        news_data = get_news(query)

    if "wiki" in tools:
        wiki_query = article_summary[:200] if article_summary else query
        wiki_data = get_wikipedia_context(wiki_query)

    try:
        analysis = analyze(article_summary, news_data, wiki_data)
    except Exception as exc:
        if not llm_warning:
            llm_warning = f"LLM unavailable: {exc}"
        news_titles = [item.get("title", "") for item in news_data if item.get("title")]
        wiki_titles = [item.get("title", "") for item in wiki_data if item.get("title")]

        fallback_lines = [
            "## Контекст",
            "LLM временно недоступна, поэтому ответ собран только из инструментов (NewsAPI + Wikipedia + parser)",
            "",
            "## Повторяющиеся темы",
        ]
        if news_titles or wiki_titles:
            for title in (news_titles[:3] + wiki_titles[:2]):
                fallback_lines.append(f"- {title}")
        else:
            fallback_lines.append("- Источники не вернули данных по запросу")

        fallback_lines.extend(
            [
                "",
                "## Источники",
                "Ответ собран без LLM и основан только на данных инструментов",
            ]
        )
        analysis = {"result": "\n".join(fallback_lines)}
    collected_at = datetime.now(timezone.utc).isoformat()
    news_sources = [item.get("url", "") for item in news_data if item.get("url")]
    wiki_sources = [item.get("url", "") for item in wiki_data if item.get("url")]

    return {
        "result": analysis.get("result", ""),
        "collected_at": collected_at,
        "news_sources": news_sources,
        "wiki_sources": wiki_sources,
        "news_items": news_data,
        "wiki_items": wiki_data,
        "warning": llm_warning,
    }