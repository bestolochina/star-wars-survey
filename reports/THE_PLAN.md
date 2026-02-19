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

# PHASE 3 — STATISTICAL VALIDATION

3.1 Chi-square tests  
3.2 Effect size (Cramér’s V)  
3.3 Multiple comparison caution  
3.4 Robustness checks  

---

# PHASE 4 — SYNTHESIS

4.1 Key demographic drivers  
4.2 Strongest segmentation signals  
4.3 Surprising findings  
4.4 What does NOT matter  
4.5 Business-style summary  

---

# PROFESSIONAL REPORTING LAYER (MANDATORY)

A) Minimal reproducible reporting  
B) Full professional reporting (TARGET)

We are implementing B:

- Automatic figure naming
- Automatic table numbering
- CSV for every table
- Registry of artifacts
- Reproducible build log
- Clean markdown structure
- Cross-referenced sections

No manual figure naming.
No ad-hoc tables.
Everything traceable.
