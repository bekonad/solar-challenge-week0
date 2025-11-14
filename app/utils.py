# app/utils.py
import pandas as pd
from pathlib import Path

def load_all_data():
    path = Path("data") / "processed"
    dfs = []
    for csv in path.glob("*_clean.csv"):
        df = pd.read_csv(csv)
        df['Country'] = csv.stem.replace("_clean", "").capitalize()
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()