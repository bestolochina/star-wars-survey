# analysis/interpretation/structural_archetypes.py

from __future__ import annotations

import pandas as pd


# ==========================================================
# 4.2.11 Structural Archetype Extraction
# ==========================================================

def derive_structural_archetypes(
    deviation_df: pd.DataFrame,
    zscore_df: pd.DataFrame,
    significance_df: pd.DataFrame,
    z_threshold: float = 1.0,
) -> pd.DataFrame:
    """
    Step 4.2.11 — Structural Archetype Extraction

    Creates interpretable audience archetype summaries
    based on statistically significant structural deviations.

    Each audience cluster receives a structural profile:
        - likes Ck     (positive deviation)
        - dislikes Ck  (negative deviation)
        - balanced / weak structural bias (no strong signals)

    Parameters
    ----------
    deviation_df :
        Output of compute_block_deviations()

    zscore_df :
        Output of compute_block_zscores()

    significance_df :
        Output of bootstrap_block_deviation_significance()

    z_threshold :
        Minimum |z-score| required to count as structural signal.

    Returns
    -------
    pd.DataFrame
        cluster | structural_profile
    """

    # ------------------------------------------------------
    # Merge required statistics
    # ------------------------------------------------------
    df = (
        deviation_df
        .merge(
            zscore_df[
                ["cluster", "character_cluster", "z_score"]
            ],
            on=["cluster", "character_cluster"],
            how="left",
        )
        .merge(
            significance_df[
                ["cluster", "character_cluster", "significant"]
            ],
            on=["cluster", "character_cluster"],
            how="left",
        )
    )

    # ------------------------------------------------------
    # Keep strong + significant structural effects
    # ------------------------------------------------------
    strong = df[
        (df["significant"]) &
        (df["z_score"].abs() >= z_threshold)
    ].copy()

    # Direction label
    strong["direction"] = strong["deviation"].apply(
        lambda x: "likes" if x > 0 else "dislikes"
    )

    # ------------------------------------------------------
    # Build textual structural profiles
    # ------------------------------------------------------
    def _build_profile(group: pd.DataFrame) -> str:
        ordered = group.sort_values(
            "z_score",
            key=lambda s: s.abs(),
            ascending=False,
        )

        return ", ".join(
            f"{row.direction} C{int(row.character_cluster)}"
            for _, row in ordered.iterrows()
        )

    if len(strong) > 0:
        archetypes = (
            strong
            .groupby("cluster", group_keys=False)
            .apply(_build_profile, include_groups=False,)
            .reset_index(name="structural_profile")
        )
    else:
        archetypes = pd.DataFrame(
            columns=["cluster", "structural_profile"]
        )

    # ------------------------------------------------------
    # Ensure ALL clusters receive an archetype
    # (important: absence of bias is meaningful)
    # ------------------------------------------------------
    all_clusters = (
        deviation_df["cluster"]
        .drop_duplicates()
        .sort_values()
    )

    archetypes = archetypes.set_index("cluster")

    missing_clusters = set(all_clusters) - set(archetypes.index)

    for cluster_id in missing_clusters:
        archetypes.loc[cluster_id] = {
            "structural_profile":
                "balanced / weak structural bias"
        }

    archetypes = (
        archetypes
        .reset_index()
        .sort_values("cluster")
        .reset_index(drop=True)
    )

    return archetypes