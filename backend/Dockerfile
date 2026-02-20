FROM python:3.10-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install pymupdf pytesseract Pillow

COPY sandbox/runner.py /app/runner.py

CMD ["python", "runner.py"]