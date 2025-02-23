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
    required_columns = {
        "playerId",
        "season",
        "name",
        "team",
        "position",
        "situation",
        "I_F_shotsOnGoal",
        "games_played",
        "I_F_goals",
        "icetime",
    }
    if required_columns.issubset(df.columns):
        # Filter for situation "all"
        df_filtered = df[df["situation"] == "all"].copy()

        # Calculate shots on goal per game, rounded to 2 decimal places
        df_filtered["shots_per_game"] = (
            df_filtered["I_F_shotsOnGoal"] / df_filtered["games_played"]
        ).round(2)

        # Calculate ice time per game, rounded to 2 decimal places
        df_filtered["icetime_per_game"] = (
            df_filtered["icetime"] / df_filtered["games_played"]
        ).round(2)

        # Format season as "YYYY-YYYY" instead of "YYYY, YYYY"
        df_filtered["season"] = df_filtered["season"].astype(str).str.replace(",", "-")

        # Select relevant columns
        df_display = df_filtered[
            [
                "season",
                "name",
                "team",
                "position",
                "I_F_goals",
                "shots_per_game",
                "icetime_per_game",
            ]
        ]

        # Sort by shots per game (descending order)
        df_display = df_display.sort_values(by="shots_per_game", ascending=False)

        # Streamlit UI
        st.title("NHL Skater Stats Dashboard")
        st.write("Shots on Goal, Goals, and Ice Time Per Game (Situation: All)")

        # Add team filter
        team_list = ["All Teams"] + sorted(df_display["team"].unique())
        selected_team = st.selectbox("Select a team:", team_list)

        # Filter data based on team selection
        if selected_team != "All Teams":
            df_display = df_display[df_display["team"] == selected_team]

        # Display dataframe
        st.dataframe(df_display)
    else:
        st.error(
            f"❌ Missing required columns in the dataset: {required_columns - set(df.columns)}"
        )
else:
    st.error(f"❌ File not found: {os.path.abspath(csv_path)}")
