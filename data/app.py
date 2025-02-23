import streamlit as st
import pandas as pd

# Load the latest CSV file
csv_path = "data/24-25_skaters_data.csv"  # Make sure this path is correct
df = pd.read_csv(csv_path)

# Display the dataframe
st.title("NHL Skater Stats Dashboard")
st.dataframe(df)