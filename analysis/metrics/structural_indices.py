# analysis/metrics/structural_indices.py

from __future__ import annotations
import pandas as pd


# ==========================================================
# 4.2.12 Block Extremeness Index
# ==========================================================

def compute_block_extremeness(
    deviation_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Computes structural extremeness for each audience cluster.

    Extremeness = mean absolute deviation across character blocs.

    Parameters
    ----------
    deviation_df :
        Output of compute_block_deviations()

    Returns
    -------
    pd.DataFrame
        cluster | block_extremeness
    """

    extremeness = (
        deviation_df
        .assign(abs_dev=lambda df: df["deviation"].abs())
        .groupby("cluster", as_index=False)["abs_dev"]
        .mean()
        .rename(columns={"abs_dev": "block_extremeness"})
        .sort_values("cluster")
        .reset_index(drop=True)
    )

    return extremeness