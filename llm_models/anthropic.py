import anthropic
from config.env_config import config
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AnthropicModel:
    def __init__(self):
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("Anthropic API key not found in environment variables")
        
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        
    async def generate_plan(self, prompt: str) -> Optional[dict]:
        try:
            logger.info("Generating plan with Anthropic Claude")
            
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            response_text = response.content[0].text
            logger.info(f"Anthropic response length: {len(response_text)}")
            
            return self._extract_json(response_text)
            
        except Exception as e:
            logger.error(f"Error generating plan with Anthropic: {str(e)}")
            return None
    
    def _extract_json(self, text: str) -> Optional[dict]:
        """Extract JSON from response text"""
        try:
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = text[start_idx:end_idx]
                return json.loads(json_str)
            
            return json.loads(text)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return None
