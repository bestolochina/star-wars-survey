# Star Wars Survey Analysis — Project Definition

## 1. Project goal

Analyze the FiveThirtyEight *Star Wars Survey* with a strong emphasis on **distribution-aware ranking analysis**, avoiding over-aggregation and misleading summaries.

Primary questions:

* How are Star Wars episodes ranked overall?
* How do **different demographic groups** rank episodes differently?
* Where do averages hide disagreement or polarization?

This project prioritizes **interpretability, statistical honesty, and visual clarity** over visual novelty.

---

## 2. Data assumptions

* Source: FiveThirtyEight Star Wars Survey (cleaned version via `load_clean_star_wars()`)
* Rankings are ordinal: **1 = best, 6 = worst**
* Missing rankings are dropped **per-episode**, never imputed
* No weighting of respondents unless explicitly introduced later

---

## 3. Analytical principles (non-negotiable)

### 3.1 Distribution first

* Means alone are insufficient for ordinal rankings
* Every summary must be visually or numerically tied to the **full rank distribution**

### 3.2 Avoid misleading smoothness

* Kernel density estimates (e.g. violins) must be justified
* Discrete ranks should be shown with **exact frequencies** whenever possible

### 3.3 Consistency checks

* Visuals must not contradict numeric summaries
* Sanity checks (e.g. percentage tables) are mandatory when introducing new plots

### 3.4 No demographic mixing (until instructed)

* Demographic slices are analyzed **one at a time**
* Never combine gender, age, income, etc. in a single plot or table at this stage

---

## 4. Project structure

### 4.1 Phase 1 — Data cleaning (completed)

* Clean rankings
* Standardize episode labels
* Drop missing ranks per episode

### 4.2 Phase 2 — Exploratory Data Analysis (current)

#### 2.1 Overall episode rankings

* Average score (for intuition only)
* Distribution-aware plots

#### 2.2 Distribution diagnostics

**Accepted plots:**

* Stacked histograms (per episode)
* Boxplots (with mean + median explicitly marked)

**Discouraged / optional:**

* Violin plots (only with explicit bandwidth control and explanation)

#### 2.3 Demographic slices (**very important**)

For **each demographic separately**:

* Gender
* Age group
* Income
* Education
* Region

Core question:

> *How does this group rank episodes differently?*

Rules:

* One demographic per analysis block
* Same plot types as overall analysis (for comparability)
* Explicit comparison to overall distribution

---

## 5. Visualization standards

### 5.1 Histograms (preferred)

* One subplot per episode
* Exact rank bins (1–6)
* Color-coded by rank (best → worst gradient)
* Annotated with:

  * Percentages
  * Mean
  * Median
  * IQR (shaded)

### 5.2 Boxplots

* Mean (triangle marker)
* Median (distinct line)
* No fliers unless explicitly justified
* Legend required

### 5.3 Stacked bars

* Used sparingly
* Must include percentage labels
* Only acceptable when exact frequency comparison is the goal

---

## 6. Reporting rules

* Each figure gets **1–2 analytical bullets**
* No descriptive filler (e.g. “This chart shows…”)
* Observations must be:

  * Data-driven
  * Precise (mention ranks, spread, concentration)
  * Consistent with numeric summaries

---

## 7. What "done" means (Phase 2)

Phase 2 is complete when:

* Overall ranking distributions are fully analyzed
* Each demographic slice has:

  * Comparable plots
  * Clear deviation or confirmation of overall trends
* No plot contradicts tabulated percentages or summary statistics

---

## 8. Explicit exclusions (for now)

* Predictive modeling
* Hypothesis testing / p-values
* Multivariate demographic interactions
* Recommendation systems

These may appear in later phases, but **not during Phase 2**.

---

## 9. Style & tone constraints

* Analytical, not promotional
* No unjustified praise or narrative dramatization
* Clarity > cleverness

---

*This document is the authoritative reference for the project. Any new analysis, plot, or report must conform to it unless explicitly revised.*
