
import os
import json
import logging
import random
from groq import Groq

logger = logging.getLogger(__name__)

class GroqProvider:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
            self.model = "llama-3.3-70b-versatile"
        else:
            logger.error("❌ GROQ_API_KEY not found in environment variables.")
            self.client = None

    def generate_word(self, history_list):
        """
        Generates a vocabulary word using Groq (Llama 3).
        """
        if not self.client:
            return None

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
        Pick a "trendy, rare, or contextually specific" word that fits the theme: **{selected_theme}**.
        
        Constraints:
        1. The word must NOT be in this list: {json.dumps(history_list[-100:])}.
        2. The word should be sophisticated but useful.
        3. Do NOT use common words.
        
        Output MUST be valid JSON only:
        {{
            "word": "TheWord",
            "meaning": "Short, sharp, witty definition (max 15 words).",
            "sentence": "A natural sentence for a tweet.",
            "domain": "The category (e.g. Tech, Meme Theory, Work)."
        }}
        """

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {{"role": "user", "content": prompt}}
                ],
                response_format={{"type": "json_object"}}
            )
            
            content = completion.choices[0].message.content
            data = json.loads(content)
            
            # Basic validation
            required = ["word", "meaning", "sentence", "domain"]
            if all(k in data for k in required):
                return data
            return None
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return None
