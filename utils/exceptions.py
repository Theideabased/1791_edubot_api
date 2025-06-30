from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProviderError(Exception):
    """Exception raised for LLM provider errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InvalidAPIKeyError(Exception):
    """Exception raised for invalid API keys"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ContentGenerationError(Exception):
    """Exception raised for content generation errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

def setup_exception_handlers(app):
    """Setup global exception handlers for the FastAPI app"""
    
    @app.exception_handler(LLMProviderError)
    async def llm_provider_exception_handler(request: Request, exc: LLMProviderError):
        logger.error(f"LLM Provider Error: {exc.message}")
        return JSONResponse(
            status_code=503,
            content={
                "error": "LLM Provider Error",
                "detail": exc.message,
                "status_code": 503
            }
        )
    
    @app.exception_handler(InvalidAPIKeyError)
    async def invalid_api_key_exception_handler(request: Request, exc: InvalidAPIKeyError):
        logger.error(f"Invalid API Key: {exc.message}")
        return JSONResponse(
            status_code=401,
            content={
                "error": "Invalid API Key",
                "detail": exc.message,
                "status_code": 401
            }
        )
    
    @app.exception_handler(ContentGenerationError)
    async def content_generation_exception_handler(request: Request, exc: ContentGenerationError):
        logger.error(f"Content Generation Error: {exc.message}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Content Generation Error",
                "detail": exc.message,
                "status_code": 500
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation Error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation Error",
                "detail": str(exc.errors()),
                "status_code": 422
            }
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error(f"HTTP Exception: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP Error",
                "detail": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unexpected error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": "An unexpected error occurred. Please try again later.",
                "status_code": 500
            }
        )
