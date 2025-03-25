from google.cloud import storage
import pandas as pd
from io import StringIO

# Initialize GCS client
client = storage.Client()
bucket_name = "inflation-data-bucket"
file_name = "raw_data/inflation_data.csv"

# Load file from GCS
bucket = client.bucket(bucket_name)
blob = bucket.blob(file_name)
data = blob.download_as_text()

# Read into a DataFrame
df = pd.read_csv(StringIO(data))

# Display data
print(df.head())


# Check for missing values
print(df.isnull().sum())

# Fill missing values with forward-fill method
df.fillna(method="ffill", inplace=True)


# Convert 'date' to datetime format
df['date'] = pd.to_datetime(df['date'])

# Convert 'value' to float
df['value'] = df['value'].astype(float)


df['inflation_rate'] = df['value'].pct_change() * 100

# Drop the first row (NaN in inflation_rate)
df.dropna(inplace=True)


print(df.head())
