import os

import pandas as pd


def main() -> None:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(repo_root, "data", "toy_multiomics_4patients.csv")
    df = pd.read_csv(csv_path)

    print("Toy multi-omics dataset (wide table):")
    print(df.to_string(index=False))

    blocks = {
        "microbiome": ["BugA", "BugB", "BugC", "BugD"],
        "metabolomics": ["Met1", "Met2", "Met3"],
        "transcriptomics": ["Gene1", "Gene2", "Gene3"],
    }

    print("\nBlock shapes:")
    for name, cols in blocks.items():
        print(f"- {name}: {df[cols].shape} ({', '.join(cols)})")


if __name__ == "__main__":
    main()
