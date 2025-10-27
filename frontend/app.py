import streamlit as st

st.title("💸 Copilot for Personal Finance")
st.write("Upload your transaction history and get AI-powered insights.")

uploaded_file = st.file_uploader("Upload transaction CSV", type=["csv"])
if uploaded_file:
    st.success("File uploaded successfully!")
else:
    st.info("Please upload a CSV file to proceed.")