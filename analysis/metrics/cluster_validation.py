# analysis/metrics/cluster_validation.py

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.metrics import (
    silhouette_score,
    adjusted_rand_score,
)


def compute_silhouette(
    matrix: pd.DataFrame,
    cluster_df: pd.DataFrame,
) -> float:
    """
    Compute silhouette score for character clustering.

    Parameters
    ----------
    matrix : respondent × character (standardized)
    cluster_df : columns ["character", "cluster"]

    Returns
    -------
    silhouette : float
    """

    # characters are observations → transpose
    X = matrix.T.values

    labels = (
        cluster_df
        .set_index("character")
        .loc[matrix.columns]["cluster"]
        .values
    )

    score = silhouette_score(X, labels, metric="euclidean")

    return float(score)


def bootstrap_cluster_stability(
    matrix: pd.DataFrame,
    base_cluster_df: pd.DataFrame,
    clustering_fn,
    n_bootstrap: int = 100,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Bootstrap stability using Adjusted Rand Index.
    """

    rng = np.random.default_rng(random_state)

    base_labels = (
        base_cluster_df
        .set_index("character")
        .loc[matrix.columns]["cluster"]
        .values
    )

    ari_scores: list[float] = []

    for _ in range(n_bootstrap):

        sample_idx = rng.choice(
            matrix.index,
            size=len(matrix),
            replace=True,
        )

        boot_matrix = matrix.loc[sample_idx]

        _, boot_cluster_df, _ = clustering_fn(
            boot_matrix,
            linkage_method="average",
            n_clusters=3,
        )

        boot_labels = (
            boot_cluster_df
            .set_index("character")
            .loc[matrix.columns]["cluster"]
            .values
        )

        ari = adjusted_rand_score(base_labels, boot_labels)
        ari_scores.append(float(ari))

    return pd.DataFrame({"ARI": ari_scores})
