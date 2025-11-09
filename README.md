Solar Challenge Week 0: Cross-Country Solar Farm Analysis
10 Academy: Artificial Intelligence Mastery
Solar Data Discovery: Week 0 Challenge
Kickstart Your AI Mastery with Cross-Country Solar Farm Analysis
Date: November 5 - 12, 2025

Project Overview
This repository is for the Week 0 challenge of the 10 Academy AI Mastery program. The project involves analyzing solar radiation data from Benin, Sierra Leone, and Togo to derive insights for MoonLight Energy Solutions' sustainable solar investments. As an Analytics Engineer, the goal is to perform exploratory data analysis (EDA), clean datasets, compare countries, and recommend high-potential regions based on trends like Global Horizontal Irradiance (GHI), humidity (RH), and wind patterns.
This is a win-win exercise: Build portfolio-worthy experience in Python, Git, EDA, CI/CD, and Streamlit, while preparing for Data Engineering (DE), Financial Analytics (FA), or Machine Learning Engineering (MLE) tracks. Focus on discipline, resilience, and proactivity—ask questions in the community and persist!
Business Objective
Develop strategies to enhance operational efficiency and sustainability via targeted solar investments. Use statistical analysis and EDA to identify key trends (e.g., diurnal GHI peaks, RH impacts on irradiance) and recommend data-driven sites aligning with long-term goals.
Dataset Overview
Data from Solar Radiation Measurement (15-min intervals, ~1 year, QC'd). Key columns:

Timestamp: yyyy-mm-dd hh:mm
Irradiance: GHI/DNI/DHI/ModA/ModB (W/m²)
Weather: Tamb (°C), RH (%), WS/WSgust/WSstdev (m/s), WD/WDstdev (°N), BP (hPa), Precipitation (mm/min)
Other: Cleaning (0/1), TModA/TModB (°C), Comments

Sourced from energydata.info (local data/ only—never commit CSVs).
Topics Covered

Python Programming (task-specific).
GitHub Commands (commits, branching).
Data Understanding & Exploration (EDA).
CI/CD (GitHub Actions).
Streamlit (dashboards).

Facilitators: Yabebal, Kerod, Mahbubah, Filimon.
Key Dates:

Introduction: Nov 5, 9:30 AM UTC.
Interim Submission: Nov 9, 8:00 PM UTC (today—Task 1 summary + Task 2 outline).
Final Submission: Nov 12, 8:00 PM UTC (full work + PDF report).


Task 1: Git & Environment Setup (Completed ✅)
Objective: Establish version control and dev environment.

Repo: Created/cloned solar-challenge-week0 on GitHub.
Venv: Set up with Python 3.13.9 (compatible with 3.12).
Branch/Commits: setup-task branch with 4+ commits (e.g., "init: add .gitignore", "chore: venv setup", "ci: add workflow", "fix: reqs for CI").
Files:
.gitignore: Ignores data/, *.csv, env/, __pycache__/, *.ipynb_checkpoints/.
requirements.txt: pandas, numpy, matplotlib, seaborn, scipy.
.github/workflows/ci.yml: Runs Python version check + pip install -r requirements.txt on push/PR.

CI: Verified green runs (Actions tab).
PR: Merged setup-task to main.
Structure: Matches suggested (notebooks/, src/, tests/, scripts/ with __init__.py/README.md).

KPIs Met: Dev environment ready; proactivity in debugging CI (added reqs.txt for pip success).

Environment Reproduction (Windows-Focused)
Tested on Windows with VS Code. Follow these steps to replicate:

Prerequisites:
Git installed (git-scm.com).
Python 3.12+ (python.org; add to PATH).
VS Code (code.visualstudio.com) + Jupyter extension (Extensions > Search "Jupyter" > Install).

Clone Repo:textgit clone https://github.com/bekonad/solar-challenge-week0.git
cd solar-challenge-week0
Virtual Environment:textpython -m venv env
Activate (Windows):textenv\Scripts\activate(Prompt shows (env); deactivate later with deactivate.)
Install Dependencies:textpython -m pip install --upgrade pip
pip install -r requirements.txt(Verifies: pip list shows pandas 2.3.3, numpy 2.3.4, etc.)
Download Data (Local Only):
Create: mkdir data.
Benin: Download → data/benin.csv.
Sierra Leone: Download → data/sierraleone.csv.
Togo: Download → data/togo.csv.
Verify: python -c "import pandas as pd; print(pd.read_csv('data/benin.csv').shape)" (~35k rows).

Run & Test:
CI: Push to main → Check GitHub Actions (green: deps install).
Notebooks: Open notebooks/benin_eda.ipynb in VS Code > Run all (Shift+Enter).


Troubleshooting (Windows):

PATH issues: Restart VS Code/PowerShell.
Large CSVs: Use low_memory=False in pd.read_csv().


Repository Structure





















































Folder/FilePurpose.github/workflows/ci.ymlCI pipeline (Python setup + pip install)..gitignoreIgnore data/, *.csv, env/, __pycache__/, *.ipynb_checkpoints/.requirements.txtpandas\nnumpy\nmatplotlib\nseaborn\nscipy.README.mdReproduction steps (clone, venv, install).notebooks/EDA .ipynb files (e.g., benin_eda.ipynb).data/Local CSVs only (not committed).reports/Interim/final PDFs.app/Bonus Streamlit (optional).src/Source scripts (__init__.py).tests/Unit tests (__init__.py).scripts/Utilities (__init__.py).

Next Steps & Plan

Task 2 (Data Profiling, Cleaning & EDA): Branches like eda-benin (planned: Z-scores, time series plots, corr heatmap; start post-interim).
Task 3 (Cross-Country Comparison): compare-countries branch (boxplots, ANOVA, summary table).
Bonus (Streamlit Dashboard): dashboard-dev (country select + GHI viz; deploy to Streamlit Cloud).

Interim Submission (Today): GitHub link + PDF report (Task 1 summary, Task 2 outline).
Challenges & Proactivity: Large files—subsample with df.sample(frac=0.1). Shared ref: Git Branching Tutorial.
References

Git/CI: Atlassian Git, GitHub Actions.
Python/EDA: Pandas Docs, SciPy Stats.
Data: ESMAP Solar Measurements.

License: MIT (see LICENSE).
Author: Bekonad | Issues: GitHub Issues.

Task 1 complete—ready for EDA! Persist through the challenge. 🚀
