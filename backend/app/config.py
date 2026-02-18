import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_IMPORTS = [
    "fitz",
    "math",
    "re"
]
FORBIDDEN_KEYWORDS = [
    "os",
    "sys",
    "subprocess",
    "socket",
    "shutil",
    "eval",
    "exec",
    "open(",
    "import",
]