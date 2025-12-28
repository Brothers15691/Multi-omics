# Other integration families (quick, intuitive map)

## MOFA
Unsupervised factor analysis across multiple omics.
Think: “PCA-like factors, but probabilistic and can be shared or view-specific.”

## JIVE
Decomposes each block into:
- **Joint** structure shared across blocks
- **Individual** structure unique to each block
- residual noise

## SNF (Similarity Network Fusion)
Build a patient similarity network per block, fuse them, then cluster patients.
Best when your goal is **patient subtyping**.

## iCluster / iClusterPlus
Learns a shared latent space and clusters patients in that space.

## Baselines
- PCA (within each block)
- CCA / PLS (between blocks)
- Concatenate + PCA / classifier (often surprisingly strong if preprocessing is solid)
