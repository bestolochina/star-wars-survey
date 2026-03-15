# analysis/pipelines/phase5_4_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import PHASE5_TABLES_DIR

from analysis.metrics.phase5_4_narrative_structure import (
    compute_cluster_narrative_deviation,
    compute_cluster_narrative_anchors,
    compute_cluster_narrative_coherence,
    compute_cluster_narrative_extremeness,
    compute_audience_narrative_archetypes,
    reshape_cluster_character_preference_matrix,
    compute_character_narrative_roles,
)


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs() -> None:

    (PHASE5_TABLES_DIR / "narrative_structure").mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# 5.4.1 Cluster Narrative Deviation Matrix
# ==========================================================

def step_541_cluster_narrative_deviation(
    character_cluster_means: pd.DataFrame,
    global_character_means: pd.Series,
) -> pd.DataFrame:

    print("\n=== 5.4.1 Cluster Narrative Deviation Matrix ===")

    df = compute_cluster_narrative_deviation(
        character_cluster_means,
        global_character_means,
    )

    path = (
        PHASE5_TABLES_DIR
        / "narrative_structure"
        / "cluster_narrative_deviation_matrix.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.4.2 Narrative Anchor Characters
# ==========================================================

def step_542_cluster_narrative_anchors(
    deviation_matrix: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.4.2 Narrative Anchor Characters ===")

    df = compute_cluster_narrative_anchors(
        deviation_matrix
    )

    path = (
        PHASE5_TABLES_DIR
        / "narrative_structure"
        / "cluster_narrative_anchor_characters.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.4.3 Narrative Coherence Index
# ==========================================================

def step_543_cluster_narrative_coherence(
    deviation_matrix: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.4.3 Narrative Coherence Index ===")

    df = compute_cluster_narrative_coherence(
        deviation_matrix
    )

    path = (
        PHASE5_TABLES_DIR
        / "narrative_structure"
        / "cluster_narrative_coherence_index.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.4.4 Narrative Extremeness
# ==========================================================

def step_544_cluster_narrative_extremeness(
    deviation_matrix: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.4.4 Narrative Extremeness ===")

    df = compute_cluster_narrative_extremeness(
        deviation_matrix
    )

    path = (
        PHASE5_TABLES_DIR
        / "narrative_structure"
        / "cluster_narrative_extremeness.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.4.5 Audience Narrative Archetypes
# ==========================================================

def step_545_audience_narrative_archetypes(
    cluster_profiles: pd.DataFrame,
    narrative_coherence: pd.DataFrame,
    anchors: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.4.5 Audience Narrative Archetypes ===")

    df = compute_audience_narrative_archetypes(
        cluster_profiles,
        narrative_coherence,
        anchors,
    )

    path = (
        PHASE5_TABLES_DIR
        / "narrative_structure"
        / "audience_cluster_narrative_archetypes.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.4.6 Character Narrative Roles
# ==========================================================

def step_546_character_narrative_roles() -> None:

    print("\n=== 5.4.6 Character Narrative Roles ===")

    polarization_index = pd.read_csv(
        PHASE5_TABLES_DIR / "alignment/character_polarization_index.csv"
    )

    polarization_summary = pd.read_csv(
        PHASE5_TABLES_DIR / "polarization/character_polarization_summary.csv"
    )

    roles = compute_character_narrative_roles(
        polarization_index,
        polarization_summary,
    )

    print(roles.to_string())

    path = (
        PHASE5_TABLES_DIR / "narrative_structure/"
        "character_narrative_roles.csv"
    )

    roles.to_csv(path, index=False)

    print(f"Saved → {path}")


# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase5_4() -> None:

    print("=== PHASE 5.4: NARRATIVE STRUCTURE SYNTHESIS ===")

    _ensure_dirs()

    alignment_dir = PHASE5_TABLES_DIR / "alignment"

    narrative_dir = PHASE5_TABLES_DIR / "narrative_profiles"

    # ------------------------------------------------------
    # Load Inputs
    # ------------------------------------------------------

    character_cluster_means = pd.read_csv(
        alignment_dir / "cluster_character_preference_profiles.csv",
        index_col=0,
    )

    character_cluster_means = reshape_cluster_character_preference_matrix(
        character_cluster_means
    )

    cluster_profiles = pd.read_csv(
        narrative_dir
        / "cluster_narrative_profiles.csv"
    )

    # ------------------------------------------------------
    # Global character baseline
    # ------------------------------------------------------

    alignment_matrix = pd.read_csv(
        alignment_dir / "audience_character_alignment_matrix.csv",
        index_col=0,
    )

    global_character_means = alignment_matrix.mean()

    # ------------------------------------------------------
    # 5.4 Steps
    # ------------------------------------------------------

    deviation_matrix = step_541_cluster_narrative_deviation(
        character_cluster_means,
        global_character_means,
    )

    anchors = step_542_cluster_narrative_anchors(
        deviation_matrix
    )

    coherence = step_543_cluster_narrative_coherence(
        deviation_matrix
    )

    step_544_cluster_narrative_extremeness(
        deviation_matrix
    )

    step_545_audience_narrative_archetypes(
        cluster_profiles,
        coherence,
        anchors,
    )

    step_546_character_narrative_roles()

