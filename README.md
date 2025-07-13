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
        │  AI Enrichment      │  (Gemini)
        └──────────┬──────────┘
                   │
             ┌─────▼─────┐
             │ MongoDB   │  (Cloud)
             └───────────┘
```

---

## 🚀 Getting Started (Local Setup)

These instructions assume you have Docker and Docker Compose installed.

### 1. 🧾 Clone the Repository

```bash
git clone https://github.com/yourusername/cloudculate.git
cd cloudculate
```

### 2. ⚙️ Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# MongoDB Configuration
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/cloudculate?retryWrites=true&w=majority

# AI Configuration
GEMINI_API_KEY=your_google_gemini_api_key

# Optional: Application Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

### 3. 🐳 Start the Application (Docker Compose)

```bash
docker-compose up --build
```

This will:
- Build and start the FastAPI backend service
- Build and start the React frontend service
- Connect to your cloud MongoDB instance

### 4. 🌐 Access the Application

- **Frontend**: Open your browser and navigate to [http://localhost:3000](http://localhost:3000)
- **Backend API**: The FastAPI backend will be available at [http://localhost:8000](http://localhost:8000)

### 5. 🛑 Stop the Services

To stop all running containers:

1. Press `CTRL+C` in the terminal where Docker Compose is running
2. Run the following command to remove containers:

```bash
docker-compose down
```
