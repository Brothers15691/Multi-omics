# DIABLO (Supervised Integration)

DIABLO is a supervised integration method implemented in the R package `mixOmics`.

## The intuition
DIABLO tries to learn:
- one component per block (one score per patient)
- that is **predictive of the group label**
- and **aligned across blocks** (block components are correlated)
- using only a subset of features (sparsity / feature selection)

## What comes out
You typically interpret:
- **Sample scores**: where each patient sits on the components
- **Selected features / loadings**: which bugs/metabolites/genes drive the component
- **Cross-block correlations**: do the block components move together?
- **Predictive performance**: via proper cross-validation

## Pitfalls
- DIABLO is **not causal**: it finds predictive + correlated features, not direction or mechanism.
- If batch effects line up with group labels, DIABLO can rediscover batch.
- Tuning on the full dataset and evaluating on the same dataset overestimates performance.

## Code
See `r/02_diablo_mixomics_example.R`.
