import requests
import pandas as pd
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
FRED_API_KEY = st.secrets["fred_api"]["api_key"]

if not FRED_API_KEY:
    raise ValueError("API Key not found! Set FRED_API_KEY in environment variables.")

# URL for CPI (Consumer Price Index)
url = f"https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={FRED_API_KEY}&file_type=json"

# Fetch data
response = requests.get(url)
data = response.json()

# Convert to DataFrame
inflation_data = pd.DataFrame(data["observations"])
inflation_data["value"] = inflation_data["value"].astype(float)

# Save locally
inflation_data.to_csv("inflation_data.csv", index=False)
print("Data saved successfully!")
#print(json.dumps(data, indent=4))