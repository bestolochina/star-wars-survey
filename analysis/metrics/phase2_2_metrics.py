# analysis/metrics/phase2_2_metrics.py

from __future__ import annotations
from pathlib import Path
from src.paths import FIGURES_DIR
import matplotlib.pyplot as plt
import pandas as pd

from src.io_utils import load_clean_star_wars

# -------------------------
# Core computation
# -------------------------

def contingency_table(
    df: pd.DataFrame,
    col_a: str,
    col_b: str,
) -> pd.DataFrame:
    """
    Returns a contingency table (counts) including NaN.
    """
    return pd.crosstab(
        df[col_a],
        df[col_b],
        dropna=False,
    )


def row_percentages(table: pd.DataFrame) -> pd.DataFrame:
    """
    Returns row-normalized percentages.
    """
    return table.div(table.sum(axis=1), axis=0) * 100


def nominal_binary_crosstab(
    df: pd.DataFrame,
    nominal_col: str,
    binary_col: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns:
    - count table
    - row-wise percentage table
    """
    counts: pd.DataFrame = pd.crosstab(
        df[nominal_col],
        df[binary_col],
        dropna=False,
        normalize=False
    )
    expected_cols = [True, False, pd.NA]
    counts = counts.reindex(
        columns=[c for c in expected_cols if c in counts.columns],
        fill_value=0,
    )

    percentages: pd.DataFrame = (
        counts.div(counts.sum(axis=1), axis=0) * 100
    ).round(1)

    return counts, percentages
