import os
import subprocess

def execute_in_sandbox(code: str, job_dir: str) -> str:
    """
    Hugging Face / Cloud friendly executor. 
    Bina naya Docker banaye, code ko ek safe subprocess mein run karega.
    """
    script_path = os.path.join(job_dir, "script.py")
    output_pdf_path = os.path.join(job_dir, "output.pdf")

    
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)

    try:
        
        result = subprocess.run(
            ["python", "script.py"],
            cwd=job_dir, 
            capture_output=True,
            text=True,
            timeout=30 
        )

       
        if result.returncode != 0:
            print("AI Code Execution Error:", result.stderr)
            raise Exception(f"AI Code Error: {result.stderr}")

        
        if not os.path.exists(output_pdf_path):
            raise Exception("Execution successful, but output.pdf was not created by the AI.")

        return output_pdf_path

    except subprocess.TimeoutExpired:
        raise Exception("Code execution timed out")
    except Exception as e:
        raise Exception(str(e))