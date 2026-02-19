import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ALLOWED_IMPORTS = [
    "fitz",
    "math",
    "re"
]
FORBIDDEN_KEYWORDS = [
   
]