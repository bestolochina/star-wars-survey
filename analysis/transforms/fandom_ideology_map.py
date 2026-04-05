# analysis/transforms/fandom_ideology_map.py

from __future__ import annotations
import pandas as pd


# ==========================================================
# Helper: Aggregate coalition roles per character (WEIGHTED)
# ==========================================================
def _aggregate_character_coalitions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapse multiple coalition assignments per character
    into a single dominant coalition using weighted strength.

    Strength = mean_preference * n_characters
    """

    df = df.copy()

    # -----------------------------------
    # Compute strength
    # -----------------------------------
    if "mean_preference" in df.columns and "n_characters" in df.columns:
        df["strength"] = df["mean_preference"] * df["n_characters"]

    elif "mean_preference" in df.columns:
        df["strength"] = df["mean_preference"]

    elif "mean_weight" in df.columns:
        df["strength"] = df["mean_weight"]

    else:
        df["strength"] = 1  # fallback

    # -----------------------------------
    # Aggregate strength per coalition
    # -----------------------------------
    grouped = (
        df.groupby(
            ["character", "ideological_role"],  # 🔥 REMOVE coalition_id here
            as_index=False,
        )
        .agg(total_strength=("strength", "sum"))
    )

    # -----------------------------------
    # Pick strongest coalition per character
    # -----------------------------------
    idx = grouped.groupby("character")["total_strength"].idxmax()
    result = grouped.loc[idx].copy()

    result = result.rename(columns={
        "ideological_role": "coalition_role"
    })

    return result[["character", "coalition_role", "total_strength"]]


# ==========================================================
# Main builder
# ==========================================================
def build_fandom_ideology_map_dataset(
    character_coords: pd.DataFrame,
    character_roles: pd.DataFrame,
    character_coalitions: pd.DataFrame,
    community_metrics: pd.DataFrame,   # 🔥 NEW
    cluster_coords: pd.DataFrame,
    audience_typology: pd.DataFrame,
    narrative_intensity: pd.DataFrame,
) -> pd.DataFrame:

    # ==========================================================
    # 1. Enrich character_coalitions with strength
    # ==========================================================
    coalitions = character_coalitions.copy()

    coalitions = coalitions.merge(
        community_metrics[
            [
                "audience_cluster",
                "community_id",
                "n_characters",
                "mean_weight",
                "mean_preference",
            ]
        ],
        left_on=["audience_cluster", "coalition_id"],
        right_on=["audience_cluster", "community_id"],
        how="left",
    )

    # Optional cleanup
    coalitions = coalitions.drop(columns=["community_id"])

    # ==========================================================
    # 2. Characters
    # ==========================================================
    char_df = character_coords.copy()

    # --- Roles
    char_df = char_df.merge(
        character_roles[["character", "narrative_role"]],
        on="character",
        how="left",
    )

    # --- Aggregate coalition roles (weighted)
    coalition_agg = _aggregate_character_coalitions(coalitions)

    char_df = char_df.merge(
        coalition_agg,
        on="character",
        how="left",
    )

    # --- Standardize
    char_df = char_df.rename(columns={
        "character": "entity_id",
    })

    char_df["entity_type"] = "character"

    # --- Fill cluster-only fields
    char_df["cluster_type"] = None
    char_df["polarization_strength"] = None
    char_df["hero_core_dominance"] = None

    # ==========================================================
    # 3. Audience Clusters
    # ==========================================================
    cluster_df = cluster_coords.copy()

    # dtype safety
    cluster_df["audience_cluster"] = cluster_df["audience_cluster"].astype(int)
    audience_typology["audience_cluster"] = audience_typology["audience_cluster"].astype(int)
    narrative_intensity["audience_cluster"] = narrative_intensity["audience_cluster"].astype(int)

    # --- Merge typology
    cluster_df = cluster_df.merge(
        audience_typology,
        on="audience_cluster",
        how="left",
    )

    # --- Merge intensity
    cluster_df = cluster_df.merge(
        narrative_intensity,
        on="audience_cluster",
        how="left",
    )

    # --- Standardize
    cluster_df = cluster_df.rename(columns={
        "audience_cluster": "entity_id",
    })

    cluster_df["entity_type"] = "audience_cluster"

    # --- Fill character-only fields
    cluster_df["narrative_role"] = None
    cluster_df["coalition_role"] = None
    cluster_df["total_strength"] = None

    # ==========================================================
    # 4. Schema alignment
    # ==========================================================
    columns = [
        "entity_id",
        "entity_type",
        "ideology_axis_1",
        "ideology_axis_2",

        # character
        "narrative_role",
        "coalition_role",
        "total_strength",  # 🔥 NEW

        # cluster
        "cluster_type",
        "polarization_strength",
        "hero_core_dominance",
    ]

    char_df = char_df[columns]
    cluster_df = cluster_df[columns]

    # ==========================================================
    # 5. Combine
    # ==========================================================
    df = pd.concat([char_df, cluster_df], ignore_index=True)

    return df
