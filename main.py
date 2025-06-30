from ariadne import QueryType, MutationType, make_executable_schema, graphql_sync, SubscriptionType
from ariadne.asgi import GraphQL
from ariadne.explorer import ExplorerGraphiQL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from typing import Any, Dict
from datetime import datetime

from resolvers.query_resolvers import query_resolvers
from resolvers.mutation_resolvers import mutation_resolvers
from resolvers.subscription_resolvers import subscription_resolvers
from utils.exceptions import setup_exception_handlers
from config import settings
import os

# Create necessary directories
os.makedirs(settings.PDF_DIRECTORY, exist_ok=True)

# Load GraphQL schema
with open("schema.graphql", "r") as f:
    type_defs = f.read()

# Create type definitions
query = QueryType()
mutation = MutationType()
subscription = SubscriptionType()

# Bind resolvers
query_resolvers(query)
mutation_resolvers(mutation)
subscription_resolvers(subscription)

# Create executable schema
schema = make_executable_schema(type_defs, query, mutation, subscription)

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Setup exception handlers
setup_exception_handlers(app)

# Create GraphQL endpoint with explorer
graphql_app = ExplorerGraphiQL(schema)

# Mount GraphQL endpoint
app.mount("/graphql", graphql_app)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to EduBot GraphQL API",
        "version": settings.API_VERSION,
        "graphql_endpoint": "/graphql",
        "explorer": "/graphql (interactive)",
        "features": [
            "Text summarization using Gemini AI",
            "Concept explanation at different levels",
            "Quiz generation with MCQs",
            "Complete educational content generation",
            "PDF export capability",
            "Topic history tracking"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "message": "EduBot GraphQL API is running",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.API_VERSION
    }

# Additional REST endpoints for Swagger documentation
@app.get("/docs-info")
async def docs_info():
    """Information about available endpoints and GraphQL operations"""
    return {
        "message": "This API uses GraphQL. Visit /graphql for interactive documentation.",
        "graphql_endpoint": "/graphql",
        "available_operations": {
            "queries": [
                "health - API health check",
                "topics - Get all saved topics", 
                "topic(id) - Get specific topic",
                "apiInfo - Get API information"
            ],
            "mutations": [
                "summarize - Summarize text content",
                "explain - Explain concepts",
                "generateQuiz - Create MCQ quizzes", 
                "educate - Generate complete educational content"
            ],
            "subscriptions": [
                "contentGeneration - Real-time generation progress"
            ]
        },
        "example_queries": {
            "health_check": """
query {
  health {
    status
    message
    version
    timestamp
  }
}""",
            "summarize": """
mutation {
  summarize(input: {
    text: "Your text here..."
    api_key: "your-gemini-api-key"
    max_length: 100
  }) {
    ... on SummarizeResponse {
      summary
      original_length
      summary_length
    }
    ... on Error {
      code
      message
    }
  }
}"""
        }
    }

@app.get("/schema")
async def get_schema():
    """Get the GraphQL schema definition"""
    return {
        "schema": type_defs,
        "note": "Visit /graphql for interactive schema exploration"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG
    )
