import math
import re

class IntentClassifier:
    """
    Advanced Intent Classification using Bag-of-Words and Cosine Similarity (Simulated).
    """
    def __init__(self):
        # Define known intents and their associated keywords/training phrases
        self.intents = {
            'dashboard': [
                "dashboard", "analytics", "admin", "charts", "graphs", "sidebar", "overview", "stats", "metrics", "panel", "console"
            ],
            'login': [
                "login", "sign in", "signin", "authentication", "register", "signup", "password", "email", "auth", "account"
            ],
            'form': [
                "form", "contact", "input", "message", "feedback", "submit", "survey", "questionnaire", "inputs"
            ],
            'landing': [
                "landing", "home", "website", "hero", "marketing", "product", "features", "pricing", "showcase", "startup", "saas", "footer", "how it works", "get started", "sections"
            ],
            'portfolio': [
                "portfolio", "resume", "cv", "personal", "profile", "projects", "work", "developer", "designer", "showcase"
            ],
            'ecommerce': [
                "ecommerce", "shop", "store", "product", "cart", "buy", "sell", "checkout", "marketplace", "retail"
            ],
            'generic': [
                "app", "site", "platform", "page", "section", "view", "component", "interface", "web app", "application"
            ]
        }
        
    def _tokenize(self, text):
        # Simple tokenization: lowercase and remove non-alphanumeric
        cleaned = re.sub(r'[^a-z0-9\s]', '', text.lower())
        return set(cleaned.split())

    def _calculate_overlap(self, tokens, keywords):
        # Calculate Intersection over Union (IoU) or simple overlap count
        keyword_set = set(keywords)
        intersection = tokens.intersection(keyword_set)
        return len(intersection)

    def predict(self, prompt):
        tokens = self._tokenize(prompt)
        scores = {}
        
        for intent, keywords in self.intents.items():
            score = self._calculate_overlap(tokens, keywords)
            scores[intent] = score
        
        # Get intent with max score
        best_intent = max(scores, key=scores.get)
        
        if scores[best_intent] == 0:
            return 'generic'
            
        return best_intent

class StyleExtractor:
    """
    Named Entity Recognition (NER) for style attributes.
    """
    def __init__(self):
        self.colors = ['blue', 'red', 'green', 'purple', 'orange', 'gray', 'black']
        
    def extract_brand_name(self, prompt):
        # Heuristic: Find text after "called" or "named"
        match = re.search(r'(?:called|named|brand)\s+["\']?([^"\']+)["\']?', prompt, re.IGNORECASE)
        if match:
            return match.group(1)
        return "Ryze AI"

    def extract_primary_color(self, prompt):
        tokens = prompt.lower().split()
        for color in self.colors:
            if color in tokens:
                return color
        return 'blue' # Default

# Singleton instance
classifier = IntentClassifier()
style_extractor = StyleExtractor()
