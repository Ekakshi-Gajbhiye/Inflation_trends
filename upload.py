from google.cloud import storage
import streamlit as st

credentials_info = st.secrets["gcp_service_account"]


client = storage.Client.from_service_account_json("C:/Users/Hp/Desktop/inflation_trends/inflation-trends-8fc563087801.json")
# Initialize GCP Storage Client
client = storage.Client()
bucket = client.bucket("inflation-data-bucket")  # Replace with your bucket name
blob = bucket.blob("raw_data/inflation_data.csv")

# Upload the file
blob.upload_from_filename("inflation_data.csv")
print("Data uploaded successfully to GCS!")
