
import os
import google.generativeai as genai
import logging
import json
import sys

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.error("❌ MISSING GEMINI_API_KEY! Check your GitHub Secrets.")
        sys.exit(1)

    logger.info(f"Using API Key: {api_key[:4]}...{api_key[-4:]}")

    try:
        genai.configure(api_key=api_key)
        
        # Testing multiple model versions just in case 2.0-flash-exp is the issue
        models_to_try = ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"]
        
        for model_name in models_to_try:
            logger.info(f"--- Testing Model: {model_name} ---")
            try:
                model = genai.GenerativeModel(model_name)
                prompt = "Generate a single JSON for a rare word. word, meaning, sentence, domain."
                
                response = model.generate_content(
                    prompt, 
                    generation_config={"response_mime_type": "application/json"}
                )
                
                logger.info(f"✅ SUCCESS with {model_name}!")
                logger.info(f"Response: {response.text}")
                # If one works, we can stop or keep testing
                break
            except Exception as e:
                logger.warning(f"⚠️ Failed with {model_name}: {e}")
        else:
            logger.error("❌ ALL models failed. This likely means an API Key issue or Region restriction.")
            sys.exit(1)

    except Exception as e:
        logger.error(f"❌ Unexpected error in Gemini Debug: {e}")
        sys.exit(1)

if __name__ == "__main__":
    debug_gemini()
