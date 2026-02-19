import os

os.chdir("/data")

with open("script.py") as f:
    code = f.read()

exec(code)