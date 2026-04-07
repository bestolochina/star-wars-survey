# analysis/pipelines/phase5_6_interpretation_pipeline.py

from __future__ import annotations

from pathlib import Path

import pandas as pd

from analysis.interpretation.audience_narrative_profile import build_audience_narrative_profiles
from analysis.transforms.fandom_ideology_map import build_fandom_ideology_map_dataset
from analysis.transforms.narrative_role_affinity import build_narrative_role_affinity
from analysis.transforms.character_coalition_roles import build_character_coalition_roles

from src.paths import (
    PHASE5_TABLES_DIR,
    PHASE4_TABLES_DIR,
    PHASE5_FIGURES_DIR,
    PHASE3_TABLES_DIR,
)

from analysis.transforms.correlation_matrix_from_edges import build_correlation_matrix_from_edges
from analysis.transforms.coalition_ideology_mapping import build_coalition_ideology_mapping
from analysis.interpretation.phase5_7_interpretation import classify_coalition, classify_audience_clusters
from analysis.interpretation.coalition_roles import add_coalition_ideological_roles
from analysis.interpretation.narrative_identity import build_narrative_identity_reports
from analysis.interpretation.audience_demographic_profile import build_audience_profiles
from analysis.interpretation.narrative_intensity import compute_narrative_intensity

from analysis.metrics.phase5_6_narrative_coalitions import (
    build_cluster_conditioned_edges,
    filter_edges,
    detect_communities,
    compute_community_metrics,
)

from analysis.visualization.phase5_plots import (
    plot_audience_conditioned_character_networks,
    plot_coalition_ideology_map,
    plot_fandom_ideology_map,
    plot_cluster_narrative_role_profiles,
)


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs() -> None:

    (PHASE5_TABLES_DIR / "narrative_coalitions").mkdir(
        parents=True,
        exist_ok=True,
    )

    (PHASE5_FIGURES_DIR / "visualizations").mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# 5.6.1 Build Networks
# ==========================================================

