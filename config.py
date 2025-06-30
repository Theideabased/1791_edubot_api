import os
from typing import Optional

class Settings:
    """Application settings and configuration"""
    
    # API Configuration
    API_TITLE = "EduBot API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "A RESTful API for generating educational materials using various LLM providers"
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    
    # PDF Configuration
    PDF_DIRECTORY = "generated_pdfs"
    MAX_PDF_SIZE_MB = 50
    
    # LLM Configuration
    DEFAULT_MAX_TOKENS = 2000
    DEFAULT_TEMPERATURE = 0.7
    REQUEST_TIMEOUT = 30  # seconds
    
    # Content Limits
    MAX_TEXT_LENGTH = 10000
    MAX_CONCEPT_LENGTH = 1000
    MAX_TOPIC_LENGTH = 500
    MIN_QUESTIONS = 1
    MAX_QUESTIONS = 20
    MIN_MODULES = 3
    MAX_MODULES = 10
    
    # Default API Keys (optional - can be set via environment variables)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    MISTRAL_API_KEY: Optional[str] = os.getenv("MISTRAL_API_KEY")
    
    # CORS Configuration
    CORS_ORIGINS = ["*"]
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]

# Global settings instance
settings = Settings()
