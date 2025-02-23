import os
import pandas as pd
import streamlit as st

# Define the relative path to the CSV file
csv_path = os.path.join("data", "24-25_skaters_data.csv")

# Debugging: Display the full absolute path and list files in the directory
st.write(f"🔍 Looking for file at: `{os.path.abspath(csv_path)}`")

# Ensure the data folder exists and list files inside it
if os.path.exists("data"):
    st.write("📂 Files in 'data' folder:", os.listdir("data"))
else:
    st.error("❌ 'data' folder not found!")

# Check if the CSV file exists before loading
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.title("NHL Skater Stats Dashboard")
    st.dataframe(df)
else:
    st.error(f"❌ File not found: `{os.path.abspath(csv_path)}`")
