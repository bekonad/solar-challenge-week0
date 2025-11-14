import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  # Add root to path

from src.data_loader import SolarDataLoader

if __name__ == "__main__":
    loader = SolarDataLoader('data/benin.csv')
    df = loader.load_data()
    df_clean = loader.clean_data()
    print("EDA run complete. Clean GHI mean:", df_clean['GHI'].mean())