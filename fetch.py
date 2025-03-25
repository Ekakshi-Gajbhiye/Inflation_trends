import requests
import pandas as pd
import json
import os 
from dotenv import load_dotenv

load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

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