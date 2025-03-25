from google.cloud import storage
import streamlit as st

credentials_info = st.secrets["gcp_service_account"]


client = storage.Client.from_service_account_json["gcp_service_account"]
# Initialize GCP Storage Client
client = storage.Client()
bucket = client.bucket("inflation-data-bucket")  
blob = bucket.blob("raw_data/inflation_data.csv")

blob.upload_from_filename("inflation_data.csv")
print("Data uploaded successfully to GCS!")
