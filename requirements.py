"""
requirements.py
Helper script to install all required dependencies into your active Python virtual environment.
Run with:
    python requirements.py
"""

import sys
import subprocess
from pathlib import Path

# Packages required for FastAPI web app and EDA notebook analysis
PACKAGES = [
    # FastAPI & Web server
    "fastapi[standard]>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "jinja2>=3.1.4",
    # Data Analysis & Modeling
    "numpy>=1.26.0",
    "pandas>=2.2.0",
    "scipy>=1.13.0",
    "statsmodels>=0.14.0",
    "scikit-learn>=1.5.0",
    # Visualization
    "matplotlib>=3.9.0",
    "seaborn>=0.13.0",
    # Jupyter Notebook Support
    "ipykernel>=6.29.0",
    "notebook>=7.2.0",
]

def is_virtual_env() -> bool:
    """Check if Python is running inside a virtual environment."""
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)

def main():
    print("=" * 60)
    print("📦 FastApi & EDA Package Installer")
    print(f"🐍 Python Executable: {sys.executable}")
    print(f"📁 Environment Path:  {sys.prefix}")
    print("=" * 60)

    if not is_virtual_env():
        print("⚠️  Warning: You do not appear to be running inside a virtual environment.")
        print("   It is recommended to activate your virtual environment (.venv) first.")
        confirm = input("   Do you want to proceed anyway? (y/n): ").strip().lower()
        if confirm != "y":
            print("Installation aborted.")
            return

    # Check if requirements.txt exists in the same directory
    req_file = Path(__file__).resolve().parent / "requirements.txt"

    print("\n[1/2] Upgrading pip...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=False)

    print("\n[2/2] Installing required packages...")
    if req_file.exists():
        print(f"📄 Found {req_file.name}, installing from file...")
        cmd = [sys.executable, "-m", "pip", "install", "-r", str(req_file)]
    else:
        print("📦 Installing from package list...")
        cmd = [sys.executable, "-m", "pip", "install"] + PACKAGES

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✅ All packages installed successfully!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Run the FastAPI server: uvicorn main:app --reload")
        print("2. Open and run your EDA notebook: jupyter notebook OTI/EDA.ipynb")
    else:
        print("\n❌ An error occurred during package installation.")
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
