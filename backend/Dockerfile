FROM python:3.10-slim

WORKDIR /app

RUN pip install pymupdf

COPY sandbox/runner.py /app/runner.py

CMD ["python", "runner.py"]