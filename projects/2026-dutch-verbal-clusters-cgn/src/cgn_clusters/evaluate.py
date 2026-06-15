"""Evaluation helpers for CGN verbal-cluster experiments."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .model import accuracy, log_loss


def word_order_summary(clusters: pd.DataFrame) -> pd.DataFrame:
    known = clusters[clusters["word_order"] != "unknown"].copy()
    if known.empty:
        return pd.DataFrame(columns=["word_order", "count", "proportion"])
    counts = (
        known.groupby("word_order")
        .size()
        .reset_index(name="count")
        .sort_values("word_order")
    )
    counts["proportion"] = counts["count"] / counts["count"].sum()
    return counts


def language_summary(clusters: pd.DataFrame) -> pd.DataFrame:
    known = clusters[clusters["word_order"] != "unknown"].copy()
    if known.empty:
        return pd.DataFrame(columns=["language", "word_order", "count", "proportion"])
    counts = (
        known.groupby(["language", "word_order"])
        .size()
        .reset_index(name="count")
        .sort_values(["language", "word_order"])
    )
    totals = counts.groupby("language")["count"].transform("sum")
    counts["proportion"] = counts["count"] / totals
    return counts


def head_type_word_order_summary(clusters: pd.DataFrame) -> pd.DataFrame:
    columns = ["head_type", "word_order", "count", "proportion"]
    if "head_type" not in clusters.columns:
        return pd.DataFrame(columns=columns)

    known = clusters[
        (clusters["word_order"] != "unknown")
        & (clusters["head_type"].isin(["modal", "auxiliary"]))
    ].copy()
    if known.empty:
        return pd.DataFrame(columns=columns)

    counts = (
        known.groupby(["head_type", "word_order"])
        .size()
        .reset_index(name="count")
        .sort_values(["head_type", "word_order"])
    )
    totals = counts.groupby("head_type")["count"].transform("sum")
    counts["proportion"] = counts["count"] / totals
    return counts


def language_head_type_word_order_summary(clusters: pd.DataFrame) -> pd.DataFrame:
    columns = ["language", "head_type", "word_order", "count", "proportion"]
    if "head_type" not in clusters.columns:
        return pd.DataFrame(columns=columns)

    known = clusters[
        (clusters["word_order"] != "unknown")
        & (clusters["head_type"].isin(["modal", "auxiliary"]))
    ].copy()
    if known.empty:
        return pd.DataFrame(columns=columns)

    counts = (
        known.groupby(["language", "head_type", "word_order"])
        .size()
        .reset_index(name="count")
        .sort_values(["language", "head_type", "word_order"])
    )
    totals = counts.groupby(["language", "head_type"])["count"].transform("sum")
    counts["proportion"] = counts["count"] / totals
    return counts


def variety_summary(clusters: pd.DataFrame) -> pd.DataFrame:
    known = clusters[clusters["word_order"] != "unknown"].copy()
    if known.empty:
        return pd.DataFrame(columns=["variety", "word_order", "count", "proportion"])
    counts = (
        known.groupby(["variety", "word_order"])
        .size()
        .reset_index(name="count")
        .sort_values(["variety", "word_order"])
    )
    totals = counts.groupby("variety")["count"].transform("sum")
    counts["proportion"] = counts["count"] / totals
    return counts


def confusion_matrix_frame(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    label_names: list[str],
) -> pd.DataFrame:
    matrix = np.zeros((len(label_names), len(label_names)), dtype=int)
    for true_label, predicted_label in zip(y_true, y_pred):
        matrix[true_label, predicted_label] += 1
    return pd.DataFrame(matrix, index=label_names, columns=label_names)


def metrics_dict(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    label_names: list[str],
) -> dict[str, object]:
    predictions = probabilities.argmax(axis=1)
    return {
        "accuracy": accuracy(y_true, predictions),
        "log_loss": log_loss(y_true, probabilities),
        "n_examples": int(len(y_true)),
        "labels": label_names,
        "confusion_matrix": confusion_matrix_frame(
            y_true, predictions, label_names
        ).to_dict(),
    }


def write_json(data: dict[str, object], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2), encoding="utf-8")
