"""Multi-omics VAE skeleton (educational).

This stays lightweight on purpose. It explains the architecture decisions
and the "conditional VAE" idea (feeding a group label as input).

To make it runnable you would:
- install torch in a dedicated env
- implement Dataset + training loop
"""

from __future__ import annotations

import sys


def main() -> None:
    try:
        import torch  # noqa: F401
    except Exception:
        print("This is a skeleton. Install PyTorch (torch) to run training.")
        print("Example: pip install torch")
        sys.exit(0)

    print("PyTorch detected. Next: implement model + training loop.")


if __name__ == "__main__":
    main()
