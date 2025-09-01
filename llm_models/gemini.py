import google.generativeai as genai
from config.env_config import config
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GeminiModel:
    def __init__(self):
        if not config.GOOGLE_API_KEY:
            raise ValueError("Google API key not found in environment variables")
        
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def generate_plan(self, prompt: str) -> Optional[dict]:
        try:
            logger.info("Generating plan with Gemini")
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=config.TEMPERATURE,
                    max_output_tokens=config.MAX_TOKENS,
                )
            )
            
            response_text = response.text
            logger.info(f"Gemini response length: {len(response_text)}")
            
            # Try to extract JSON from the response
            return self._extract_json(response_text)
            
        except Exception as e:
            logger.error(f"Error generating plan with Gemini: {str(e)}")
            return None
    
    def _extract_json(self, text: str) -> Optional[dict]:
        """Extract JSON from response text"""
        try:
            # Try to find JSON in the response
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = text[start_idx:end_idx]
                return json.loads(json_str)
            
            # If no JSON found, try to parse the entire response
            return json.loads(text)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return None
