"""Baseline integration: CCA between microbiome and metabolomics (no sklearn).

CCA (Canonical Correlation Analysis) finds linear projections of two blocks that are maximally correlated.

This is a classic integration baseline: it finds *shared linear structure* across two omics layers.

Run:
  python python/04_baseline_cca_microbe_met.py

Notes:
- This demonstrates association, not direction/causality.
- With only 4 patients, CCA is unstable; this script can simulate more samples for a clearer demo.
"""

from __future__ import annotations

import argparse
import os

import numpy as np
import pandas as pd

MICROBE_COLS = ["BugA", "BugB", "BugC", "BugD"]
MET_COLS = ["Met1", "Met2", "Met3"]


def repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_toy_df() -> pd.DataFrame:
    path = os.path.join(repo_root(), "data", "toy_multiomics_4patients.csv")
    return pd.read_csv(path)


def alr_log_ratios(df: pd.DataFrame, denom: str = "BugD", pseudocount: float = 1e-6) -> np.ndarray:
    denom_v = df[denom].to_numpy(dtype=float) + pseudocount
    ratios = []
    for col in ["BugA", "BugB", "BugC"]:
        num = df[col].to_numpy(dtype=float) + pseudocount
        ratios.append(np.log(num / denom_v))
    return np.column_stack(ratios)


def invert_alr_to_composition(r: np.ndarray) -> np.ndarray:
    exp_r = np.exp(r)
    denom = 1.0 / (1.0 + exp_r.sum(axis=1, keepdims=True))
    bugs_abc = exp_r * denom
    bug_d = denom
    return np.column_stack([bugs_abc, bug_d])


def simulate_from_toy(df_toy: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    base = df_toy.sample(n=n, replace=True, random_state=seed).reset_index(drop=True)

    r = alr_log_ratios(base)
    r = r + rng.normal(0.0, 0.15, size=r.shape)
    bugs = invert_alr_to_composition(r)

    met_log = np.log1p(base[MET_COLS].to_numpy(dtype=float))
    met_log = met_log + rng.normal(0.0, 0.10, size=met_log.shape)
    met = np.expm1(met_log)
    met = np.clip(met, 0.0, None)

    out = pd.DataFrame(
        {
            "Patient": [f"S{i+1}" for i in range(n)],
            "Group": base["Group"].to_numpy(dtype=int),
            "BugA": bugs[:, 0],
            "BugB": bugs[:, 1],
            "BugC": bugs[:, 2],
            "BugD": bugs[:, 3],
            "Met1": met[:, 0],
            "Met2": met[:, 1],
            "Met3": met[:, 2],
        }
    )
    return out


def zscore(X: np.ndarray) -> np.ndarray:
    mean = X.mean(axis=0, keepdims=True)
    std = X.std(axis=0, ddof=0, keepdims=True)
    std = np.where(std == 0, 1.0, std)
    return (X - mean) / std


def inv_sqrtm_spd(A: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    """Inverse sqrt of a symmetric PSD matrix using eigen-decomposition."""
    A = 0.5 * (A + A.T)
    w, V = np.linalg.eigh(A)
    w = np.clip(w, eps, None)
    return V @ np.diag(1.0 / np.sqrt(w)) @ V.T


def cca(X: np.ndarray, Y: np.ndarray, reg: float = 1e-3) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """CCA via whitening + SVD.

    Returns (A, B, corr):
      - A: weights for X
      - B: weights for Y
      - corr: canonical correlations (descending)
    """
    n = X.shape[0]
    Xc = X - X.mean(axis=0, keepdims=True)
    Yc = Y - Y.mean(axis=0, keepdims=True)

    Sxx = (Xc.T @ Xc) / (n - 1) + reg * np.eye(X.shape[1])
    Syy = (Yc.T @ Yc) / (n - 1) + reg * np.eye(Y.shape[1])
    Sxy = (Xc.T @ Yc) / (n - 1)

    Wx = inv_sqrtm_spd(Sxx)
    Wy = inv_sqrtm_spd(Syy)

    M = Wx @ Sxy @ Wy
    U, s, Vt = np.linalg.svd(M, full_matrices=False)

    A = Wx @ U
    B = Wy @ Vt.T
    return A, B, s


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--simulate-n", type=int, default=300, help="Train/demo sample size.")
    p.add_argument("--seed", type=int, default=0)
    return p.parse_args()


def main() -> None:
    args = parse_args()

    df_toy = load_toy_df()
    df = simulate_from_toy(df_toy, n=args.simulate_n, seed=args.seed)

    X = zscore(alr_log_ratios(df))
    Y = zscore(np.log1p(df[MET_COLS].to_numpy(dtype=float)))

    A, B, corr = cca(X, Y, reg=1e-3)

    print("CCA between microbiome (ALR log-ratios) and metabolomics (log1p):")
    print(f"- simulated samples: {len(df)}")
    print("- canonical correlations:")
    print("  " + ", ".join(f"{c:.3f}" for c in corr))
    print()

    # Show where the 4 toy patients land on the first canonical variate.
    X_toy = zscore(alr_log_ratios(df_toy))
    Y_toy = zscore(np.log1p(df_toy[MET_COLS].to_numpy(dtype=float)))

    u1 = (X_toy - X_toy.mean(axis=0, keepdims=True)) @ A[:, 0]
    v1 = (Y_toy - Y_toy.mean(axis=0, keepdims=True)) @ B[:, 0]

    out = pd.DataFrame(
        {
            "Patient": df_toy["Patient"],
            "Group": df_toy["Group"],
            "CCA1_micro": u1,
            "CCA1_met": v1,
        }
    )
    print("Toy patients on the first canonical variate (CCA1):")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
