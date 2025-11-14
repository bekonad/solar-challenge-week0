# app/main.py
import pandas as pd
import streamlit as st
import plotly.express as px
from utils import load_all_data

st.set_page_config(page_title="Solar Dashboard", layout="wide")
st.title("MoonLight Energy: Solar Site Selection")
st.markdown("**Benin • Sierra Leone • Togo**")

df = load_all_data()
if df.empty:
    st.error("No data! Run `python scripts/clean_data.py` first.")
    st.stop()

# Sidebar
countries = st.sidebar.multiselect("Countries", df['Country'].unique(), df['Country'].unique())
metric = st.sidebar.selectbox("Metric", ['GHI', 'DNI', 'DHI', 'Tamb', 'RH'])

filtered = df[df['Country'].isin(countries)]

# Plots
col1, col2 = st.columns(2)
with col1:
    fig = px.box(filtered, x='Country', y=metric, color='Country')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.write("### Stats")
    st.dataframe(filtered.groupby('Country')[metric].agg(['mean', 'median', 'std']).round(2))

# Time series
daily = filtered.copy()
daily['Date'] = pd.to_datetime(filtered['Timestamp']).dt.date
daily_avg = daily.groupby(['Country', 'Date'])['GHI'].mean().reset_index()
fig_line = px.line(daily_avg, x='Date', y='GHI', color='Country', title="Daily GHI Trend")
st.plotly_chart(fig_line, use_container_width=True)

# Recommendation
st.success("""
**Recommendation**:  
**Invest in Togo** – highest stable GHI.  
**Benin** – low variability, easy maintenance.  
Avoid large-scale in Sierra Leone due to cloud variance.
""")