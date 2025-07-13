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
