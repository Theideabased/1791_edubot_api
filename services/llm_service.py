import google.generativeai as genai
import asyncio
from typing import Dict, Any
from utils.exceptions import LLMProviderError, InvalidAPIKeyError

class LLMService:
    """Service class to handle Google Gemini LLM provider"""
    
    def __init__(self):
        self.provider = "gemini"
    
    async def generate_content(self, api_key: str, prompt: str, system_prompt: str = None) -> str:
        """Generate content using Google Gemini"""
        try:
            return await self._call_gemini(api_key, prompt, system_prompt)
        except Exception as e:
            if "invalid" in str(e).lower() or "unauthorized" in str(e).lower():
                raise InvalidAPIKeyError(f"Invalid API key for Gemini")
            raise LLMProviderError(f"Error calling Gemini: {str(e)}")
    
    async def _call_gemini(self, api_key: str, prompt: str, system_prompt: str = None) -> str:
        """Call Google Gemini API"""
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = await asyncio.get_event_loop().run_in_executor(
                None, model.generate_content, full_prompt
            )
            
            if response.text:
                return response.text
            else:
                raise LLMProviderError("Empty response from Gemini")
                
        except Exception as e:
            if "API_KEY_INVALID" in str(e) or "invalid" in str(e).lower():
                raise InvalidAPIKeyError("Invalid Gemini API key")
            raise LLMProviderError(f"Gemini API error: {str(e)}")

# Singleton instance
llm_service = LLMService()
