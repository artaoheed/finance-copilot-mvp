import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = "http://127.0.0.1:8000"

def show_forecast_page():
    st.title("📈 Spending Forecast Dashboard")

    # --- Select forecast method ---
    method = st.selectbox(
        "Select Forecast Method:",
        ["rolling", "linear"],
        format_func=lambda x: "Rolling Average" if x == "rolling" else "Linear Regression"
    )

    st.markdown(
        """
        **Rolling Average** → Uses the past few months’ averages and spending trend.  
        **Linear Regression** → Fits a straight line trend across your spending history.
        """
    )

    if st.button("Run Forecast"):
        with st.spinner(f"Fetching {method.capitalize()} Forecast..."):
            try:
                # Call backend
                response = requests.get(f"{BASE_URL}/forecast", params={"method": method})
                if response.status_code != 200:
                    st.error(f"Request failed with status code {response.status_code}")
                    return

                data = response.json()
                if "error" in data:
                    st.error(data["error"])
                    return

                # --- Prepare data ---
                months = data.get("historical_months", [])
                amounts = data.get("historical_amounts", [])
                next_pred = data.get("predicted_next_month_amount", None)

                if not months or not amounts:
                    st.warning("No transaction data found to plot.")
                    return

                df = pd.DataFrame({"Month": months, "Amount": amounts})

                # --- Plot historical and forecast ---
                fig, ax = plt.subplots()

                df["Month"] = pd.to_datetime(df["Month"], errors="coerce")

                ax.plot(df["Month"], df["Amount"], marker="o", label="Historical Spending")
                ax.set_xlabel("Month")
                ax.set_ylabel("Spending (USD)")
                plt.xticks(rotation=45)

                if next_pred is not None:
                    next_month = df["Month"].max() + pd.DateOffset(months=1)
                    ax.scatter(next_month, next_pred, color="red", label="Forecast")
                    ax.axhline(y=next_pred, color="red", linestyle="--", alpha=0.6)
                    st.success(f"💵 Forecast for {next_month.strftime('%B %Y')}: **${next_pred:,.2f}**")

                ax.set_title(f"Spending Forecast ({method.capitalize()} Method)")
                ax.legend()
                st.pyplot(fig)

                # --- Display raw data ---
                with st.expander("📊 View Raw Forecast Data"):
                    st.dataframe(df)

            except Exception as e:
                st.error(f"An error occurred: {e}")
