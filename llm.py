import json
from dotenv import load_dotenv
import os

load_dotenv()

def run_llm(recipe_text):

    # temporary dummy output
    data = {
        "title": "Sample Recipe",
        "cuisine": "Unknown",
        "difficulty": "easy"
    }

    return data