import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sales Forecast", layout="wide")

st.title("📈 Sales Forecast Dashboard")
st.markdown("See predicted sales for the next 30 days, and how accurate our predictions have been.")

# Load data
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

predictions = pd.read_csv(
    os.path.join(BASE_DIR, '..', 'data', 'predictions_multi.csv')
)

future = pd.read_csv(
    os.path.join(BASE_DIR, '..', 'data', 'future_forecast.csv')
)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
predictions = pd.read_csv(os.path.join(BASE_DIR, '..', 'data', 'predictions_multi.csv'))
future = pd.read_csv(os.path.join(BASE_DIR, '..', 'data', 'future_forecast.csv'))

# Sidebar dropdown
st.sidebar.header("Choose what to view")
combo_options = predictions[['store_nbr','family']].drop_duplicates()
combo_labels = combo_options.apply(lambda x: f"Store {x['store_nbr']} — {x['family'].title()}", axis=1).tolist()
selected = st.sidebar.selectbox("Store & Product", combo_labels)

sel_store = int(selected.split(' ')[1])
sel_family = selected.split('— ')[1].upper()

filtered_pred = predictions[(predictions['store_nbr']==sel_store) & (predictions['family']==sel_family)]
filtered_future = future[(future['store_nbr']==sel_store) & (future['family']==sel_family)]

# KPIs
accuracy = 1 - ((filtered_pred['sales'] - filtered_pred['predicted']).abs() / filtered_pred['sales']).mean()
avg_future = filtered_future['predicted'].mean()
total_future = filtered_future['predicted'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Prediction Accuracy", f"{accuracy:.0%}", help="How close our past predictions were to actual sales")
col2.metric("Expected Daily Sales (Next 30 Days)", f"{avg_future:,.0f} units")
col3.metric("Expected Total Sales (Next 30 Days)", f"{total_future:,.0f} units")

# Trend indicator
last_30_avg = filtered_pred['sales'].mean()
next_30_avg = filtered_future['predicted'].mean()
change = ((next_30_avg - last_30_avg) / last_30_avg) * 100

if change > 0:
    st.success(f"📈 Sales are expected to **increase by {change:.1f}%** next month compared to the last 30 days.")
else:
    st.warning(f"📉 Sales are expected to **decrease by {abs(change):.1f}%** next month compared to the last 30 days.")

# What drives this forecast
st.info("ℹ️ This forecast is based on: **day of the week patterns, recent sales trends, and holidays.**")

st.divider()

tab1, tab2 = st.tabs(["🔮 What's Coming Next", "✅ How Accurate Were We"])

with tab2:
    st.subheader("Actual Sales vs Our Predictions (Last 30 Days)")
    st.caption("The closer the two lines, the more accurate our forecast was.")

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=filtered_pred['date'], y=filtered_pred['sales'],
                               mode='lines+markers', name='Actual Sales',
                               line=dict(color='#2E86DE', width=3)))
    fig1.add_trace(go.Scatter(x=filtered_pred['date'], y=filtered_pred['predicted'],
                               mode='lines+markers', name='Our Prediction',
                               line=dict(color='#FF6B35', width=3, dash='dot')))
    fig1.update_layout(xaxis_title='Date', yaxis_title='Units Sold', legend_title_text='')
    st.plotly_chart(fig1, use_container_width=True)

with tab1:
    st.subheader("Sales Forecast — Next 30 Days")
    st.caption("Solid line: what actually happened. Dashed orange line: what we expect to happen next.")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=filtered_pred['date'], y=filtered_pred['sales'],
                               mode='lines', name='Past Sales', line=dict(color='#4C9AFF')))
    fig2.add_trace(go.Scatter(x=filtered_future['date'], y=filtered_future['predicted'],
                               mode='lines+markers', name='Predicted Future Sales',
                               line=dict(dash='dash', color='#FF8C42')))
    fig2.update_layout(xaxis_title='Date', yaxis_title='Units Sold', legend_title_text='')
    st.plotly_chart(fig2, use_container_width=True)

    # Download button
    csv = filtered_future[['date','predicted']].rename(columns={'predicted':'Predicted Sales', 'date':'Date'}).to_csv(index=False)
    st.download_button("📥 Download This Forecast (CSV)", csv, f"forecast_store{sel_store}_{sel_family}.csv", "text/csv")

    st.caption("Note: This forecast is based on historical patterns. Actual results may vary due to unforeseen events like promotions, supply issues, or unexpected demand shifts.")

st.divider()
st.caption("Forecast generated using historical sales patterns, seasonality, and holiday effects.")