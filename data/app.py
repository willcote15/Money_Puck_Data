import os
import pandas as pd
import streamlit as st

# Get the correct path
csv_path = os.path.join("data", "24-25_skaters_data.csv")  # Relative path

# Debugging: Show the actual path being used
st.write(f"Looking for file at: {os.path.abspath(csv_path)}")

# Check if file exists
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.title("NHL Skater Stats Dashboard")
    st.dataframe(df)
else:
    st.error(f"❌ File not found: {os.path.abspath(csv_path)}")
