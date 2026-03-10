# analysis/metrics/character_audience_structure_validation.py

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from sklearn.metrics import silhouette_score, adjusted_rand_score


def compute_character_correlation(
    matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Pearson correlation between characters.
    """

    corr = matrix.corr(method="pearson")

    return corr


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
    matrix_filled = matrix.fillna(matrix.mean())

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
    distance = distance.clip(0.0, 2.0)

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
            "character_cluster": labels,
        }
    ).sort_values("character_cluster")

    return Z, cluster_df, distance_df


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
        .loc[matrix.columns]["character_cluster"]
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
        .loc[matrix.columns]["character_cluster"]
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
            .loc[matrix.columns]["character_cluster"]
            .values
        )

        ari = adjusted_rand_score(base_labels, boot_labels)
        ari_scores.append(float(ari))

    return pd.DataFrame({"ARI": ari_scores})


# ==========================================================
# PHASE 3 — CHARACTER CLUSTER PROFILES
# ==========================================================

def compute_cluster_profiles(
    matrix_raw: pd.DataFrame,
    cluster_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Phase 3:
    Compute mean character ratings within each CHARACTER cluster.

    Returns LONG format:
        character | cluster | mean_rating
    """

    # -----------------------------------
    # Character → cluster mapping
    # -----------------------------------
    char_to_cluster = dict(
        zip(cluster_df["character"], cluster_df["character_cluster"])
    )

    # -----------------------------------
    # Wide → Long
    # -----------------------------------
    long_df = (
        matrix_raw
        .melt(
            var_name="character",
            value_name="rating",
        )
        .dropna(subset=["rating"])
    )

    long_df["character_cluster"] = long_df["character"].map(char_to_cluster)

    # -----------------------------------
    # Mean rating per character per cluster
    # -----------------------------------
    profile_df = (
        long_df
        .groupby(["character", "character_cluster"], as_index=False)["rating"]
        .mean()
        .rename(columns={"rating": "mean_rating"})
        .sort_values(["character_cluster", "character"])
    )

    # -----------------------------------
    # Cluster sizes (number of ratings)
    # -----------------------------------
    cluster_sizes = (
        long_df
        .groupby("character_cluster")["rating"]
        .count()
        .rename("n_ratings")
        .reset_index()
    )

    profile_df = profile_df.merge(
        cluster_sizes,
        on="character_cluster",
        how="left",
    )

    return profile_df


# ==========================================================
# PHASE 4 — CLUSTER MEAN PROFILES (AUDIENCE SEGMENTS)
# ==========================================================

def load_cluster_profiles(path: str | pd.PathLike) -> pd.DataFrame:
    """
    Load cluster mean profiles and validate schema.

    Expected columns:
        character | audience_cluster | mean_rating
    """

    df = pd.read_csv(path)

    required = {"character", "audience_cluster", "mean_rating"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    return df.sort_values(["audience_cluster", "character"]).reset_index(drop=True)


# ==========================================================
# Overall Mean Reference
# ==========================================================

def compute_overall_means(
    profile_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute overall mean rating per character
    across all clusters.

    Returns:
        character | mean_rating_overall
    """

    overall_df = (
        profile_df
        .groupby("character", as_index=False)["mean_rating"]
        .mean()
        .rename(
            columns={"mean_rating": "mean_rating_overall"}
        )
        .sort_values("character")
    )

    return overall_df


# ==========================================================
# Cluster Extremeness Metric
# ==========================================================

def compute_cluster_extremeness(
    profile_df: pd.DataFrame,
    overall_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Measure how strongly each cluster deviates
    from overall audience taste.

    Extremeness =
        mean absolute deviation from global mean.
    """

    merged = profile_df.merge(
        overall_df,
        on="character",
        how="left",
    )

    merged["abs_deviation"] = (
        merged["mean_rating"]
        - merged["mean_rating_overall"]
    ).abs()

    extreme_df = (
        merged
        .groupby("audience_cluster", as_index=False)["abs_deviation"]
        .mean()
        .rename(
            columns={"abs_deviation": "extremeness_score"}
        )
        .sort_values("extremeness_score", ascending=False)
    )

    return extreme_df

# analysis/metrics/cluster_profiles.py

def compute_audience_cluster_profiles(
    matrix_raw: pd.DataFrame,
    respondent_clusters: pd.DataFrame,
) -> pd.DataFrame:
    """
    Phase 4:
    Compute mean character ratings within RESPONDENT clusters.

    Parameters
    ----------
    matrix_raw :
        Wide matrix
            index = respondent_id
            columns = characters

    respondent_clusters :
        DataFrame:
            respondent_id | audience_cluster

    Returns
    -------
    LONG format:
        character | audience_cluster | mean_rating
    """

    # -----------------------------------
    # Attach cluster labels to respondents
    # -----------------------------------
    df = matrix_raw.copy()

    cluster_map = respondent_clusters.set_index(
        "respondent_id"
    )["audience_cluster"]

    df["audience_cluster"] = cluster_map

    # -----------------------------------
    # Wide → Long
    # -----------------------------------
    long_df = (
        df.reset_index()
        .melt(
            id_vars=["respondent_id", "audience_cluster"],
            var_name="character",
            value_name="rating",
        )
        .dropna(subset=["rating"])
    )

    # -----------------------------------
    # Mean rating per character per cluster
    # -----------------------------------
    profile_df = (
        long_df
        .groupby(["character", "audience_cluster"], as_index=False)["rating"]
        .mean()
        .rename(columns={"rating": "mean_rating"})
        .sort_values(["audience_cluster", "character"])
    )

    return profile_df


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
        columns={
            "character": "respondent_id",
            "character_cluster": "audience_cluster",
        }
    )

    return Z, respondent_cluster_df, model
