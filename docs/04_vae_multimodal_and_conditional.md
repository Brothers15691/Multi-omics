# VAEs for Multi-Omics Integration (and Label Conditioning)

VAEs are a flexible way to learn **nonlinear latent representations** from high-dimensional data.
In multi-omics, they are often used to learn a shared latent embedding of samples from which each block can be reconstructed.

## Start with the simplest intuition: “compress → reconstruct”

An autoencoder has two parts:

- **Encoder**: compresses input features into a small latent vector
- **Decoder**: reconstructs the original features from that latent vector

If the latent space is small, the model is forced to keep only the most important structure.

## What makes it a VAE?

A VAE (Variational Autoencoder) makes the latent space **probabilistic** and **regularized**.

Practical takeaway:
- you usually get a smoother, better-behaved latent space than a plain autoencoder
- you can sample from the latent space (useful in some settings)

## Multi-omics VAE (multi-modal VAE)

A common multi-modal design is:

- one encoder per block
- one shared latent space `Z` per patient
- one decoder per block

In words:

> Each omics block gets compressed into a shared representation, and each block is reconstructed from that shared representation.

## Conditional VAEs (including group labels)

Sometimes people feed the group label (e.g., Group 0/1) into the model.

This is useful for tasks like:
- group-conditional reconstruction / denoising
- conditional generation
- learning group-specific structure

But there is a key interpretation trap:

> If you provide the label as input, “nice separation by group” is not necessarily a discovery — the model was told the group.

So:
- label-conditioning can be useful
- label-conditioned separation is **not evidence of biology** on its own

## Trade-offs vs DIABLO / DIVAS

VAEs are powerful when:
- relationships are nonlinear
- features are high-dimensional and noisy
- you want an embedding for visualization/clustering or reconstruction/imputation

VAEs are a poor fit when:
- sample size is very small
- you need transparent, feature-level signatures
- you want something easy to tune and explain

## Code

- Multi-omics demo (Python): `python/02_multimodal_vae_skeleton.py`
  - runs a linear shared-latent baseline by default
  - can train a multi-modal VAE if you install PyTorch and pass `--vae`
