# DIVAS (Idea): Shared-by-All vs Shared-by-Some vs Unique Structure

Many integration methods implicitly assume:

> If there is a real biological signal, it should show up in every omics block.

In practice, that is often false.

Examples you’ll recognize in real studies:
- Microbiome and metabolomics share a strong metabolic axis
- Transcriptomics reflects something different (or much weaker)
- Some variation is block-specific technical noise

**DIVAS** (Data Integration via Analysis of Subspaces) is built around a simple but important principle:

> Don’t force everything into one shared latent signal. First ask *who shares what*.

## Intuition: decompose variation by “who shares it”

Given multiple blocks, DIVAS asks:

- Which patterns are present in **all blocks**?
- Which patterns are shared by **some blocks but not all**?
- Which patterns are **unique** to a single block?

That makes DIVAS especially useful for exploratory, hypothesis-generating analyses.

## What you get out (how to use it)

DIVAS identifies **directions / subspaces** of variation that are characterized by which blocks they involve.

A practical workflow is:

1) Project samples onto each discovered direction
2) Look at which patients score high/low
3) Inspect which features contribute (when available)
4) Interpret “shared-by-some” patterns as hypotheses (e.g., microbe–metabolite modules)

## What DIVAS is *not*

- It is **not supervised** (not designed for classification)
- It is **not** a single “best embedding” method by default
- It does **not** guarantee mechanism; “shared” can still be shared batch/confounding

A good way to phrase what DIVAS answers is:

> How is variation distributed across omics layers: shared across all, shared across some, or unique?

## When DIVAS is a good choice

Use DIVAS when:
- you want structure discovery without labels
- you suspect partial sharing across blocks
- you want to avoid forcing a single shared latent signal

Avoid (or be cautious) when:
- your primary goal is prediction
- you need a single compact representation for clustering
- you mainly want outcome-tied feature selection

## Related method families

Even if you never run DIVAS, the “shared vs unique” idea shows up across the ecosystem:

- **MOFA**: factor analysis that can learn shared and view-specific factors
- **JIVE**: explicit decomposition into joint + individual + residual

## Code

This repo focuses on the concept and how to interpret it.
See also `docs/05_other_methods_mofa_jive_snf_icluster.md`.
