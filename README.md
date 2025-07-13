# ☁️ CloudCulate – AWS Architecture Parser

CloudCulate is a full-stack application that scrapes AWS service descriptions, enriches them with AI using Google's Gemini, and stores the structured data in MongoDB. It includes a FastAPI backend and a Vite-powered React frontend.

---

## 📦 Features

- ✅ Scrape and parse AWS architecture data using Selenium
- 🤖 AI-powered enrichment using Google Gemini (extract services & summaries)
- 🧠 FastAPI backend with validation, logging, and CORS support
- 🌐 React + Vite frontend to view parsed architectures
- 🐳 Fully containerized with Docker Compose
- 💾 MongoDB (Cloud) for persistent storage

---

## 🧱 Architecture Overview

```text
             ┌─────────────┐
             │  Frontend   │  (Vite + React)
             └─────┬───────┘
                   │ REST (port 3000)
                   ▼
             ┌─────────────┐
             │  Backend    │  (FastAPI)
             └─────┬───────┘
                   │
        ┌──────────▼──────────┐
        │  AI Enrichment (Gemini) │
        └──────────┬──────────┘
                   │
             ┌─────▼─────┐
             │ MongoDB   │  (Cloud)
             └───────────┘

🚀 Getting Started (Local Setup)
These instructions will help you set up and run CloudCulate locally using Docker Compose.

Prerequisites
Docker installed on your machine

Docker Compose installed (usually comes with Docker Desktop)

Step 1: Clone the repository
bash
Copy
Edit
git clone https://github.com/yourusername/cloudculate.git
cd cloudculate
Step 2: Configure environment variables
If your project requires any environment variables (e.g., for AI API keys or MongoDB connection), create a .env file in the root directory or update the docker-compose.yml accordingly.

Example .env file:

env
Copy
Edit
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/cloudculate?retryWrites=true&w=majority
GEMINI_API_KEY=your_google_gemini_api_key
Step 3: Start all services with Docker Compose
bash
Copy
Edit
docker-compose up --build
This will:

Build and start the FastAPI backend service

Build and start the React frontend service

Start a MongoDB container if configured locally or connect to your cloud MongoDB

Step 4: Access the application
Open your browser and navigate to: http://localhost:3000 for the React frontend

The FastAPI backend will be available at: http://localhost:8000

Step 5: Stop the services
To stop all running containers, press CTRL+C in the terminal where Docker Compose is running, then run:

bash
Copy
Edit
docker-compose down