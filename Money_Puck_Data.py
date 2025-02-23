import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import pytz  # Import pytz for timezone conversion

# MoneyPuck website URL
URL = "https://moneypuck.com/data.htm"

# Headers to pretend we're a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def get_csv_url():
    """Scrapes MoneyPuck to find the skaters' data CSV link."""
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the link containing skaters.csv
    link = soup.find("a", href=lambda href: href and "skaters.csv" in href)

    if link:
        return "https://moneypuck.com/" + link["href"]
    else:
        print("CSV link not found.")
        return None


def download_csv(csv_url):
    """Downloads the CSV file and saves it as 24-25_skaters_data.csv."""
    if not csv_url:
        print("No CSV URL provided.")
        return

    os.makedirs("data", exist_ok=True)  # Ensure the data folder exists

    try:
        # Send request with User-Agent
        response = requests.get(csv_url, headers=HEADERS)
        response.raise_for_status()

        # Save CSV file
        filename = "data/24-25_skaters_data.csv"
        with open(filename, "wb") as file:
            file.write(response.content)

        # Log the update time in Eastern Time
        utc_now = datetime.utcnow()
        eastern = pytz.timezone("America/New_York")
        et_now = (
            utc_now.replace(tzinfo=pytz.utc)
            .astimezone(eastern)
            .strftime("%Y-%m-%d %I:%M:%S %p ET")
        )

        print(f"✅ Data saved to {filename} at {et_now}")

    except Exception as e:
        print(f"Error downloading or saving the CSV: {e}")


if __name__ == "__main__":
    csv_url = get_csv_url()
    if csv_url:
        print(f"🔗 Found CSV URL: {csv_url}")
        download_csv(csv_url)
    else:
        print("❌ Failed to retrieve CSV URL.")
