# analysis/interpretation/block_structure_interpretations.py

from __future__ import annotations

import pandas as pd


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
        audience_cluster | structural_profile
    """

    # ------------------------------------------------------
    # Merge required statistics
    # ------------------------------------------------------
    df = (
        deviation_df
        .merge(
            zscore_df[
                ["audience_cluster", "character_cluster", "z_score"]
            ],
            on=["audience_cluster", "character_cluster"],
            how="left",
        )
        .merge(
            significance_df[
                ["audience_cluster", "character_cluster", "significant"]
            ],
            on=["audience_cluster", "character_cluster"],
            how="left",
        )
    )

    df["rating_deviation"] = df["rating_deviation"].astype(float)

    # ------------------------------------------------------
    # Keep strong + significant structural effects
    # ------------------------------------------------------
    strong = df[
        (df["significant"]) &
        (df["z_score"].abs() >= z_threshold)
    ].copy()

    # Direction label
    strong["direction"] = strong["rating_deviation"].apply(
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
            .groupby("audience_cluster", group_keys=False)
            .apply(_build_profile, include_groups=False,)
            .reset_index(name="structural_profile")
        )
    else:
        archetypes = pd.DataFrame(
            columns=["audience_cluster", "structural_profile"]
        )

    # ------------------------------------------------------
    # Ensure ALL clusters receive an archetype
    # (important: absence of bias is meaningful)
    # ------------------------------------------------------
    all_clusters = (
        deviation_df["audience_cluster"]
        .drop_duplicates()
        .sort_values()
    )

    archetypes = archetypes.set_index("audience_cluster")

    missing_clusters = set(all_clusters) - set(archetypes.index)

    for cluster_id in missing_clusters:
        archetypes.loc[cluster_id] = {
            "structural_profile":
                "balanced / weak structural bias"
        }

    archetypes = (
        archetypes
        .reset_index()
        .sort_values("audience_cluster")
        .reset_index(drop=True)
    )

    return archetypes


def _intensity_label(value: float) -> str:
    if value >= 0.45:
        return "very strong"
    if value >= 0.38:
        return "strong"
    if value >= 0.32:
        return "moderate"
    return "mild"


def _selectivity_label(value: float) -> str:
    if value >= 0.50:
        return "highly selective"
    if value >= 0.40:
        return "selective"
    if value >= 0.30:
        return "balanced"
    return "broad"


def generate_narrative_identity_reports(
    archetypes_df: pd.DataFrame,
    identity_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Step 4.2.15 — Narrative Identity Reports

    Produces natural-language summaries describing
    each audience cluster.
    """

    df = identity_df.merge(
        archetypes_df,
        on="audience_cluster",
        how="left",
    )

    def build_report(row: pd.Series) -> str:

        intensity = _intensity_label(row["block_extremeness"])
        selectivity = _selectivity_label(row["narrative_selectivity"])

        profile = row.get("structural_profile", "")

        text = (
            f"Cluster {int(row.audience_cluster)} represents a "
            f"{row.structural_identity_type} audience with "
            f"{intensity} preference intensity and "
            f"{selectivity} narrative engagement."
        )

        if isinstance(profile, str) and profile.strip():
            text += f" Structurally, this group {profile}."

        return text

    df["narrative_identity_report"] = df.apply(
        build_report,
        axis=1,
    )

    return df[
        [
            "audience_cluster",
            "structural_identity_type",
            "block_extremeness",
            "narrative_selectivity",
            "narrative_identity_report",
        ]
    ].sort_values("audience_cluster").reset_index(drop=True)


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
        on="audience_cluster",
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

    return df.sort_values("audience_cluster").reset_index(drop=True)