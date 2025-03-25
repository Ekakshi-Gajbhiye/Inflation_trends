import pandas as pd
from google.cloud import bigquery
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

# Setup BigQuery client
client = bigquery.Client()

# Fetch data from BigQuery
query = """
SELECT 
    year,
    annual_inflation_rate, 
    cumulative_inflation_rate, 
    avg_cpi_present,
    inflation_for_future
FROM `inflation-trends.inflation_analysis.inflation_data_for_prediction`
"""
data = client.query(query).to_dataframe()


# **✅ Check & Fix NaN in Target Variable**
if data['inflation_for_future'].isnull().sum() > 0:
    print(f"⚠️ Warning: {data['inflation_for_future'].isnull().sum()} NaN values found in target variable!")
    data['inflation_for_future'] = data['inflation_for_future'].fillna(data['inflation_for_future'].mean())

# **✅ Feature Engineering**
X = data[['year', 'annual_inflation_rate', 'cumulative_inflation_rate', 'avg_cpi_present']]
y = data['inflation_for_future']

# **✅ Scale the Year Feature**
scaler = StandardScaler()
X['year_scaled'] = scaler.fit_transform(X[['year']])
X['year_squared'] = X['year_scaled'] ** 2  # Add a squared feature for better trend analysis

# Drop the original 'year' column (we now have `year_scaled` and `year_squared`)
X = X.drop(columns=['year'])

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test data
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# **✅ Save Model & Scaler**
joblib.dump(model, 'inflation_model.pkl')
joblib.dump(scaler, 'scaler.pkl')  # Save the scaler for future use

# Print evaluation metrics
print(f"✅ Model Training Completed!")
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

