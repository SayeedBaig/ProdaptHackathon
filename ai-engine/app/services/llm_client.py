import os
import json
import logging
from typing import Type, TypeVar, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

T = TypeVar('T', bound=BaseModel)

logger = logging.getLogger("ai_engine.llm_client")

class LLMClient:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.use_mock = os.getenv("USE_MOCK_LLM", "false").lower() in ("true", "1", "yes")

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        system_instruction: Optional[str] = None,
        mock_generator_fn: Optional[callable] = None
    ) -> T:
        """
        Generates structured response matching response_model Pydantic class.
        Uses Gemini API or OpenAI API if keys are present, else falls back to mock_generator_fn.
        """
        if self.use_mock or (not self.gemini_key and not self.openai_key):
            logger.info("Using mock response generator for structured output")
            if mock_generator_fn:
                return mock_generator_fn()
            else:
                raise ValueError("Mock LLM enabled but no mock_generator_fn provided.")

        # Try Gemini API if key available
        if self.gemini_key:
            try:
                from google import genai
                from google.genai import types
                client = genai.Client(api_key=self.gemini_key)
                full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
                # Try modern model names (gemini-2.0-flash or gemini-1.5-flash)
                model_name = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash")
                response = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=response_model,
                    ),
                )
                return response_model.model_validate_json(response.text)
            except Exception as e:
                logger.warning(f"Gemini API call failed: {e}. Falling back to mock generator if available.")
                if mock_generator_fn:
                    return mock_generator_fn()
                raise e

        # Try OpenAI API if key available
        if self.openai_key:
            try:
                import openai
                client = openai.OpenAI(api_key=self.openai_key)
                messages = []
                if system_instruction:
                    messages.append({"role": "system", "content": system_instruction})
                messages.append({"role": "user", "content": prompt})

                response = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=messages,
                    response_format=response_model,
                )
                return response.choices[0].message.parsed
            except Exception as e:
                logger.warning(f"OpenAI API call failed: {e}. Falling back to mock generator if available.")
                if mock_generator_fn:
                    return mock_generator_fn()
                raise e

        if mock_generator_fn:
            return mock_generator_fn()
        raise RuntimeError("No LLM provider available and no mock generator provided.")

llm_client = LLMClient()
