from app.services.llm_service import ask_llm

def summarize(text: str) -> str:
    prompt = f"""
Сделай краткое содержание статьи:
- 3-5 пунктов
- ключевые идеи
- простое объяснение

Текст:
{text}
"""
    return ask_llm(prompt)