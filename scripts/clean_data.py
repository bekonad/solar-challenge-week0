# scripts/clean_data.py
import pandas as pd
import numpy as np
from scipy import stats
import os
from pathlib import Path

# ------------------------------------------------------------------
# CONFIGURATION – change only if you move folders
# ------------------------------------------------------------------
RAW_DIR = Path("data") / "raw"
PROCESSED_DIR = Path("data") / "processed"

# create folders if they do not exist
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_and_clean(country: str,
                   raw_dir: Path = RAW_DIR,
                   out_dir: Path = PROCESSED_DIR) -> pd.DataFrame:
    """
    Load raw CSV → clean → save to processed folder.
    Returns the cleaned DataFrame.
    """
    raw_path = raw_dir / f"{country}.csv"
    if not raw_path.is_file():
        raise FileNotFoundError(
            f"Raw file not found: {raw_path}\n"
            "   • Put the original challenge CSV into data/raw/"
        )

    print(f"Loading {country.upper()} raw data from {raw_path}")
    df = pd.read_csv(raw_path)

    # ------------------------------------------------------------------
    # BASIC PRE-PROCESSING
    # ------------------------------------------------------------------
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna(subset=["Timestamp"]).copy()

    key_cols = ["GHI", "DNI", "DHI", "ModA", "ModB", "WS", "WSgust"]

    # ------------------------------------------------------------------
    # OUTLIER REMOVAL (Z-score > 3)
    # ------------------------------------------------------------------
    z = np.abs(stats.zscore(df[key_cols], nan_policy="omit"))
    mask = (z < 3).all(axis=1)
    df_clean = df.loc[df.index[mask]].copy()

    # ------------------------------------------------------------------
    # IMPUTE MISSING VALUES WITH MEDIAN
    # ------------------------------------------------------------------
    for col in key_cols:
        median_val = df_clean[col].median()
        df_clean[col] = df_clean[col].fillna(median_val)

    # ------------------------------------------------------------------
    # SAVE CLEANED FILE
    # ------------------------------------------------------------------
    out_path = out_dir / f"{country}_clean.csv"
    df_clean.to_csv(out_path, index=False)
    print(f"Cleaned data saved → {out_path} ({len(df_clean):,} rows)")

    return df_clean


# ------------------------------------------------------------------
# RUN FOR ALL COUNTRIES (only when executed directly)
# ------------------------------------------------------------------
if __name__ == "__main__":
    countries = ["benin", "sierraleone", "togo"]
    for c in countries:
        try:
            load_and_clean(c)
        except FileNotFoundError as e:
            print(e)
            print("   → Skipping this country.\n")