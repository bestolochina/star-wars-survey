# analysis/transforms/character_coalition_roles.py

from __future__ import annotations

import pandas as pd


def build_character_coalition_roles(
    community_df: pd.DataFrame,
    coalition_roles_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Expand coalition-level roles to character-level.

    Input:
    ------
    community_df:
        audience_cluster | character | community_id

    coalition_roles_df:
        audience_cluster | community_id | ideological_role | ...

    Output:
    -------
    character | coalition_id | ideological_role
    (per audience cluster)

    Notes:
    ------
    - Keeps audience_cluster because coalitions are cluster-specific
    - Renames community_id → coalition_id for semantic clarity
    """

    # Merge character membership with coalition ideology
    df = community_df.merge(
        coalition_roles_df[
            ["audience_cluster", "community_id", "ideological_role"]
        ],
        on=["audience_cluster", "community_id"],
        how="left",
    )

    # Rename for consistency with downstream expectations
    df = df.rename(columns={
        "community_id": "coalition_id"
    })

    # Optional: reorder columns for clarity
    df = df[
        ["audience_cluster", "character", "coalition_id", "ideological_role"]
    ]

    return df