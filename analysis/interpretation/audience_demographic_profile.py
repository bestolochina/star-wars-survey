# analysis/interpretation/audience_demographic_profile.py

from __future__ import annotations
import pandas as pd


def build_audience_profiles(
    survey_df: pd.DataFrame,
    cluster_labels: pd.Series,
    demographics: list[str],
) -> pd.DataFrame:
    """
    Build demographic distribution per audience cluster.
    """

    df = survey_df.copy()

    # 🔥 FIX: proper merge instead of direct assignment
    df = df.merge(
        cluster_labels.rename("audience_cluster"),
        left_on="respondent_id",
        right_index=True,
        how="inner",
    )

    results = []

    for demo in demographics:

        dist = (
            df
            .groupby(["audience_cluster", demo], observed=False)
            .size()
            .reset_index(name="count")
        )

        total = dist.groupby("audience_cluster")["count"].transform("sum")
        dist["share"] = dist["count"] / total

        dist = dist.rename(columns={demo: "category"})
        dist["demographic"] = demo

        results.append(dist)

    audience_profiles = pd.concat(results, ignore_index=True)
    audience_profiles["audience_cluster"] = audience_profiles["audience_cluster"].astype(int)

    return audience_profiles