# frontend/app.py
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import hashlib

# --- App Metadata ---
APP_VERSION = "v1.0.0"
APP_AUTHOR = "and built with ❤️ by Taoheed Abdulraheem"


# --- Backend Base URL ---
BASE_URL = "http://127.0.0.1:8000"

# --- Cached Functions ---
@st.cache_data(ttl=600, show_spinner=False)
def cached_analyze():
    """Cache the AI analysis response for 10 minutes."""
    response = requests.post(f"{BASE_URL}/analyze")
    return response.json()

@st.cache_data(ttl=600, show_spinner=False)
def cached_forecast(method="rolling"):
    """Cache the forecast response for 10 minutes."""
    response = requests.get(f"{BASE_URL}/forecast", params={"method": method})
    return response.json()

# --- Page Config ---
st.set_page_config(page_title="💸 Copilot for Personal Finance", layout="wide")

# --- Initialize Session State ---
if "df" not in st.session_state:
    st.session_state.df = None
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

# --- Sidebar Navigation ---
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to:", ["Upload CSV", "AI Analysis", "Forecast"])

# --- Header ---
st.title("💸 Copilot for Personal Finance")
st.markdown("_An AI-powered assistant that helps you understand and forecast your spending._")

# ===========================
# 📤 PAGE 1: UPLOAD CSV
# ===========================
if page == "Upload CSV":
    st.subheader("📤 Upload Transaction Data")
    uploaded_file = st.file_uploader("Upload your transaction CSV", type=["csv"])

    if uploaded_file:
        # --- Check for cached file ---
        file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()
        if "last_file_hash" in st.session_state and file_hash == st.session_state.last_file_hash:
            st.info("⚡ Using cached upload (same file as before).")
            df = st.session_state.df
            st.session_state.uploaded = True
            st.dataframe(df.head(10))
            st.stop()
        else:
            st.session_state.last_file_hash = file_hash

        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.session_state.uploaded = True

            st.success("✅ File uploaded successfully!")
            st.dataframe(df.head(10))

            # --- Send file to backend ---
            st.info("⏳ Sending data to backend...")
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            upload_response = requests.post(f"{BASE_URL}/upload", files=files)

            if upload_response.status_code == 200:
                st.success("📡 Transactions successfully sent to backend!")
            else:
                st.error(f"Backend upload failed: {upload_response.text}")

            # --- Charts ---
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                monthly = df.groupby(df["date"].dt.to_period("M"))["amount"].sum().reset_index()
                monthly["month"] = monthly["date"].dt.to_timestamp()

                st.markdown("### 📈 Monthly Spending Trend")
                fig, ax = plt.subplots()
                ax.plot(monthly["month"], monthly["amount"], marker="o", color="blue")
                ax.set_xlabel("Month")
                ax.set_ylabel("Total Spending ($)")
                ax.set_title("Monthly Spending Trend")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            if "category" in df.columns:
                cat = df.groupby("category")["amount"].sum().sort_values(ascending=False)
                st.markdown("### 🥧 Spending by Category")
                st.bar_chart(cat)

        except Exception as e:
            st.error(f"❌ Could not process CSV: {e}")
    else:
        st.info("📁 Upload a CSV file to start analyzing your finances.")

# ===========================
# 🧠 PAGE 2: AI ANALYSIS
# ===========================
elif page == "AI Analysis":
    st.subheader("🧠 Analyze Transactions with AI")

    if not st.session_state.uploaded:
        st.warning("⚠️ Please upload a CSV first under 'Upload CSV'.")
    else:
        if st.button("Run AI Analysis"):
            try:
                data = cached_analyze()
                if "error" in data:
                    st.error(data["error"])
                else:
                    results = data["results"]
                    st.success(f"✅ Analysis completed using {data['analysis_source']}")

                    st.markdown("### 💡 Summary")
                    st.info(results.get("summary", "No summary available."))

                    st.markdown("### 💬 Advice")
                    st.success(results.get("advice", "No advice available."))

                    st.markdown("### 💰 Top Categories")
                    top_cats = pd.DataFrame(results.get("top_categories", []))
                    if not top_cats.empty:
                        st.dataframe(top_cats)
            except Exception as e:
                st.error(f"Analysis failed: {e}")

# ===========================
# 📊 PAGE 3: FORECAST
# ===========================
elif page == "Forecast":
    st.subheader("📊 Spending Forecast")

    if not st.session_state.uploaded:
        st.warning("⚠️ Please upload a CSV first under 'Upload CSV'.")
    else:
        method = st.selectbox("Forecast Method", ["rolling", "linear"])
        if st.button("Run Forecast"):
            try:
                data = cached_forecast(method=method)
                if "error" in data:
                    st.error(data["error"])
                else:
                    next_amount = data["predicted_next_month_amount"]
                    st.success(f"💵 Predicted next month spending: **${next_amount:,.2f}**")

                    months = pd.to_datetime(data["historical_months"], errors="coerce")
                    amounts = data["historical_amounts"]

                    fig, ax = plt.subplots()
                    ax.plot(months, amounts, marker="o", label="Historical")
                    ax.scatter(
                        months.max() + pd.DateOffset(months=1),
                        next_amount,
                        color="red",
                        label="Forecast"
                    )
                    ax.axhline(y=next_amount, color="red", linestyle="--", alpha=0.6)
                    ax.set_xlabel("Month")
                    ax.set_ylabel("Spending ($)")
                    ax.legend()
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
            except Exception as e:
                st.error(f"Forecast failed: {e}")
from datetime import datetime
st.caption(f"🕒 Last updated: {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")




# ===========================
# 🌍 FOOTER (Visible on all pages)
# ===========================
st.markdown(
    """
    <hr style="margin-top: 40px; margin-bottom: 10px;"/>
    <div style="text-align: center; color: grey; font-size: 14px;">
        <p>💸 Copilot for Personal Finance — {version}</p>
        <p>Developed by <b>{author}</b> | © 2025 All Rights Reserved</p>
    </div>
    """.format(version=APP_VERSION, author=APP_AUTHOR),
    unsafe_allow_html=True
)
