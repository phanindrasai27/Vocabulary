import logging
import os
import json
from groq_provider import GroqProvider

# Configure logger
logger = logging.getLogger(__name__)

class ContentManager:
    def __init__(self, history_path="data/history.json"):
        self.groq_provider = GroqProvider()
        self.history_path = history_path
        self.history = self.load_history()

    def load_history(self):
        """Loads the history of used words from JSON file."""
        if not os.path.exists(self.history_path):
            return []
        
        try:
            with open(self.history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            return []

    def save_history(self):
        """Saves the current history back to JSON."""
        try:
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving history: {e}")

    def get_next_word(self):
        """
        Generates a word using Groq, avoiding history.
        """
        word_data = self.groq_provider.generate_word(self.history)
        if word_data:
            return word_data
        
        logger.error("Groq failed to generate a word.")
        return None

    def mark_as_used(self, word_text):
        """Marks a word as used in the history file."""
        if word_text not in self.history:
            self.history.append(word_text)
            self.save_history()

    def generate_post_text(self, word_data):
        """Formats the tweet content."""
        # Format:
        # WORD
        # Meaning
        # Sentence
        # Domain
        
        return (
            f"{word_data['word'].upper()}\n\n"
            f"ℹ️ {word_data['meaning']}\n\n"
            f"🗣️ “{word_data['sentence']}”\n\n"
            f"🏷️ {word_data['domain']}"
        )

if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    cm = ContentManager()
    print("Generating word with Groq...")
    word = cm.get_next_word()
    if word:
        print(cm.generate_post_text(word))
    else:
        print("Failed to generate word.")
