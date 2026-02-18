import re
from .config import FORBIDDEN_KEYWORDS

def validate_code(code: str):
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", code):
            raise Exception(f"Forbidden keyword detected: {keyword}")

    if "import fitz" not in code:
        raise Exception("fitz import required")

    return True