# analysis/interpretation/coalition_roles.py

from __future__ import annotations

import pandas as pd


def classify_coalition_ideological_role(row: pd.Series) -> str:
    """
    Assign ideological meaning to a coalition based on its position.
    """

    x = row["ideology_axis_1"]
    y = row["ideology_axis_2"]

    # -------------------------
    # Strong poles (clear meaning)
    # -------------------------
    if x >= 1:
        if y >= 0.2:
            return "Mythic Hero Core"
        elif y <= -0.1:
            return "Pragmatic Hero Bloc"
        else:
            return "Hero Core"

    if x <= -1:
        if row["mean_preference"] < 2.5:
            return "Rejected Dark Core"  # 🔥 new
        elif row["mean_preference"] < 3.5:
            return "Contested Dark Core"
        else:
            return "Dark Power Core"

    # -------------------------
    # Middle zone (mixed narratives)
    # -------------------------
    if -1 < x < 1:
        if y >= 0.2:
            return "Complex / Divided Field"
        elif y <= -0.2:
            return "Low-Engagement Field"
        else:
            return "Narrative Middle Ground"

    return "Unclassified"


def add_coalition_ideological_roles(
    coalition_ideology_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Adds ideological role labels to coalition ideology table.
    """

    df = coalition_ideology_df.copy()

    df["ideological_role"] = df.apply(
        classify_coalition_ideological_role,
        axis=1,
    )

    return df