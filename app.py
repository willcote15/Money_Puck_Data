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

    # Ensure necessary columns exist
    required_columns = {"playerId", "situation", "I_F_shotsOnGoal", "games_played"}
    if required_columns.issubset(df.columns):
        # Filter for situation "all"
        df_filtered = df[df["situation"] == "all"].copy()

        # Calculate shots on goal per game
        df_filtered["shots_per_game"] = df_filtered["I_F_shotsOnGoal"] / df_filtered["games_played"]

        # Display the processed data
        st.title("NHL Skater Stats Dashboard")
        st.write("Shots on Goal Per Game for Each Player (Situation: All)")
        st.dataframe(df_filtered[["playerId", "shots_per_game"]])
    else:
        st.error(f"❌ Missing required columns in the dataset: {required_columns - set(df.columns)}")
else:
    st.error(f"❌ File not found: {os.path.abspath(csv_path)}")
