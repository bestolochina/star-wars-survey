# analysis/phase5_1_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import PHASE5_TABLES_DIR
from src.config import DEMOGRAPHICS_COLUMNS
from src.io_utils import load_respondent_clusters
from analysis.utils.labels import attach_all_labels

from analysis.metrics.segmentation_strength import (
    build_contingency_table,
    compute_chisquare,
    compute_cramers_v,
    adjust_pvalues,
    check_min_expected,
)


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs() -> None:

    (PHASE5_TABLES_DIR / "segmentation").mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# 5.1.1 Load Respondent Audience Clusters
# ==========================================================

def step_511_load_respondent_audience_clusters(
    df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.1.1 Load Respondent Audience Clusters ===")

    clusters = load_respondent_clusters()

    merged = df.merge(
        clusters,
        on="respondent_id",
        how="inner",
    )

    merged = attach_all_labels(merged)

    print(merged.head().to_string())

    return merged


# ==========================================================
# 5.1.2 Audience Cluster × Demographic Contingency Tables
# ==========================================================

def step_512_audience_cluster_demographic_contingency_tables(
    df: pd.DataFrame,
) -> dict:

    print("\n=== 5.1.2 Audience Cluster × Demographic Contingency Tables ===")

    tables = {}

    for demo in DEMOGRAPHICS_COLUMNS.keys():
        table = build_contingency_table(
            df,
            demo,
            cluster_col="audience_cluster",
        )

        tables[demo] = table

        path = (
                PHASE5_TABLES_DIR
                / "segmentation"
                / f"audience_cluster_by_{demo}_contingency_table.csv"
        )

        table.to_csv(path)

        print(f"\n{demo}")
        print(table.to_string())
        print(f"Saved → {path}")

    return tables


# ==========================================================
# 5.1.3 Audience Cluster–Demographic Chi-square Tests
# ==========================================================

def step_513_audience_cluster_demographic_chisquare_tests(
    tables: dict,
) -> pd.DataFrame:

    print("\n=== 5.1.3 Audience Cluster–Demographic Chi-square Tests ===")

    rows = []

    for demo, table in tables.items():

        stats = compute_chisquare(table)

        rows.append(
            {
                "demographic_variable": demo,
                **stats,
            }
        )

    df = pd.DataFrame(rows)

    print(df.to_string(index=False))

    return df


# ==========================================================
# 5.1.4 Audience Cluster–Demographic Effect Sizes
# ==========================================================

def step_514_audience_cluster_demographic_effect_sizes(
    chisq: pd.DataFrame,
    tables: dict,
) -> pd.DataFrame:

    print("\n=== 5.1.4 Audience Cluster–Demographic Effect Sizes (Cramér's V) ===")

    values = []

    for _, row in chisq.iterrows():

        demo = row["demographic_variable"]

        v = compute_cramers_v(
            row["chi_square_statistic"],
            row["sample_size"],
            tables[demo],
        )

        values.append(v)

    chisq["cramers_v_effect_size"] = values

    print(chisq.to_string(index=False))

    return chisq


# ==========================================================
# 5.1.5 Multiple Comparison Correction
# ==========================================================

def step_515_adjust_demographic_association_pvalues(
    results: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.1.5 Adjust Demographic Association P-values (FDR) ===")

    results = adjust_pvalues(results)

    print(results.to_string(index=False))

    path = (
            PHASE5_TABLES_DIR
            / "segmentation"
            / "audience_cluster_demographic_association_statistics.csv"
    )

    results.to_csv(path, index=False)

    print(f"Saved → {path}")

    return results


# ==========================================================
# 5.1.6 Robustness Checks
# ==========================================================

def step_516_demographic_association_robustness_checks(
    tables: dict,
) -> pd.DataFrame:

    print("\n=== 5.1.6 Demographic Association Robustness Checks ===")

    rows = []

    for demo, table in tables.items():

        ok = check_min_expected(table)

        rows.append(
            {
                "demographic_variable": demo,
                "min_expected_cell_count_ok": ok,
            }
        )

    df = pd.DataFrame(rows)

    print(df.to_string(index=False))

    path = (
            PHASE5_TABLES_DIR
            / "segmentation"
            / "audience_cluster_demographic_association_assumption_checks.csv"
    )

    df.to_csv(path, index=False)

    print(f"Saved → {path}")

    return df


# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase5_1(
    df: pd.DataFrame,
) -> None:

    print("=== PHASE 5.1: AUDIENCE SEGMENTATION STRENGTH ===")

    _ensure_dirs()

    df = step_511_load_respondent_audience_clusters(df)

    tables = step_512_audience_cluster_demographic_contingency_tables(df)

    chisq = step_513_audience_cluster_demographic_chisquare_tests(tables)

    chisq = step_514_audience_cluster_demographic_effect_sizes(chisq, tables)

    chisq = step_515_adjust_demographic_association_pvalues(chisq)

    step_516_demographic_association_robustness_checks(tables)