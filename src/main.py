from pathlib import Path
import pandas as pd
import cleaning

COLUMNS = [
    "respondent_id",
    "seen_star_wars",
    "fan_star_wars",
    "seen_ep1_phantom_menace",
    "seen_ep2_attack_clones",
    "seen_ep3_revenge_sith",
    "seen_ep4_new_hope",
    "seen_ep5_empire_strikes_back",
    "seen_ep6_return_jedi",
    "rank_ep1",
    "rank_ep2",
    "rank_ep3",
    "rank_ep4",
    "rank_ep5",
    "rank_ep6",
    "rating_han_solo",
    "rating_luke_skywalker",
    "rating_princess_leia_organa",
    "rating_anakin_skywalker",
    "rating_obi_wan_kenobi",
    "rating_emperor_palpatine",
    "rating_darth_vader",
    "rating_lando_calrissian",
    "rating_boba_fett",
    "rating_c-3p0",
    "rating_r2_d2",
    "rating_jar_jar_binks",
    "rating_padme_amidala",
    "rating_yoda",
    "who_shot_first",
    "familiar_expanded_universe",
    "fan_expanded_universe",
    "fan_star_trek",
    "gender",
    "age_group",
    "household_income",
    "education_level",
    "census_region",
]


def load_data(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(
            path,
            encoding="utf-8",
            skiprows=2,
            header=None,
            names=COLUMNS,
        )
    except UnicodeDecodeError:
        return pd.read_csv(
            path,
            encoding="ISO-8859-1",
            skiprows=2,
            header=None,
            names=COLUMNS,
        )


def main() -> None:
    # pd.set_option("display.max_columns", None)
    # pd.set_option("display.width", None)

    project_root = Path(__file__).resolve().parent.parent
    input_path = project_root / "data" / "raw" / "StarWars.csv"
    output_dir = project_root / "data" / "processed"
    output_path = output_dir / "star_wars_survey_clean.csv"

    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(input_path)
    assert df.shape[1] == len(COLUMNS), "Column count mismatch"

    df = cleaning.clean_all(df)

    df.to_csv(output_path, index=False, encoding="utf-8")

    print("Cleaning complete.")
    print(df.shape)
    print(df.dtypes)

    columns = ['seen_star_wars',]
    for col in columns:
        print(col)
        print(df[col].isna().sum())
        print(df[col].unique())


if __name__ == "__main__":
    main()