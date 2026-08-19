import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Forecasting Dashboard", layout="wide")
st.title("📈 Sales Forecasting Dashboard")
st.markdown("Prophet vs XGBoost — Store 1, Grocery I")

# Load data
predictions = pd.read_csv('../data/predictions.csv')
predictions['date'] = pd.to_datetime(predictions['date'])

# KPI Cards
col1, col2, col3 = st.columns(3)
mape = ((predictions['sales'] - predictions['predicted']).abs() / predictions['sales']).mean()
col1.metric("Model", "XGBoost")
col2.metric("MAPE", f"{mape:.2%}")
col3.metric("Days Forecasted", len(predictions))

# Actual vs Predicted Chart
fig = px.line(predictions, x='date', y=['sales','predicted'],
              title='Actual vs Predicted Sales',
              labels={'value':'Sales', 'date':'Date'})
st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("Prediction Details")
st.dataframe(predictions)