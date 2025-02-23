import os
import pandas as pd
import streamlit as st

# Get the absolute path
csv_path = os.path.join(os.getcwd(), "data", "24-25_skaters_data.csv")

# Debugging: Print the path to check correctness
st.write(f"Looking for file at: {csv_path}")

# Check if file exists before loading
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.title("NHL Skater Stats Dashboard")
    st.dataframe(df)
else:
    st.error(f"❌ File not found: {csv_path}")
