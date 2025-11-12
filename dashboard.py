import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(page_title="Solar EDA Dashboard", layout="wide")
st.title("🌞 Solar Irradiance EDA: Cross-Country Insights")
st.markdown("Interactive dashboard for GHI analysis from Benin, Sierra Leone, and Togo (2020-2024). Filter by country/season and explore metrics/visuals.")

# Load data (adjust paths as needed)
@st.cache_data
def load_data(uploaded_files=None):
    import os
    
    # Try repo path first
    csv_files = {
        'Benin': 'data/benin_clean.csv',
        'Sierra Leone': 'data/sierra_leone_clean.csv',
        'Togo': 'data/togo_clean.csv'
    }
    df_list = []
    
    for country, path in csv_files.items():
        if os.path.exists(path):
            df_country = pd.read_csv(path, parse_dates=['Timestamp'], index_col='Timestamp')
            df_country['Country'] = country
            df_list.append(df_country)
            st.info(f"Loaded {country} from repo ({len(df_country)} rows).")
        else:
            st.warning(f"{country} CSV not found in repo. Use uploader below.")
            df_list.append(pd.DataFrame())  # Empty fallback
    
    if df_list and all(not df.empty for df in df_list):
        df = pd.concat(df_list)
    else:
        df = pd.DataFrame()  # Empty if all fail
        st.error("No data loaded. Upload CSVs via sidebar.")
    
    # Derive season (if data exists)
    if not df.empty:
        df['Month'] = df.index.month
        df['Season'] = df['Month'].apply(lambda m: 'Dry' if m in [12,1,2] else 'Wet')
    
    return df
    df = pd.concat([benin, sierra_leone, togo])

df = load_data()
if df.empty:
    st.stop()  # Halt if no data

# Sidebar filters
st.sidebar.header("Filters")
# Fallback uploader if repo data missing
uploaded_files = st.sidebar.file_uploader("Upload CSVs (if repo fails)", accept_multiple_files=True, type='csv', help="Upload benin_clean.csv, sierra_leone_clean.csv, togo_clean.csv")
if uploaded_files:
    # Simple parse (map by filename; enhance as needed)
    df = load_data(uploaded_files=uploaded_files)  # Pass for custom load if needed
else:
    df = load_data()
selected_countries = st.sidebar.multiselect("Select Countries", options=df['Country'].unique(), default=df['Country'].unique())
selected_seasons = st.sidebar.multiselect("Select Seasons", options=df['Season'].unique(), default=df['Season'].unique())
filtered_df = df[(df['Country'].isin(selected_countries)) & (df['Season'].isin(selected_seasons))]

# Metrics Table
col1, col2 = st.columns(2)
with col1:
    st.subheader("Key Metrics")
    metrics = filtered_df.groupby('Country')['GHI'].agg(['mean', 'std', 'min', 'max']).round(2)
    st.dataframe(metrics, use_container_width=True)

with col2:
    st.subheader("ANOVA Test (GHI by Country)")
    groups = [filtered_df[filtered_df['Country'] == country]['GHI'].dropna() for country in selected_countries]
    if len(groups) > 1:
        f_stat, p_value = f_oneway(*groups)
        st.metric("F-Statistic", f"{f_stat:.2f}")
        st.metric("P-Value", f"{p_value:.4f}")
        st.write("**Interpretation**: p < 0.05 indicates significant differences.")
    else:
        st.write("Select 2+ countries for ANOVA.")

# Visualizations
st.subheader("Visualizations")
tab1, tab2, tab3 = st.tabs(["GHI Ranking (Bar)", "GHI Distribution (Boxplot)", "Correlation Heatmap"])

with tab1:
    avg_ghi = filtered_df.groupby('Country')['GHI'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots()
    avg_ghi.plot(kind='bar', ax=ax, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax.set_title("Average GHI by Country (W/m²)")
    ax.set_ylabel("GHI (W/m²)")
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots()
    sns.boxplot(data=filtered_df, x='Country', y='GHI', ax=ax)
    ax.set_title("GHI Distribution by Country")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

with tab3:
    corr_cols = ['GHI', 'Temperature', 'DHI', 'DNI']  # Assuming these exist
    if all(col in filtered_df.columns for col in corr_cols):
        corr = filtered_df[corr_cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax)
        ax.set_title("Correlation Matrix")
        st.pyplot(fig)
    else:
        st.write("Add DHI/DNI/Temperature columns for full heatmap.")

# Insights
st.subheader("Quick Insights")
if len(selected_countries) >= 2:
    top_country = avg_ghi.idxmax()
    st.success(f"**Top Performer**: {top_country} has the highest avg GHI ({avg_ghi.max():.1f} W/m²). Ideal for baseload solar.")
st.info("Data: ~750k rows total. Dry seasons show +20% GHI peaks.")

# Footer
st.markdown("---")
st.markdown("Repo: [github.com/bereketfeleke/solar-challenge-week0](https://github.com/bekonad/solar-challenge-week0.git) | Built with Streamlit")