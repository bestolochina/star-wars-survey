# analysis/transforms/fandom_ideology_map.py

from __future__ import annotations
import pandas as pd


def build_fandom_ideology_map_dataset(
    character_coords: pd.DataFrame,
    character_roles: pd.DataFrame,
    character_coalitions: pd.DataFrame,
    cluster_coords: pd.DataFrame,
    audience_typology: pd.DataFrame,
    narrative_intensity: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build unified dataset for fandom ideology map visualization.

    Output schema (consistent across entity types):
    ------------------------------------------------
    entity_id
    entity_type  ("character" | "audience_cluster")

    ideology_axis_1
    ideology_axis_2

    # Character-only
    narrative_role
    coalition_id
    coalition_role

    # Cluster-only
    cluster_type
    polarization_strength
    hero_core_dominance
    """

    # ==========================================================
    # 1. Characters
    # ==========================================================
    char_df = character_coords.copy()

    # --- Roles
    char_df = char_df.merge(
        character_roles[["character", "narrative_role"]],
        on="character",
        how="left",
    )

    # --- Coalition info
    char_df = char_df.merge(
        character_coalitions[["character", "coalition_id", "ideological_role"]],
        on="character",
        how="left",
    )

    # --- Standardize columns
    char_df = char_df.rename(columns={
        "character": "entity_id",
        "ideological_role": "coalition_role",
    })

    char_df["entity_type"] = "character"

    # --- Fill cluster-only fields
    char_df["cluster_type"] = None
    char_df["polarization_strength"] = None
    char_df["hero_core_dominance"] = None

    # ==========================================================
    # 2. Audience Clusters
    # ==========================================================
    cluster_df = cluster_coords.copy()

    # Ensure consistent dtype for merging
    cluster_df["audience_cluster"] = cluster_df["audience_cluster"].astype(int)
    audience_typology["audience_cluster"] = audience_typology["audience_cluster"].astype(int)
    narrative_intensity["audience_cluster"] = narrative_intensity["audience_cluster"].astype(int)

    # --- Typology
    cluster_df = cluster_df.merge(
        audience_typology,
        on="audience_cluster",
        how="left",
    )

    # --- Narrative intensity
    cluster_df = cluster_df.merge(
        narrative_intensity,
        on="audience_cluster",
        how="left",
    )

    # --- Standardize columns
    cluster_df = cluster_df.rename(columns={
        "audience_cluster": "entity_id",
    })

    cluster_df["entity_type"] = "audience_cluster"

    # --- Fill character-only fields
    cluster_df["narrative_role"] = None
    cluster_df["coalition_id"] = None
    cluster_df["coalition_role"] = None

    # ==========================================================
    # 3. Enforce Schema Consistency
    # ==========================================================
    columns = [
        "entity_id",
        "entity_type",
        "ideology_axis_1",
        "ideology_axis_2",

        # character
        "narrative_role",
        "coalition_id",
        "coalition_role",

        # cluster
        "cluster_type",
        "polarization_strength",
        "hero_core_dominance",
    ]

    char_df = char_df[columns]
    cluster_df = cluster_df[columns]

    # ==========================================================
    # 4. Combine
    # ==========================================================
    df = pd.concat([char_df, cluster_df], ignore_index=True)

    return df