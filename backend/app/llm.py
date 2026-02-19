import google.generativeai as genai
from .config import GEMINI_API_KEY
import re

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """
You are a Python PDF editing assistant.

Strict rules:
- Use ONLY PyMuPDF (import fitz)
- Do NOT import os
- Do NOT import sys
- Do NOT use subprocess
- Do NOT use socket
- Do NOT use eval or exec
- Open file strictly as: fitz.open("input.pdf")
- Save file strictly as: doc.save("output.pdf")
- Do NOT use any file system operations
- Do NOT use absolute paths
- Output ONLY raw Python code
- No explanations
"""

def generate_code(user_prompt: str):
    full_prompt = SYSTEM_PROMPT + "\nUser instruction:\n" + user_prompt

    response = model.generate_content(full_prompt)
    code = response.text.strip()

    # 🔥 Remove triple backticks and language tags
    code = re.sub(r"```.*?\n","",code)
    code = code.replace("```", "")

    # 🔥 Remove standalone 'python' if present
    lines = code.split("\n")
    if lines and lines[0].strip().lower() == "python":
        lines = lines[1:]

    code = "\n".join(lines)

    return code.strip()