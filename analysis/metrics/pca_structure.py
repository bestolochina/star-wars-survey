# analysis/metrics/pca_structure.py

from __future__ import annotations

import pandas as pd
from sklearn.decomposition import PCA


def compute_character_pca(
    matrix: pd.DataFrame,
) -> tuple[PCA, pd.DataFrame, pd.DataFrame]:
    """
    Perform PCA on character rating matrix.

    Missing values are imputed using column means
    (standard approach for correlation-based PCA).
    """

    # --------------------------------------------------
    # Handle missing values
    # --------------------------------------------------

    matrix_filled = matrix.copy()

    # fill NaN with column mean
    matrix_filled = matrix_filled.apply(
        lambda col: col.fillna(col.mean()),
        axis=0,
    )

    # --------------------------------------------------
    # PCA
    # --------------------------------------------------

    pca = PCA()
    components = pca.fit_transform(matrix_filled)

    # --------------------------------------------------
    # Variance explained
    # --------------------------------------------------

    explained_variance_df = pd.DataFrame(
        {
            "component": range(1, len(pca.explained_variance_) + 1),
            "eigenvalue": pca.explained_variance_,
            "variance_explained": pca.explained_variance_ratio_,
            "cumulative_variance": pca.explained_variance_ratio_.cumsum(),
        }
    )

    # --------------------------------------------------
    # Loadings
    # --------------------------------------------------

    loadings_df = pd.DataFrame(
        pca.components_.T,
        index=matrix.columns,
        columns=[
            f"PC{i}"
            for i in range(1, pca.components_.shape[0] + 1)
        ],
    )

    return pca, explained_variance_df, loadings_df