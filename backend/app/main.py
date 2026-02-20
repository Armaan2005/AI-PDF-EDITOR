from fastapi.responses import FileResponse
from fastapi import FastAPI,UploadFile,File,Form
from .llm import generate_code
from .validator import validate_code
from .executor import execute_in_sandbox
import uuid
import os
import shutil
import uvicorn

app=FastAPI()

from fastapi.responses import FileResponse
from fastapi import BackgroundTasks

@app.post("/process")
async def process_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        job_id = str(uuid.uuid4())
        job_dir = f"./sandbox_jobs/{job_id}"
        os.makedirs(job_dir, exist_ok=True)

        input_path = os.path.join(job_dir, "input.pdf")
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        code = generate_code(prompt)
        validate_code(code)

        output_path = execute_in_sandbox(code, job_dir)

        if not os.path.exists(output_path):
            raise Exception("Output file not created")

       

        return FileResponse(
            path=output_path,
            filename="edited.pdf",
            media_type="application/pdf"
        )

    except Exception as e:
        return {"error": str(e)}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=7860)