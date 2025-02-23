import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import io  # Import io for StringIO
from datetime import datetime
import pytz

# MoneyPuck website URL
URL = "https://moneypuck.com/data.htm"

# Headers to pretend we're a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# File path
DATA_FOLDER = "data"
FILENAME = "24-25_skaters_data.csv"
FILE_PATH = os.path.join(DATA_FOLDER, FILENAME)


def get_csv_url():
    """Scrapes MoneyPuck to find the skaters' data CSV link for the latest season."""
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching the webpage: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the link containing "2024" & "skaters.csv"
    link = soup.find(
        "a", href=lambda href: href and "2024" in href and "skaters.csv" in href
    )

    if link:
        csv_url = "https://moneypuck.com/" + link["href"]
        print(f"🔗 Found latest CSV URL: {csv_url}")
        return csv_url
    else:
        print("❌ CSV link for 2024-2025 season not found.")
        return None


def download_csv(csv_url):
    """Downloads the CSV file and saves it as 24-25_skaters_data.csv after validation."""
    if not csv_url:
        print("❌ No CSV URL provided.")
        return

    os.makedirs(DATA_FOLDER, exist_ok=True)  # Ensure the data folder exists

    try:
        # Send request with User-Agent
        response = requests.get(csv_url, headers=HEADERS)
        response.raise_for_status()

        # Load into Pandas to verify data
        df = pd.read_csv(io.StringIO(response.text))  # ✅ Fixed issue

        # Check if the season column contains 2024
        if (
            "season" not in df.columns
            or not df["season"].astype(str).str.contains("2024").any()
        ):
            print("⚠️ Warning: The downloaded CSV does NOT contain 2024 data.")
            return

        # Delete old file if it exists
        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)

        # Save CSV file
        with open(FILE_PATH, "wb") as file:
            file.write(response.content)

        # Log the update time in Eastern Time
        utc_now = datetime.utcnow()
        eastern = pytz.timezone("America/New_York")
        et_now = (
            utc_now.replace(tzinfo=pytz.utc)
            .astimezone(eastern)
            .strftime("%Y-%m-%d %I:%M:%S %p ET")
        )

        print(f"✅ Data saved to {FILE_PATH} at {et_now}")

    except Exception as e:
        print(f"❌ Error downloading or saving the CSV: {e}")


if __name__ == "__main__":
    csv_url = get_csv_url()
    if csv_url:
        download_csv(csv_url)
    else:
        print("❌ Failed to retrieve CSV URL.")
