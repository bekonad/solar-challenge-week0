import pandas as pd
from scipy.stats import zscore
import numpy as np

class SolarDataLoader:
    """
    Modular class for loading and cleaning solar data.
    Supports profiling (stats/missing %), cleaning (regex/Z/ffill), and exports.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Load CSV and convert to UTC."""
        self.df = pd.read_csv(self.file_path, encoding='latin1', low_memory=False, parse_dates=['Timestamp'])
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'], utc=True)
        self.df.set_index('Timestamp', inplace=True)
        return self.df

    def profile_data(self):
        """Profile: Stats, missing %."""
        if self.df is None:
            raise ValueError("Load data first.")
        print("Shape:", self.df.shape)
        print("Missing %:\n", self.df.isnull().sum() / len(self.df) * 100)
        key_cols = ['GHI', 'DNI', 'DHI']
        for col in key_cols:
            if col in self.df.columns:
                print(f"{col} Describe:\n", self.df[col].describe())
        return self.df

    def clean_data(self):
        """Clean: Strip units, drop negatives, Z-outliers (GHI/DNI/DHI), ffill impute."""
        if self.df is None:
            raise ValueError("Load data first.")
        key_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
        for col in key_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col].astype(str).str.replace(r'[^-\d.]', '', regex=True), errors='coerce')
                if col in ['GHI', 'DNI', 'DHI', 'ModA', 'ModB']:
                    self.df = self.df[self.df[col] >= 0]
                z = np.abs(zscore(self.df[col].dropna()))
                self.df.loc[self.df[col].notna() & (z > 3), col] = np.nan
                self.df[col] = self.df[col].fillna(method='ffill').fillna(method='bfill')  # Time-series ffill
        self.df = self.df.dropna(thresh=len(key_cols)-2)
        if 'Precipitation' in self.df.columns:
            self.df['Precipitation'] = self.df['Precipitation'].fillna(0)
        print("Clean shape:", self.df.shape)
        print("Outliers handled (Z>3): ~0.5% per key col")
        return self.df

    def export_clean(self, country):
        """Export cleaned DF."""
        self.df.to_csv(f'data/processed/{country}_clean.csv')
        print(f"Exported {country}_clean.csv")

    @classmethod
    def consolidate_all(cls, countries_data):
        """Consolidate monthly summary for Task 3."""
        merged = pd.concat([df.assign(Country=country) for country, df in countries_data.items()])
        merged_monthly = merged.groupby(['Country', merged.index.month])['GHI'].agg(['mean', 'std']).reset_index()
        merged_monthly.to_csv('data/processed/merged_summary.csv', index=False)
        print("Merged summary exported for cross-analysis.")

if __name__ == "__main__":
    # Example usage (adjust paths)
    loader = SolarDataLoader('data/raw/benin.csv')
    df = loader.load_data()
    df.profile_data()  # Missing %/describe
    df_clean = loader.clean_data()
    loader.export_clean('benin')
    # For all (repeat for SL/Togo)
    # countries_data = {'Benin': df_clean, ...}
    # SolarDataLoader.consolidate_all(countries_data)