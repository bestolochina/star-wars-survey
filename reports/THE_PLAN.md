# THE PLAN
Star Wars Survey — Authoritative Analytical Roadmap

This document is the governing checklist for the entire project.
All future work must align with it.

---

# PHASE 1 — DATA FOUNDATION

1.1 Raw data inspection  
1.2 Missingness analysis  
1.3 Cleaning strategy  
1.4 Demographic variable construction  
1.5 Validation of cleaned dataset  

Deliverable:
- Clean dataset
- Cleaning documentation

---

# PHASE 2 — EXPLORATORY DATA ANALYSIS

## 2.1 Core Distributions
- Fandom rates
- Movie viewing rates
- Trilogy preference
- Character favorability

## 2.2 Cross-Metrics
- Fandom vs viewing
- Viewing vs liking
- Trilogy comparison

## 2.3 Demographic Slices (VERY IMPORTANT)

For each demographic:

- Gender
- Age group
- Income
- Education
- Region

Answer:

1. Does fandom vary?
2. Does trilogy preference vary?
3. Are differences statistically significant?
4. Are effects practically meaningful?
5. What patterns are structurally consistent?

Each slice must include:
- Sample size
- Percent tables
- CSV export
- Plot
- Statistical test
- Interpretation

---

## 2.3.8+ Deep Crossed Slices (Advanced Layer)

- Gender × Age
- Gender × Education
- Age × Income
- Other high-signal interactions

Only after single-variable slices are complete.

---

Yes — and this is the correct structural move.

Right now THE PLAN jumps too quickly into inferential testing (Chi-square, Cramér’s V) without formally codifying the structural discovery stage you’ve completed.

Below is a clean updated version of **THE PLAN (Structural Section only)** with proper insertion and logical ordering.

---

# THE PLAN (Updated Structural & Segmentation Flow)

---

# Phase 1 — Data Preparation

*(unchanged)*

---

# Phase 2 — Descriptive Exploration

*(unchanged)*

---

# Phase 3 — Structural Analysis of Character Preferences

## 3.1 Correlation Structure

* Compute correlation matrix of character ratings
* Visualize via heatmap
* Detect bloc patterns
* Justify correlation-based distance

## 3.2 Hierarchical Clustering

* Use correlation distance: ( d = 1 - \rho )
* Apply Ward linkage
* Generate dendrogram
* Examine hierarchical splits

## 3.3 k Selection

* Identify natural structural breaks in dendrogram
* Justify selected k (structural, not arbitrary)
* Confirm compact within-cluster merges

## 3.4 Dimensional Structure (PCA)

* Standardize character ratings
* Compute PCA
* Scree plot (eigenvalues)
* Cumulative variance plot
* Interpret dominant components

## 3.5 Cluster Geometry Validation

* Project clusters into PCA space
* PC1 vs PC2
* PC1 vs PC3
* Confirm geometric separation

### Deliverable of Phase 3:

A defensible cluster solution grounded in structural evidence.

---

# Phase 4 — Cluster Profiling & Substantive Interpretation

## 4.1 Cluster Mean Profiles

* Compute average ratings per cluster
* Identify defining characters
* Detect polarity patterns

## 4.2 Character Archetype Labeling

* Interpret clusters substantively
* Avoid narrative overreach
* Base labels on rating patterns

---

# Phase 5 — Segmentation Strength & Demographic Association

*(This is where Chi-square belongs)*

## 5.1 Chi-square Tests

For each demographic variable:

* Gender
* Age group
* Income
* Education
* Region

Test: Cluster × Demographic independence

## 5.2 Effect Size (Cramér’s V)

* Compute Cramér’s V
* Interpret magnitude (not just p-values)

## 5.3 Multiple Comparison Control

* Adjust p-values (Bonferroni or FDR)
* Prevent false positives

## 5.4 Robustness Checks

* Minimum cell counts
* Sensitivity to rare categories
* Stability of results

---

# Phase 6 — Segmentation Strength Summary

* Rank demographics by segmentation power
* Compare effect sizes
* Identify strongest structural drivers

---

