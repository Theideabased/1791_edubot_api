# 🤖 EduBot GraphQL API

A comprehensive GraphQL API for generating educational materials using Google Gemini AI. Built with Ariadne and FastAPI, featuring proper schema design, query optimization, and real-time subscriptions.

## 🌟 Features

- **GraphQL First**: Complete GraphQL API with queries, mutations, and subscriptions
- **Gemini AI Integration**: Powered by Google's Gemini AI for content generation
- **Educational Content**: Generate summaries, explanations, quizzes, and complete courses
- **PDF Export**: Beautiful PDF generation of educational materials
- **Real-time Updates**: Subscriptions for content generation progress
- **Type Safety**: Strongly typed GraphQL schema with proper validation
- **Interactive Playground**: GraphQL Explorer for testing and documentation

## 📋 GraphQL Schema Overview

### Types
- **Query**: Health checks, topic retrieval, API information
- **Mutation**: Content generation operations
- **Subscription**: Real-time progress updates
- **Unions**: Error handling with typed responses

### Core Operations

| Type | Operation | Description |
|------|-----------|-------------|
| `Query` | `health` | API health check |
| `Query` | `topics` | Get saved topics |
| `Query` | `topic(id)` | Get specific topic |
| `Query` | `apiInfo` | Get API information |
| `Mutation` | `summarize` | Summarize text content |
| `Mutation` | `explain` | Explain concepts at different levels |
| `Mutation` | `generateQuiz` | Create MCQ quizzes |
| `Mutation` | `educate` | Generate complete educational content |
| `Subscription` | `contentGeneration` | Real-time generation progress |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd 1791_edubot_api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**
   ```bash
   python main.py
   ```

4. **Access the API**
   - **GraphQL Endpoint**: `http://localhost:8000/graphql` (Main API)
   - **GraphQL Explorer**: `http://localhost:8000/graphql` (Interactive documentation)
   - **Health Check**: `http://localhost:8000/health`
   - **Swagger/OpenAPI**: `http://localhost:8000/docs` (Limited - only shows REST endpoints)
   
   > **Note**: This is a GraphQL API, not REST. The main functionality is accessed through the single `/graphql` endpoint. Use the GraphQL Explorer for interactive testing and documentation.

## 📖 GraphQL Examples

### Basic Health Check
```graphql
query {
  health {
    status
    message
    version
    timestamp
  }
}
```

### Summarize Text
```graphql
mutation {
  summarize(input: {
    text: "Machine learning is a subset of artificial intelligence..."
    api_key: "your-gemini-api-key"
    max_length: 100
  }) {
    ... on SummarizeResponse {
      summary
      original_length
      summary_length
      provider_used
    }
    ... on Error {
      code
      message
      details
    }
  }
}
```

### Explain Concept
```graphql
mutation {
  explain(input: {
    concept: "Neural Networks"
    api_key: "your-gemini-api-key"
    level: BEGINNER
  }) {
    ... on ExplainResponse {
      explanation
      concept
      level
      provider_used
    }
    ... on Error {
      code
      message
    }
  }
}
```

### Generate Quiz
```graphql
mutation {
  generateQuiz(input: {
    topic: "Python Programming"
    api_key: "your-gemini-api-key"
    num_questions: 5
    difficulty: MEDIUM
  }) {
    ... on QuizResponse {
      questions {
        question
        options
        correct_answer
        explanation
      }
      topic
      difficulty
      total_questions
    }
    ... on Error {
      code
      message
    }
  }
}
```

### Generate Complete Educational Content
```graphql
mutation {
  educate(input: {
    topic: "Introduction to Data Science"
    api_key: "your-gemini-api-key"
    modules_count: 4
    include_pdf: true
  }) {
    ... on EducateResponse {
      topic
      generated_at
      pdf_url
      syllabus {
        overview
        modules {
          title
          description
        }
        learning_objectives
      }
      modules {
        title
        content
        key_points
        estimated_duration
      }
      quiz {
        questions {
          question
          options
          correct_answer
        }
        total_questions
      }
    }
    ... on Error {
      code
      message
    }
  }
}
```

### Real-time Subscription
```graphql
subscription {
  contentGeneration(topic: "Machine Learning") {
    step
    progress
    message
    completed
  }
}
```

## 🏗️ Architecture

