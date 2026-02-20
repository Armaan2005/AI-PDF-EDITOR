import os
from dotenv import load_dotenv
load_dotenv()


raw_keys = os.getenv("GEMINI_API_KEYS", "")
if raw_keys:
    GEMINI_API_KEYS_LIST = [k.strip() for k in raw_keys.split(",") if k.strip()]
else:
    
    single_key = os.getenv("GEMINI_API_KEY", "")
    GEMINI_API_KEYS_LIST = [single_key] if single_key else []

ALLOWED_IMPORTS = [
    "fitz",
    "math",
    "re",
    "pytesseract", 
    "PIL",         
    "io"           
]
FORBIDDEN_KEYWORDS = [
   
]