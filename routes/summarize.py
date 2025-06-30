from fastapi import APIRouter, HTTPException
from schemas import SummarizeRequest, SummarizeResponse
from services.content_service import content_service

router = APIRouter()

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest):
    """
    Summarize a block of text using Google Gemini.
    
    - **text**: The text to summarize (max 10,000 characters)
    - **api_key**: Your Gemini API key
    - **max_length**: Maximum length of the summary (50-500 words)
    """
    try:
        result = await content_service.summarize_text(
            text=request.text,
            api_key=request.api_key,
            max_length=request.max_length
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
