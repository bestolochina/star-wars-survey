# analysis/visualization/anova_plots.py

import matplotlib.pyplot as plt
import pandas as pd


def plot_eta_squared_summary(
    anova_df: pd.DataFrame,
    save_path,
) -> None:

    fig, ax = plt.subplots(figsize=(7, 5))

    axes = ["age_group", "gender", "census_region"]

    data = [
        anova_df.loc[anova_df["axis"] == a, "eta_sq"]
        for a in axes
    ]

    ax.boxplot(data, labels=["Age", "Gender", "Region"])

    # jittered points
    for i, vals in enumerate(data, start=1):
        ax.scatter(
            [i] * len(vals),
            vals,
            alpha=0.6,
        )

    ax.set_ylabel("η² (Effect Size)")
    ax.set_title("Segmentation Strength by Demographic Axis")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()