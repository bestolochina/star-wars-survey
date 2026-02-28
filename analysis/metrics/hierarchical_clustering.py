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
    Compute 1 - Pearson correlation distance.

    Handles missing-overlap cases safely and guarantees
    symmetry required by scipy.squareform.
    """

    # -----------------------------------
    # Correlation
    # -----------------------------------
    corr = matrix.corr(method="pearson")

    # -----------------------------------
    # Handle undefined correlations
    # (no shared ratings)
    # -----------------------------------
    corr = corr.fillna(0.0)

    # -----------------------------------
    # Convert to distance
    # -----------------------------------
    distance = 1.0 - corr

    # -----------------------------------
    # Force symmetry (floating safety)
    # -----------------------------------
    distance = (distance + distance.T) / 2

    # -----------------------------------
    # Clean numerical artifacts
    # -----------------------------------
    distance = distance.clip(lower=0.0)

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

    if not np.allclose(
            distance_df.values,
            distance_df.values.T,
            equal_nan=True,
    ):
        raise ValueError("Distance matrix not symmetric.")

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