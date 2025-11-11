import pandas as pd
from scipy.stats import zscore
import numpy as np

class SolarDataLoader:
    """
    Modular class for loading and cleaning solar data.
    Docstring for readability.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Load CSV with fixes."""
        self.df = pd.read_csv(self.file_path, encoding='latin1', low_memory=False, parse_dates=['Timestamp'])
        self.df.set_index('Timestamp', inplace=True)
        return self.df

    def clean_data(self):
        """Clean: Strip units, drop negatives, Z-outliers, impute medians."""
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
                self.df[col] = self.df[col].fillna(self.df[col].median())
        self.df = self.df.dropna(thresh=len(key_cols)-2)
        if 'Precipitation' in self.df.columns:
            self.df['Precipitation'] = self.df['Precipitation'].fillna(0)
        return self.df

if __name__ == "__main__":
    loader = SolarDataLoader('data/benin.csv')  # Fixed path
    df = loader.load_data()
    df_clean = loader.clean_data()
    print("Clean shape:", df_clean.shape)