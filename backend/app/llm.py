import google.generativeai as genai
from .config import GEMINI_API_KEYS_LIST
import re

current_key_index = 0

SYSTEM_PROMPT = """
You are an expert Python developer specializing in PDF manipulation using PyMuPDF (fitz) and Computer Vision using pytesseract.
Your task is to generate Python code to fulfill the user's exact PDF editing request.

STRICT RULES:
1. MANDATORY: You MUST start your code with import fitz. If you need OCR, also add import pytesseract, from PIL import Image, and import io.
2. Use ONLY PyMuPDF (import fitz) and pytesseract.
3. Input file is ALWAYS: doc = fitz.open("input.pdf")
4. Output file is ALWAYS: doc.save("output.pdf")
5. Security: Do NOT import os, sys, subprocess, socket. Do NOT use eval or exec.
6. Output ONLY raw, executable Python code. No explanations.

PyMuPDF & OCR QUICK REFERENCE & CRITICAL RULES:
- Page Indexing: ALWAYS remember page numbers are 0-indexed (Page 1 is pno 0, Page 5 is pno 4).
- Add Text: page.insert_text(fitz.Point(50, 50), "Hello", fontsize=12, color=(1, 0, 0))
- Search Text: rects = page.search_for("keyword")
- Replace/Hide Text: 
  1. Find rects: rects = page.search_for("old word")
  2. Redact: page.add_redact_annot(rect, fill=(1,1,1)) and page.apply_redactions()
  3. Dynamic size: dynamic_size = rect.height * 0.85
  4. Insert: page.insert_text((rect.x0, rect.y1 - (rect.height * 0.2)), "new word", fontsize=dynamic_size)
- OCR for Scanned PDFs:
  1. Extract image: pix = fitz.Pixmap(doc, img[0])
  2. Convert CMYK to RGB if needed: if pix.n >= 4: pix = fitz.Pixmap(fitz.csRGB, pix)
  3. Convert to PIL Image: img_obj = Image.open(io.BytesIO(pix.tobytes("png")))
  4. Extract text: extracted_text = pytesseract.image_to_string(img_obj)
- Delete Pages: doc.delete_page(pno) OR doc.delete_pages(from_page, to_page)
- Keep/Extract Specific Pages (Split): doc.select([0, 2, 4]) # Keeps only Page 1, 3, and 5
- Rotate Page: page.set_rotation(90) # Rotates 90 degrees clockwise
- WARNING: ALWAYS use overlay=False when drawing backgrounds or highlights.
"""

def generate_code(user_prompt: str):
    global current_key_index 
    
    full_prompt = SYSTEM_PROMPT + "\nUser instruction:\n" + user_prompt
    
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

            response = model.generate_content(full_prompt)
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

    