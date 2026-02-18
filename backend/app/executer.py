import subprocess
import uuid
import os

def execute_in_sandbox(code: str):
    job_id = str(uuid.uuid4())
    job_dir = f"/tmp/{job_id}"
    os.makedirs(job_dir, exist_ok=True)

    script_path = os.path.join(job_dir, "script.py")
    with open(script_path, "w") as f:
        f.write(code)

    subprocess.run([
        "docker", "run", "--rm",
        "--memory=256m",
        "--cpus=0.5",
        "--network=none",
        "-v", f"{job_dir}:/app",
        "pdf-sandbox"
    ], timeout=10)

    return os.path.join(job_dir, "output.pdf")