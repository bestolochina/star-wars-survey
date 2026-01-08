from src.io_utils import load_clean_star_wars
import matplotlib.pyplot as plt
import pandas as pd

# For each boolean column, we want to answer:
# How many True / False / NA?
# Are the proportions reasonable?
# Do any columns look suspicious or contradictory?
# Are there implicit filters (e.g. fan without having seen)?

BOOLEAN_COLUMNS = [
    "seen_star_wars",
    "fan_star_wars",
    "seen_ep1_phantom_menace",
    "seen_ep2_attack_clones",
    "seen_ep3_revenge_sith",
    "seen_ep4_new_hope",
    "seen_ep5_empire_strikes_back",
    "seen_ep6_return_jedi",
    "familiar_expanded_universe",
    "fan_expanded_universe",
    "fan_star_trek",
]

def summarize_boolean_column(df: pd.DataFrame, col: str) -> pd.Series:
    total: int = len(df)

    counts = df[col].value_counts(dropna=False)
    true_count = counts.get(True, 0)
    false_count = counts.get(False, 0)
    na_count = counts.get(pd.NA, 0)

    return pd.Series(
        {
            "true": true_count,
            "false": false_count,
            "na": na_count,
            "true_pct": true_count / total,
            "false_pct": false_count / total,
            "na_pct": na_count / total,
        }
    )

def summarize_boolean_columns(
    df: pd.DataFrame, columns: list[str]
) -> pd.DataFrame:
    summary = {
        col: summarize_boolean_column(df, col)
        for col in columns
    }
    return pd.DataFrame(summary).T

def main():
    pd.set_option('display.max_columns', None)  # to print all columns
    pd.set_option('display.width', None)  # avoid line wrapping

    df = load_clean_star_wars()
    summary = summarize_boolean_columns(df, BOOLEAN_COLUMNS)
    print(summary)

    for cat in BOOLEAN_COLUMNS:
        df1 = df[df[cat] == True]
        df2 = df[df[cat] != True]
        summary1 = summarize_boolean_columns(df1, BOOLEAN_COLUMNS)
        summary2 = summarize_boolean_columns(df2, BOOLEAN_COLUMNS)
        print(cat, '== True')
        print(summary1)
        print(cat, '!= True')
        print(summary2)
        print()



if __name__ == "__main__":
    main()
