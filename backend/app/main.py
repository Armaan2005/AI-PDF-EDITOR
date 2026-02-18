from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

from .llm import generate_code
from .validator import validate_code
from .executor import execute_in_sandbox

app = FastAPI()

@app.post("/process")
async def process_pdf(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    input_path = "input.pdf"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    code = generate_code(prompt)

    validate_code(code)

    output_path = execute_in_sandbox(code)

    return {"status": "success", "output": output_path}