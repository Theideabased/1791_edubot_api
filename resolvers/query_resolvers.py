from datetime import datetime
from typing import Any, Dict, Optional
from services.content_service import content_service
from config import settings

def query_resolvers(query):
    """Bind query resolvers to the QueryType"""
    
    @query.field("health")
    async def resolve_health(*_) -> Dict[str, Any]:
        """Health check resolver"""
        return {
            "status": "healthy",
            "message": "EduBot GraphQL API is running",
            "version": settings.API_VERSION,
            "timestamp": datetime.utcnow()
        }
    
    @query.field("topics")
    async def resolve_topics(*_) -> Dict[str, Any]:
        """Get all saved topics"""
        try:
            result = content_service.get_saved_topics()
            return result
        except Exception as e:
            return {
                "topics": [],
                "total": 0
            }
    
    @query.field("topic")
    async def resolve_topic(_, info, id: str) -> Optional[Dict[str, Any]]:
        """Get specific topic by ID"""
        try:
            topics_data = content_service.get_saved_topics()
            for topic in topics_data["topics"]:
                if topic["id"] == id:
                    return topic
            return None
        except Exception:
            return None
    
    @query.field("apiInfo")
    async def resolve_api_info(*_) -> Dict[str, Any]:
        """Get API information"""
        return {
            "name": "EduBot GraphQL API",
            "version": settings.API_VERSION,
            "description": "Educational content generation using Google Gemini AI",
            "endpoints": [
                "Query: health - Health check",
                "Query: topics - Get saved topics",
                "Query: topic(id) - Get specific topic",
                "Mutation: summarize - Summarize text",
                "Mutation: explain - Explain concept", 
                "Mutation: generateQuiz - Generate quiz",
                "Mutation: educate - Generate complete educational content"
            ],
            "features": [
                "Text summarization using Gemini AI",
                "Concept explanation at different levels",
                "Quiz generation with multiple choice questions",
                "Complete educational content generation",
                "PDF export capability",
                "Topic history tracking",
                "GraphQL schema with proper validation",
                "Real-time subscriptions (optional)"
            ]
        }
