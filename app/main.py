from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI News Agent",
    description="FastAPI агент: parser + NewsAPI + Grok",
    version="1.0.0",
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "AI News Agent",
        "version": "1.0.0",
        "endpoint": "POST /analyze",
    }