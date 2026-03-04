# analysis/metrics/narrative_selectivity.py

from __future__ import annotations

import pandas as pd
import numpy as np


def compute_narrative_selectivity(
    deviation_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Step 4.2.13 — Narrative Selectivity Index (NSI)

    Measures how concentrated each audience cluster's
    structural preferences are across character archetypes.

    High selectivity:
        → strong preference for few archetypes

    Low selectivity:
        → diffuse or general preference pattern
    """

    required_cols = {
        "cluster",
        "character_cluster",
        "deviation",
    }

    missing = required_cols - set(deviation_df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    df = deviation_df.copy()

    # --------------------------------------------------
    # Absolute structural strength
    # --------------------------------------------------
    df["abs_dev"] = df["deviation"].abs()

    results = []

    # --------------------------------------------------
    # Compute concentration per audience cluster
    # --------------------------------------------------
    for cluster, g in df.groupby("cluster"):

        total = g["abs_dev"].sum()

        if total == 0:
            selectivity = 0.0
        else:
            proportions = g["abs_dev"] / total

            # Herfindahl concentration index
            selectivity = float(np.sum(proportions**2))

        results.append(
            {
                "cluster": cluster,
                "narrative_selectivity": selectivity,
            }
        )

    result_df = (
        pd.DataFrame(results)
        .sort_values("narrative_selectivity", ascending=False)
        .reset_index(drop=True)
    )

    return result_df