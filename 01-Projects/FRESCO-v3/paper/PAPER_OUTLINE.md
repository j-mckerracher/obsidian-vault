# Paper Outline: Building FRESCO v3 for Cross-Cluster Insights

**Last Updated**: 2026-02-03

## Title (Working)
FRESCO v3: A Provenance-Rich, Reproducible Pipeline for Defensible Cross-Cluster Workload Comparisons

## Abstract
- Motivation: cross-cluster insights are difficult due to measurement + workload shift
- Contribution: unified schema + normalization + provenance + regime matching
- Results: within-cluster prediction works; cross-cluster transfer requires matching/adaptation

## 1. Introduction
- Why cross-cluster comparisons matter
- Why naive transfer fails (covariate + conditional shift)
- Contributions and guarantees

## 2. Background & Dataset
- FRESCO overview
- Clusters (Conte, Stampede, Anvil)
- Prior limitations in v1/v2

## 3. Methods: Pipeline
- Extraction sources
- Transformations
- Schema union + dtype stability
- Memory normalization and semantics metadata

## 4. Methods: Comparability Framework
- Workload taxonomy
- Overlap-aware cohort selection
- Reporting requirements (coverage, KS, domain AUC)

## 5. Validation
- Schema validation
- Sanity checks
- Missingness and drift

## 6. Experiments
- Within-cluster predictive sanity (EXP-015-like)
- Transfer failure characterization
- Regime-matched transfer (v3)

## 7. Results
- What is comparable
- Where comparisons fail and why

## 8. Threats to Validity
- Measurement non-equivalence
- Temporal drift
- Hidden confounding

## 9. Reproducibility & Artifact Evaluation
- How to rerun pipeline
- Manifests and environment locks

## 10. Conclusion
- Practical guidance + future work
