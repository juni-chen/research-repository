#!/usr/bin/env python3
"""Run the CGN verbal-cluster extraction and MaxEnt pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
DEFAULT_REAL_TOKENS = PROJECT_ROOT / "data" / "processed" / "cgn_tokens.csv"
DEFAULT_REAL_OUT = PROJECT_ROOT / "outputs" / "cgn-run"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cgn_clusters.evaluate import (
    language_head_type_word_order_summary,
    language_summary,
    write_json,
)
from cgn_clusters.experiment import (
    ExperimentConfig,
    run_separate_language_experiments,
)
from cgn_clusters.extract import ClusterExtractionConfig, extract_clusters
from cgn_clusters.io import write_csv
from cgn_clusters.streaming import extract_clusters_to_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tokens",
        default=str(DEFAULT_REAL_TOKENS),
        help="Normalized real CGN token table. Defaults to data/processed/cgn_tokens.csv.",
    )
    parser.add_argument(
        "--out",
        default=str(DEFAULT_REAL_OUT),
        help="Output directory. Defaults to outputs/cgn-run.",
    )
    parser.add_argument("--min-verbs", type=int, default=2)
    parser.add_argument(
        "--use-pandas-extraction",
        action="store_true",
        help="Use the older in-memory extractor. Streaming is the default.",
    )
    parser.add_argument("--iterations", type=int, default=1500)
    parser.add_argument("--learning-rate", type=float, default=0.15)
    parser.add_argument("--l2", type=float, default=0.01)
    parser.add_argument("--test-size", type=float, default=0.25)
    parser.add_argument(
        "--languages",
        nargs="+",
        default=["Dutch", "Flemish"],
        help="Languages to analyze separately.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    token_path = Path(args.tokens)
    if not token_path.exists():
        raise SystemExit(
            "Real CGN token table not found:\n"
            f"  {token_path}\n\n"
            "Create this file by converting your CGN export into the normalized "
            "one-token-per-row table described in the project README."
        )

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    cluster_path = out_dir / "all_clusters.csv"
    if args.use_pandas_extraction:
        from cgn_clusters.io import read_token_table

        tokens, schema_report = read_token_table(token_path)
        clusters = extract_clusters(
            tokens,
            ClusterExtractionConfig(min_verbs=args.min_verbs),
        )
        write_csv(clusters, cluster_path)
        write_json(schema_report.__dict__, out_dir / "schema_report.json")
    else:
        extraction_report = extract_clusters_to_csv(
            token_path,
            cluster_path,
            ClusterExtractionConfig(min_verbs=args.min_verbs),
        )
        write_json(extraction_report, out_dir / "schema_report.json")
        clusters = pd.read_csv(cluster_path)

    write_csv(language_summary(clusters), out_dir / "language_summary.csv")
    write_csv(
        language_head_type_word_order_summary(clusters),
        out_dir / "head_type_language_summary.csv",
    )

    config = ExperimentConfig(
        iterations=args.iterations,
        learning_rate=args.learning_rate,
        l2=args.l2,
        test_size=args.test_size,
    )
    experiment_summary = run_separate_language_experiments(
        clusters,
        out_dir,
        languages=tuple(args.languages),
        config=config,
    )
    write_csv(experiment_summary, out_dir / "experiment_summary.csv")
    print(f"Wrote separate language outputs to {out_dir}")


if __name__ == "__main__":
    main()
