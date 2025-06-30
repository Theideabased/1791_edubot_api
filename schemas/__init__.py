from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum

class BaseRequest(BaseModel):
    api_key: str = Field(..., min_length=1, description="Your Gemini API key")

class SummarizeRequest(BaseRequest):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to summarize")
    max_length: Optional[int] = Field(150, ge=50, le=500, description="Maximum summary length")

class ExplainRequest(BaseRequest):
    concept: str = Field(..., min_length=1, max_length=1000, description="Concept to explain")
    level: Optional[str] = Field("intermediate", description="Explanation level: beginner, intermediate, advanced")
    
    @validator('level')
    def validate_level(cls, v):
        if v not in ['beginner', 'intermediate', 'advanced']:
            raise ValueError('Level must be beginner, intermediate, or advanced')
        return v

class QuizRequest(BaseRequest):
    topic: Optional[str] = Field(None, description="Topic for quiz generation")
    text: Optional[str] = Field(None, description="Text content for quiz generation")
    num_questions: Optional[int] = Field(5, ge=1, le=20, description="Number of questions to generate")
    difficulty: Optional[str] = Field("medium", description="Quiz difficulty: easy, medium, hard")
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        if v not in ['easy', 'medium', 'hard']:
            raise ValueError('Difficulty must be easy, medium, or hard')
        return v
    
    @validator('text')
    def validate_topic_or_text(cls, v, values):
        if not v and not values.get('topic'):
            raise ValueError('Either topic or text must be provided')
        return v

class EducateRequest(BaseRequest):
    topic: str = Field(..., min_length=1, max_length=500, description="Topic for educational content generation")
    modules_count: Optional[int] = Field(5, ge=3, le=10, description="Number of modules in the syllabus")
    include_pdf: Optional[bool] = Field(False, description="Generate PDF export")

# Response Models
class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    provider_used: str = "gemini"

class ExplainResponse(BaseModel):
    explanation: str
    concept: str
    level: str
    provider_used: str = "gemini"

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class QuizResponse(BaseModel):
    questions: List[QuizQuestion]
    topic: Optional[str]
    difficulty: str
    total_questions: int
    provider_used: str = "gemini"

class Module(BaseModel):
    title: str
    description: str
    content: str
    key_points: List[str]
    estimated_duration: str

class Syllabus(BaseModel):
    topic: str
    overview: str
    modules: List[Dict[str, str]]
    total_duration: str
    learning_objectives: List[str]

class EducateResponse(BaseModel):
    topic: str
    syllabus: Syllabus
    modules: List[Module]
    quiz: QuizResponse
    pdf_url: Optional[str]
    provider_used: str = "gemini"

class TopicItem(BaseModel):
    id: str
    topic: str
    created_at: str
    provider_used: str = "gemini"
    modules_count: int

class TopicsResponse(BaseModel):
    topics: List[TopicItem]
    total: int

class ErrorResponse(BaseModel):
    error: str
    detail: str
    status_code: int
