import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title='Copilot for Personal Finance', layout='centered')
st.title("💸 Copilot for Personal Finance (Demo)")
st.write("Upload a Cash-App-style transaction CSV and get AI insights + a naive forecast.")

# File uploader
uploaded_file = st.file_uploader("Upload transaction CSV", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file) # Read CSV file
        st.subheader("Preview of uploaded data") # Display data preview
        st.dataframe(df.head(20)) # Display first 20 rows

        if st.button("Analyze with AI (local stub)"):
            # Local stub analysis using ai/llm_client.py if running in same env
            try:
                from ai.llm_client import analyze_transactions # Import analysis function
                result = analyze_transactions(df) # Call analysis function
                st.subheader("AI Analysis") # Display AI analysis
                st.json(result)
            except Exception as e: # Handle exceptions
                st.error(f"AI analysis failed: {e}")

        if st.button("Forecast (naive)" ): # Forecast button
            try: 
                from models.forecast import forecast_next_month_spending # Import forecasting function
                # Aggregate by month
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                monthly = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().sort_index()
                history = [float(x) for x in monthly.values]
                pred = forecast_next_month_spending(history)
                st.subheader("Forecast")
                st.write(f"Predicted next month spending: ${pred:.2f}")
                st.line_chart(history + [pred])
            except Exception as e:
                st.error(f"Forecast failed: {e}")
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")
else:
    st.info("Use the sample CSV in /data to try the demo.")
