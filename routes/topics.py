from fastapi import APIRouter
from schemas import TopicsResponse
from services.content_service import content_service

router = APIRouter()

@router.get("/topics", response_model=TopicsResponse)
async def get_saved_topics():
    """
    Get all saved/generated topics with their basic information.
    
    Returns a list of previously generated educational topics with:
    - Topic ID
    - Topic name
    - Creation date
    - Provider used
    - Number of modules
    """
    try:
        result = content_service.get_saved_topics()
        return TopicsResponse(**result)
    except Exception as e:
        return TopicsResponse(topics=[], total=0)
