from fastapi import APIRouter, HTTPException
from schemas import QuizRequest, QuizResponse
from services.content_service import content_service

router = APIRouter()

@router.post("/quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """
    Generate multiple-choice quiz questions based on a topic or text using Google Gemini.
    
    - **topic**: Topic for quiz generation (optional if text is provided)
    - **text**: Text content for quiz generation (optional if topic is provided)
    - **api_key**: Your Gemini API key
    - **num_questions**: Number of questions to generate (1-20)
    - **difficulty**: Quiz difficulty level (easy, medium, hard)
    """
    try:
        result = await content_service.generate_quiz(
            topic=request.topic,
            text=request.text,
            num_questions=request.num_questions,
            difficulty=request.difficulty,
            api_key=request.api_key
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
