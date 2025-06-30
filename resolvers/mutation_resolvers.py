from datetime import datetime
from typing import Any, Dict
from services.content_service import content_service
from utils.exceptions import LLMProviderError, InvalidAPIKeyError, ContentGenerationError

def mutation_resolvers(mutation):
    """Bind mutation resolvers to the MutationType"""
    
    @mutation.field("summarize")
    async def resolve_summarize(_, info, input: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize text using Gemini AI"""
        try:
            result = await content_service.summarize_text(
                text=input["text"],
                api_key=input["api_key"],
                max_length=input.get("max_length", 150)
            )
            return result.__dict__
        except (LLMProviderError, InvalidAPIKeyError) as e:
            return {
                "__typename": "Error",
                "code": "LLM_ERROR",
                "message": str(e),
                "details": "Please check your API key and try again"
            }
        except Exception as e:
            return {
                "__typename": "Error", 
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": str(e)
            }
    
    @mutation.field("explain")
    async def resolve_explain(_, info, input: Dict[str, Any]) -> Dict[str, Any]:
        """Explain a concept using Gemini AI"""
        try:
            # Map GraphQL enum to string
            level_map = {
                "BEGINNER": "beginner",
                "INTERMEDIATE": "intermediate", 
                "ADVANCED": "advanced"
            }
            level = level_map.get(input.get("level", "INTERMEDIATE"), "intermediate")
            
            result = await content_service.explain_concept(
                concept=input["concept"],
                level=level,
                api_key=input["api_key"]
            )
            
            # Map back to GraphQL enum
            result_dict = result.__dict__
            result_dict["level"] = input.get("level", "INTERMEDIATE")
            return result_dict
            
        except (LLMProviderError, InvalidAPIKeyError) as e:
            return {
                "__typename": "Error",
                "code": "LLM_ERROR", 
                "message": str(e),
                "details": "Please check your API key and try again"
            }
        except Exception as e:
            return {
                "__typename": "Error",
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred", 
                "details": str(e)
            }
    
    @mutation.field("generateQuiz")
    async def resolve_generate_quiz(_, info, input: Dict[str, Any]) -> Dict[str, Any]:
        """Generate quiz using Gemini AI"""
        try:
            # Map GraphQL enum to string
            difficulty_map = {
                "EASY": "easy",
                "MEDIUM": "medium",
                "HARD": "hard"
            }
            difficulty = difficulty_map.get(input.get("difficulty", "MEDIUM"), "medium")
            
            result = await content_service.generate_quiz(
                topic=input.get("topic"),
                text=input.get("text"),
                num_questions=input.get("num_questions", 5),
                difficulty=difficulty,
                api_key=input["api_key"]
            )
            
            # Convert to dict and map difficulty back to GraphQL enum
            result_dict = result.__dict__
            result_dict["difficulty"] = input.get("difficulty", "MEDIUM")
            
            # Convert questions to dicts
            result_dict["questions"] = [q.__dict__ for q in result.questions]
            
            return result_dict
            
        except (LLMProviderError, InvalidAPIKeyError) as e:
            return {
                "__typename": "Error",
                "code": "LLM_ERROR",
                "message": str(e),
                "details": "Please check your API key and try again"
            }
        except Exception as e:
            return {
                "__typename": "Error",
                "code": "INTERNAL_ERROR", 
                "message": "An unexpected error occurred",
                "details": str(e)
            }
    
    @mutation.field("educate")
    async def resolve_educate(_, info, input: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete educational content using Gemini AI"""
        try:
            result = await content_service.generate_education_content(
                topic=input["topic"],
                modules_count=input.get("modules_count", 5),
                api_key=input["api_key"]
            )
            
            # Convert to dict
            result_dict = {
                "topic": result.topic,
                "provider_used": result.provider_used,
                "pdf_url": result.pdf_url,
                "generated_at": datetime.utcnow()
            }
            
            # Convert syllabus
            syllabus_dict = result.syllabus.__dict__
            result_dict["syllabus"] = syllabus_dict
            
            # Convert modules
            result_dict["modules"] = [module.__dict__ for module in result.modules]
            
            # Convert quiz
            quiz_dict = result.quiz.__dict__
            quiz_dict["questions"] = [q.__dict__ for q in result.quiz.questions]
            result_dict["quiz"] = quiz_dict
            
            # Handle PDF generation if requested
            if input.get("include_pdf", False):
                try:
                    from services.pdf_service import pdf_service
                    pdf_path = pdf_service.generate_education_pdf({
                        "topic": result.topic,
                        "provider_used": result.provider_used,
                        "syllabus": syllabus_dict,
                        "modules": result_dict["modules"],
                        "quiz": quiz_dict
                    })
                    result_dict["pdf_url"] = f"/download/pdf/{pdf_path.split('/')[-1]}"
                except Exception as pdf_error:
                    print(f"PDF generation failed: {pdf_error}")
                    result_dict["pdf_url"] = None
            
            return result_dict
            
        except (LLMProviderError, InvalidAPIKeyError) as e:
            return {
                "__typename": "Error",
                "code": "LLM_ERROR",
                "message": str(e),
                "details": "Please check your API key and try again"
            }
        except Exception as e:
            return {
                "__typename": "Error",
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": str(e)
            }