def step_561_build_networks(
    alignment_matrix: pd.DataFrame,
    correlation_matrix: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.6.1 Build Cluster-Conditioned Networks ===")

    edges_df = build_cluster_conditioned_edges(
        alignment_matrix,
        correlation_matrix,
    )

    print(f"Total edges: {len(edges_df)}")

    return edges_df


# ==========================================================
# 5.6.2 Filter Edges
# ==========================================================

def step_562_filter_edges(
    edges_df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.6.2 Filter Network Edges ===")

    filtered = filter_edges(edges_df)

    print(f"Edges after filtering: {len(filtered)}")

    print(filtered.groupby("audience_cluster").size())

    return filtered


# ==========================================================
# 5.6.3 Detect Communities
# ==========================================================

def step_563_detect_communities(
    edges_df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.6.3 Detect Communities ===")

    community_df = detect_communities(edges_df)

    print(community_df.to_string())

    return community_df


# ==========================================================
# 5.6.4 Save Tables
# ==========================================================

def step_564_save_tables(
    edges_df: pd.DataFrame,
    community_df: pd.DataFrame,
) -> None:

    print("\n=== 5.6.4 Save Narrative Coalition Tables ===")

    out_dir = PHASE5_TABLES_DIR / "narrative_coalitions"

    edges_path = out_dir / "audience_cluster_character_network_edges.csv"
    communities_path = out_dir / "audience_cluster_character_communities.csv"

    edges_df.to_csv(edges_path, index=False)
    community_df.to_csv(communities_path, index=False)

    print(f"Saved → {edges_path}")
    print(f"Saved → {communities_path}")


# ==========================================================
# 5.6.5 Visualization
# ==========================================================

def step_565_plot_networks(
    edges_df: pd.DataFrame,
    community_df: pd.DataFrame,
) -> None:

    print("\n=== 5.6.5 Audience-Conditioned Character Networks ===")

    path = (
        PHASE5_FIGURES_DIR
        / "visualizations"
        / "audience_conditioned_character_networks.png"
    )

    plot_audience_conditioned_character_networks(
        edges_df=edges_df,
        community_df=community_df,
        output_path=path,
    )

    print(f"Saved → {path}")


# ==========================================================
# 5.6.6 Community Metrics
# ==========================================================

def step_566_compute_community_metrics(
    edges_df: pd.DataFrame,
    community_df: pd.DataFrame,
    alignment_matrix: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.6.6 Community Metrics ===")

    path = PHASE5_TABLES_DIR / "narrative_coalitions" / "community_metrics.csv"

    metrics_df = compute_community_metrics(
        edges_df,
        community_df,
        alignment_matrix,
    )

    metrics_df.to_csv(path, index=False)

    print(metrics_df.to_string())

    print(f"Saved → {path}")

    return metrics_df


# ==========================================================
# 5.7.1 Coalition Typology
# ==========================================================

def step_571_classify_coalitions(
    metrics_df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.7.1 Coalition Typology ===")

    path = PHASE5_TABLES_DIR / "narrative_coalitions" / "coalition_typology.csv"

    metrics_df = metrics_df.copy()

    metrics_df["coalition_type"] = metrics_df.apply(
        classify_coalition,
        axis=1,
    )

    metrics_df.to_csv(path, index=False)

    print(metrics_df.to_string())

    print(f"Saved → {path}")

    return metrics_df


# ==========================================================
# 5.7.2 Audience Typology
# ==========================================================

def step_572_classify_audience_clusters(
        metrics_df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.7.2 Audience Typology ===")

    path = PHASE5_TABLES_DIR / "narrative_coalitions" / "audience_typology.csv"

    audience_typology = classify_audience_clusters(metrics_df)

    audience_typology.to_csv(path, index=False)

    print(audience_typology.to_string())

    print(f"Saved → {path}")

    return audience_typology


# ==========================================================
# 5.7.3 Coalition Ideological Positioning
# ==========================================================

def step_573_map_coalitions_to_ideology(
    metrics_df: pd.DataFrame,
    community_df: pd.DataFrame,
    ideology_df: pd.DataFrame,
    alignment_matrix: pd.DataFrame
) -> pd.DataFrame:

    print("\n=== 5.7.3 Coalition Ideology Mapping ===")

    coalition_ideology = build_coalition_ideology_mapping(
        community_df=community_df,
        ideology_df=ideology_df,
        metrics_df=metrics_df,
        alignment_matrix=alignment_matrix
    )

    path = (
        PHASE5_TABLES_DIR
        / "narrative_coalitions"
        / "coalition_ideology_mapping.csv"
    )

    coalition_ideology.to_csv(path, index=False)

    print(coalition_ideology.to_string())
    print(f"Saved → {path}")

    return coalition_ideology

# ==========================================================
# 5.7.4 Coalition Ideology Map
# ==========================================================

def step_574_plot_coalition_ideology(
    coalition_df: pd.DataFrame,
) -> None:

    print("\n=== 5.7.4 Coalition Ideology Map ===")

    path = (
        PHASE5_FIGURES_DIR
        / "visualizations"
        / "coalition_ideology_map.png"
    )

    plot_coalition_ideology_map(
        coalition_df=coalition_df,
        output_path=path,
    )

    print(f"Saved → {path}")


# ==========================================================
# 5.7.5 Coalition Ideological Roles
# ==========================================================

def step_575_add_coalition_roles(
    coalition_ideology: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.7.5 Coalition Ideological Roles ===")

    df = add_coalition_ideological_roles(coalition_ideology)

    path = (
        PHASE5_TABLES_DIR
        / "narrative_coalitions"
        / "coalition_ideology_roles.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.7.6 Character–Coalition Mapping
# ==========================================================

def step_576_build_character_coalitions(
    community_df: pd.DataFrame,
    coalition_roles: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.7.6 Character–Coalition Mapping ===")

    df = build_character_coalition_roles(
        community_df=community_df,
        coalition_roles_df=coalition_roles,
    )

    path = (
        PHASE5_TABLES_DIR
        / "narrative_coalitions"
        / "character_coalition_roles.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.7.7 Narrative Role Affinity
# ==========================================================

def step_577_narrative_role_affinity(
    alignment_matrix: pd.DataFrame,
    character_roles: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.7.7 Narrative Role Affinity ===")

    df = build_narrative_role_affinity(
        alignment_matrix,
        character_roles,
    )

    path = (
        PHASE5_TABLES_DIR
        / "narrative_coalitions"
        / "cluster_narrative_role_affinity.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.7.8 Narrative Role Profiles Plot
# ==========================================================

def step_578_plot_narrative_role_profiles(
    role_affinity_df: pd.DataFrame,
) -> None:

    print("\n=== 5.7.8 Narrative Role Profiles ===")

    path = (
        PHASE5_FIGURES_DIR
        / "visualizations"
        / "cluster_narrative_role_profiles.png"
    )

    plot_cluster_narrative_role_profiles(
        role_affinity_df,
        path,
    )

    print(f"Saved → {path}")


# ==========================================================
# 5.8.1 Narrative Identity Reports
# ==========================================================

def step_581_generate_narrative_identity(
    coalition_roles: pd.DataFrame,
    audience_typology: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.8.1 Narrative Identity Reports ===")

    narrative_identity = build_narrative_identity_reports(
        coalition_roles_df=coalition_roles,
        audience_typology_df=audience_typology,
    )

    path = (
        PHASE5_TABLES_DIR
        / "narrative_coalitions"
        / "narrative_identity_reports.csv"
    )

    narrative_identity.to_csv(path, index=False)

    print(narrative_identity.to_string())
    print(f"Saved → {path}")

    return narrative_identity


# ==========================================================
# 5.8.2 Narrative Intensity
# ==========================================================

def step_582_compute_narrative_intensity(
    coalition_roles_df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.8.2 Narrative Intensity ===")

    intensity_df = compute_narrative_intensity(coalition_roles_df)

    path = (
        PHASE5_TABLES_DIR
        / "narrative_coalitions"
        / "narrative_intensity.csv"
    )

    intensity_df.to_csv(path, index=False)

    print(intensity_df.to_string())
    print(f"Saved → {path}")

    return intensity_df


# ==========================================================
# 5.8.3 Audience Profiles
# ==========================================================

def step_583_build_audience_profiles(
    survey_df: pd.DataFrame,
    cluster_labels: pd.Series,
) -> pd.DataFrame:

    print("\n=== 5.8.3 Audience Profiles ===")

    demographics = [
        "gender",
        "age_group",
        "education_level",
        "household_income",
    ]

    profile_df = build_audience_profiles(
        survey_df,
        cluster_labels,
        demographics,
    )

    path = (
        PHASE5_TABLES_DIR
        / "narrative_coalitions"
        / "audience_profiles.csv"
    )

    profile_df.to_csv(path, index=False)

    print(profile_df.to_string())
    print(f"Saved → {path}")

    return profile_df


# ==========================================================
# 5.8.4 Audience Narrative Profiles
# ==========================================================

def step_584_build_audience_narrative_profiles(
    narrative_identity: pd.DataFrame,
    narrative_intensity: pd.DataFrame,
    audience_profiles: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.8.4 Audience Narrative Profiles ===")

    result_df = build_audience_narrative_profiles(
        narrative_identity,
        narrative_intensity,
        audience_profiles,
    )

    path = (
        PHASE5_TABLES_DIR
        / "narrative_coalitions"
        / "audience_narrative_profiles.csv"
    )

    result_df.to_csv(path, index=False)

    print(result_df.to_string())
    print(f"Saved → {path}")

    return result_df


# ==========================================================
# 5.8.5 Fandom Ideology Dataset (Enriched)
# ==========================================================

def step_585_build_fandom_ideology_dataset(
    character_coords: pd.DataFrame,
    character_roles: pd.DataFrame,
    character_coalitions: pd.DataFrame,
    community_metrics: pd.DataFrame,
    cluster_coords: pd.DataFrame,
    audience_typology: pd.DataFrame,
    narrative_intensity: pd.DataFrame,
    character_polarization: pd.DataFrame,
    audience_profiles: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.8.5 Fandom Ideology Dataset (Enriched) ===")

    df = build_fandom_ideology_map_dataset(
        character_coords=character_coords,
        character_roles=character_roles,
        character_coalitions=character_coalitions,
        community_metrics=community_metrics,
        cluster_coords=cluster_coords,
        audience_typology=audience_typology,
        narrative_intensity=narrative_intensity,
        character_polarization=character_polarization,
        audience_profiles=audience_profiles,
    )

    path = (
        PHASE5_TABLES_DIR
        / "ideology_map"
        / "fandom_ideology_map_dataset.csv"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved dataset → {path}")

    return df


# ==========================================================
# 5.8.6 Fandom Ideology Dataset (Enriched)
# ==========================================================

def step_586_plot_fandom_ideology_map(
    df: pd.DataFrame,
    alignment_matrix,
) -> None:

    print("\n=== 5.8.6 Fandom Ideology Map (Enriched) ===")

    path = (
        PHASE5_FIGURES_DIR
        / "visualizations"
        / "fandom_ideology_map.png"
    )

    plot_fandom_ideology_map(
        df=df,
        alignment_matrix=alignment_matrix,
        output_path=path,
    )

    print(f"Saved plot → {path}")


# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase5_6(clean_dataset: pd.DataFrame) -> None:

    print("=== PHASE 5.6: NARRATIVE COALITIONS ===")

    _ensure_dirs()

    alignment_dir = PHASE5_TABLES_DIR / "alignment"
    phase4_dir = PHASE4_TABLES_DIR / "polarization"

    # ------------------------------------------------------
    # Load Inputs
    # ------------------------------------------------------

    alignment_matrix = pd.read_csv(
        alignment_dir / "cluster_character_preference_profiles.csv",
        index_col=0,
    )

    # FIX 1: transpose
    alignment_matrix = alignment_matrix.T

    # FIX 2: build correlation matrix from edge list
    correlation_edges = pd.read_csv(
        phase4_dir / "character_correlation_network.csv"
    )

    correlation_matrix = build_correlation_matrix_from_edges(
        correlation_edges
    )

    # FIX 3: align characters
    common_characters = [
        c for c in correlation_matrix.columns
        if c in alignment_matrix.columns
    ]

    alignment_matrix = alignment_matrix[common_characters]
    correlation_matrix = correlation_matrix.loc[
        common_characters,
        common_characters,
    ]

    character_coords = pd.read_csv(
        PHASE4_TABLES_DIR
        / "polarization"
        / "character_ideology_coordinates.csv"
    )

    cluster_coords = pd.read_csv(
        PHASE4_TABLES_DIR
        / "polarization"
        / "audience_cluster_ideology_coordinates.csv"
    )


    print(f"Characters used: {len(common_characters)}")

    respondent_cluster_assignments = pd.read_csv(
        PHASE3_TABLES_DIR
        / "respondent_cluster_assignments.csv"
    ).set_index("respondent_id")["audience_cluster"]

    character_polarization = pd.read_csv(
        PHASE5_TABLES_DIR
        / "polarization"
        / "character_polarization_summary.csv"
    )

    # ------------------------------------------------------
    # Run Steps
    # ------------------------------------------------------

    edges_df = step_561_build_networks(
        alignment_matrix,
        correlation_matrix,
    )

    edges_df = step_562_filter_edges(edges_df)

    community_df = step_563_detect_communities(edges_df)

    step_564_save_tables(edges_df, community_df)

    step_565_plot_networks(edges_df, community_df)

    community_metrics_df = step_566_compute_community_metrics(
        edges_df,
        community_df,
        alignment_matrix,
    )

    community_metrics_df = step_571_classify_coalitions(community_metrics_df)

    audience_cluster_interpretation = step_572_classify_audience_clusters(community_metrics_df)

    coalition_ideology = step_573_map_coalitions_to_ideology(
        community_df=community_df,
        metrics_df=community_metrics_df,
        ideology_df=character_coords,
        alignment_matrix=alignment_matrix,
    )

    step_574_plot_coalition_ideology(coalition_ideology)

    coalition_roles = step_575_add_coalition_roles(coalition_ideology)

    character_coalitions = step_576_build_character_coalitions(
        community_df,
        coalition_roles,
    )

    character_roles = pd.read_csv(
        PHASE5_TABLES_DIR
        / "narrative_structure"
        / "character_narrative_roles.csv"
    )

    archetype_affinity = step_577_narrative_role_affinity(
        alignment_matrix,
        character_roles,
    )

    step_578_plot_narrative_role_profiles(archetype_affinity)

    narrative_identity = step_581_generate_narrative_identity(
        coalition_roles,
        audience_cluster_interpretation,
    )

    narrative_intensity = step_582_compute_narrative_intensity(coalition_roles)

    audience_profiles = step_583_build_audience_profiles(
        survey_df=clean_dataset,
        cluster_labels=respondent_cluster_assignments
    )

    audience_narrative_profiles = step_584_build_audience_narrative_profiles(
        narrative_identity=narrative_identity,
        narrative_intensity=narrative_intensity,
        audience_profiles=audience_profiles,
    )

    fandom_map_df = step_585_build_fandom_ideology_dataset(
        character_coords=character_coords,
        character_roles=character_roles,
        character_coalitions=character_coalitions,
        community_metrics=community_metrics_df,  # 🔥 NEW
        cluster_coords=cluster_coords,
        audience_typology=audience_cluster_interpretation,
        narrative_intensity=narrative_intensity,
        character_polarization=character_polarization,
        audience_profiles=audience_profiles,
    )

    step_586_plot_fandom_ideology_map(
        fandom_map_df,
        alignment_matrix=alignment_matrix,  # NEW
    )
