import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = "http://127.0.0.1:8000"

def extract_list_from_response(resp_json):
    # If top-level is a dict, try common wrapper keys
    if isinstance(resp_json, dict):
        for k in ("data", "transactions", "items", "results", "payload"):
            if k in resp_json and isinstance(resp_json[k], list):
                return resp_json[k]
        # maybe the list is under a single key that's not common:
        # find the first list value
        for v in resp_json.values():
            if isinstance(v, list):
                return v
        # else not a list
        return None
    elif isinstance(resp_json, list):
        return resp_json
    else:
        return None

def find_amount_field(df):
    # common amount-like column names
    candidates = ["amount", "Amount", "amt", "value", "transaction_amount", "amount_usd"]
    for c in candidates:
        if c in df.columns:
            return c
    # try numeric columns (if only one numeric column exists besides date)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) == 1:
        return numeric_cols[0]
    return None


# ✅ Wrapped main logic inside a reusable function
def show_forecast_page():
    st.title("📈 Spending Forecast Dashboard")
    st.subheader("💳 Transaction Summary (robust)")

    if st.button("View Transaction Summary"):
        try:
            resp = requests.get(f"{BASE_URL}/transactions?limit=200")
            data_json = resp.json()

            records = extract_list_from_response(data_json)
            if not records:
                st.error("No transaction list found in response.")
                return

            df = pd.DataFrame(records)

            # If 'amount' missing, try to discover it
            amount_field = find_amount_field(df)
            if not amount_field:
                st.error("The 'amount' field is missing. Available fields: " + ", ".join(df.columns.tolist()))
                return

            # normalize to numeric
            df[amount_field] = pd.to_numeric(df[amount_field], errors="coerce")
            # create a canonical column 'amount' for downstream code
            df["amount"] = df[amount_field]

            # If date column exists, parse it
            date_cols = [c for c in df.columns if "date" in c.lower()]
            if date_cols:
                df["date"] = pd.to_datetime(df[date_cols[0]], errors="coerce")

            # now safe to compute metrics
            total_spent = df["amount"].sum()
            num_txns = df.shape[0]
            avg_tx = df["amount"].mean()

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Transactions", f"{num_txns}")
            col2.metric("Total Amount ($)", f"{total_spent:,.2f}")
            col3.metric("Average Transaction ($)", f"{avg_tx:,.2f}" if not pd.isna(avg_tx) else "N/A")

            # Top categories if present
            if "category" in df.columns:
                top_cats = df.groupby("category")["amount"].sum().nlargest(5).reset_index()
                st.markdown("### 🥇 Top Categories")
                st.bar_chart(top_cats.set_index("category"))
            else:
                st.info("No 'category' field available to produce a breakdown.")

            # Trend chart if date exists
            if "date" in df.columns and df["date"].notna().any():
                trend = (
                    df.dropna(subset=["date"])
                      .sort_values("date")
                      .set_index("date")
                      .resample("D")["amount"]
                      .sum()
                      .rolling(7)
                      .mean()
                )
                st.markdown("### 📅 7-Day Rolling Trend")
                st.line_chart(trend)

        except Exception as e:
            st.error(f"An error occurred while fetching transactions: {e}")
