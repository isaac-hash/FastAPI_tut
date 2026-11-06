#!/usr/bin/env python
"""
eda.py — Launcher for PSS_SCALP_XAUUSDm EDA
Run from the OTI directory:
    python outputs/eda.py

This will re-execute EDA.ipynb and regenerate all outputs.
Requirements: jupyter, pandas, numpy, matplotlib, seaborn, scipy, statsmodels, scikit-learn
"""
import subprocess, sys, os

nb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'EDA.ipynb')
print(f"Executing notebook: {nb_path}")
result = subprocess.run(
    [sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'notebook',
     '--execute', '--inplace', nb_path],
    capture_output=True, text=True
)
print(result.stdout)
if result.returncode != 0:
    print("STDERR:", result.stderr)
    print("\nAlternatively, run: jupyter notebook EDA.ipynb and execute all cells.")
else:
    print("All outputs regenerated successfully.")
