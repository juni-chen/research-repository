"""A small MaxEnt-style classifier for word-order experiments."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


DEFAULT_FEATURES = [
    "cluster_length",
    "sentence_length_type",
    "cluster_position",
    "has_te",
    "has_modal",
    "has_auxiliary",
    "has_semi_auxiliary",
    "component",
    "genre",
    "register",
    "speaker_region",
]


def feature_value(value: object) -> str:
    if pd.isna(value):
        return "NA"
    return str(value)


def row_to_features(
    row: pd.Series,
    feature_columns: Iterable[str] = DEFAULT_FEATURES,
    include_interactions: bool = False,
    interaction_anchor: str = "language",
) -> list[str]:
    features: list[str] = []
    anchor_value = feature_value(row.get(interaction_anchor, "NA"))

    for column in feature_columns:
        value = feature_value(row.get(column, "NA"))
        features.append(f"{column}={value}")
        if include_interactions and column != interaction_anchor:
            features.append(f"{interaction_anchor}={anchor_value} & {column}={value}")
    return features


@dataclass
class EncodedData:
    X: np.ndarray
    y: np.ndarray
    feature_names: list[str]
    label_names: list[str]


def encode_examples(
    clusters: pd.DataFrame,
    label_column: str = "word_order",
    feature_columns: Iterable[str] = DEFAULT_FEATURES,
    include_interactions: bool = False,
) -> EncodedData:
    usable = clusters[clusters[label_column] != "unknown"].copy()
    if usable.empty:
        raise ValueError("No usable clusters with known word_order labels.")

    labels = sorted(usable[label_column].unique().tolist())
    label_to_index = {label: index for index, label in enumerate(labels)}

    feature_sets = [
        row_to_features(
            row,
            feature_columns=feature_columns,
            include_interactions=include_interactions,
        )
        for _, row in usable.iterrows()
    ]
    vocabulary = sorted({feature for features in feature_sets for feature in features})
    feature_to_index = {feature: index for index, feature in enumerate(vocabulary)}

    X = np.zeros((len(usable), len(vocabulary)), dtype=float)
    for row_index, features in enumerate(feature_sets):
        for feature in features:
            X[row_index, feature_to_index[feature]] = 1.0

    y = np.array([label_to_index[label] for label in usable[label_column]], dtype=int)
    return EncodedData(X=X, y=y, feature_names=vocabulary, label_names=labels)


def stable_train_test_split(
    y: np.ndarray,
    test_size: float = 0.25,
    seed: int = 7,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    train_indices: list[int] = []
    test_indices: list[int] = []

    for label in sorted(set(y.tolist())):
        label_indices = np.where(y == label)[0]
        shuffled = label_indices.copy()
        rng.shuffle(shuffled)
        n_test = max(1, int(round(len(shuffled) * test_size)))
        if len(shuffled) <= 2:
            n_test = 0
        test_indices.extend(shuffled[:n_test].tolist())
        train_indices.extend(shuffled[n_test:].tolist())

    if not test_indices:
        all_indices = np.arange(len(y))
        return all_indices, all_indices
    return np.array(train_indices, dtype=int), np.array(test_indices, dtype=int)


class MaxEntClassifier:
    """Multinomial logistic regression trained with batch gradient descent."""

    def __init__(
        self,
        learning_rate: float = 0.15,
        l2: float = 0.01,
        iterations: int = 1500,
        seed: int = 7,
    ) -> None:
        self.learning_rate = learning_rate
        self.l2 = l2
        self.iterations = iterations
        self.seed = seed
        self.weights: np.ndarray | None = None
        self.loss_history: list[float] = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> "MaxEntClassifier":
        Xb = add_bias(X)
        n_examples, n_features = Xb.shape
        n_labels = int(y.max()) + 1
        rng = np.random.default_rng(self.seed)
        weights = rng.normal(0, 0.01, size=(n_features, n_labels))
        target = np.eye(n_labels)[y]

        for _ in range(self.iterations):
            probabilities = softmax(Xb @ weights)
            error = probabilities - target
            gradient = (Xb.T @ error) / n_examples
            gradient[1:] += self.l2 * weights[1:]
            weights -= self.learning_rate * gradient
            self.loss_history.append(cross_entropy(target, probabilities))

        self.weights = weights
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if self.weights is None:
            raise ValueError("Model has not been fitted.")
        return softmax(add_bias(X) @ self.weights)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.predict_proba(X).argmax(axis=1)


def add_bias(X: np.ndarray) -> np.ndarray:
    return np.column_stack([np.ones(len(X)), X])


def softmax(scores: np.ndarray) -> np.ndarray:
    shifted = scores - scores.max(axis=1, keepdims=True)
    exp_scores = np.exp(shifted)
    return exp_scores / exp_scores.sum(axis=1, keepdims=True)


def cross_entropy(target: np.ndarray, probabilities: np.ndarray) -> float:
    clipped = np.clip(probabilities, 1e-12, 1.0)
    return float(-(target * np.log(clipped)).sum(axis=1).mean())


def log_loss(y: np.ndarray, probabilities: np.ndarray) -> float:
    clipped = np.clip(probabilities, 1e-12, 1.0)
    return float(-np.log(clipped[np.arange(len(y)), y]).mean())


def accuracy(y: np.ndarray, predictions: np.ndarray) -> float:
    return float((y == predictions).mean())


def coefficients_frame(
    model: MaxEntClassifier,
    feature_names: list[str],
    label_names: list[str],
) -> pd.DataFrame:
    if model.weights is None:
        raise ValueError("Model has not been fitted.")

    names = ["<bias>"] + feature_names
    records = []
    for feature_index, feature_name in enumerate(names):
        for label_index, label_name in enumerate(label_names):
            records.append(
                {
                    "feature": feature_name,
                    "word_order": label_name,
                    "weight": model.weights[feature_index, label_index],
                }
            )
    return pd.DataFrame.from_records(records).sort_values(
        ["word_order", "weight"], ascending=[True, False]
    )


def write_coefficients(
    model: MaxEntClassifier,
    feature_names: list[str],
    label_names: list[str],
    path: str | Path,
) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    coefficients_frame(model, feature_names, label_names).to_csv(target, index=False)
