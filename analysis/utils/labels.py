# analysis/utils/labels.py

from __future__ import annotations

import pandas as pd
from src.config import (
    ALL_CLUSTER_LABELS,
    CHARACTER_IDEOLOGY_AXES_READABLE,
    CHARACTER_IDEOLOGY_QUADRANTS,
    CHARACTER_COMMUNITY_LABELS,
)


# ============================================================
# Helper: Move column after another column
# ============================================================

def _move_column_after(
    df: pd.DataFrame,
    column: str,
    after: str,
) -> pd.DataFrame:

    if column not in df.columns or after not in df.columns:
        return df

    cols = list(df.columns)

    cols.remove(column)

    insert_position = cols.index(after) + 1
    cols.insert(insert_position, column)

    return df[cols]


# ============================================================
# Audience Cluster Labels
# ============================================================

def add_audience_labels(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    if "cluster" not in df.columns:
        return df

    if "cluster_label" not in df.columns:

        df["cluster_label"] = (
            df["cluster"]
            .map(ALL_CLUSTER_LABELS["audience"])
        )

    df = _move_column_after(df, "cluster_label", "cluster")

    return df


# ============================================================
# Character Cluster Labels
# ============================================================

def add_character_labels(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    if "character_cluster" not in df.columns:
        return df

    if "character_cluster_label" not in df.columns:

        df["character_cluster_label"] = (
            df["character_cluster"]
            .map(ALL_CLUSTER_LABELS["character"])
        )

    df = _move_column_after(
        df,
        "character_cluster_label",
        "character_cluster",
    )

    return df


# ============================================================
# Dominant Character Cluster Labels
# ============================================================

def add_dominant_cluster_labels(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    if "dominant_character_cluster" not in df.columns:
        return df

    if "dominant_character_cluster_label" not in df.columns:

        df["dominant_character_cluster_label"] = (
            df["dominant_character_cluster"]
            .map(ALL_CLUSTER_LABELS["character"])
        )

    df = _move_column_after(
        df,
        "dominant_character_cluster_label",
        "dominant_character_cluster",
    )

    return df


# ============================================================
# Attached Character Cluster Labels
# ============================================================

def add_attached_cluster_labels(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    if "attached_cluster" not in df.columns:
        return df

    if "attached_cluster_label" not in df.columns:

        df["attached_cluster_label"] = (
            df["attached_cluster"]
            .map(ALL_CLUSTER_LABELS["character"])
        )

    df = _move_column_after(
        df,
        "attached_cluster_label",
        "attached_cluster",
    )

    return df


# ============================================================
# Master Label Attacher
# ============================================================

def attach_all_labels(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Attach all available cluster labels to a dataframe.
    Safe to run multiple times.
    """

    df = add_audience_labels(df)
    df = add_character_labels(df)
    df = add_attached_cluster_labels(df)
    df = add_dominant_cluster_labels(df)
    df = add_ideology_quadrant_labels(df)

    return df


def format_ideology_axes_column_names(df: pd.DataFrame) -> pd.DataFrame:

    axis1 = CHARACTER_IDEOLOGY_AXES_READABLE[1]
    axis2 = CHARACTER_IDEOLOGY_AXES_READABLE[2]

    df = df.rename(
        columns={
            "ideology_axis_1": axis1,
            "ideology_axis_2": axis2,
        }
    )

    return df


def add_ideology_quadrant_labels(df):

    df = df.copy()

    if "ideology_quadrant" not in df.columns:
        return df

    if "ideology_quadrant_label" not in df.columns:
        df["ideology_quadrant_label"] = (
            df["ideology_quadrant"]
            .map(CHARACTER_IDEOLOGY_QUADRANTS)
        )

    df = _move_column_after(
        df,
        "ideology_quadrant_label",
        "ideology_quadrant",
    )

    return df


def attach_character_community_labels(
    df,
):

    if "community" in df.columns:

        df["community_label"] = df["community"].map(
            CHARACTER_COMMUNITY_LABELS
        )

    return df