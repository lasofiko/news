from app.services.llm_service import ask_llm

def analyze(summary: str, news: list, wiki: list):
    summary_text = summary if summary else "Нет исходной статьи (пользователь ввел тему, а не URL)"
    news_text = "\n".join([f"- {n['title']}: {n['description']}" for n in news])
    if not news_text:
        news_text = "- Нет новостей по запросу или источник недоступен"
    wiki_text = "\n".join([f"- {w['title']}: {w['summary']}" for w in wiki])
    if not wiki_text:
        wiki_text = "- Нет результатов Wikipedia по запросу или источник недоступен"
    prompt = f"""
Есть данные из трех источников:

1. Краткое содержание статьи:
{summary_text}

2. Новости по теме:
{news_text}

3. Информация из Википедии:
{wiki_text}

Сформируй ответ СТРОГО по абзацам, с заголовками, в человеческом виде:

### Контекст
4-8 предложения без воды

### Повторяющиеся темы
- 3-5 развернутых пунктов

Просто дай полезный контекст по тем данным, которые есть, без выдуманных фактов.
"""
    return {"result": ask_llm(prompt)}