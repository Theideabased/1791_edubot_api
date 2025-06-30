import json
import uuid
from datetime import datetime
from typing import Dict, List, Any
from services.llm_service import llm_service
from schemas import (
    SummarizeResponse, ExplainResponse, QuizResponse, EducateResponse,
    QuizQuestion, Module, Syllabus
)

class ContentService:
    """Service for generating educational content"""
    
    def __init__(self):
        # In-memory storage for topics (replace with database in production)
        self.topics_storage = {}
    
    async def summarize_text(self, text: str, api_key: str, max_length: int = 150) -> SummarizeResponse:
        """Summarize given text"""
        system_prompt = (
            "You are an expert at creating concise, accurate summaries. "
            "Provide a clear and informative summary that captures the main points."
        )
        
        prompt = f"""
        Please summarize the following text in approximately {max_length} words or less:
        
        Text: {text}
        
        Requirements:
        - Keep the summary concise and informative
        - Capture the main ideas and key points
        - Make it easy to understand
        """
        
        summary = await llm_service.generate_content(api_key, prompt, system_prompt)
        
        return SummarizeResponse(
            summary=summary.strip(),
            original_length=len(text.split()),
            summary_length=len(summary.split()),
            provider_used="gemini"
        )
    
    async def explain_concept(self, concept: str, level: str, api_key: str) -> ExplainResponse:
        """Explain a concept at the specified level"""
        level_instructions = {
            "beginner": "Explain in simple terms, avoid jargon, use analogies and examples",
            "intermediate": "Provide a balanced explanation with some technical details",
            "advanced": "Include technical details, advanced concepts, and theoretical background"
        }
        
        system_prompt = (
            f"You are an expert educator. Explain concepts clearly at the {level} level. "
            f"{level_instructions[level]}. Always provide practical examples when possible."
        )
        
        prompt = f"""
        Please explain the concept: "{concept}"
        
        Level: {level}
        
        Requirements:
        - Make the explanation appropriate for the {level} level
        - Include practical examples
        - Structure the explanation clearly
        - Make it engaging and easy to understand
        """
        
        explanation = await llm_service.generate_content(api_key, prompt, system_prompt)
        
        return ExplainResponse(
            explanation=explanation.strip(),
            concept=concept,
            level=level,
            provider_used="gemini"
        )
    
    async def generate_quiz(self, topic: str, text: str, num_questions: int, difficulty: str, 
                          api_key: str) -> QuizResponse:
        """Generate quiz questions"""
        difficulty_instructions = {
            "easy": "basic understanding and recall",
            "medium": "application and analysis",
            "hard": "synthesis and evaluation"
        }
        
        system_prompt = (
            "You are an expert quiz creator. Generate multiple-choice questions that test "
            f"{difficulty_instructions[difficulty]}. Each question should have 4 options with "
            "one correct answer. Always provide explanations for the correct answers."
        )
        
        content_source = f"Topic: {topic}" if topic else f"Text: {text}"
        
        prompt = f"""
        Create {num_questions} multiple-choice questions based on the following:
        
        {content_source}
        
        Difficulty: {difficulty}
        
        Requirements:
        - Each question should have exactly 4 options (A, B, C, D)
        - Only one correct answer per question
        - Include an explanation for each correct answer
        - Questions should test {difficulty_instructions[difficulty]}
        
        Format your response as valid JSON:
        {{
            "questions": [
                {{
                    "question": "Question text here?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": 0,
                    "explanation": "Explanation of the correct answer"
                }}
            ]
        }}
        """
        
        response = await llm_service.generate_content(api_key, prompt, system_prompt)
        
        try:
            # Parse JSON response
            quiz_data = json.loads(response.strip())
            questions = [
                QuizQuestion(**q) for q in quiz_data["questions"]
            ]
        except (json.JSONDecodeError, KeyError) as e:
            # Fallback: create questions manually if JSON parsing fails
            questions = await self._create_fallback_quiz(topic or text, num_questions, difficulty, api_key)
        
        return QuizResponse(
            questions=questions,
            topic=topic,
            difficulty=difficulty,
            total_questions=len(questions),
            provider_used="gemini"
        )
    
    async def generate_education_content(self, topic: str, modules_count: int, 
                                       api_key: str) -> EducateResponse:
        """Generate complete educational content including syllabus, modules, and quiz"""
        
        # Generate syllabus
        syllabus = await self._generate_syllabus(topic, modules_count, api_key)
        
        # Generate detailed content for each module
        modules = []
        for module_info in syllabus.modules:
            module_content = await self._generate_module_content(
                topic, module_info["title"], module_info["description"], api_key
            )
            modules.append(module_content)
        
        # Generate quiz for the entire topic
        quiz = await self.generate_quiz(topic, None, 10, "medium", api_key)
        
        # Save topic to storage
        topic_id = str(uuid.uuid4())
        self.topics_storage[topic_id] = {
            "id": topic_id,
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "provider_used": "gemini",
            "modules_count": modules_count
        }
        
        return EducateResponse(
            topic=topic,
            syllabus=syllabus,
            modules=modules,
            quiz=quiz,
            pdf_url=None,  # PDF generation will be implemented separately
            provider_used="gemini"
        )
    
    async def _generate_syllabus(self, topic: str, modules_count: int, api_key: str) -> Syllabus:
        """Generate a comprehensive syllabus"""
        system_prompt = (
            "You are an expert curriculum designer. Create comprehensive syllabi that provide "
            "clear learning paths with well-structured modules and realistic time estimates."
        )
        
        prompt = f"""
        Create a comprehensive syllabus for the topic: "{topic}"
        
        Requirements:
        - Create exactly {modules_count} modules
        - Include an overview of the entire topic
        - Provide learning objectives
        - Estimate duration for each module and total course
        - Make modules progressive (building on each other)
        
        Format your response as valid JSON:
        {{
            "overview": "Brief overview of the topic and what students will learn",
            "modules": [
                {{
                    "title": "Module 1 Title",
                    "description": "What this module covers"
                }}
            ],
            "total_duration": "Total estimated time (e.g., '4 weeks', '20 hours')",
            "learning_objectives": ["Objective 1", "Objective 2", "Objective 3"]
        }}
        """
        
        response = await llm_service.generate_content(api_key, prompt, system_prompt)
        
        try:
            syllabus_data = json.loads(response.strip())
            return Syllabus(
                topic=topic,
                overview=syllabus_data["overview"],
                modules=syllabus_data["modules"],
                total_duration=syllabus_data["total_duration"],
                learning_objectives=syllabus_data["learning_objectives"]
            )
        except (json.JSONDecodeError, KeyError):
            # Fallback syllabus
            return await self._create_fallback_syllabus(topic, modules_count, api_key)
    
    async def _generate_module_content(self, topic: str, module_title: str, 
                                     module_description: str, api_key: str) -> Module:
        """Generate detailed content for a specific module"""
        system_prompt = (
            "You are an expert educator creating detailed learning content. "
            "Provide comprehensive, well-structured content with practical examples."
        )
        
        prompt = f"""
        Create detailed learning content for this module:
        
        Topic: {topic}
        Module Title: {module_title}
        Module Description: {module_description}
        
        Requirements:
        - Provide comprehensive content that covers the module thoroughly
        - Include key points (5-7 bullet points)
        - Estimate realistic duration for studying this module
        - Make content engaging and informative
        - Include practical examples where relevant
        
        Format your response as valid JSON:
        {{
            "content": "Detailed content for the module (2-3 paragraphs)",
            "key_points": ["Key point 1", "Key point 2", "Key point 3"],
            "estimated_duration": "Estimated study time (e.g., '2 hours', '1 week')"
        }}
        """
        
        response = await llm_service.generate_content(api_key, prompt, system_prompt)
        
        try:
            module_data = json.loads(response.strip())
            return Module(
                title=module_title,
                description=module_description,
                content=module_data["content"],
                key_points=module_data["key_points"],
                estimated_duration=module_data["estimated_duration"]
            )
        except (json.JSONDecodeError, KeyError):
            # Fallback module content
            return await self._create_fallback_module(module_title, module_description, api_key)
    
    async def _create_fallback_quiz(self, content: str, num_questions: int, difficulty: str, 
                                  api_key: str) -> List[QuizQuestion]:
        """Create a fallback quiz when JSON parsing fails"""
        # Simple fallback - create basic questions
        questions = []
        for i in range(num_questions):
            question = QuizQuestion(
                question=f"Question {i+1} about {content}?",
                options=["Option A", "Option B", "Option C", "Option D"],
                correct_answer=0,
                explanation="This is the correct answer explanation."
            )
            questions.append(question)
        return questions
    
    async def _create_fallback_syllabus(self, topic: str, modules_count: int, 
                                      api_key: str) -> Syllabus:
        """Create a fallback syllabus when JSON parsing fails"""
        modules = []
        for i in range(modules_count):
            modules.append({
                "title": f"Module {i+1}: {topic} - Part {i+1}",
                "description": f"This module covers important aspects of {topic}"
            })
        
        return Syllabus(
            topic=topic,
            overview=f"This course provides a comprehensive introduction to {topic}",
            modules=modules,
            total_duration="4-6 weeks",
            learning_objectives=[
                f"Understand the fundamentals of {topic}",
                f"Apply {topic} concepts in practice",
                f"Analyze and evaluate {topic} applications"
            ]
        )
    
    async def _create_fallback_module(self, title: str, description: str, 
                                    api_key: str) -> Module:
        """Create a fallback module when JSON parsing fails"""
        return Module(
            title=title,
            description=description,
            content=f"This module covers {description}. Students will learn key concepts and practical applications.",
            key_points=[
                "Key concept 1",
                "Key concept 2", 
                "Key concept 3",
                "Practical application",
                "Best practices"
            ],
            estimated_duration="2-3 hours"
        )
    
    def get_saved_topics(self) -> Dict[str, Any]:
        """Get all saved topics"""
        return {
            "topics": list(self.topics_storage.values()),
            "total": len(self.topics_storage)
        }

# Singleton instance
content_service = ContentService()
