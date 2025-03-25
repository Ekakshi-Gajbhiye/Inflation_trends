import streamlit as st
import numpy as np
import pandas as pd
import joblib
import plotly.express as px


model = joblib.load("inflation_model.pkl")
scaler = joblib.load("scaler.pkl")

# Commented out BigQuery client and data fetch for now
# from google.cloud import bigquery
# client = bigquery.Client()

# Load data (read from local file)
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("inflation_data.csv")
        return df
    except Exception as e:
        st.error(f"Error loading local data: {e}")
        return pd.DataFrame()

data = load_data()

def calculate_future_value(present_value, rate, years):
    return present_value * ((1 + (rate / 100)) ** years)

# Function to predict inflation rate & calculate future money value
def predict_inflation(year, present_value):
    # Get past 5 years' data to compute moving averages
    recent_years = data[data['year'] < year].tail(5)

    if not recent_years.empty:
        annual_inflation_rate = recent_years['annual_inflation_rate'].mean()
        cumulative_inflation_rate = recent_years['cumulative_inflation_rate'].mean()
        avg_cpi_present = recent_years['avg_cpi_present'].mean()
    else:
        
        annual_inflation_rate = 5.0  
        cumulative_inflation_rate = 50.0
        avg_cpi_present = 200.0

    year_scaled = scaler.transform(np.array(year).reshape(-1, 1)).flatten()[0]
    year_squared = (year_scaled ** 2).flatten()[0]

    input_features = np.array([year_scaled, year_squared, annual_inflation_rate, cumulative_inflation_rate, avg_cpi_present]).reshape(1, -1)
    predicted_rate = model.predict(input_features)[0]

    last_year = data['year'].max()
    years_ahead = year - last_year
    predicted_cumulative_inflation = cumulative_inflation_rate + (predicted_rate * years_ahead)

    future_value = calculate_future_value(present_value, predicted_rate, years_ahead)

    return predicted_rate, annual_inflation_rate, predicted_cumulative_inflation, avg_cpi_present, future_value


st.title("Inflation & Future Money Value Prediction (INR)")

year = st.number_input("Enter Year for Prediction", min_value=2025, max_value=2100, step=1, format="%d")
present_value = st.number_input("Enter Present Money Value (₹)", min_value=1.0, step=1.0, format="%.2f")

if st.button("Predict Inflation & Money Value"):
    predicted_rate, ann_inf, pred_cum_inf, avg_cpi, future_value = predict_inflation(year, present_value)

    st.subheader(f"Predicted Inflation Rate for {year}: **{predicted_rate:.2f}%**")
    st.write(f"Annual Inflation Rate (Avg Last 5 Years): **{ann_inf:.2f}%**")
    st.write(f"Predicted Cumulative Inflation Rate: **{pred_cum_inf:.2f}%**")
    st.write(f"Average CPI: **{avg_cpi:.2f}**")
    st.subheader(f"Future Money Value in {year}: **₹{future_value:,.2f}**")

    data_updated = data.copy()
    new_row = pd.DataFrame({"year": [year], "cumulative_inflation_rate": [pred_cum_inf]})
    data_updated = pd.concat([data_updated, new_row], ignore_index=True)

    st.subheader("Inflation Trends Over Time (Including Prediction)")
    fig = px.line(data_updated, x="year", y="cumulative_inflation_rate", title="Cumulative Inflation Rate Over Time")
    fig.update_traces(line_color='blue')
    fig.update_layout(xaxis_title="Year", yaxis_title="Cumulative Inflation Rate (%)")
    st.plotly_chart(fig)
