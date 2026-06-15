"""Input/output helpers for CGN verbal-cluster experiments."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .schema import SchemaReport, prepare_token_table


def read_token_table(path: str | Path) -> tuple[pd.DataFrame, SchemaReport]:
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(source)

    if source.suffix.lower() in {".tsv", ".tab"}:
        raw = pd.read_csv(source, sep="\t")
    else:
        raw = pd.read_csv(source)
    return prepare_token_table(raw)


def write_csv(df: pd.DataFrame, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target, index=False)
