# analysis/phase4_1_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import PHASE4_TABLES_DIR, PHASE4_FIGURES_DIR, PHASE3_TABLES_DIR
from src.config import CHARACTER_RATING_COLUMNS

from analysis.transforms.matrix_builder import build_character_matrix

from analysis.metrics.audience_cluster_metrics import(
    compute_audience_cluster_profiles,
    compute_overall_means,
    compute_cluster_extremeness,
)

from analysis.visualization.cluster_profile_plots import (
    plot_cluster_profile_heatmap,
    plot_deviation_heatmap,
    plot_cluster_radar_plots,
)

PHASE4_1_TABLES_DIR = (
    PHASE4_TABLES_DIR / "phase4_1_audience_cluster_profiles"
)

PHASE4_1_FIGURES_DIR = (
    PHASE4_FIGURES_DIR / "phase4_1_audience_cluster_profiles"
)


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs() -> None:
    PHASE4_1_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    PHASE4_1_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# 4.1.1 Build Rating Matrix (RAW)
# ==========================================================

def step_411_build_matrix(df: pd.DataFrame) -> pd.DataFrame:

    print("\n=== 4.1.1 Build Raw Rating Matrix ===")

    matrix_raw = build_character_matrix(
        df,
        respondent_id="respondent_id",
        character_columns=CHARACTER_RATING_COLUMNS,
        standardize=False,
    )

    print(f"Matrix shape: {matrix_raw.shape}")

    return matrix_raw


# ==========================================================
# 4.1.2 Load Respondent Clusters
# ==========================================================

def step_412_load_clusters(path) -> pd.DataFrame:

    print("\n=== 4.1.2 Load Respondent Clusters ===")

    cluster_df = pd.read_csv(path)

    cluster_df = cluster_df.rename(
        columns={"cluster": "audience_cluster"}
    )

    required = {"respondent_id", "audience_cluster"}
    missing = required - set(cluster_df.columns)

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    print(cluster_df.head())

    return cluster_df


# ==========================================================
# 4.1.3 Audience Cluster Profiles
# ==========================================================

def step_413_cluster_profiles(
    matrix_raw: pd.DataFrame,
    cluster_df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.1.3 Audience Cluster Profiles ===")

    profile_df = compute_audience_cluster_profiles(
        matrix_raw,
        cluster_df,
    )

    profile_df.to_csv(
        PHASE4_1_TABLES_DIR / "cluster_mean_profiles.csv",
        index=False,
    )

    print(profile_df.to_string(index=False))

    return profile_df


# ==========================================================
# 4.1.4 Overall Means
# ==========================================================

def step_414_overall_means(
    profile_df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.1.4 Overall Character Means ===")

    overall_df = compute_overall_means(profile_df)

    overall_df.to_csv(
        PHASE4_1_TABLES_DIR / "cluster_overall_means.csv",
        index=False,
    )

    return overall_df


# ==========================================================
# 4.1.5 Extremeness Analysis
# ==========================================================

def step_415_extremeness(
    profile_df: pd.DataFrame,
    overall_df: pd.DataFrame,
) -> None:

    print("\n=== 4.1.5 Cluster Extremeness ===")

    extreme_df = compute_cluster_extremeness(
        profile_df,
        overall_df,
    )

    extreme_df.to_csv(
        PHASE4_1_TABLES_DIR / "cluster_extremeness_scores.csv",
        index=False,
    )

    print(extreme_df.to_string(index=False))


# ==========================================================
# 4.1.6 Heatmap
# ==========================================================

def step_416_heatmap(profile_df: pd.DataFrame) -> None:

    print("\n=== 4.1.6 Cluster Profile Heatmap ===")

    plot_cluster_profile_heatmap(
        profile_df,
        save_path=PHASE4_1_FIGURES_DIR / "audience_cluster_profile_heatmap.png",
    )


# ==========================================================
# 4.1.7 Compute Deviations (CORE OBJECT)
# ==========================================================

def step_417_compute_deviations(
    profile_df: pd.DataFrame,
    overall_df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.1.7 Compute Cluster Deviations ===")

    deviations = profile_df.merge(
        overall_df,
        on="character",
        how="left",
    )

    deviations["deviation"] = (
            deviations["mean_rating"]
            - deviations["mean_rating_overall"]
    )

    deviations.to_csv(
        PHASE4_1_TABLES_DIR / "audience_cluster_deviations.csv",
        index=False,
    )

    print(deviations.columns.tolist())

    return deviations


# ==========================================================
# 4.1.8 Deviation Heatmap
# ==========================================================

def step_418_deviation_heatmap(
    deviations: pd.DataFrame,
) -> None:

    print("\n=== 4.1.8 Deviation Heatmap ===")

    plot_deviation_heatmap(
        deviations,
        save_path=PHASE4_1_FIGURES_DIR / "audience_cluster_deviation_heatmap.png",
    )


# ==========================================================
# 4.1.9 Radar Plots
# ==========================================================

def step_419_cluster_radar_plots(
    deviations: pd.DataFrame,
) -> None:

    print("\n=== 4.1.9 Cluster Radar Plots ===")

    plot_cluster_radar_plots(
        deviations,
        save_path=PHASE4_1_FIGURES_DIR / "audience_cluster_radar_plots.png",
    )


# ==========================================================
# 4.1.10 Top Deviations Table
# ==========================================================

def step_420_top_deviations_table(
    deviations: pd.DataFrame,
    top_n: int = 5,
) -> None:

    print("\n=== 4.1.10 Top Deviations Table ===")

    top_dev = (
        deviations.assign(abs_dev=lambda d: d["deviation"].abs())
        .sort_values(["audience_cluster", "abs_dev"], ascending=[True, False])
        .groupby("audience_cluster")
        .head(top_n)
        .drop(columns="abs_dev")
    )

    top_dev.to_csv(
        PHASE4_1_TABLES_DIR / "audience_cluster_top_deviations.csv",
        index=False,
    )

    print(top_dev.to_string(index=False))


# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase4_1(
    df: pd.DataFrame,
) -> None:

    print("=== PHASE 4.1: AUDIENCE CLUSTER PROFILES ===")

    _ensure_dirs()

    respondent_cluster_path = (
        PHASE3_TABLES_DIR
        / "respondent_cluster_assignments.csv"
    )

    # -----------------------------------------
    # Matrix
    # -----------------------------------------
    matrix_raw = step_411_build_matrix(df)

    # -----------------------------------------
    # Respondent clusters
    # -----------------------------------------
    cluster_df = step_412_load_clusters(
        respondent_cluster_path
    )

    # -----------------------------------------
    # Profiles
    # -----------------------------------------
    profile_df = step_413_cluster_profiles(
        matrix_raw,
        cluster_df,
    )

    # -----------------------------------------
    # Reference baseline
    # -----------------------------------------
    overall_df = step_414_overall_means(profile_df)

    # -----------------------------------------
    # Extremeness
    # -----------------------------------------
    step_415_extremeness(profile_df, overall_df)

    # -----------------------------------------
    # Profile heatmap
    # -----------------------------------------
    step_416_heatmap(profile_df)

    # -----------------------------------------
    # Deviations (NEW CORE OBJECT)
    # -----------------------------------------
    deviations = step_417_compute_deviations(
        profile_df,
        overall_df,
    )

    # -----------------------------------------
    # New visualizations + tables
    # -----------------------------------------
    step_418_deviation_heatmap(deviations)
    step_419_cluster_radar_plots(deviations)
    step_420_top_deviations_table(deviations)
