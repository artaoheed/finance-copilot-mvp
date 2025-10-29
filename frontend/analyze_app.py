import streamlit as st
import requests
import pandas as pd

st.title("🧠 AI Transaction Summary Dashboard")

# --- Backend Base URL ---
BASE_URL = "http://127.0.0.1:8000"

# --- Trigger AI Analysis ---
st.subheader("📊 Analyze Transactions with LLM")

if st.button("Run AI Analysis"):
    with st.spinner("Analyzing transactions using LLM..."):
        try:
            response = requests.post(f"{BASE_URL}/analyze")
            if response.status_code == 200:
                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.success(f"✅ Analysis completed successfully using **{data['analysis_source']}**")

                    results = data["results"]

                    # --- Display Summary ---
                    st.markdown("### 🧾 Summary")
                    st.info(results.get("summary", "No summary available."))

                    # --- Display Advice ---
                    st.markdown("### 💡 Advice")
                    st.success(results.get("advice", "No advice available."))

                    # --- Display Top Categories Table ---
                    st.markdown("### 💰 Top Spending Categories")
                    top_cats = pd.DataFrame(results["top_categories"])
                    st.dataframe(top_cats)

            else:
                st.error(f"Request failed with status code {response.status_code}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
