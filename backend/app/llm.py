import google.generativeai as genai
from config import GEMINI_API_KEYS_LIST
import re

current_key_index = 0

SYSTEM_PROMPT = """
You are an expert Python developer specializing in PDF manipulation using PyMuPDF (fitz).
You have VISION capabilities: You can see the actual PDF file provided to you. Use this to identify exact text, layout, and colors.
STRICT RULES:
1. MANDATORY: Start your code with 'import fitz'. 
2. INPUT/OUTPUT: Source is always 'input.pdf', output must be 'output.pdf'.
3. ACCURACY: Use your vision to find the exact strings for page.search_for(). Do not guess.
4. SUMMARIZATION: If the user asks to summarize, generate a concise summary of the PDF and write code to insert it into a NEW page (doc.new_page()) using page.insert_textbox().
5. FORMATTING: Use colors and font sizes that match the document's style.
6. SECURITY: Do NOT import os, sys, subprocess, or use eval/exec.
7. OUTPUT: Return ONLY raw, executable Python code. No text before or after the code block.
PyMuPDF QUICK REF:
- Search: rects = page.search_for("exact text from vision")
- Redact & Replace: page.add_redact_annot(rect, fill=(1,1,1)); page.apply_redactions(); page.insert_text(rect.tl, "new text")
- New Page: page = doc.new_page()
- Textbox: page.insert_textbox(rect, "text content", fontsize=10)
"""
def generate_code(user_prompt: str, pdf_file=None): 
    global current_key_index 
    
    
    prompt_parts = [
        SYSTEM_PROMPT,
        "\n--- PDF ANALYSIS ---\nHere is the actual PDF file for your reference. Use it to understand the layout, colors, and content.",
        pdf_file if pdf_file else "No PDF file provided.", 
        f"\nUser instruction: {user_prompt}"
    ]
    
    if not GEMINI_API_KEYS_LIST:
        raise ValueError("API Keys nahi mili! Please check .env file.")

    total_keys = len(GEMINI_API_KEYS_LIST)
    attempts = 0
    code = ""

   

    
    while attempts < total_keys:
        try:
            current_key = GEMINI_API_KEYS_LIST[current_key_index]
            genai.configure(api_key=current_key)
            
            
            model = genai.GenerativeModel("gemini-2.5-flash")

            response = model.generate_content(prompt_parts)
            code = response.text.strip()
            
            print(f" Success with API Key Index: {current_key_index}")
            break 

        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Quota" in error_msg or "exhausted" in error_msg.lower():
                print(f" Key index {current_key_index} ki limit khatam. Switching to next key...")
                current_key_index = (current_key_index + 1) % total_keys
                attempts += 1
            else:
                print(f" API Error (Not Quota limit): {error_msg}")
                raise e

    if attempts == total_keys:
        raise Exception("429 Quota Exceeded: Bhai, saari API keys ki limit khatam ho gayi hai!")

    
    code = re.sub(r"^```python\n", "", code, flags=re.IGNORECASE)
    code = re.sub(r"^```\n","",code)
    code = re.sub(r"```$","",code)

    lines = code.split("\n")
    if lines and lines[0].strip().lower() == "python":
        lines = lines[1:]
    

    code = "\n".join(lines)
    if "import fitz" not in code:
        code = "import fitz\n" + code

    return code.strip()
