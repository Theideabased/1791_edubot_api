import asyncio
from typing import Any, Dict, AsyncGenerator
from datetime import datetime

def subscription_resolvers(subscription):
    """Bind subscription resolvers to the SubscriptionType"""
    
    @subscription.source("contentGeneration")
    async def content_generation_source(_, info, topic: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Source for content generation progress updates"""
        steps = [
            {"step": "Initializing", "progress": 0, "message": f"Starting content generation for '{topic}'"},
            {"step": "Generating Syllabus", "progress": 20, "message": "Creating course outline and structure"},
            {"step": "Creating Modules", "progress": 40, "message": "Generating detailed module content"},
            {"step": "Generating Quiz", "progress": 70, "message": "Creating assessment questions"},
            {"step": "Finalizing", "progress": 90, "message": "Preparing final content"},
            {"step": "Complete", "progress": 100, "message": "Content generation completed successfully"}
        ]
        
        for step_data in steps:
            yield {
                **step_data,
                "completed": step_data["progress"] >= 100,
                "timestamp": datetime.utcnow()
            }
            await asyncio.sleep(2)  # Simulate processing time
    
    @subscription.field("contentGeneration")
    def content_generation_resolver(data, *_) -> Dict[str, Any]:
        """Resolver for content generation subscription"""
        return data
