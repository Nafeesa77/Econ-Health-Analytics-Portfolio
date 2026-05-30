import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("../data/master_econ_data.csv")
df["date"] = pd.to_datetime(df["date"])

# App title
st.title("Economic Dashboard (2024–Today)")
st.write("Interactive dashboard showing CPI, Unemployment, GDP, and Fed Funds Rate.")

# Add dropdown 
st.sidebar.title("Dashboard Controls")
indicator = st.selectbox(
    "Select an indicator:",
    ["cpi", "unemployment_rate", "gdp", "fed_funds_rate"]
)

# Add date range filter
start_date = st.sidebar.date_input("Start date", df["date"].min())
end_date = st.sidebar.date_input("End date", df["date"].max())

df_filtered = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

# Create an interactive Plotly chart
fig = px.line(df, x="date", y=indicator, title=f"{indicator.replace('_', ' ').title()} (2024–Today)")
st.plotly_chart(fig, use_container_width=True)

# Add EHI
st.subheader("Economic Health Index")

fig_ehi = px.line(df, x="date", y="economic_health_index",
                  title="Economic Health Index (2024–Today)")
st.plotly_chart(fig_ehi)

# Add KPI cards
st.subheader("Key Metrics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(label="CPI", value=f"{df_filtered['cpi'].iloc[-1]:.2f}")
kpi2.metric(label="Unemployment Rate", value=f"{df_filtered['unemployment_rate'].iloc[-1]:.2f}%")
kpi3.metric(label="GDP", value=f"${df_filtered['gdp'].iloc[-1]:,.2f}")
kpi4.metric(label="Fed Funds Rate", value=f"{df_filtered['fed_funds_rate'].iloc[-1]:.2f}%")

# Create a 2-collumn layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Economic Health Index")
    fig_ehi = px.line(df_filtered, x="date", y="economic_health_index")
    st.plotly_chart(fig_ehi, use_container_width=True)

with col2:
    st.subheader("GDP vs Unempployment")
    fig_indicator = px.line(df_filtered, x="date", y=["gpd", "unemployment_rate"])
    st.plotly_chart(fig_indicator, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("Data Source: [FRED](https://fred.stlouisfed.org/)")
    st.markdown("Created by Nafeesa Hassanin - Economic Health Analytics Dashboard]")
    
                            