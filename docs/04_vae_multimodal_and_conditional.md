# VAEs for multi-omics integration (and label conditioning)

## Autoencoder (start here)
An autoencoder has:
- **Encoder**: compresses features into a latent vector
- **Decoder**: reconstructs the input from the latent vector

A small latent space forces compression.

## What makes it a VAE?
A VAE makes the latent space probabilistic and regularized (often smoother embeddings).

## Multi-omics VAE (multi-modal VAE)
Common pattern:
- one encoder per block
- one shared latent `Z` per patient
- one decoder per block

## Conditional VAE: “include group as categorical input”
If you feed the group label into the model, you are providing label information.

This can be useful (conditional reconstruction, denoising, imputation), but it also means:
- separation by group may be *because you told the model the group*

Rule:
> Don’t interpret label-conditioned separation as a discovery.

## Code
See `python/02_multimodal_vae_skeleton.py`.
