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

  ## 📅 Day 4 — Forecasting Baseline (Simple & Fast)

**Goal:**  
Build a quick, reliable forecasting module to predict next month’s spending using historical transaction data.

---

### 🧩 Tasks Completed

#### 1️⃣ Created `models/forecast.py`
- Designed a modular forecasting pipeline to generate spending predictions.
- Implemented **two lightweight forecasting approaches**:
  - **Rolling Average + Linear Trend:** computes the next month's value based on recent averages and direction of change.
  - **Linear Regression (Scikit-learn):** fits a simple regression model to monthly totals to extrapolate the next period.

#### 2️⃣ Key Functions Implemented
| Function | Purpose |
|-----------|----------|
| `prepare_monthly_data()` | Aggregates transactions by month for analysis. |
| `forecast_rolling_trend()` | Calculates rolling averages and trend direction. |
| `forecast_linear_regression()` | Uses a trained regression model to project future spending. |
| `get_forecast()` | Unifies both forecasting methods under a single callable interface. |

---

### ⚙️ Sample Logic Overview
```python
def get_forecast(transactions_df, method="rolling"):
    monthly = prepare_monthly_data(transactions_df)
    if method == "rolling":
        forecast = forecast_rolling_trend(monthly)
    elif method == "linear":
        forecast = forecast_linear_regression(monthly)

    return {
        "predicted_next_month_amount": forecast,
        "historical_months": monthly["month"].dt.strftime("%Y-%m").tolist(),
        "historical_amounts": monthly["amount"].tolist()
    }
```
---
## 📅 Day 5 — Streamlit Frontend MVP

**Goal:**  
Develop a lightweight Streamlit dashboard that allows users to upload transaction data, analyze spending with AI, and forecast future expenses — all powered by the FastAPI backend.

---

### 🧩 Tasks Completed

#### 1️⃣ Built the Frontend App Structure
- Created a dedicated **`frontend/`** folder containing:
  - `app.py` — main entry point for the Streamlit dashboard.
  - `analyze_app.py` — AI insights and summary visualization page.
  - `forecast_app.py` — forecast visualization and trend plotting page.
- Configured navigation using Streamlit’s **sidebar** (`st.sidebar.radio`) for three primary pages:
  - **Upload CSV**
  - **AI Analysis**
  - **Forecast**

---

### 💡 Key Features Implemented

#### 🗂️ **CSV Upload & Visualization**
- Added a clean upload interface using `st.file_uploader`.
- Previewed uploaded transactions using `pandas.DataFrame`.
- Automatically generated charts:
  - **📈 Monthly Spending Trend:** Line chart of total spending per month.
  - **🥧 Category Breakdown:** Bar chart for spending by category.

#### 🧠 **AI-Powered Analysis**
- Integrated “Analyze with AI” button to call `/analyze` backend route.
- Displayed AI-generated results:
  - Financial **summary** (3-sentence overview)
  - Personalized **advice** (actionable tip)
  - **Top spending categories** (table format)
- Used `st.info()` and `st.success()` for friendly visualization of text responses.

#### 📊 **Forecasting Interface**
- Added “Forecast Spending” button to call `/forecast` endpoint.
- Supported both methods:
  - `?method=rolling`
  - `?method=linear`
- Plotted results using Matplotlib:
  - Displayed historical data as a blue line.
  - Highlighted predicted next month’s spending as a red marker.
  - Added axis labels, legends, and currency formatting.

---

### ⚙️ **Backend Integration**
- Configured API connections to the local FastAPI server (`http://127.0.0.1:8000`).
- Used the Python `requests` library for GET and POST calls.
- Ensured proper error handling for connection and data issues.
- Verified successful responses from `/upload`, `/analyze`, and `/forecast`.

---

### 🧱 **Code Architecture Snapshot**
frontend/
│
├── app.py # Main Streamlit app with navigation
├── analyze_app.py # AI insights & summary
├── forecast_app.py # Forecast dashboard with charts
└── init.py


---

### 🧠 **Technical Insights**
- Learned how to manage multi-page Streamlit apps without using experimental page APIs.
- Practiced clean API communication between Streamlit and FastAPI.
- Applied data visualization principles for readability and UX simplicity.
- Enhanced debugging with backend logs and visual feedback in Streamlit.

---

### ✅ **Deliverables**

| Item | Description | Status |
|------|--------------|--------|
| Streamlit App (`app.py`) | Core frontend application | ✅ Done |
| Upload CSV Page | File upload + data preview | ✅ Done |
| AI Analysis Page | LLM integration for insights | ✅ Done |
| Forecast Page | Chart + prediction integration | ✅ Done |
| Backend Connectivity | API calls to FastAPI | ✅ Done |
| Visual Polish | Titles, spacing, and color-coded sections | ✅ Done |

---

### 🎨 **UI Demo Summary**
- Users can now:
  - Upload a CSV file.
  - View their monthly spending visually.
  - Get AI-powered insights and actionable advice.
  - Predict next month’s spending instantly.

Example Output:
💡 "You spend most in 'Food'. Try setting a weekly budget to reduce spending."
💵 Predicted next month spending: $19,435.44


---

### 🏁 **Outcome**
By the end of Day 5:
- The **frontend and backend were fully connected**.
- The app transitioned from a backend-only API to an **interactive AI-powered dashboard**.
- Real-time AI analysis and forecasting became accessible via a clean, responsive UI.

> **Milestone:** Reached the *Minimum Viable Product (MVP)* stage — a working, AI-integrated financial assistant.



## 📅 Day 6 — Integration, Caching & Logging (4–6 hrs)

**Goal:**  
Polish the integration between the FastAPI backend and the Streamlit frontend, improve performance, and introduce observability (logging + caching) to prepare the system for production-level reliability.

---

### 🧩 Tasks Completed

#### 1️⃣ **Frontend Performance Boost with Caching**
- Implemented **`@st.cache_data`** in the Streamlit app to cache results for:
  - AI analysis (`/analyze`)
  - Forecasting (`/forecast`)
- Cached data for 10 minutes (`ttl=600`) to prevent unnecessary backend calls.
- Improved frontend responsiveness — repeated actions now load instantly.

**Code Example**
```python
@st.cache_data(ttl=600, show_spinner=False)
def cached_analyze():
    response = requests.post(f"{BASE_URL}/analyze")
    return response.json()
```

**Backend Logging System**
```python
from backend.utils.logger import logger
logger.info(f"Received {len(records)} transactions in upload route")
```
**⚙️ Updated App Structure**

frontend/
│
├── app.py                # Main Streamlit dashboard
├── analyze_app.py        # AI insights page
├── forecast_app.py       # Forecast visualization
└── __init__.py

backend/
│
├── main.py               # FastAPI entry point
├── routes/
│   ├── upload.py
│   ├── analyze.py
│   └── forecast.py
├── ai/
│   └── llm_client.py
├── models/
│   └── forecast.py
└── utils/
    └── logger.py


**🏁 Outcome**
By the end of Day 6:

The app became faster, more reliable, and easier to debug.

Frontend caching cut load times dramatically.

Logging and CORS integration prepared the system for real deployment.

Milestone: The project transitioned from a working prototype to a polished, production-ready MVP 🚀