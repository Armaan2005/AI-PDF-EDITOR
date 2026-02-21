# 📄 AI PDF Studio: Intelligent Document Manipulation System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF)
![Deployment](https://img.shields.io/badge/Deployed_on-Hugging_Face_%26_Vercel-success)

AI PDF Studio is an advanced, LLM-powered document processing tool that allows users to edit, redact, and manipulate PDF files using natural language prompts. Instead of rigid UI buttons, it dynamically generates and executes Python code in a secure sandboxed environment to perform highly custom PDF operations.

🚀 Live Demo: https://ai-pdf-editor-alpha.vercel.app/

⚙️ Backend API Status: Hosted on [Hugging Face Spaces]https://armaan2005-ai-pdf-studio.hf.space/docs

## ✨ Key Features

* Natural Language Processing: Tell the AI what to do (e.g., "Redact all names," "Delete page 2," "Extract tables"), and it handles the complex PDF manipulations automatically.
* Dynamic Code Execution: Uses an LLM (Gemini) to generate context-aware Python scripts using PyMuPDF (fitz).
*✨ Multimodal Vision Intelligence: Unlike traditional editors, it "sees" the PDF. It uses Gemini 2.5 Flash's native vision to understand layouts, diagrams, and scanned text without needing external OCR libraries like Tesseract.
*​🧠 Intelligent Summarization: Can analyze multi-page documents and generate a concise summary directly onto a new page within the PDF.
* Secure Sandbox Environment: Executes generated AI code via secure subprocesses with strict timeouts to prevent infinite loops and ensure server stability.
* Decoupled Architecture: A lightweight frontend connected to a heavy, Dockerized FastAPI backend hosted on the cloud.

## 🏗️ System Architecture & MLOps

This project follows production-grade software engineering practices:

* Vision-Centric Workflow: The system now uploads the entire document to the LLM's vision context, ensuring 100% accuracy in finding text locations and preserving original formatting.
* Containerization: The backend environment is fully Dockerized, ensuring consistent Tesseract and Python dependencies across local and cloud environments.
* Continuous Integration (CI): Integrated GitHub Actions pipeline that automatically builds and tests the Docker image upon every push to the main branch.
* Cloud Deployment: * Frontend: Deployed on Vercel for fast, edge-network delivery.
* Backend: Hosted on Hugging Face Spaces (Docker Space) exposing port 7860, utilizing secure Environment Secrets for API keys.

## 📂 Project Structure

    AI-PDF-EDITOR/
    │
    ├── frontend/                  # Vercel Deployment
    │   ├── index.html             # UI Structure
    │   ├── style.css              # UI Styling
    │   └── script.js              # API Integration logic
    │
    ├── backend/                   # Hugging Face Spaces Deployment
    │   ├── app/                   # Core FastAPI Application
    │   │   ├── main.py            # FastAPI server & endpoints
    │   │   ├── llm.py             # Gemini LLM integration
    │   │   ├── executor.py        # Secure subprocess sandbox
    │   │   ├── validator.py       # AI code validation
    │   │   └── config.py          # Environment variables setup
    │   │
    │   ├── sandbox/               # Isolated execution environment
    │   │   └── runner.py          # Script for running generated code safely
    │   │
    │   ├── Dockerfile             # Container configuration
    │   └── requirements.txt       # Python dependencies
    │
    ├── .github/workflows/
    │   └── ci.yml                 # GitHub Actions CI pipeline
    │
    ├── docker-compose.yml         # Local container orchestration
    └── README.md

## 🛠️ Tech Stack

* Backend: FastAPI, Python, Uvicorn
* PDF Processing & OCR: PyMuPDF (fitz)
* AI / LLM: Google Gemini API
* DevOps / Deployment: Docker, Docker Compose, GitHub Actions, Hugging Face Spaces, Vercel
* Frontend: HTML/CSS/JS

## 💻 Local Setup & Installation

If you want to run this project locally, follow these steps:

### 1. Clone the repository
    git clone https://github.com/Armaan2005/AI-PDF-EDITOR.git
    cd AI-PDF-EDITOR

### 2. Backend Setup
Navigate to the backend folder and create a .env file:
    cd backend
    touch .env

Add your API key to the .env file:
GEMINI_API_KEY=your_api_key_here

### 3. Run with Docker (Recommended)
docker build -t ai-pdf-studio .
docker run -p 8000:7860 ai-pdf-studio

The API will be available at http://localhost:8000/docs.
### 4. Frontend Setup
Navigate to the frontend directory, update the API fetch URL in your script to http://localhost:8000/process, and launch your local server using Live Server or a similar tool.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 👨‍💻 Developed By
Armaan Joshi * Passionate about Deep Learning, Computer Vision, and MLOps.
*  | [GitHub](https://github.com/Armaan2005)




