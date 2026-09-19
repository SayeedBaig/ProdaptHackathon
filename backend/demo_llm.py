import sys
import os
import asyncio

# Ensure app is importable
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from app.ai.providers.openrouter import OpenRouterProvider

async def demo_llm_engine():
    print("Initializing PitchPilot LLM Engine (OpenRouter/DeepSeek V4 Flash)...")
    provider = OpenRouterProvider()
    
    prompt = """
    You are PitchPilot AI. 
    Return a strictly valid JSON object with the following keys:
    - "status": string (say "Operational")
    - "message": string (a short greeting to the Hackathon Judges)
    """
    
    print("Sending prompt to LLM...")
    try:
        response = await provider.complete_json(prompt, timeout=30)
        print("\nReceived Valid JSON Response from LLM:")
        print(response)
    except Exception as e:
        print(f"\nLLM Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(demo_llm_engine())
