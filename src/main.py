from pathlib import Path
import pandas as pd
import cleaning

def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="ISO-8859-1", skiprows=[0, 1],
                       names=["respondent_id", "seen_star_wars", "fan_star_wars", "seen_ep1_phantom_menace",
                              "seen_ep2_attack_clones", "seen_ep3_revenge_sith", "seen_ep4_new_hope",
                              "seen_ep5_empire_strikes_back", "seen_ep6_return_jedi", "rank_ep1", "rank_ep2",
                              "rank_ep3", "rank_ep4", "rank_ep5", "rank_ep6", 'rating_han_solo',
                              'rating_luke_skywalker', 'rating_princess_leia_organa', 'rating_anakin_skywalker',
                              'rating_obi_wan_kenobi', 'rating_emperor_palpatine', 'rating_darth_vader',
                              'rating_lando_calrissian', 'rating_boba_fett', 'rating_c-3p0', 'rating_r2_d2',
                              'rating_jar_jar_binks', 'rating_padme_amidala', 'rating_yoda', "who_shot_first",
                              "familiar_expanded_universe", "fan_expanded_universe", "fan_star_trek", "gender",
                              "age_group", "household_income", "education_level", "census_region"])


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "raw" / "StarWars.csv"

    df = load_data(data_path)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)

    # print(df.head())
    # print(df.info())
    # print(df.isna().sum())

    cleaning.clean_seen_fun_columns(df)
    cleaning.clean_seen_ep_columns(df)
    cleaning.clean_rank_ep_columns(df)
    cleaning.clean_rank_character_columns(df)
    cleaning.clean_who_shot_first(df)

    columns = ["who_shot_first",]
    for col in columns:
        print(col)
        print(df[col].isna().sum())
        print(df[col].unique())


if __name__ == "__main__":
    main()