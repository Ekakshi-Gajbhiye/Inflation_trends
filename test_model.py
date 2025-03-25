import numpy as np
import joblib

# Load the trained model and scaler
model = joblib.load("inflation_model.pkl")
scaler = joblib.load("scaler.pkl")

def predict_inflation(year, annual_inflation_rate, cumulative_inflation_rate, avg_cpi_present):
    # Reshape year for scaler
    year_scaled = scaler.transform(np.array(year).reshape(-1, 1)).flatten()[0]  # Extract scalar
    year_squared = (year_scaled ** 2).flatten()[0]  # Extract scalar

    # Create input feature array (should be a 1D list, not nested array)
    input_features = np.array([year_scaled, year_squared, annual_inflation_rate, cumulative_inflation_rate, avg_cpi_present]).reshape(1, -1)

    # Predict inflation rate
    predicted_rate = model.predict(input_features)[0]
    return predicted_rate

# Example test
year = 2060
annual_inflation_rate = 3.5
cumulative_inflation_rate = 50.0
avg_cpi_present = 250.0

predicted_rate = predict_inflation(year, annual_inflation_rate, cumulative_inflation_rate, avg_cpi_present)
print(f"📊 Predicted Inflation Rate for {year}: {predicted_rate:.2f}%")
