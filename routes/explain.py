from fastapi import APIRouter, HTTPException
from schemas import ExplainRequest, ExplainResponse
from services.content_service import content_service

router = APIRouter()

@router.post("/explain", response_model=ExplainResponse)
async def explain_concept(request: ExplainRequest):
    """
    Explain a concept at the specified level using Google Gemini.
    
    - **concept**: The concept to explain (max 1,000 characters)
    - **api_key**: Your Gemini API key
    - **level**: Explanation level (beginner, intermediate, advanced)
    """
    try:
        result = await content_service.explain_concept(
            concept=request.concept,
            level=request.level,
            api_key=request.api_key
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
