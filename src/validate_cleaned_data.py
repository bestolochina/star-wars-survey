from __future__ import annotations

import pandas as pd

from src.io_utils import load_raw_star_wars
from src.cleaning import clean_all
from src.config import (
    BOOLEAN_COLUMNS,
    EPISODE_RANK_COLUMNS,
    CHARACTER_RATING_COLUMNS,
)


# ==========================================================
# BASIC DATASET CHECKS
# ==========================================================

def check_row_count(raw: pd.DataFrame, clean: pd.DataFrame) -> None:
    """Ensure cleaning does not add or remove rows."""
    assert len(raw) == len(clean), "Row count changed during cleaning"


def check_index_integrity(df: pd.DataFrame) -> None:
    """Ensure index and columns are valid."""
    assert df.index.is_unique, "Index is not unique"
    assert not df.columns.duplicated().any(), "Duplicate columns detected"


# ==========================================================
# BOOLEAN COLUMN VALIDATION
# ==========================================================

def check_boolean_columns(df: pd.DataFrame) -> None:
    """Boolean columns must use pandas nullable boolean dtype."""
    for col in BOOLEAN_COLUMNS.keys():
        dtype = df[col].dtype.name
        print(f"{col}: {dtype}")
        assert dtype == "boolean", f"{col} is not boolean dtype"


# ==========================================================
# EPISODE RANK VALIDATION
# ==========================================================

def check_rank_columns(df: pd.DataFrame) -> None:
    """Episode ranks must be integers 1–6 (or NA)."""
    valid = {1, 2, 3, 4, 5, 6}

    for col in EPISODE_RANK_COLUMNS:
        values = set(df[col].dropna().unique())
        assert values.issubset(valid), f"{col} contains invalid rank values"


# ==========================================================
# CHARACTER RATING VALIDATION
# ==========================================================

def check_rating_columns(df: pd.DataFrame) -> None:
    """Character ratings must be integers 1–5 (or NA)."""
    valid = {1, 2, 3, 4, 5}

    for col in CHARACTER_RATING_COLUMNS:
        values = set(df[col].dropna().unique())
        assert values.issubset(valid), f"{col} contains invalid rating values"


# ==========================================================
# SPECIAL VARIABLE VALIDATION
# ==========================================================

def check_who_shot_first(df: pd.DataFrame) -> None:
    """Validate 'who_shot_first' responses."""
    values = set(df["who_shot_first"].dropna().unique())
    assert values.issubset({"Han", "Greedo"}), "Invalid values in who_shot_first"


# ==========================================================
# ORDERED CATEGORY VALIDATION
# ==========================================================

def check_category_order(
    df: pd.DataFrame,
    col: str,
    expected_categories: list[str],
) -> None:
    """Ensure categorical variables have correct ordering."""
    cat = df[col].cat

    print(f"\n{col}")
    print("categories:", list(cat.categories))
    print("ordered:", cat.ordered)
    print(df[col].value_counts(dropna=False))

    assert list(cat.categories) == expected_categories, f"{col} category mismatch"
    assert cat.ordered, f"{col} should be ordered"


# ==========================================================
# MAIN VALIDATION
# ==========================================================

if __name__ == "__main__":

    raw_df = load_raw_star_wars()
    clean_df = clean_all(raw_df.copy())

    print("\n=== VALIDATING CLEANED DATA ===")

    check_row_count(raw_df, clean_df)
    check_index_integrity(clean_df)

    check_boolean_columns(clean_df)
    check_rank_columns(clean_df)
    check_rating_columns(clean_df)

    check_who_shot_first(clean_df)

    check_category_order(
        clean_df,
        "age_group",
        ["18-29", "30-44", "45-60", "60+"],
    )

    check_category_order(
        clean_df,
        "household_income",
        ["$0–24k", "$25–49k", "$50–99k", "$100–149k", "$150k+"],
    )

    check_category_order(
        clean_df,
        "education_level",
        [
            "Less than HS",
            "High school",
            "Some college / Associate",
            "Bachelor’s",
            "Graduate",
        ],
    )

    print("\n✅ Cleaned-data validation passed\n")