# 💸 Copilot for Personal Finance  
_An AI-powered financial assistant that helps users understand spending, get AI-driven insights, and forecast future expenses._

![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?logo=streamlit)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green?logo=fastapi)
![Gemini](https://img.shields.io/badge/LLM-Gemini-blue?logo=google)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

---

## 🌍 Live Demo  

- **Frontend (Streamlit):** [https://artaoheed-finance-copilot-mvp-frontendapp-ywqu7m.streamlit.app/](https://artaoheed-finance-copilot-mvp-frontendapp-ywqu7m.streamlit.app/)  
- **Backend (FastAPI):** [https://finance-copilot.up.railway.app/docs](https://finance-copilot.up.railway.app/docs)  

---

## 🧠 Overview  

**Copilot for Personal Finance** is a lightweight AI and ML-driven web app that enables users to:  

- 📤 Upload transaction CSVs (Cash App / Bank format)  
- 📊 Visualize monthly trends and category spending  
- 🧠 Get **AI-generated insights** from Gemini/OpenAI LLMs  
- 📈 Forecast next-month spending using **linear regression & rolling averages**  
- 🔒 Maintain privacy through automatic PII sanitization  

This project was developed as part of a **14-day build challenge** to showcase AI, ML, and cloud deployment skills.

---

## ⚙️ Tech Stack  

| Layer | Tools & Frameworks |
|-------|--------------------|
| **Frontend (UI)** | Streamlit + Plotly + Matplotlib |
| **Backend (API)** | FastAPI + Uvicorn |
| **Machine Learning** | Scikit-Learn (Linear Regression, Rolling Average) |
| **AI/LLM Integration** | Google Gemini / OpenAI GPT / Anthropic Claude |
| **Hosting** | Railway (Backend), Streamlit Cloud (Frontend) |
| **Data** | Pandas + NumPy |
| **Version Control** | Git + GitHub |

---

## 🚀 Getting Started (Run Locally)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/finance-copilot-mvp.git
cd finance-copilot-mvp
```

### 2️⃣ Clone the repository
```python
pip install -r requirements.txt
```

### 3️⃣ Set up environment variables
Create a .env file in the project root:
```python
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key  # optional
CORS_ORIGINS=http://localhost:8501,https://finance-copilot.streamlit.app
```

### 4️⃣ Run the backend
```bash
uvicorn backend.main:app --reload
```
Access API docs at 👉 http://127.0.0.1:8000/docs

### 5️⃣ Run the frontend
```bash
streamlit run frontend/app.py
```
Then open 👉 http://localhost:8501


## 📊 Features

✅ Upload CSV transactions (auto-parsed by Pandas)
✅ Interactive visualizations — monthly spending & category breakdown
✅ AI analysis via LLM (Gemini / OpenAI)
✅ Forecast spending using ML (rolling + linear models)
✅ Privacy sanitization — removes long descriptions or names
✅ Caching for faster repeated analysis
✅ Logging & retry mechanism for robust LLM calls


## System Architecture

Frontend (Streamlit)
|
|  calls REST APIs →
|
Backend (FastAPI)
|--/upload       → Upload & store transactions
|--/forecast     → Predict next-month spending
|--/analyze      → AI-powered financial insight (LLM)
|
|__ Models
    |-- Linear Regression
    |-- Rolling Average
    |-- LLMClient (Gemini/OpenAI/Claude)


## 🧪 Testing

Run all tests using pytest:
```python
pytest backend/tests
```
Example test files:

test_forecast_model.py — validates ML output ranges
test_llm_wrapper.py — mocks LLM JSON parsing
test_upload_parser.py — ensures CSV parsing integrity


## 🚀 Deployment

| Component | Platform | Status | Live URL |
|-----------|----------|--------|----------|
| **Backend (FastAPI + Uvicorn)** | Railway | ✅ Deployed | https://finance-copilot.up.railway.app |
| **API Docs (Swagger UI)** | Railway | ✅ Available | https://finance-copilot.up.railway.app/docs |
| **Frontend (Streamlit)** | Streamlit Cloud | ✅ Deployed | https://finance-copilot.streamlit.app |
| **Model Hosting / LLM** | Google Gemini API / OpenAI API | ✅ Cloud-based | N/A (private API keys) |

---

### 🔐 Environment Variables

These environment variables must be configured in both **Railway (backend)** and **Streamlit Cloud (frontend)** — _do not commit them to GitHub._

| Variable | Required? | Used By | Description |
|----------|-----------|---------|-------------|
| `LLM_PROVIDER` | ✅ | Backend & Frontend | Selects AI provider: `gemini`, `openai`, or `claude` |
| `GEMINI_API_KEY` | ✅ (if using Gemini) | Backend | API key for Google Gemini models |
| `OPENAI_API_KEY` | ✅ (if using OpenAI) | Backend | API key for GPT models (optional fallback) |
| `CLAUDE_API_KEY` | ✅ (if using Claude) | Backend | API key for Anthropic Claude models |
| `CORS_ORIGINS` | ✅ | Backend | Comma-separated list of allowed frontend URLs |
| `PORT` | ✅ (Railway auto-injects) | Backend | Required for production server |
| `BASE_URL` | ✅ | Frontend | URL pointing to deployed backend API |

#### ✅ Example `.env` for local development

```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
CORS_ORIGINS=http://localhost:8501,https://finance-copilot.streamlit.app
```

## 🧱 Build Journey

🗓 Timeline:

Week 1: Backend setup, ML forecast models, and AI analysis pipeline

Week 2: Streamlit frontend, charting, caching, and full deployment

💡 Copilot & Cursor Assistance:
Used to generate scaffolding for FastAPI routes, LLM integration boilerplate, and testing utilities (e.g., llm_client.py, forecast.py).

⚙️ Challenges & Fixes:

CORS configuration → resolved with CORSMiddleware

Missing python-multipart → added to requirements.txt

JSON parsing in LLM responses → implemented fallback parser

Full build log in BUILD_JOURNEY.md


---

## 📜 License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it as long as attribution is preserved.

---

## 🤝 Contributing

Contributions are welcome!  
If you'd like to improve this project:

1. **Fork** this repository  
2. Create a new branch: `git checkout -b feature/your-feature-name`  
3. Make your changes and commit: `git commit -m "Add some feature"`  
4. Push to your branch: `git push origin feature/your-feature-name`  
5. Open a **Pull Request** 🚀  

Please follow TODOs, formatting style, and keep commits clean.

If you're reporting a bug, include:

- ✅ Steps to reproduce  
- ✅ Expected vs actual behavior  
- ✅ Screenshots or logs when helpful  

---

## 👨‍💻 Author

**Taoheed Abdulraheem**  
ML Advocate • AI Builder • Community Manager • Tech Educator  

🌐 **Portfolio:** _coming soon_  
🐙 **GitHub:** https://github.com/artaoheed  
🔗 **LinkedIn:** https://linkedin.com/in/artaoheed  
🐤 **X / Twitter:** https://x.com/artaoheed 

If this project helped you, consider giving it a ⭐ on GitHub!

---

## 🚀 Summary

> **Copilot for Personal Finance** is a full-stack AI-powered web app that combines FastAPI, Streamlit, machine learning, and LLMs to give users financial insight, spending forecasts, and clean UI visualizations — all built in **14 days** as a portfolio project.

✅ Upload CSV → stored & validated  
✅ AI LLM insight (Gemini/OpenAI)  
✅ ML spending forecast (Linear Regression + Rolling Avg)  
✅ Deployed live: backend on Railway, frontend on Streamlit  
✅ Fully documented + tested  

This project demonstrates:

| Skill Area | Proof |
|------------|-------|
| Full-stack development | FastAPI backend + Streamlit frontend |
| AI engineering | LLM wrapper + JSON structured outputs |
| Machine learning | Forecast modeling with Scikit-Learn |
| DevOps & deployment | Cloud deployment, env config, CORS, caching |
| Software engineering | Tests, logging, versioning, modular app design |
| Product thinking | Clear UX, privacy safeguards, mobile-friendly UI |

---

