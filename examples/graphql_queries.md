# EduBot GraphQL API - Example Queries and Mutations

## Health Check Query
```graphql
query HealthCheck {
  health {
    status
    message
    version
    timestamp
  }
}
```

## Get API Information
```graphql
query GetAPIInfo {
  apiInfo {
    name
    version
    description
    endpoints
    features
  }
}
```

## Get All Topics
```graphql
query GetAllTopics {
  topics {
    topics {
      id
      topic
      created_at
      provider_used
      modules_count
    }
    total
  }
}
```

## Get Specific Topic
```graphql
query GetTopic($topicId: ID!) {
  topic(id: $topicId) {
    id
    topic
    created_at
    provider_used
    modules_count
  }
}
```

## Summarize Text
```graphql
mutation SummarizeText($input: SummarizeInput!) {
  summarize(input: $input) {
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

# Variables:
{
  "input": {
    "text": "Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines that work and react like humans. Some of the activities computers with artificial intelligence are designed for include speech recognition, learning, planning, and problem-solving. AI is being used in various fields such as healthcare, finance, transportation, and entertainment. Machine learning, a subset of AI, enables computers to learn and improve from experience without being explicitly programmed.",
    "api_key": "your-gemini-api-key-here",
    "max_length": 100
  }
}
```

## Explain Concept
```graphql
mutation ExplainConcept($input: ExplainInput!) {
  explain(input: $input) {
    ... on ExplainResponse {
      explanation
      concept
      level
      provider_used
    }
    ... on Error {
      code
      message
      details
    }
  }
}

# Variables:
{
  "input": {
    "concept": "Machine Learning",
    "api_key": "your-gemini-api-key-here",
    "level": "BEGINNER"
  }
}
```

## Generate Quiz
```graphql
mutation GenerateQuiz($input: QuizInput!) {
  generateQuiz(input: $input) {
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
      provider_used
    }
    ... on Error {
      code
      message
      details
    }
  }
}

# Variables:
{
  "input": {
    "topic": "Python Programming Basics",
    "api_key": "your-gemini-api-key-here",
    "num_questions": 5,
    "difficulty": "MEDIUM"
  }
}
```

## Generate Complete Educational Content
```graphql
mutation GenerateEducationalContent($input: EducateInput!) {
  educate(input: $input) {
    ... on EducateResponse {
      topic
      generated_at
      provider_used
      pdf_url
      syllabus {
        topic
        overview
        modules {
          title
          description
        }
        total_duration
        learning_objectives
      }
      modules {
        title
        description
        content
        key_points
        estimated_duration
      }
      quiz {
        questions {
          question
          options
          correct_answer
          explanation
        }
        difficulty
        total_questions
      }
    }
    ... on Error {
      code
      message
      details
    }
  }
}

# Variables:
{
  "input": {
    "topic": "Introduction to Data Science",
    "api_key": "your-gemini-api-key-here",
    "modules_count": 4,
    "include_pdf": true
  }
}
```

## Subscribe to Content Generation Progress (Optional)
```graphql
subscription ContentGenerationProgress($topic: String!) {
  contentGeneration(topic: $topic) {
    step
    progress
    message
    completed
  }
}

# Variables:
{
  "topic": "Machine Learning Basics"
}
```

## Advanced Query with Multiple Operations
```graphql
query DashboardData {
  health {
    status
    version
  }
  topics {
    total
    topics {
      id
      topic
      created_at
    }
  }
  apiInfo {
    name
    features
  }
}
```

## Mutation with Error Handling
```graphql
mutation GenerateContentWithErrorHandling($input: EducateInput!) {
  educate(input: $input) {
    ... on EducateResponse {
      topic
      provider_used
      syllabus {
        overview
        learning_objectives
      }
    }
    ... on Error {
      code
      message
      details
    }
  }
}
```

## Query Variables Examples

### For Text Summarization:
```json
{
  "input": {
    "text": "Cloud computing is the delivery of computing services including servers, storage, databases, networking, software, analytics, and intelligence over the Internet to offer faster innovation, flexible resources, and economies of scale.",
    "api_key": "your-gemini-api-key",
    "max_length": 80
  }
}
```

### For Concept Explanation:
```json
{
  "input": {
    "concept": "Neural Networks",
    "api_key": "your-gemini-api-key",
    "level": "ADVANCED"
  }
}
```

### For Quiz Generation from Text:
```json
{
  "input": {
    "text": "The water cycle is the continuous movement of water on, above, and below the surface of the Earth. The water cycle involves the exchange of energy, which leads to temperature changes.",
    "api_key": "your-gemini-api-key",
    "num_questions": 3,
    "difficulty": "EASY"
  }
}
```

### For Educational Content Generation:
```json
{
  "input": {
    "topic": "Fundamentals of Web Development",
    "api_key": "your-gemini-api-key",
    "modules_count": 6,
    "include_pdf": false
  }
}
```
