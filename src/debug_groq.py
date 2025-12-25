
import os
import json
import logging
import sys
from groq import Groq

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_groq():
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        logger.error("❌ MISSING GROQ_API_KEY! Check your GitHub Secrets.")
        sys.exit(1)

    logger.info(f"Using Groq API Key: {api_key[:4]}...{api_key[-4:]}")

    try:
        client = Groq(api_key=api_key)
        model = "llama-3.3-70b-versatile"
        
        logger.info(f"--- Testing Groq Model: {model} ---")
        prompt = "Generate a single JSON for a rare word. include word, meaning, sentence, and domain."
        
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = completion.choices[0].message.content
        logger.info(f"✅ SUCCESS with Groq!")
        logger.info(f"Response: {content}")
        
    except Exception as e:
        logger.error(f"❌ Groq Debug Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    debug_groq()
