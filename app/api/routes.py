from fastapi import APIRouter, HTTPException
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse
from app.agent.orchestrator import run_agent

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    try:
        return run_agent(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))