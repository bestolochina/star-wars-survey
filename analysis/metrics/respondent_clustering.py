# analysis/metrics/respondent_clustering.py

from __future__ import annotations

import pandas as pd

from analysis.metrics.hierarchical_clustering import (
    hierarchical_character_clustering,
)


# ==========================================================
# Respondent Clustering (Phase 3B)
# ==========================================================

def hierarchical_respondent_clustering(
    matrix: pd.DataFrame,
    n_clusters: int,
):
    """
    Cluster RESPONDENTS based on rating patterns.

    Reuses character clustering by transposing matrix.

    Parameters
    ----------
    matrix :
        standardized matrix
            rows = respondents
            columns = characters

    Returns
    -------
    Z :
        linkage matrix

    respondent_cluster_df :
        respondent_id | cluster
    """

    # -----------------------------------
    # transpose → respondents become "features"
    # -----------------------------------
    matrix_T = matrix.T

    Z, cluster_df, model = hierarchical_character_clustering(
        matrix_T,
        linkage_method="average",
        n_clusters=n_clusters,
    )

    # rename column for clarity
    respondent_cluster_df = cluster_df.rename(
        columns={"character": "respondent_id"}
    )

    return Z, respondent_cluster_df, model