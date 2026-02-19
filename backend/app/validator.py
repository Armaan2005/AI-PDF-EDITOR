import re
from .config import FORBIDDEN_KEYWORDS

def validate_code(code: str):

    for keyword in FORBIDDEN_KEYWORDS:
        pattern = re.escape(keyword)   # 🔥 Important
        if re.search(pattern, code):
            raise Exception(f"Forbidden keyword detected: {keyword}")

    return True