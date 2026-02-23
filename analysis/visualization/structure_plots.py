# analysis/visualization/structure_plots.py

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_correlation_heatmap(
    corr: pd.DataFrame,
    save_path,
) -> None:

    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.imshow(corr.values)

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))

    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticklabels(corr.columns)

    fig.colorbar(im, ax=ax)

    ax.set_title("Character Rating Correlation")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()