# analysis/utils/labels.py

from __future__ import annotations

import pandas as pd

from src.config import ALL_CLUSTER_LABELS


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

    return df