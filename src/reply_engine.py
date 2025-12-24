
import random
import re

class ReplyEngine:
    def __init__(self):
        # A simple mapping of "overcomplicated" or "jargon" words to simpler alternatives
        self.replacements = {
            "utilize": "use",
            "leverage": "use",
            "facilitate": "help",
            "exacerbate": "worsen",
            "ameliorate": "improve",
            "optimal": "best",
            "cognizant": "aware",
            "paradigm shift": "change",
            "synergy": "teamwork",
            "bandwidth": "time/energy",
            "bottom line": "result",
            "deep dive": "look closer",
            "circle back": "return",
            "loop in": "include"
        }
        
        self.templates = [
            "Why say '{complex}' when '{simple}' works just as well?",
            "'{simple}' is the word you're looking for. It's punchier than '{complex}'.",
            "Brevity is wit. Try '{simple}' instead of '{complex}'.",
            "Cut the fluff: '{complex}' -> '{simple}'.",
        ]

    def analyze_text(self, text):
        """
        Scans text for trigger words.
        Returns a tuple (found_word, suggested_replacement) or None.
        """
        # clean text to lower case for matching
        lower_text = text.lower()
        
        for complex_word, simple_word in self.replacements.items():
            # Check for the word with word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(complex_word) + r'\b'
            if re.search(pattern, lower_text):
                return complex_word, simple_word
        
        return None

    def generate_reply(self, found_word, suggestion):
        """Generates a witty reply based on the found word."""
        template = random.choice(self.templates)
        return template.format(complex=found_word, simple=suggestion)

# Example usage
if __name__ == "__main__":
    engine = ReplyEngine()
    test_text = "We need to leverage our synergy to facilitate growth."
    result = engine.analyze_text(test_text)
    if result:
        print(engine.generate_reply(*result))
    else:
        print("No jargon found.")
