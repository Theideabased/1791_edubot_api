#!/usr/bin/env python3
"""
EduBot API Example Usage
Demonstrates how to use the EduBot API with real examples.
"""

import requests
import json
import time

class EduBotClient:
    """Simple client for EduBot API"""
    
    def __init__(self, base_url="http://localhost:8000", api_key=None, provider="openai"):
        self.base_url = base_url
        self.api_key = api_key
        self.provider = provider
    
    def summarize(self, text, max_length=150):
        """Summarize text"""
        data = {
            "text": text,
            "provider": self.provider,
            "api_key": self.api_key,
            "max_length": max_length
        }
        response = requests.post(f"{self.base_url}/api/v1/summarize", json=data)
        return response.json()
    
    def explain(self, concept, level="intermediate"):
        """Explain a concept"""
        data = {
            "concept": concept,
            "level": level,
            "provider": self.provider,
            "api_key": self.api_key
        }
        response = requests.post(f"{self.base_url}/api/v1/explain", json=data)
        return response.json()
    
    def generate_quiz(self, topic=None, text=None, num_questions=5, difficulty="medium"):
        """Generate a quiz"""
        data = {
            "provider": self.provider,
            "api_key": self.api_key,
            "num_questions": num_questions,
            "difficulty": difficulty
        }
        
        if topic:
            data["topic"] = topic
        if text:
            data["text"] = text
            
        response = requests.post(f"{self.base_url}/api/v1/quiz", json=data)
        return response.json()
    
    def create_course(self, topic, modules_count=5, include_pdf=False):
        """Create complete educational content"""
        data = {
            "topic": topic,
            "provider": self.provider,
            "api_key": self.api_key,
            "modules_count": modules_count,
            "include_pdf": include_pdf
        }
        response = requests.post(f"{self.base_url}/api/v1/educate", json=data)
        return response.json()
    
    def get_topics(self):
        """Get saved topics"""
        response = requests.get(f"{self.base_url}/api/v1/topics")
        return response.json()

def demo_basic_usage():
    """Demonstrate basic API usage"""
    print("🤖 EduBot API Demo")
    print("=" * 50)
    
    # Initialize client (replace with your API key)
    api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    if not api_key:
        print("⚠️  Skipping API calls (no API key provided)")
        return
    
    client = EduBotClient(api_key=api_key, provider="openai")
    
    # Example 1: Summarize text
    print("\n📝 Example 1: Text Summarization")
    print("-" * 30)
    
    sample_text = """
    The Internet of Things (IoT) refers to the network of physical objects embedded with sensors, 
    software, and other technologies to connect and exchange data over the internet. IoT devices 
    can range from ordinary household objects to sophisticated industrial tools. These devices 
    collect and share data, enabling automation and intelligent decision-making. IoT applications 
    span various sectors including smart homes, healthcare, agriculture, transportation, and 
    smart cities. However, IoT also presents challenges such as security vulnerabilities, 
    privacy concerns, and the need for robust infrastructure.
    """
    
    try:
        result = client.summarize(sample_text, max_length=80)
        print(f"Original length: {len(sample_text.split())} words")
        print(f"Summary: {result.get('summary', 'Failed to generate summary')}")
        print(f"Summary length: {result.get('summary_length', 0)} words")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Explain a concept
    print("\n🧠 Example 2: Concept Explanation")
    print("-" * 30)
    
    try:
        result = client.explain("Blockchain Technology", level="beginner")
        print(f"Concept: Blockchain Technology")
        print(f"Level: Beginner")
        print(f"Explanation: {result.get('explanation', 'Failed to generate explanation')[:300]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Generate quiz
    print("\n❓ Example 3: Quiz Generation")
    print("-" * 30)
    
    try:
        result = client.generate_quiz(topic="Python Programming", num_questions=3, difficulty="easy")
        print(f"Topic: Python Programming")
        print(f"Questions generated: {result.get('total_questions', 0)}")
        
        questions = result.get('questions', [])
        for i, q in enumerate(questions[:2], 1):  # Show first 2 questions
            print(f"\nQuestion {i}: {q.get('question', '')}")
            options = q.get('options', [])
            for j, option in enumerate(options):
                print(f"  {chr(65+j)}. {option}")
            print(f"Correct answer: {chr(65+q.get('correct_answer', 0))}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Create mini course
    print("\n🎓 Example 4: Mini Course Creation")
    print("-" * 30)
    
    course_topic = input("Enter a topic for a mini course (or press Enter for default): ").strip()
    if not course_topic:
        course_topic = "Web Development Fundamentals"
    
    try:
        print(f"Creating course: {course_topic}")
        print("⏳ This may take a minute...")
        
        result = client.create_course(course_topic, modules_count=3, include_pdf=False)
        
        print(f"✅ Course created successfully!")
        print(f"Topic: {result.get('topic', '')}")
        
        syllabus = result.get('syllabus', {})
        print(f"Overview: {syllabus.get('overview', '')[:200]}...")
        print(f"Total modules: {len(result.get('modules', []))}")
        print(f"Quiz questions: {result.get('quiz', {}).get('total_questions', 0)}")
        
        modules = result.get('modules', [])
        if modules:
            print(f"\nFirst module: {modules[0].get('title', '')}")
            print(f"Duration: {modules[0].get('estimated_duration', '')}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Show saved topics
    print("\n📚 Saved Topics")
    print("-" * 30)
    
    try:
        topics = client.get_topics()
        total_topics = topics.get('total', 0)
        print(f"Total saved topics: {total_topics}")
        
        for topic in topics.get('topics', [])[:3]:  # Show first 3
            print(f"- {topic.get('topic', '')} ({topic.get('provider_used', '')})")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("Visit http://localhost:8000/docs for interactive API documentation")
    print("=" * 50)

if __name__ == "__main__":
    demo_basic_usage()
