import os
import sys
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Execution timed out")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)

script_path = "/app/script.py"

with open(script_path) as f:
    code = f.read()

exec(code)