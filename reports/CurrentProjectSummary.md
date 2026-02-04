# 📊 Star Wars Survey EDA — Project Context Summary

## Project goal

Exploratory Data Analysis of the **Star Wars Survey dataset**, following a strict, phased analytical plan (**“THE PLAN”**) to avoid premature conclusions and plot-driven bias.

---

## Structure & tooling

* **Language**: Python 3.12
* **Environment**: PyCharm (no Jupyter)
* **Libraries**: pandas, numpy, matplotlib (no seaborn unless explicitly justified)
* **Project layout**:

  ```
  analysis/
    eda_episode_rankings.py
  reports/
    phase_1_eda.md
    phase_2_eda.md
  src/
    io_utils.py
    cleaning.py
    paths.py
  ```
* All figures saved to `FIGURES_DIR`
* Code is run via scripts (e.g. `run_cleaning.py`, EDA scripts), not notebooks

---

## Dataset specifics

* Episode rankings:

  * Columns: `rank_ep1` … `rank_ep6`
  * Values: integers 1–6 (1 = best, 6 = worst)
* Rankings are **ordinal**, not continuous
* Missing rankings are dropped *only* at the analysis stage (not during cleaning)

---

## EDA phases (current status)

### ✅ Phase 1 — Data cleaning & structure

Completed and documented.

### ✅ Phase 2.1 — Binary × Binary & Binary × Nominal

* Focused on fandom variables (`fan_star_wars`, `fan_star_trek`)
* Used crosstabs, row percentages, bar plots
* Saved results to `phase_2_eda.md`

### ✅ Phase 2.2 — Overall Episode Rankings

Implemented and validated:

* Average score bars (score = 7 − rank)
* **Stacked histograms** per episode (preferred)

  * Exact frequency distributions (no KDE guessing)
  * Rank-colored bars (green → red)
  * Percentage labels above bars (non-transparent background)
  * Mean, Median, IQR overlays
* Boxplots and violins were explored but are now secondary
* Sanity checks via normalized crosstabs
* Episode V correctly shows mean ≈ 2.5 (expected & validated)

### ❌ Phase 2.3 — Demographic slices (IN PROGRESS)

**Not finished yet — currently starting here**

Planned question:

> “How does this group rank episodes differently?”

Rules:

* Analyze **one demographic at a time**
* Do **not** mix demographics
* Reuse the **same visual language** for comparability

Demographics to analyze (in order):

1. Gender
2. Age group
3. Education
4. Income
5. Region

Primary visualization for Phase 2.3:

* Faceted / repeated **stacked histograms by episode**, split by demographic group
* Same bins, colors, scales across groups
* Mean / Median / IQR overlays
* Numeric sanity tables for validation

---

## Reporting style

* Reports live in `reports/phase_2_eda.md`
* Each figure gets **1–2 short analytical bullets**
* No speculation, no fluff, no praise
* Observations must match numeric summaries

---

## Design principles agreed upon

* Prefer **exact distributions** over smoothed estimates
* Trust visuals only after numeric sanity checks
* Avoid “plot variety for its own sake”
* Consistency > novelty
* If a plot doesn’t add insight, drop it

---

## Current next step

👉 **Start Phase 2.3.1: Gender × Episode rankings**

---

