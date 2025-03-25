import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import joblib
# import numpy as np

# **Commenting out BigQuery client and data fetch**
# from google.cloud import bigquery
# client = bigquery.Client()


data = pd.read_csv('inflation_data.csv')  # Ensure this file exists in your working directory

if data['inflation_for_future'].isnull().sum() > 0:
    print(f" Warning: {data['inflation_for_future'].isnull().sum()} NaN values found in target variable!")
    data['inflation_for_future'] = data['inflation_for_future'].fillna(data['inflation_for_future'].mean())


X = data[['year', 'annual_inflation_rate', 'cumulative_inflation_rate', 'avg_cpi_present']]
y = data['inflation_for_future']

scaler = StandardScaler()
X['year_scaled'] = scaler.fit_transform(X[['year']])
X['year_squared'] = X['year_scaled'] ** 2  # Add a squared feature for better trend analysis

X = X.drop(columns=['year'])

imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

joblib.dump(model, 'inflation_model.pkl')
joblib.dump(scaler, 'scaler.pkl')  # Save the scaler for future use

print(f" Model Training Completed!")
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")
