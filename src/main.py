from pathlib import Path
import pandas as pd
import cleaning
from io_utils import load_raw_data, COLUMNS


def main() -> None:

    project_root = Path(__file__).resolve().parent.parent
    input_path = project_root / "data" / "raw" / "StarWars.csv"
    output_dir = project_root / "data" / "processed"
    output_path = output_dir / "star_wars_survey_clean.csv"

    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_raw_data(input_path)
    assert df.shape[1] == len(COLUMNS), "Column count mismatch"

    df = cleaning.clean_all(df)

    df.to_csv(output_path, index=False, encoding="utf-8")

    print("Cleaning complete.")
    print(df.shape)
    print(df.dtypes)


if __name__ == "__main__":
    main()