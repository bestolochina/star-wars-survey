# analysis/interpretation/phase5_7_interpretation.py

import pandas as pd


def classify_coalition(row: pd.Series) -> str:

    if row["density"] >= 0.9 and row["mean_weight"] >= 0.5:
        if row["mean_preference"] >= 4.5:
            return "Core Alliance"
        elif row["mean_preference"] < 3:
            return "Antagonist Bloc"
        else:
            return "Elite Clique"

    if row["density"] >= 0.6:
        if row["mean_preference"] >= 4:
            return "Strong Alliance"
        else:
            return "Contested Bloc"

    if row["mean_preference"] >= 4:
        return "Peripheral Alliance"

    return "Fragmented Field"


def classify_audience_clusters(
    metrics_df: pd.DataFrame
) -> pd.DataFrame:

    results = []

    for audience_cluster, df in metrics_df.groupby("audience_cluster"):

        n_comms = df["community_id"].nunique()

        low_pref = (df["mean_preference"] < 3).any()
        high_pref = (df["mean_preference"] > 4.5).any()
        high_pref_ratio = (df["mean_preference"] > 4.5).mean()

        mean_density = df["density"].mean()

        if n_comms == 1:
            label = "Unified Narrative"

        elif low_pref and high_pref:
            label = "Polarized Narrative"

        elif n_comms >= 3 and mean_density < 0.5:
            label = "Fragmented Weak Narrative"

        elif n_comms >= 3 and high_pref_ratio > 0.7:
            label = "Multi-Core Strong Narrative"  # 🔥 NEW

        elif n_comms >= 3:
            label = "Fragmented Narrative"

        else:
            label = "Layered Narrative"

        results.append({
            "audience_cluster": audience_cluster,
            "n_communities": n_comms,
            "mean_density": mean_density,
            "cluster_type": label,
        })

    return pd.DataFrame(results)