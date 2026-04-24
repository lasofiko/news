def is_url(text: str) -> bool:
    return text.startswith("http://") or text.startswith("https://")

def decide_tools(query: str):
    if is_url(query):
        return ["parser", "news", "wiki"]
    return ["news", "wiki"]