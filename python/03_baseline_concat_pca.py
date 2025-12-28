"""Baseline integration: z-score within block -> concatenate -> PCA (no sklearn).

This is the simplest "early integration" baseline.

Run:
  python python/03_baseline_concat_pca.py
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd


def load_df() -> pd.DataFrame:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(repo_root, "data", "toy_multiomics_4patients.csv")
    return pd.read_csv(csv_path)


def zscore(X: np.ndarray) -> np.ndarray:
    mean = X.mean(axis=0, keepdims=True)
    std = X.std(axis=0, ddof=0, keepdims=True)
    std = np.where(std == 0, 1.0, std)
    return (X - mean) / std


def pca_scores(X: np.ndarray, n_components: int = 2) -> tuple[np.ndarray, np.ndarray]:
    Xc = X - X.mean(axis=0, keepdims=True)
    U, s, _Vt = np.linalg.svd(Xc, full_matrices=False)
    scores = U[:, :n_components] * s[:n_components]
    return scores, s


def main() -> None:
    df = load_df()

    blocks = {
        "microbiome": ["BugA", "BugB", "BugC", "BugD"],
        "metabolomics": ["Met1", "Met2", "Met3"],
        "transcriptomics": ["Gene1", "Gene2", "Gene3"],
    }

    X_parts: list[np.ndarray] = []
    for cols in blocks.values():
        X_parts.append(zscore(df[cols].to_numpy(dtype=float)))

    X = np.concatenate(X_parts, axis=1)
    scores, s = pca_scores(X, n_components=2)

    out = pd.DataFrame({"Patient": df["Patient"], "Group": df["Group"], "PC1": scores[:, 0], "PC2": scores[:, 1]})
    print("Concatenate + PCA (after z-scoring within each block):")
    print(out.to_string(index=False))
    print("\nSingular values:")
    print(np.round(s, 4))


if __name__ == "__main__":
    main()
