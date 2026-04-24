from pydantic import BaseModel
from typing import List

class AnalyzeResponse(BaseModel):
    result: str
    collected_at: str
    news_sources: List[str]
    wiki_sources: List[str]
    news_items: List[dict]
    wiki_items: List[dict]
    warning: str