# scripts/compare.py
import pandas as pd
import plotly.express as px
from scipy.stats import f_oneway
from pathlib import Path

PROCESSED_DIR = Path("data") / "processed"
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

def compare_countries():
    files = list(PROCESSED_DIR.glob("*_clean.csv"))
    if not files:
        print("No cleaned files found! Run: python scripts/clean_data.py")
        return

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        country = f.stem.replace("_clean", "").capitalize()
        df['Country'] = country
        dfs.append(df)

    data = pd.concat(dfs, ignore_index=True)

    # === Summary Table ===
    summary = data.groupby('Country')[['GHI', 'DNI', 'DHI']].agg(['mean', 'median', 'std']).round(2)
    print("\n=== SUMMARY STATISTICS ===")
    print(summary)

    # === Boxplot ===
    fig1 = px.box(data, x='Country', y='GHI', color='Country', title='GHI Distribution by Country')
    fig1.write_html(REPORTS_DIR / "ghi_boxplot.html")
    fig1.show()

    # === ANOVA ===
    groups = [data[data['Country'] == c]['GHI'] for c in data['Country'].unique()]
    f_stat, p_val = f_oneway(*groups)
    print(f"\nANOVA (GHI): F={f_stat:.2f}, p-value={p_val:.2e}")

    # === Ranking Bar ===
    ranking = summary['GHI']['mean'].sort_values(ascending=False)
    fig2 = px.bar(x=ranking.index, y=ranking.values,
                  title="Average GHI by Country",
                  labels={'x': 'Country', 'y': 'Mean GHI (W/m²)'})
    fig2.show()

if __name__ == "__main__":
    compare_countries()