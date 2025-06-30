import asyncio
import json
from ariadne import graphql
from main import schema
import pytest

class TestEduBotGraphQLAPI:
    """Test suite for EduBot GraphQL API"""
    
    def setup_method(self):
        """Setup test configuration"""
        self.test_api_key = "test-gemini-api-key-replace-with-real"
        self.context = {}
    
    async def execute_query(self, query, variables=None):
        """Execute GraphQL query"""
        success, result = await graphql(
            schema,
            {"query": query, "variables": variables or {}},
            context_value=self.context
        )
        return success, result
    
    async def test_health_query(self):
        """Test health check query"""
        query = """
        query {
            health {
                status
                message
                version
                timestamp
            }
        }
        """
        
        success, result = await self.execute_query(query)
        assert success
        assert result["data"]["health"]["status"] == "healthy"
        assert "EduBot" in result["data"]["health"]["message"]
    
    async def test_api_info_query(self):
        """Test API info query"""
        query = """
        query {
            apiInfo {
                name
                version
                description
                endpoints
                features
            }
        }
        """
        
        success, result = await self.execute_query(query)
        assert success
        assert "EduBot" in result["data"]["apiInfo"]["name"]
        assert len(result["data"]["apiInfo"]["features"]) > 0
    
    async def test_topics_query(self):
        """Test topics query"""
        query = """
        query {
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
        """
        
        success, result = await self.execute_query(query)
        assert success
        assert isinstance(result["data"]["topics"]["topics"], list)
        assert isinstance(result["data"]["topics"]["total"], int)
    
    async def test_summarize_mutation(self):
        """Test summarize mutation"""
        query = """
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
        """
        
        variables = {
            "input": {
                "text": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed.",
                "api_key": self.test_api_key,
                "max_length": 50
            }
        }
        
        success, result = await self.execute_query(query, variables)
        assert success
        
        # With test API key, this will likely return an error
        # In real testing, use valid API key
        if "summary" in result["data"]["summarize"]:
            assert len(result["data"]["summarize"]["summary"]) > 0
        else:
            # Expected with test API key
            assert result["data"]["summarize"]["code"] == "LLM_ERROR"
    
    async def test_explain_mutation(self):
        """Test explain mutation"""
        query = """
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
        """
        
        variables = {
            "input": {
                "concept": "Neural Networks",
                "api_key": self.test_api_key,
                "level": "BEGINNER"
            }
        }
        
        success, result = await self.execute_query(query, variables)
        assert success
        
        # Check if we got a response or error
        if "explanation" in result["data"]["explain"]:
            assert result["data"]["explain"]["concept"] == "Neural Networks"
            assert result["data"]["explain"]["level"] == "BEGINNER"
        else:
            assert result["data"]["explain"]["code"] == "LLM_ERROR"
    
    async def test_quiz_mutation(self):
        """Test quiz generation mutation"""
        query = """
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
        """
        
        variables = {
            "input": {
                "topic": "Python Programming",
                "api_key": self.test_api_key,
                "num_questions": 3,
                "difficulty": "EASY"
            }
        }
        
        success, result = await self.execute_query(query, variables)
        assert success
        
        if "questions" in result["data"]["generateQuiz"]:
            assert len(result["data"]["generateQuiz"]["questions"]) <= 3
            assert result["data"]["generateQuiz"]["difficulty"] == "EASY"
        else:
            assert result["data"]["generateQuiz"]["code"] == "LLM_ERROR"
    
    async def test_educate_mutation(self):
        """Test complete education content generation"""
        query = """
        mutation GenerateEducationalContent($input: EducateInput!) {
            educate(input: $input) {
                ... on EducateResponse {
                    topic
                    generated_at
                    provider_used
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
        """
        
        variables = {
            "input": {
                "topic": "Introduction to GraphQL",
                "api_key": self.test_api_key,
                "modules_count": 3,
                "include_pdf": False
            }
        }
        
        success, result = await self.execute_query(query, variables)
        assert success
        
        if "topic" in result["data"]["educate"]:
            assert result["data"]["educate"]["topic"] == "Introduction to GraphQL"
            assert len(result["data"]["educate"]["modules"]) <= 3
        else:
            assert result["data"]["educate"]["code"] == "LLM_ERROR"
    
    async def test_invalid_input_validation(self):
        """Test input validation"""
        query = """
        mutation SummarizeText($input: SummarizeInput!) {
            summarize(input: $input) {
                ... on SummarizeResponse {
                    summary
                }
                ... on Error {
                    code
                    message
                }
            }
        }
        """
        
        # Test with missing required field
        variables = {
            "input": {
                "text": "Test text"
                # Missing api_key
            }
        }
        
        success, result = await self.execute_query(query, variables)
        # Should fail validation
        assert not success or "errors" in result
    
    async def test_topic_by_id_query(self):
        """Test getting specific topic by ID"""
        query = """
        query GetTopic($topicId: ID!) {
            topic(id: $topicId) {
                id
                topic
                created_at
                provider_used
                modules_count
            }
        }
        """
        
        variables = {
            "topicId": "non-existent-id"
        }
        
        success, result = await self.execute_query(query, variables)
        assert success
        assert result["data"]["topic"] is None


async def run_tests():
    """Run all tests"""
    test_instance = TestEduBotGraphQLAPI()
    
    print("🧪 Running EduBot GraphQL API Tests...")
    
    tests = [
        ("Health Check", test_instance.test_health_query),
        ("API Info", test_instance.test_api_info_query),
        ("Topics Query", test_instance.test_topics_query),
        ("Summarize Mutation", test_instance.test_summarize_mutation),
        ("Explain Mutation", test_instance.test_explain_mutation),
        ("Quiz Mutation", test_instance.test_quiz_mutation),
        ("Educate Mutation", test_instance.test_educate_mutation),
        ("Input Validation", test_instance.test_invalid_input_validation),
        ("Topic by ID", test_instance.test_topic_by_id_query),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            await test_func()
            print(f"✅ {test_name}: PASSED")
            passed += 1
        except Exception as e:
            print(f"❌ {test_name}: FAILED - {str(e)}")
            failed += 1
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check API key configuration and Gemini service availability.")


if __name__ == "__main__":
    asyncio.run(run_tests())
