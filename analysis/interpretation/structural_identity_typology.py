# analysis/interpretation/structural_identity_typology.py

from __future__ import annotations

import pandas as pd


def derive_structural_identity_typology(
    extremeness_df: pd.DataFrame,
    selectivity_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Step 4.2.14 — Structural Identity Typology

    Classifies audience clusters into interpretable
    narrative identity types using:

        - block extremeness
        - narrative selectivity
    """

    df = extremeness_df.merge(
        selectivity_df,
        on="cluster",
        how="inner",
    )

    # --------------------------------------------
    # Adaptive thresholds (dataset-relative)
    # --------------------------------------------
    extremeness_threshold = df["block_extremeness"].median()
    selectivity_threshold = df["narrative_selectivity"].median()

    def classify(row: pd.Series) -> str:

        high_e = row["block_extremeness"] >= extremeness_threshold
        high_s = row["narrative_selectivity"] >= selectivity_threshold

        if high_e and high_s:
            return "Cult Archetype"

        if high_e and not high_s:
            return "Passionate Generalist"

        if not high_e and high_s:
            return "Niche Minimalist"

        return "Broad Mainstream"

    df["structural_identity_type"] = df.apply(
        classify,
        axis=1,
    )

    return df.sort_values("cluster").reset_index(drop=True)