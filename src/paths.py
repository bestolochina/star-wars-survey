# src/paths.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEAN_DATA_DIR = DATA_DIR / "clean"

ANALYSIS_DIR = PROJECT_ROOT / "analysis"
FIGURES_DIR = ANALYSIS_DIR / "figures"

REPORTS_DIR = PROJECT_ROOT / "reports"
