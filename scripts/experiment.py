#!/usr/bin/env python3
"""Small common interface for the experiment operations registry."""
from pathlib import Path

from experiment_ops.core import main


if __name__ == "__main__":
    raise SystemExit(main(root=Path(__file__).resolve().parents[1]))
