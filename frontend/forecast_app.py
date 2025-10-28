import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("💰 Spending Forecast Dashboard")

BASE_URL = "http://127.0.0.1:8000"

st.subheader("📈 Forecasting Monthly Spending")

if st.button("Run Forecast"):
    with st.spinner("Fetching forecast data..."):
        try:
            response = requests.post(f"{BASE_URL}/forecast")
            if response.status_code == 200:
                data = response.json()

                # Convert to DataFrame
                df = pd.DataFrame({
                    "Month": data["months"],
                    "Amount": data["amounts"]
                })

                # --- Plot forecast ---
                fig, ax = plt.subplots()
                ax.plot(df["Month"], df["Amount"], marker="o", label="Historical Spending")

                # Add forecast point
                next_month = pd.to_datetime(df["Month"]).max() + pd.DateOffset(months=1)
                ax.scatter(next_month.strftime("%Y-%m"), data["forecast_next_month"], color="red", label="Forecast (Next Month)")
                ax.axhline(y=data["forecast_next_month"], color="red", linestyle="--", alpha=0.6)

                # Style
                ax.set_xlabel("Month")
                ax.set_ylabel("Spending (USD)")
                ax.set_title("Monthly Spending Forecast")
                plt.xticks(rotation=45)
                plt.tight_layout()
                ax.legend()

                st.pyplot(fig)

                # --- Display clean summary ---
                st.markdown(f"### 💵 Next Month Forecast: **${data['forecast_next_month']:,.2f}**")
                st.caption(f"Predicted spending for {next_month.strftime('%B %Y')}")

            else:
                st.error(f"Request failed with status code {response.status_code}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.info("Click the button to run the forecast.")