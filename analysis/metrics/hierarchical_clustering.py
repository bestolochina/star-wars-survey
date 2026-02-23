# analysis/metrics/hierarchical_clustering.py

from __future__ import annotations

import pandas as pd
import numpy as np

from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform


# ==========================================================
# BUILD CORRELATION DISTANCE MATRIX
# ==========================================================

def correlation_distance_matrix(
    matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute 1 - Pearson correlation distance between characters.
    """

    corr = matrix.corr(method="pearson")

    distance = 1.0 - corr

    # numerical safety
    np.fill_diagonal(distance.values, 0.0)

    return distance


# ==========================================================
# HIERARCHICAL CLUSTERING
# ==========================================================

def hierarchical_character_clustering(
    matrix: pd.DataFrame,
    *,
    linkage_method: str = "average",
    n_clusters: int = 4,
):
    """
    Perform hierarchical clustering on characters.

    Returns:
        linkage_matrix
        cluster_assignments (DataFrame)
        distance_matrix
    """

    distance_df = correlation_distance_matrix(matrix)

    # scipy expects condensed distance vector
    condensed = squareform(distance_df.values)

    Z = linkage(condensed, method=linkage_method)

    labels = fcluster(Z, n_clusters, criterion="maxclust")

    cluster_df = pd.DataFrame(
        {
            "character": distance_df.index,
            "cluster": labels,
        }
    ).sort_values("cluster")

    return Z, cluster_df, distance_df