"""Reusable experiment runners for separate Dutch and Flemish analyses."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .evaluate import (
    head_type_word_order_summary,
    metrics_dict,
    word_order_summary,
    write_json,
)
from .io import write_csv
from .model import (
    DEFAULT_FEATURES,
    MaxEntClassifier,
    coefficients_frame,
    encode_examples,
    stable_train_test_split,
)


@dataclass(frozen=True)
class ExperimentConfig:
    iterations: int = 1500
    learning_rate: float = 0.15
    l2: float = 0.01
    test_size: float = 0.25
    feature_columns: tuple[str, ...] = tuple(DEFAULT_FEATURES)


def language_slug(language: str) -> str:
    return language.strip().lower().replace(" ", "-")


def run_language_experiment(
    clusters: pd.DataFrame,
    language: str,
    out_dir: str | Path,
    config: ExperimentConfig | None = None,
) -> dict[str, object]:
    """Run the same MaxEnt analysis for one language subset."""

    config = config or ExperimentConfig()
    target_dir = Path(out_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    language_clusters = clusters[clusters["language"] == language].copy()
    write_csv(language_clusters, target_dir / "clusters.csv")
    write_csv(word_order_summary(language_clusters), target_dir / "word_order_summary.csv")
    write_csv(
        head_type_word_order_summary(language_clusters),
        target_dir / "head_type_word_order_summary.csv",
    )

    known = language_clusters[language_clusters["word_order"] != "unknown"].copy()
    summary: dict[str, object] = {
        "language": language,
        "n_clusters": int(len(language_clusters)),
        "n_known_clusters": int(len(known)),
        "word_orders": sorted(known["word_order"].unique().tolist()),
        "features": list(config.feature_columns),
    }

    if known.empty:
        summary["warning"] = "No clusters with known word_order labels."
        write_json(summary, target_dir / "metrics.json")
        return summary

    if known["word_order"].nunique() < 2:
        summary["warning"] = "Need at least two word_order labels to train MaxEnt."
        write_json(summary, target_dir / "metrics.json")
        return summary

    encoded = encode_examples(
        known,
        feature_columns=config.feature_columns,
        include_interactions=False,
    )
    train_idx, test_idx = stable_train_test_split(
        encoded.y,
        test_size=config.test_size,
    )

    model = MaxEntClassifier(
        learning_rate=config.learning_rate,
        l2=config.l2,
        iterations=config.iterations,
    )
    model.fit(encoded.X[train_idx], encoded.y[train_idx])

    probabilities = model.predict_proba(encoded.X[test_idx])
    metrics = metrics_dict(
        encoded.y[test_idx],
        probabilities,
        encoded.label_names,
    )
    metrics.update(summary)
    metrics["train_examples"] = int(len(train_idx))
    metrics["test_examples"] = int(len(test_idx))
    metrics["final_training_loss"] = model.loss_history[-1]

    write_json(metrics, target_dir / "metrics.json")
    coefficients = coefficients_frame(
        model,
        encoded.feature_names,
        encoded.label_names,
    )
    write_csv(coefficients, target_dir / "coefficients.csv")
    return metrics


def run_separate_language_experiments(
    clusters: pd.DataFrame,
    out_dir: str | Path,
    languages: tuple[str, ...] = ("Dutch", "Flemish"),
    config: ExperimentConfig | None = None,
) -> pd.DataFrame:
    """Apply the same analysis function to Dutch and Flemish separately."""

    records = []
    for language in languages:
        metrics = run_language_experiment(
            clusters,
            language,
            Path(out_dir) / language_slug(language),
            config=config,
        )
        records.append(
            {
                "language": language,
                "n_clusters": metrics.get("n_clusters", 0),
                "n_known_clusters": metrics.get("n_known_clusters", 0),
                "word_orders": ";".join(metrics.get("word_orders", [])),
                "accuracy": metrics.get("accuracy", pd.NA),
                "log_loss": metrics.get("log_loss", pd.NA),
                "warning": metrics.get("warning", ""),
            }
        )
    return pd.DataFrame.from_records(records)
