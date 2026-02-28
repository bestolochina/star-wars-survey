# analysis/metrics/imputation.py

from __future__ import annotations

import pandas as pd
from sklearn.impute import KNNImputer


def knn_impute_matrix(
    matrix: pd.DataFrame,
    *,
    n_neighbors: int = 5,
    weights: str = "distance",
) -> pd.DataFrame:
    """
    Impute missing values using KNN.

    Parameters
    ----------
    matrix : respondent × character matrix (standardized)
    n_neighbors : number of neighbors
    weights : 'uniform' or 'distance'

    Returns
    -------
    DataFrame with imputed values.
    """

    imputer = KNNImputer(
        n_neighbors=n_neighbors,
        weights=weights,
    )

    imputed_array = imputer.fit_transform(matrix)

    return pd.DataFrame(
        imputed_array,
        index=matrix.index,
        columns=matrix.columns,
    )
