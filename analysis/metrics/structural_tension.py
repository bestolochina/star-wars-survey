# analysis/metrics/structural_tension.py

from __future__ import annotations
import pandas as pd


def compute_structural_tension(
    deviation_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Step 4.2.17 — Structural Narrative Tension

    Measures disagreement between audience clusters
    for each character cluster.
    """

    tension = (
        deviation_df
        .groupby("character_cluster")["deviation"]
        .agg(
            tension_variance="var",
            tension_std="std",
            mean_abs_deviation=lambda x: x.abs().mean(),
        )
        .reset_index()
        .sort_values("tension_variance", ascending=False)
    )

    return tension
