# analysis/visualization/structural_identity_map.py

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_structural_identity_map(
    identity_df: pd.DataFrame,
    output_path,
) -> None:
    """
    Step 4.2.16 — Structural Identity Map

    Scatter plot positioning audience clusters
    in structural identity space.
    """

    fig, ax = plt.subplots(figsize=(8, 6))

    # group by identity type for coloring
    for identity_type, group in identity_df.groupby(
        "structural_identity_type"
    ):
        ax.scatter(
            group["narrative_selectivity"],
            group["block_extremeness"],
            label=identity_type,
            s=120,
        )

        # annotate clusters
        for _, row in group.iterrows():
            ax.text(
                row["narrative_selectivity"] + 0.005,
                row["block_extremeness"] + 0.005,
                f"C{int(row.cluster)}",
                fontsize=10,
            )

    # reference lines (interpretation quadrants)
    ax.axhline(
        identity_df["block_extremeness"].mean(),
        linestyle="--",
        linewidth=1,
    )

    ax.axvline(
        identity_df["narrative_selectivity"].mean(),
        linestyle="--",
        linewidth=1,
    )

    ax.set_xlabel("Narrative Selectivity")
    ax.set_ylabel("Structural Extremeness")
    ax.set_title("Structural Identity Map")

    ax.legend(title="Identity Type")
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved identity map → {output_path}")