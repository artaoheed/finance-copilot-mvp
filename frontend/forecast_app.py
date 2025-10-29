import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = "http://127.0.0.1:8000"

def extract_list_from_response(resp_json):
    if isinstance(resp_json, dict):
        for k in ("data", "transactions", "items", "results", "payload"):
            if k in resp_json and isinstance(resp_json[k], list):
                return resp_json[k]
        for v in resp_json.values():
            if isinstance(v, list):
                return v
        return None
    elif isinstance(resp_json, list):
        return resp_json
    else:
        return None

def find_amount_field(df):
    candidates = ["amount", "Amount", "amt", "value", "transaction_amount", "amount_usd"]
    for c in candidates:
        if c in df.columns:
            return c
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) == 1:
        return numeric_cols[0]
    return None

def show_forecast_page():
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
            amount_field = find_amount_field(df)

            if not amount_field:
                st.error("The 'amount' field is missing. Available fields: " + ", ".join(df.columns.tolist()))
                return

            df[amount_field] = pd.to_numeric(df[amount_field], errors="coerce")
            df["amount"] = df[amount_field]

            date_cols = [c for c in df.columns if "date" in c.lower()]
            if date_cols:
                df["date"] = pd.to_datetime(df[date_cols[0]], errors="coerce")

            total_spent = df["amount"].sum()
            num_txns = df.shape[0]
            avg_tx = df["amount"].mean()

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Transactions", f"{num_txns}")
            col2.metric("Total Amount ($)", f"{total_spent:,.2f}")
            col3.metric("Average Transaction ($)", f"{avg_tx:,.2f}" if not pd.isna(avg_tx) else "N/A")

            if "category" in df.columns:
                top_cats = df.groupby("category")["amount"].sum().nlargest(5).reset_index()
                st.markdown("### 🥇 Top Categories")
                st.bar_chart(top_cats.set_index("category"))
            else:
                st.info("No 'category' field available to produce a breakdown.")

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
                st.line_chart(trend)

        except Exception as e:
            st.error(f"An error occurred while fetching transactions: {e}")
