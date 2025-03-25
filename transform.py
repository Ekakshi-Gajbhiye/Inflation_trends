from google.cloud import storage
import pandas as pd
from io import StringIO

client = storage.Client()
bucket_name = "inflation-data-bucket"
file_name = "raw_data/inflation_data.csv"

bucket = client.bucket(bucket_name)
blob = bucket.blob(file_name)
data = blob.download_as_text()

df = pd.read_csv(StringIO(data))

print(df.head())

print(df.isnull().sum())

df.fillna(method="ffill", inplace=True)
df['date'] = pd.to_datetime(df['date'])
df['value'] = df['value'].astype(float)
df['inflation_rate'] = df['value'].pct_change() * 100
df.dropna(inplace=True)

print(df.head())