### Project Structure
```
/home/seyman/1791_edubot_api/
├── main.py                    # GraphQL server setup
├── schema.graphql             # GraphQL schema definition
├── config.py                  # Configuration management
├── requirements.txt           # Dependencies
├── resolvers/                 # GraphQL resolvers
│   ├── query_resolvers.py     # Query resolvers
│   ├── mutation_resolvers.py  # Mutation resolvers
│   └── subscription_resolvers.py # Subscription resolvers
├── services/                  # Business logic
│   ├── llm_service.py         # Gemini AI integration
│   ├── content_service.py     # Content generation
│   └── pdf_service.py         # PDF generation
├── schemas/                   # Pydantic models (legacy)
├── utils/                     # Utilities
│   └── exceptions.py          # Error handling
├── examples/                  # Query examples
│   └── graphql_queries.md     # Example queries
└── test_graphql_api.py        # Test suite
```

### Schema Design Principles

1. **Type Safety**: Strongly typed inputs and outputs
2. **Error Handling**: Union types for error responses
3. **Nullable Fields**: Proper null handling for optional data
4. **Enums**: Predefined values for consistency
5. **Scalars**: Custom scalars for complex types (DateTime)

### Resolver Implementation

- **Query Resolvers**: Simple data fetching operations
- **Mutation Resolvers**: Complex business logic with error handling
- **Subscription Resolvers**: Real-time data streaming
- **Error Handling**: Comprehensive error responses

## 🔧 Configuration

### Environment Variables
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export DEBUG=true
export HOST="0.0.0.0"
export PORT=8000
```

### Schema Validation
The API includes comprehensive input validation:
- Required fields enforcement
- Type checking
- Enum validation
- Custom scalar validation

## 🧪 Testing

### Run Tests
```bash
python test_graphql_api.py
```

### Manual Testing
1. Open GraphQL Explorer at `http://localhost:8000/graphql`
2. Use the interactive playground to test queries
3. View schema documentation in the sidebar
4. Test with real API keys for full functionality

## 📊 Query Optimization

### DataLoader Pattern
- Implemented for efficient data fetching
- Batches similar requests
- Reduces N+1 query problems

### Caching Strategy
- In-memory caching for frequently accessed data
- Topic history caching
- Generated content caching

### Performance Features
- Async/await throughout the application
- Connection pooling for external APIs
- Request timeouts and retry logic

## 🛡️ Error Handling

### GraphQL Error Types
```graphql
type Error {
  code: String!
  message: String!
  details: String
}
```

### Common Error Codes
- `LLM_ERROR`: Gemini AI service errors
- `INVALID_API_KEY`: Authentication failures
- `VALIDATION_ERROR`: Input validation failures
- `INTERNAL_ERROR`: Unexpected server errors

### Error Response Pattern
```graphql
union SummarizeResult = SummarizeResponse | Error
```

## 📈 Monitoring and Logging

### Health Monitoring
```graphql
query {
  health {
    status
    message
    version
    timestamp
  }
}
```

### Request Logging
- All GraphQL operations are logged
- Error tracking with stack traces
- Performance metrics collection

## 🔒 Security

### API Key Security
- API keys are validated but not stored
- Secure transmission over HTTPS
- Rate limiting per API key

### Input Validation
- GraphQL schema validation
- Custom field validation
- SQL injection prevention

### CORS Configuration
- Configurable CORS settings
- Secure default settings
- Domain whitelist support

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Support
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 API Documentation

### Interactive Documentation
- GraphQL Explorer with schema browser
- Query and mutation examples
- Real-time testing environment

### Schema Documentation
- Comprehensive type descriptions
- Field-level documentation
- Example usage patterns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Update GraphQL schema if needed
5. Submit a pull request

### Development Guidelines
- Follow GraphQL best practices
- Write comprehensive tests
- Document new schema types
- Use proper error handling

## 🆘 Support

For questions and issues:
- 📚 Interactive docs at `/graphql`
- 🐛 GitHub Issues
- 📧 Direct support contact

## 📄 License

MIT License - see LICENSE file for details.

---

## 🎉 Why GraphQL?

### Advantages over REST
- **Single Endpoint**: One URL for all operations
- **Flexible Queries**: Request exactly what you need
- **Strong Type System**: Built-in validation and documentation
- **Real-time**: Native subscription support
- **Introspection**: Self-documenting API
- **Efficient**: Reduce over-fetching and under-fetching

### Use Cases
- Educational content generation workflows
- Real-time learning progress tracking
- Flexible content querying
- Mobile app backends
- Microservice orchestration

### Perfect for Educational Content
- Complex nested data structures (courses, modules, quizzes)
- Variable content requirements
- Real-time progress updates
- Multiple client applications
- API evolution without versioning
