from src.cleaning import clean_all
from src.io_utils import load_raw_star_wars, save_clean_star_wars


def main() -> None:
    df = load_raw_star_wars()
    df = clean_all(df)
    save_clean_star_wars(df)

    print("Cleaning complete.")
    print(df.shape)
    print(df.dtypes)


if __name__ == "__main__":
    main()
