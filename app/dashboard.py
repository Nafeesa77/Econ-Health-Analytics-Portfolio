import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv(".../data/master_econ_data.csv")
df["date"] = pd.to_datetime(df["date"])

# App title
st.title("Economic Dashboard (2024-Today)")
st.write("Interactive dashboard showing CPI, Unemployment Rate, GDP, and Fed Funds Rate.")

# Sidebar controls
st.sidebar.title("Dashboard Controls")
indicators = st.sidebar.selectbox(
    "Select an Indicator",
    ["cpi", "unemployment_rate", "gdp", "fed_funds_rate"]
)

# Date ranger filter
start_date = st.sidebar.date_input("Start Date", df["date"].min())
end_date = st.sidebar.date_input("End Date", df["date"].max())
df_filtered = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

# Main indicator chart
fig = px.line(df_filtered, x="date", y=indicators, title=f"{indicators.replace('_', ' ').title()} (Filtered)")
st.plotly_chart(fig, use_container_width=True)

# KPI cards
st.subheader("Key Metrics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(label="CPI", value=f"{df_filtered['cpi'].iloc[-1]:.2f}", delta=f"{df_filtered['cpi'].pct_change().iloc[-1]*100:.2f}%")
kpi2.metric(label="Unemployment Rate", value=f"{df_filtered['unemployment_rate'].iloc[-1]:.2f}%", delta=f"{df_filtered['unemployment_rate'].pct_change().iloc[-1]*100:.2f}%")
kpi3.metric(label="GDP", value=f"${df_filtered['gdp'].iloc[-1]:,.2f}", delta=f"{df_filtered['gdp'].pct_change().iloc[-1]*100:.2f}%")
kpi4.metric(label="Fed Funds Rate", value=f"{df_filtered['fed_funds_rate'].iloc[-1]:.2f}%", delta=f"{df_filtered['fed_funds_rate'].pct_change().iloc[-1]*100:.2f}%")

# Two column layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Economic Health Index")
    fig_ehi = px.line(df_filtered, x="date", y="economic_health_index")
    st.plotly_chart(fig_ehi, use_container_width=True)

with col2:
    st.subheader("GDP vs Unemployment")
    fig_combo = px.line(df_filtered, x="date", y=["gdp", "unemployment_rate"])
    st.plotly_chart(fig_combo, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Data Soure: [FRED](https://fred.stlouisfed.org/)")
st.markdown("Created by Nafeesa Hassanin - Economic Health Index")

