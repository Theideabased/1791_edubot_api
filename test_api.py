#!/usr/bin/env python3
"""
EduBot API Test Script
Simple test script to verify all endpoints are working correctly.
"""

import requests
import json
import time
import os

# Configuration
BASE_URL = "http://localhost:8000"
TEST_API_KEY = "test-key-replace-with-real-key"

# Test data
TEST_TEXT = """
Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines 
that work and react like humans. Some of the activities computers with artificial intelligence are 
designed for include speech recognition, learning, planning, and problem-solving. AI is being used 
in various fields such as healthcare, finance, transportation, and entertainment. Machine learning, 
a subset of AI, enables computers to learn and improve from experience without being explicitly programmed.
"""

TEST_CONCEPT = "Neural Networks"
TEST_TOPIC = "Introduction to Python Programming"

def test_endpoint(method, endpoint, data=None, description=""):
    """Test an API endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"   {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Success")
            if len(response.text) > 200:
                print(f"   Response preview: {response.text[:200]}...")
            else:
                print(f"   Response: {response.text}")
        else:
            print("   ❌ Failed")
            print(f"   Error: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🤖 EduBot API Test Suite")
    print("=" * 40)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Server is not running or not healthy")
            return
    except:
        print("❌ Cannot connect to server. Make sure it's running on localhost:8000")
        return
    
    print("✅ Server is running and healthy")
    
    # Test basic endpoints
    test_endpoint("GET", "/", description="Root endpoint")
    test_endpoint("GET", "/health", description="Health check")
    test_endpoint("GET", "/api/v1/topics", description="Get topics")
    
    # Note: The following tests require valid API keys
    print("\n" + "=" * 40)
    print("⚠️  The following tests require valid API keys")
    print("   Replace TEST_API_KEY with a real API key to test")
    print("=" * 40)
    
    # Test summarize endpoint
    summarize_data = {
        "text": TEST_TEXT,
        "provider": "openai",
        "api_key": TEST_API_KEY,
        "max_length": 100
    }
    test_endpoint("POST", "/api/v1/summarize", summarize_data, "Summarize text")
    
    # Test explain endpoint
    explain_data = {
        "concept": TEST_CONCEPT,
        "level": "beginner",
        "provider": "openai",
        "api_key": TEST_API_KEY
    }
    test_endpoint("POST", "/api/v1/explain", explain_data, "Explain concept")
    
    # Test quiz endpoint
    quiz_data = {
        "topic": TEST_TOPIC,
        "provider": "openai",
        "api_key": TEST_API_KEY,
        "num_questions": 3,
        "difficulty": "medium"
    }
    test_endpoint("POST", "/api/v1/quiz", quiz_data, "Generate quiz")
    
    # Test educate endpoint (this might take longer)
    educate_data = {
        "topic": "Machine Learning Basics",
        "provider": "openai",
        "api_key": TEST_API_KEY,
        "modules_count": 3,
        "include_pdf": False
    }
    test_endpoint("POST", "/api/v1/educate", educate_data, "Generate education content")
    
    print("\n" + "=" * 40)
    print("🎉 Test suite completed!")
    print("   Visit http://localhost:8000/docs for interactive testing")
    print("=" * 40)

if __name__ == "__main__":
    main()
