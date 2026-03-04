# analysis/interpretation/narrative_identity_reports.py

from __future__ import annotations

import pandas as pd


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
        on="cluster",
        how="left",
    )

    def build_report(row: pd.Series) -> str:

        intensity = _intensity_label(row["block_extremeness"])
        selectivity = _selectivity_label(row["narrative_selectivity"])

        profile = row.get("structural_profile", "")

        text = (
            f"Cluster {int(row.cluster)} represents a "
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
            "cluster",
            "structural_identity_type",
            "block_extremeness",
            "narrative_selectivity",
            "narrative_identity_report",
        ]
    ].sort_values("cluster").reset_index(drop=True)
