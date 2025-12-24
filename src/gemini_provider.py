
import os
import json
import logging
import google.generativeai as genai
from datetime import datetime

logger = logging.getLogger(__name__)

class GeminiProvider:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        else:
            logger.warning("GEMINI_API_KEY not found. GeminiProvider will fail unless mocked.")
            self.model = None

    def generate_word(self, history_list):
        """
        Generates a specific JSON object for a new vocabulary word.
        Excludes words in `history_list`.
        Uses dynamic themes to ensure variety and context.
        """
        if not self.model:
            logger.error("Cannot generate word: No API Key.")
            return None

        # Themes to rotate for variety
        import random
        themes = [
            "Current Tech News & AI (e.g. Hallucination, Alignment)",
            "Modern Corporate Work Life (e.g. Boilerplate, Bandwidth)",
            "Internet Culture & Memes (e.g. Cringe, Based, ratio)",
            "Psychology & Emotions (e.g. Imposter Syndrome, Burnout)",
            "Global Affairs & Politics (e.g. Brinkmanship, Sanctions)",
            "Philosophy of Modern Life (e.g. Ennui, Angst)"
        ]
        selected_theme = random.choice(themes)

        prompt = f"""
        You are a witty, sophisticated vocabulary assistant.
        Target Audience: Smart professionals and internet-native users.
        
        Task: Pick a "trendy, rare, or contextually specific" word that fits the theme: **{selected_theme}**.
        
        Constraints:
        1. The word must NOT be in this list: {json.dumps(history_list[-100:])} (checking last 100).
        2. The word should be sophisticated yet useful. It can be a neologism if it's widely accepted (e.g. 'Enshittification').
        3. Do NOT use extremely common words.
        
        Output format (JSON only, no markdown):
        {{
            "word": "TheWord",
            "meaning": "A short, sharp, witty definition (max 15 words). Avoiding dictionary speak.",
            "sentence": "A natural sentence showing how to use it in a tweet or casual conversation.",
            "domain": "The theme/category (e.g. Tech, Meme Theory, Work)."
        }}
        """

        try:
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            text = response.text.strip()
            
            # Clean potential markdown wrapping if API doesn't enforce strict JSON (though response_mime_type should)
            if text.startswith("```json"):
                text = text[7:-3]
            
            data = json.loads(text)
            
            # Validate keys
            required_keys = ["word", "meaning", "sentence", "domain"]
            if all(key in data for key in required_keys):
                return data
            else:
                logger.error(f"Gemini returned invalid JSON structure: {data.keys()}")
                return None
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {e}")
            return None
