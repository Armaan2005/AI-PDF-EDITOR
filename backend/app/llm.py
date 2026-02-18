from openai import OpenAI
from .config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a professional PDF automation Python expert.
Generate ONLY safe Python code.
Use ONLY PyMuPDF (fitz).
Never use os, sys, subprocess, socket, eval, exec, or file operations.
Input file is 'input.pdf'
Output file must be 'output.pdf'
Do not explain anything. Only return Python code.
"""

def generate_code(user_prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content