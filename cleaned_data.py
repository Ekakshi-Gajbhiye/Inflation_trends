from transform import df
from google.cloud import bigquery
import pandas as pd

# Initialize BigQuery client
bq_client = bigquery.Client()

# Define dataset and table IDs
project_id = "inflation-trends"  # Change if needed
dataset_name = "inflation_analysis"
table_name = "inflation_data"
table_id = f"{project_id}.{dataset_name}.{table_name}"

# Load your transformed DataFrame (Make sure df is already created)
# Keep only required columns
df = df[['realtime_start', 'date', 'value', 'inflation_rate']]
df['realtime_start'] = pd.to_datetime(df['realtime_start']).dt.date
df['date'] = pd.to_datetime(df['date']).dt.date
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df['inflation_rate'] = pd.to_numeric(df['inflation_rate'], errors='coerce')

# Delete the table if schema mismatch occurs
bq_client.delete_table(table_id, not_found_ok=True)

# Define correct schema for BigQuery
schema = [
    bigquery.SchemaField("realtime_start", "DATE"),
    bigquery.SchemaField("date", "DATE"),
    bigquery.SchemaField("value", "FLOAT"),
    bigquery.SchemaField("inflation_rate", "FLOAT"),
]

# Recreate the table with the correct schema
table = bigquery.Table(table_id, schema=schema)
bq_client.create_table(table)
print(f"✅ Table {table_id} created successfully!")

# Upload the DataFrame to BigQuery
job = bq_client.load_table_from_dataframe(df, table_id, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"))
job.result()  # Wait for job to complete

print("✅ Data uploaded successfully!")
