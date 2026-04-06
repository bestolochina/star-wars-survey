# analysis/transforms/fandom_ideology_map.py

from __future__ import annotations
import pandas as pd


# ==========================================================
# Helper: Normalize cluster IDs
# ==========================================================
def _normalize_cluster_id(df: pd.DataFrame, col: str = "audience_cluster") -> pd.DataFrame:
    df = df.copy()

    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    return df


# ==========================================================
# Helper: Aggregate coalition roles per character (WEIGHTED)
# ==========================================================
def _aggregate_character_coalitions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if {"mean_preference", "n_characters"}.issubset(df.columns):
        df["strength"] = df["mean_preference"] * df["n_characters"]
    elif "mean_preference" in df.columns:
        df["strength"] = df["mean_preference"]
    elif "mean_weight" in df.columns:
        df["strength"] = df["mean_weight"]
    else:
        df["strength"] = 1.0

    grouped = (
        df.groupby(["character", "ideological_role"], as_index=False)
        .agg(total_strength=("strength", "sum"))
    )

    idx = grouped.groupby("character")["total_strength"].idxmax()
    dominant = grouped.loc[idx].copy()

    dominant = dominant.rename(columns={
        "ideological_role": "dominant_ideological_role"
    })

    return dominant[
        ["character", "dominant_ideological_role", "total_strength"]
    ]


# ==========================================================
# Helper: Normalize polarization input
# ==========================================================
def _prepare_character_polarization(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "polarization_index" in df.columns:
        return df[["character", "polarization_index"]]

    if "character_mean_rating_divergence_across_clusters" in df.columns:
        return df.rename(columns={
            "character_mean_rating_divergence_across_clusters": "polarization_index"
        })[["character", "polarization_index"]]

    if "character_rating_range_across_clusters" in df.columns:
        return df.rename(columns={
            "character_rating_range_across_clusters": "polarization_index"
        })[["character", "polarization_index"]]

    raise ValueError("Unsupported character_polarization format")


# ==========================================================
# Helper: Extract cluster size
# ==========================================================
def _extract_cluster_size(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "cluster_size" in df.columns:
        return df[["audience_cluster", "cluster_size"]]

    if {"audience_cluster", "count"}.issubset(df.columns):
        return (
            df.groupby("audience_cluster")["count"]
            .max()
            .reset_index(name="cluster_size")
        )

    raise ValueError("Unsupported audience_profiles format")


# ==========================================================
# Main builder
# ==========================================================
def build_fandom_ideology_map_dataset(
    character_coords: pd.DataFrame,
    character_roles: pd.DataFrame,
    character_coalitions: pd.DataFrame,
    community_metrics: pd.DataFrame,
    cluster_coords: pd.DataFrame,
    audience_typology: pd.DataFrame,
    narrative_intensity: pd.DataFrame,
    character_polarization: pd.DataFrame | None = None,
    audience_profiles: pd.DataFrame | None = None,
) -> pd.DataFrame:

    # ==========================================================
    # Normalize cluster IDs
    # ==========================================================
    cluster_coords = _normalize_cluster_id(cluster_coords)
    audience_typology = _normalize_cluster_id(audience_typology)
    narrative_intensity = _normalize_cluster_id(narrative_intensity)

    if audience_profiles is not None:
        audience_profiles = _normalize_cluster_id(audience_profiles)

    # ==========================================================
    # 1. Enrich coalition data
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
    ).drop(columns=["community_id"], errors="ignore")

    # ==========================================================
    # 2. Characters
    # ==========================================================
    char_df = character_coords.copy()

    char_df = char_df.merge(
        character_roles[["character", "narrative_role"]],
        on="character",
        how="left",
    )

    coalition_agg = _aggregate_character_coalitions(coalitions)

    char_df = char_df.merge(
        coalition_agg,
        on="character",
        how="left",
    )

    # --- Polarization
    if character_polarization is not None:
        pol_df = _prepare_character_polarization(character_polarization)

        char_df = char_df.merge(
            pol_df,
            on="character",
            how="left",
        )
    else:
        char_df["polarization_index"] = None

    # --- Fill missing meaningfully
    char_df["dominant_ideological_role"] = char_df["dominant_ideological_role"].fillna("Unaligned")
    char_df["total_strength"] = char_df["total_strength"].fillna(0)

    char_df = char_df.rename(columns={"character": "entity_id"})
    char_df["entity_type"] = "character"

    char_df["cluster_type"] = None
    char_df["polarization_strength"] = None
    char_df["hero_core_dominance"] = None
    char_df["cluster_size"] = None

    # ==========================================================
    # 3. Audience clusters
    # ==========================================================
    cluster_df = cluster_coords.copy()

    cluster_df = cluster_df.merge(
        audience_typology,
        on="audience_cluster",
        how="left",
    )

    cluster_df = cluster_df.merge(
        narrative_intensity,
        on="audience_cluster",
        how="left",
    )

    if audience_profiles is not None:
        cluster_size_df = _extract_cluster_size(audience_profiles)

        cluster_df = cluster_df.merge(
            cluster_size_df,
            on="audience_cluster",
            how="left",
        )
    else:
        cluster_df["cluster_size"] = None

    cluster_df = cluster_df.rename(columns={
        "audience_cluster": "entity_id",
    })

    # 🔥 Make cluster IDs explicit
    cluster_df["entity_id"] = "cluster_" + cluster_df["entity_id"].astype(str)

    cluster_df["entity_type"] = "audience_cluster"

    cluster_df["narrative_role"] = None
    cluster_df["dominant_ideological_role"] = None
    cluster_df["total_strength"] = None
    cluster_df["polarization_index"] = None

    # ==========================================================
    # 4. Schema alignment
    # ==========================================================
    columns = [
        "entity_id",
        "entity_type",
        "ideology_axis_1",
        "ideology_axis_2",

        "narrative_role",
        "dominant_ideological_role",
        "total_strength",
        "polarization_index",

        "cluster_type",
        "polarization_strength",
        "hero_core_dominance",
        "cluster_size",
    ]

    char_df = char_df.reindex(columns=columns)
    cluster_df = cluster_df.reindex(columns=columns)

    # ==========================================================
    # 5. Combine (SAFE CONCAT)
    # ==========================================================

    # Ensure consistent dtypes across both frames
    for col in columns:
        if col not in char_df.columns:
            char_df[col] = pd.NA
        if col not in cluster_df.columns:
            cluster_df[col] = pd.NA

    # Force consistent dtype (object is safest for mixed schema)
    char_df = char_df.astype({col: "object" for col in columns})
    cluster_df = cluster_df.astype({col: "object" for col in columns})

    df = pd.concat(
        [char_df, cluster_df],
        ignore_index=True
    )

    df["entity_id"] = df["entity_id"].astype(str)

    return df
