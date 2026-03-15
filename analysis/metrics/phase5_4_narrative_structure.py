# analysis/metrics/phase5_4_narrative_structure.py

from __future__ import annotations

import pandas as pd
import numpy as np


# ==========================================================
# Cluster Narrative Deviation Matrix
# ==========================================================

def compute_cluster_narrative_deviation(
    character_cluster_means: pd.DataFrame,
    global_character_means: pd.Series,
) -> pd.DataFrame:
    """
    Computes deviation of each cluster's character ratings
    from the global narrative baseline.

    Returns
    -------
    DataFrame
        audience_cluster + character deviation columns
    """

    df = character_cluster_means.copy()

    character_cols = df.columns.drop("audience_cluster")

    for c in character_cols:
        df[c] = df[c] - global_character_means[c]

    return df


# ==========================================================
# Narrative Anchor Characters
# ==========================================================

def compute_cluster_narrative_anchors(
    deviation_matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Identifies strongest positive and negative narrative anchors
    for each audience cluster.

    Returns
    -------
    DataFrame
        audience_cluster
        strongest_affinity_character
        strongest_rejection_character
        affinity_strength
        rejection_strength
    """

    records = []

    character_cols = deviation_matrix.columns.drop("audience_cluster")

    for _, row in deviation_matrix.iterrows():

        cluster = row["audience_cluster"]

        scores = row[character_cols]

        affinity_char = scores.idxmax()
        rejection_char = scores.idxmin()

        records.append(
            {
                "audience_cluster": cluster,
                "strongest_affinity_character": affinity_char,
                "strongest_rejection_character": rejection_char,
                "affinity_strength": scores.max(),
                "rejection_strength": scores.min(),
            }
        )

    return pd.DataFrame(records)


# ==========================================================
# Narrative Coherence Index
# ==========================================================

def compute_cluster_narrative_coherence(
    deviation_matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Measures how strongly a cluster deviates from the
    global narrative baseline.

    Higher = stronger narrative identity.

    Returns
    -------
    DataFrame
        audience_cluster
        narrative_coherence_index
    """

    records = []

    character_cols = deviation_matrix.columns.drop("audience_cluster")

    for _, row in deviation_matrix.iterrows():

        cluster = row["audience_cluster"]

        scores = row[character_cols].values

        coherence = np.mean(np.abs(scores))

        records.append(
            {
                "audience_cluster": cluster,
                "narrative_coherence_index": coherence,
            }
        )

    return pd.DataFrame(records)


# ==========================================================
# Narrative Extremeness
# ==========================================================

def compute_cluster_narrative_extremeness(
    deviation_matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Measures the maximum narrative deviation inside each cluster.

    Returns
    -------
    DataFrame
        audience_cluster
        narrative_extremeness
    """

    records = []

    character_cols = deviation_matrix.columns.drop("audience_cluster")

    for _, row in deviation_matrix.iterrows():

        cluster = row["audience_cluster"]

        scores = row[character_cols].values

        extremeness = np.max(np.abs(scores))

        records.append(
            {
                "audience_cluster": cluster,
                "narrative_extremeness": extremeness,
            }
        )

    return pd.DataFrame(records)


# ==========================================================
# Audience Narrative Archetypes
# ==========================================================

def compute_audience_narrative_archetypes(
    cluster_profiles: pd.DataFrame,
    narrative_coherence: pd.DataFrame,
    anchors: pd.DataFrame,
) -> pd.DataFrame:

    # ------------------------------------------------------
    # Ensure consistent key types
    # ------------------------------------------------------

    cluster_profiles = cluster_profiles.copy()
    narrative_coherence = narrative_coherence.copy()
    anchors = anchors.copy()

    cluster_profiles["audience_cluster"] = cluster_profiles["audience_cluster"].astype(int)
    narrative_coherence["audience_cluster"] = narrative_coherence["audience_cluster"].astype(int)
    anchors["audience_cluster"] = anchors["audience_cluster"].astype(int)

    # ------------------------------------------------------
    # Merge
    # ------------------------------------------------------

    df = (
        cluster_profiles
        .merge(narrative_coherence, on="audience_cluster")
        .merge(anchors, on="audience_cluster")
    )

    archetypes = []

    for _, row in df.iterrows():

        profile = row["narrative_profile"]
        coherence = row["narrative_coherence_index"]

        if profile == "hero_oriented_audience" and coherence > 0.25:
            archetype = "hero_loyalists"

        elif profile == "dark_side_oriented_audience" and coherence > 0.25:
            archetype = "dark_side_sympathizers"

        elif profile == "balanced_high_engagement_audience":
            archetype = "balanced_mythology_consumers"

        elif profile == "low_engagement_audience":
            archetype = "detached_casual_audience"

        else:
            archetype = "mixed_narrative_consumers"

        archetypes.append(archetype)

    df["narrative_archetype"] = archetypes

    return df


def reshape_cluster_character_preference_matrix(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Converts character × cluster matrix to
    cluster × character matrix.

    Input format
    ------------
    index: characters
    columns: clusters

    Output format
    -------------
    audience_cluster | character columns
    """

    reshaped = (
        df.T
        .reset_index()
        .rename(columns={"index": "audience_cluster"})
    )

    return reshaped
