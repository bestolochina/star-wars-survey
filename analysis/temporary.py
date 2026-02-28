import pandas as pd
from src.paths import PHASE3_TABLES_DIR

df = pd.read_csv(
    PHASE3_TABLES_DIR / "respondent_cluster_assignments.csv"
)

print(df.head())
print()
print(df["cluster"].value_counts())