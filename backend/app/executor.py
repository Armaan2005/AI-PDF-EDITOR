import subprocess
import uuid
import os
import subprocess
import os

def execute_in_sandbox(code: str, job_dir: str):

    script_path = os.path.join(job_dir, "script.py")

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)

    result = subprocess.run(
        [
            "docker", "run", "--rm",
            "-v", f"{os.path.abspath(job_dir)}:/data",
            "pdf-sandbox"
        ],
        capture_output=True,
        text=True
    )

    print("DOCKER STDOUT:", result.stdout)
    print("DOCKER STDERR:", result.stderr)

    return os.path.join(job_dir, "output.pdf")