import numpy as np
import joblib

model = joblib.load("inflation_model.pkl")
scaler = joblib.load("scaler.pkl")

def predict_inflation(year, annual_inflation_rate, cumulative_inflation_rate, avg_cpi_present):
    
    year_scaled = scaler.transform(np.array(year).reshape(-1, 1)).flatten()[0]  # Extract scalar
    year_squared = (year_scaled ** 2).flatten()[0]  

    input_features = np.array([year_scaled, year_squared, annual_inflation_rate, cumulative_inflation_rate, avg_cpi_present]).reshape(1, -1)

    predicted_rate = model.predict(input_features)[0]
    return predicted_rate

year = 2060
annual_inflation_rate = 3.5
cumulative_inflation_rate = 50.0
avg_cpi_present = 250.0

predicted_rate = predict_inflation(year, annual_inflation_rate, cumulative_inflation_rate, avg_cpi_present)
print(f" Predicted Inflation Rate for {year}: {predicted_rate:.2f}%")
