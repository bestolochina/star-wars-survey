# analysis/visualization/segmentation_plots.py

import os
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict


# ==========================================================
# UTIL
# ==========================================================

def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


# ==========================================================
# 1️⃣ COMPARISON BAR CHART
# ==========================================================

def plot_segmentation_comparison(
    comparison_table: pd.DataFrame,
    *,
    save_dir: str,
) -> None:

    _ensure_dir(save_dir)

    fig, ax = plt.subplots(figsize=(8, 5))

    comparison_table["avg_range"].plot(
        kind="bar",
        ax=ax,
    )

    ax.set_title("Average Divergence by Demographic")
    ax.set_ylabel("Average Value Range")
    ax.set_xlabel("Demographic")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    filepath = os.path.join(save_dir, "segmentation_comparison.png")
    plt.savefig(filepath, dpi=300)
    plt.close()


# ==========================================================
# 2️⃣ VARIABLE DIVERGENCE HEATMAP
# ==========================================================

def plot_variable_divergence_heatmap(
    metrics_store: Dict[str, dict],
    *,
    save_dir: str,
) -> None:

    _ensure_dir(save_dir)

    series_list = []

    for demo, metrics in metrics_store.items():
        s = metrics["range_per_variable"].copy()
        s.name = demo
        series_list.append(s)

    heatmap_df = pd.concat(series_list, axis=1)
    heatmap_df = heatmap_df.astype(float)

    fig, ax = plt.subplots(figsize=(10, 6))

    im = ax.imshow(
        heatmap_df.to_numpy(dtype=float),
        aspect="auto",
    )

    ax.set_xticks(range(len(heatmap_df.columns)))
    ax.set_xticklabels(heatmap_df.columns, rotation=45, ha="right")

    ax.set_yticks(range(len(heatmap_df.index)))
    ax.set_yticklabels(heatmap_df.index)

    ax.set_title("Variable Divergence Heatmap (Range)")

    fig.colorbar(im, ax=ax)

    plt.tight_layout()

    filepath = os.path.join(save_dir, "variable_divergence_heatmap.png")
    plt.savefig(filepath, dpi=300)
    plt.close()


# ==========================================================
# 3️⃣ DRIVER VISUALIZATION
# ==========================================================

def plot_variable_drivers(
    drivers: Dict[str, pd.DataFrame],
    *,
    save_dir: str,
) -> None:

    _ensure_dir(save_dir)

    for demo, df in drivers.items():

        if df.empty:
            continue

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.barh(
            df["variable"],
            df["value_gap"],
        )

        ax.set_title(f"Top Drivers – {demo}")
        ax.set_xlabel("Value Gap (Worst - Best)")
        ax.set_ylabel("Variable")

        plt.tight_layout()

        filename = f"drivers_{demo}.png"
        filepath = os.path.join(save_dir, filename)

        plt.savefig(filepath, dpi=300)
        plt.close()
