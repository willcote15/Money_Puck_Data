import streamlit as st
import os
import pandas as pd
from datetime import datetime
import pytz  # Import for timezone conversion

# Set page layout to wide (must be the first Streamlit command)
st.set_page_config(layout="wide")

# Get the correct path
csv_path = os.path.join("data", "24-25_skaters_data.csv")  # Relative path

# Function to get the last modified timestamp of the CSV
def get_file_timestamp(filepath):
    if os.path.exists(filepath):
        utc_time = datetime.utcfromtimestamp(os.path.getmtime(filepath))
        eastern = pytz.timezone("America/New_York")
        return utc_time.replace(tzinfo=pytz.utc).astimezone(eastern).strftime("%Y-%m-%d %I:%M:%S %p ET")
    return None

# Function to load the latest data without caching
def load_data():
    return pd.read_csv(csv_path)

# Display the last updated timestamp
file_timestamp = get_file_timestamp(csv_path)

if file_timestamp:
    st.sidebar.markdown(f"📅 **Data last updated:** {file_timestamp}")
else:
    st.sidebar.markdown("⚠️ **Data file not found!**")

# Check if file exists before loading
if os.path.exists(csv_path):
    df = load_data()  # Always loads the latest CSV

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

        # Convert ice time from seconds to minutes and round to 2 decimal places
        df_filtered["icetime_per_game"] = (
            df_filtered["icetime"] / df_filtered["games_played"] / 60
        ).round(2)

        # Rename I_F_goals to goals
        df_filtered.rename(columns={"I_F_goals": "goals"}, inplace=True)

        # Format season as "YYYY-YYYY" instead of "YYYY, YYYY"
        df_filtered["season"] = df_filtered["season"].astype(str).str.replace(",", "-")

        # Select relevant columns (moving shots per game before goals)
        df_display = df_filtered[
            [
                "season",
                "name",
                "team",
                "position",
                "shots_per_game",
                "goals",
                "icetime_per_game",
            ]
        ]

        # Sort by shots per game (descending order)
        df_display = df_display.sort_values(by="shots_per_game", ascending=False)

        # Apply Streamlit UI modifications
        st.title("NHL Skater Stats Dashboard")
        st.write("Compare Skater Stats Between Two Teams")

        # Custom CSS to increase table width
        st.markdown(
            """
            <style>
                .dataframe { width: 100% !important; }
                [data-testid="stDataFrame"] { overflow: auto; }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Create two wide columns for side-by-side comparison
        col1, col2 = st.columns([1, 1])  # Equal width

        # Get unique teams
        team_list = sorted(df_display["team"].unique())

        # Left column - Team 1 selection and table
        with col1:
            st.subheader("Team 1")
            team_1 = st.selectbox("Select Team 1:", team_list, key="team_1")
            df_team_1 = df_display[df_display["team"] == team_1]
            st.dataframe(df_team_1, use_container_width=True)

        # Right column - Team 2 selection and table
        with col2:
            st.subheader("Team 2")
            team_2 = st.selectbox("Select Team 2:", team_list, key="team_2")
            df_team_2 = df_display[df_display["team"] == team_2]
            st.dataframe(df_team_2, use_container_width=True)

    else:
        st.error(
            f"❌ Missing required columns in the dataset: {required_columns - set(df.columns)}"
        )
else:
    st.error(f"❌ File not found: {os.path.abspath(csv_path)}")
