# Core Concepts for Multi-Omics Integration (blocks, latent spaces, leakage)

This doc defines the minimum vocabulary you need to read DIABLO / MOFA / JIVE / VAEs without getting lost.

## Block / view / modality
A **block** (also called a *view* or *modality*) is one omics layer measured on the **same samples**.

Integration assumes aligned samples: “Patient P3” must mean the same person in every block.

## Latent component / latent factor / embedding
A **latent** thing is “hidden”:
- you don’t measure it directly
- the method learns it as a compressed summary

Practical definition:
> A latent component is **one number per patient** summarizing a multi-feature pattern.

## Supervised vs unsupervised
- **Supervised**: you have a target label/outcome and you want components that help predict it.
- **Unsupervised**: no labels; you want to discover structure.

## Bias (plain language)
**Bias** = a systematically wrong conclusion that doesn’t go away with more data.

Common sources in integration:
- **Batch effects** (technical differences masquerading as biology)
- **Confounding** (a third thing drives multiple blocks)
- **Leakage** (label/test info sneaks into training and inflates performance)

## Leakage (the most common “oops”)
Leakage examples:
- You pick features using all samples, then cross-validate on those same samples.
- You scale/normalize using all samples, then cross-validate.

Rule:
> Any preprocessing step that “looks at the data” should happen **inside** the cross-validation loop.
