# analysis/interpretation/narrative_intensity.py

from __future__ import annotations
import pandas as pd


def compute_narrative_intensity(
    coalition_roles_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute intensity scores per audience cluster.

    Returns:
    - audience_cluster
    - polarization_strength
    - hero_core_dominance
    """

    results = []

    for audience_cluster, df in coalition_roles_df.groupby("audience_cluster"):

        total_coalitions = len(df)

        # -------------------------
        # 1. Polarization strength
        # -------------------------
        has_hero = (df["ideological_role"] == "Hero Core").any()
        has_dark = df["ideological_role"].isin([
            "Dark Power Core",
            "Rejected Dark Core"
        ]).any()

        if has_hero and has_dark:
            # Strength based on ideological distance
            hero_center = df[df["ideological_role"] == "Hero Core"][
                "ideology_axis_1"
            ].mean()

            dark_center = df[df["ideological_role"].isin([
                "Dark Power Core",
                "Rejected Dark Core"
            ])]["ideology_axis_1"].mean()

            polarization_strength = abs(hero_center - dark_center)
        else:
            polarization_strength = 0

        # -------------------------
        # 2. Hero dominance
        # -------------------------
        hero_share = (
            (df["ideological_role"] == "Hero Core").sum()
            / total_coalitions
        )

        # Weight by preference intensity
        hero_strength = df[df["ideological_role"] == "Hero Core"][
            "mean_preference"
        ].mean()

        hero_core_dominance = hero_share * hero_strength

        results.append({
            "audience_cluster": audience_cluster,
            "polarization_strength": polarization_strength,
            "hero_core_dominance": hero_core_dominance,
        })

    narrative_intensity = pd.DataFrame(results)
    narrative_intensity["audience_cluster"] = narrative_intensity["audience_cluster"].astype(int)

    return narrative_intensity