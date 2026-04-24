from openai import OpenAI
from app.core.config import GROQ_API_KEY, GROQ_MODEL

client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

def _fix_mojibake(text: str) -> str:

    if "Ð" not in text and "Ñ" not in text:
        return text
    try:
        return text.encode("latin-1", errors="ignore").decode("utf-8", errors="ignore")
    except Exception:
        return text

def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000,
    )
    content = response.choices[0].message.content or ""
    return _fix_mojibake(content)