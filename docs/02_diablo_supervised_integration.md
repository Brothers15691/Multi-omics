# DIABLO (Supervised Multi-Omics Integration)

DIABLO is a supervised integration method from `mixOmics` (R) that is designed for a very common multi-omics situation:

- You have **multiple blocks** measured on the same samples (microbiome, metabolomics, transcriptomics, …)
- You also have a **label/outcome** you care about (case/control, responder/non-responder)

DIABLO’s core question is:

> Which *cross-omics* feature patterns best separate the groups, while still agreeing across blocks?

## Intuition: “matching patterns across omics that separate groups”

DIABLO does not analyze each omics layer in isolation. Instead, it tries to learn:

- **One component per block** (a weighted sum of features)
- such that **samples separate by group** along those components
- and the block components are **aligned** (correlated across blocks)
- while using only a **small subset of features** per block (sparsity)

A mental picture:

- Microbiome component: “Bug A high, Bug B low”
- Metabolite component: “Met1 high, Met3 low”
- Transcript component: “Gene2 high”

…and DIABLO tries to make those *move together* across patients, while also separating Group 0 vs Group 1.

## What DIABLO produces (what you interpret)

Most DIABLO workflows focus on four outputs:

1) **Sample scores** (per component, per block): where each patient sits
2) **Selected features / loadings**: which features define the signatures in each block
3) **Cross-block correlations**: whether the learned components actually align
4) **Predictive performance**: cross-validated accuracy/AUC (if you’re using it as a classifier)

## Why feature selection matters

Without sparsity, components can be “dense” (many small weights) and hard to interpret biologically.

With sparsity, you get:
- a short, interpretable **multi-omics signature**
- a manageable list of candidates for follow-up

## What DIABLO is *not*

DIABLO is useful, but it doesn’t answer causal questions.

- It does **not** tell you what is upstream vs downstream
- It does **not** distinguish mediator vs confounder
- It can find strong predictive signatures that are actually **batch/confounding**

A good way to phrase what DIABLO *does* answer is:

> What combination of features across omics best predicts group membership and is mutually consistent across blocks?

## When DIABLO is a good choice

Use DIABLO when:
- you have a clear label/outcome
- you want a cross-omics signature (not separate per-omics hit lists)
- interpretability matters
- prediction and biological insight are both goals

Avoid (or be cautious) when:
- your primary goal is unsupervised discovery
- you want directionality/causal mechanism
- you suspect most structure is **not shared** across all blocks

## Practical pitfalls (common ways to fool yourself)

- **Leakage**: tuning or selecting features on the full dataset, then reporting performance on the same data.
  - If you tune, use **nested cross-validation**.
- **Batch effects aligned with group**: DIABLO can rediscover batch as a “signature”.
- **Scaling/preprocessing**: choices like log transforms and standardization strongly affect results.

## Code

- Mechanics demo (R): `r/02_diablo_mixomics_example.R` (requires `mixOmics`)
