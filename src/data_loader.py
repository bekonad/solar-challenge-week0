import pandas as pd
from scipy import stats
import os

def clean_solar(file_path, country):
    df = pd.read_csv(file_path, low_memory=False, dtype_backend='pyarrow')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], utc=True)
    df.set_index('Timestamp', inplace=True)
    key_cols = ['GHI', 'DNI', 'DHI']
    for col in key_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[^-\d.]', ''), errors='coerce')
            df[col] = df[col].clip(lower=0)  # No negatives
            df[col] = df[col].fillna(method='ffill').fillna(method='bfill')  # Impute <5%
            z_scores = stats.zscore(df[col].dropna())
            df[col] = df[col].where(abs(z_scores) < 3, np.nan).fillna(method='ffill')  # Z-clip
    df.to_csv(f'data/processed/{country}_clean.csv')
    print(f"Cleaned {country}: {df.shape}, GHI mean {df['GHI'].mean():.1f}")
    return df

# Run for each
benin_clean = clean_solar('data/raw/benin.csv', 'benin')
sl_clean = clean_solar('data/raw/sierra_leone.csv', 'sierra_leone')
togo_clean = clean_solar('data/raw/togo.csv', 'togo')

# Consolidated
merged = pd.concat([benin_clean.assign(Country='Benin'), sl_clean.assign(Country='Sierra Leone'), togo_clean.assign(Country='Togo')])
merged_monthly = merged.groupby(['Country', merged.index.month])['GHI'].agg(['mean', 'std']).reset_index()
merged_monthly.to_csv('data/processed/merged_summary.csv', index=False)
print("Merged summary exported.")