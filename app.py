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
        "playerId", "season", "name", "team", "position", "situation",
        "I_F_shotsOnGoal", "games_played", "I_F_goals", "icetime"
    }
    if required_columns.issubset(df.columns):
        # Filter for situation "all"
        df_filtered = df[df["situation"] == "all"].copy()

        # Calculate shots on goal per game, rounded to 2 decimal places
        df_filtered["shots_per_game"] = (df_filtered["I_F_shotsOnGoal"] / df_filtered["games_played"]).round(2)

        # Convert ice time from seconds to minutes and round to 2 decimal places
        df_filtered["icetime_per_game"] = (df_filtered["icetime"] / df_filtered["games_played"] / 60).round(2)

        # Rename I_F_goals to goals
        df_filtered.rename(columns={"I_F_goals": "goals"}, inplace=True)

        # Format season as "YYYY-YYYY" instead of "YYYY, YYYY"
        df_filtered["season"] = df_filtered["season"].astype(str).str.replace(",", "-")

        # Select relevant columns (moving shots per game before goals)
        df_display = df_filtered[["season", "name", "team", "position", "shots_per_game", "goals", "icetime_per_game"]]

        # Sort by shots per game (descending order)
        df_display = df_display.sort_values(by="shots_per_game", ascending=False)

        # Streamlit UI
        st.title("NHL Skater Stats Dashboard")
        st.write("Compare Skater Stats Between Two Teams")

        # Create two columns for side-by-side comparison
        col1, col2 = st.columns(2)

        # Get unique teams
        team_list = sorted(df_display["team"].unique())

        # Left column - Team 1 selection and table
        with col1:
            st.subheader("Team 1")
       

