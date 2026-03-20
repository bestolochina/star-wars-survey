# analysis/pipelines/phase5_6_interpretation_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import (
    PHASE5_TABLES_DIR,
    PHASE4_TABLES_DIR,
    PHASE5_FIGURES_DIR,
)

from analysis.transforms.correlation_matrix_from_edges import build_correlation_matrix_from_edges
from analysis.transforms.coalition_ideology_mapping import build_coalition_ideology_mapping
from analysis.interpretation.phase5_7_interpretation import classify_coalition, classify_audience_clusters

from analysis.metrics.phase5_6_narrative_coalitions import (
    build_cluster_conditioned_edges,
    filter_edges,
    detect_communities,
    compute_community_metrics,
)

from analysis.visualization.phase5_plots import (
    plot_audience_conditioned_character_networks,
    plot_coalition_ideology_map,
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

    print(f"Rows: {len(community_df)}")

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
# Pipeline Entry
# ==========================================================

def run_phase5_6() -> None:

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

    print(f"Characters used: {len(common_characters)}")

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

    metrics_df = step_566_compute_community_metrics(
        edges_df,
        community_df,
        alignment_matrix,
    )

    metrics_df = step_571_classify_coalitions(metrics_df)

    audience_cluster_interpretation = step_572_classify_audience_clusters(metrics_df)

    coalition_ideology = step_573_map_coalitions_to_ideology(
        community_df=community_df,
        metrics_df=metrics_df,
        ideology_df=character_coords,
        alignment_matrix=alignment_matrix,
    )

    step_574_plot_coalition_ideology(coalition_ideology)
