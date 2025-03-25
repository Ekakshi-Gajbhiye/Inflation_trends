# Import necessary libraries
import pandas as pd
from google.cloud import bigquery
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Initialize BigQuery client
client = bigquery.Client()

# Fetch data from BigQuery
query = """
SELECT 
  year, 
  annual_inflation_rate, 
  cumulative_inflation_rate, 
  avg_cpi_present, 
  inflation_for_future, 
  future_value
FROM `inflation-trends.inflation_analysis.inflation_data_for_prediction`
ORDER BY year
"""
data = client.query(query).to_dataframe()

# Check for missing values
print("Missing values in data:\n", data.isnull().sum())

# Handle missing values (if any)
# Option 1: Fill missing values with the mean (or median) of each column
data = data.fillna(data.mean())

# Option 2: Drop rows with missing values (if you want to ignore missing data)
# data = data.dropna()

# Feature selection (you can modify this as per your needs)
X = data[[ 'cumulative_inflation_rate', 'avg_cpi_present']]
y = data['inflation_for_future']

# Normalize the features (optional but often recommended for ML models)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-Test split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Now data is ready for the next step (building a machine learning model)
print("Preprocessing complete. Data ready for model training.")
