# 🧱 Build Journey: Copilot for Personal Finance

> A 7-day AI-powered finance app sprint — from idea to working MVP with FastAPI, Streamlit, ML forecasting, and LLM analysis.

---

## 💡 Project Overview

**Goal:**  
Build an AI-driven personal finance assistant that can:
- Analyze transactions using Large Language Models (LLMs)
- Forecast future monthly spending using machine learning
- Display insights and predictions in a user-friendly Streamlit dashboard  

**Core Stack:**
- 🧠 **AI / NLP:** OpenAI, Gemini, or Claude
- ⚙️ **Backend:** FastAPI
- 📊 **Frontend:** Streamlit
- 📈 **ML Models:** Scikit-learn (Linear Regression, Rolling Trend)
- 🗃️ **Data:** CSV-based (simulated transactions)
- 🧪 **Tests:** Pytest
- 🧾 **Docs:** README, Build Journey

---

## 🗓️ **Development Timeline**

### **Checklist 1 — Project Scaffold & Environment Setup**
**Focus:** Initialize the project structure, dependencies, and virtual environment.

- Created the main project folders: `backend/`, `frontend/`, `data/`, and `models/`.
- Added a virtual environment (`venv/`) to isolate dependencies.
- Installed base packages: `fastapi`, `uvicorn`, `pandas`, `scikit-learn`, and `streamlit`.
- Created `generate_sample.py` to produce synthetic financial transaction data.
- Verified environment setup using `uvicorn backend.main:app --reload`.

**Outcome:** Project scaffold running locally with a placeholder FastAPI app.

---

### **Checklist 2 — Backend API & Endpoints**
**Focus:** Implemented FastAPI routes for the core backend functions.

- Added four main routes:
  - `POST /upload` — Accept CSV or JSON transaction uploads.
  - `GET /transactions` — Retrieve stored transactions (paginated).
  - `POST /analyze` — Perform AI-driven spending analysis.
  - `POST /forecast` — Predict next month's spending.
- Tested routes using Swagger UI (`http://127.0.0.1:8000/docs`).
- Fixed missing dependency (`python-multipart`) for file uploads.
- Confirmed working responses for `/upload` and `/transactions`.

**Outcome:** Fully functional API endpoints with correct input/output behavior.

---

### **Checklist 3 — LLM Integration & Prompt Engineering**
**Focus:** Connected the backend to an LLM engine (Gemini, OpenAI, or Claude).

- Built `backend/ai/llm_client.py` to abstract between AI providers.
- Supported multiple models:
  - **Gemini** via `google.generativeai`
  - **OpenAI GPT** via `openai`
  - **Claude** via `anthropic`
- Implemented `analyze_transactions_with_llm()` for structured financial analysis.
- Created robust prompt templates:
  ```text
  You are a financial analyst. Given a list of transactions,
  identify top 3 spending categories, give one actionable advice,
  and summarize this month’s financial behavior.

  
