"""Streaming extraction for large normalized CGN token tables."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Iterable

from .extract import (
    AUXILIARY_LEMMAS,
    MODAL_LEMMAS,
    ClusterExtractionConfig,
    classify_head_lemma,
    head_index_from_forms_and_ranks,
    infer_verb_form,
    is_verb_like,
    lower,
)
from .schema import LANGUAGE_BY_VARIETY, normalize_language, normalize_variety


CLUSTER_COLUMNS = [
    "cluster_id",
    "utterance_id",
    "start_token_index",
    "end_token_index",
    "variety",
    "language",
    "speaker_id",
    "speaker_region",
    "component",
    "genre",
    "register",
    "cluster_length",
    "surface_tokens",
    "surface_lemmas",
    "verb_tokens",
    "verb_lemmas",
    "verb_forms",
    "head_position",
    "head_token",
    "head_lemma",
    "head_pos",
    "head_type",
    "word_order",
    "finite_position",
    "has_te",
    "has_modal",
    "has_auxiliary",
]


def normalize_stream_row(row: dict[str, str]) -> dict[str, object]:
    normalized = dict(row)
    normalized["token_index"] = int(float(normalized["token_index"]))
    normalized["variety"] = normalize_variety(normalized["variety"])
    if normalized.get("language"):
        normalized["language"] = normalize_language(normalized["language"])
    else:
        normalized["language"] = LANGUAGE_BY_VARIETY[normalized["variety"]]
    return normalized


def iter_utterances(token_path: str | Path) -> Iterable[tuple[str, list[dict[str, object]]]]:
    with Path(token_path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        current_id: str | None = None
        rows: list[dict[str, object]] = []

        for raw_row in reader:
            row = normalize_stream_row(raw_row)
            utterance_id = str(row["utterance_id"])
            if current_id is None:
                current_id = utterance_id
            if utterance_id != current_id:
                yield current_id, rows
                current_id = utterance_id
                rows = []
            rows.append(row)

        if current_id is not None:
            yield current_id, rows


def extract_clusters_to_csv(
    token_path: str | Path,
    cluster_path: str | Path,
    config: ClusterExtractionConfig | None = None,
) -> dict[str, object]:
    config = config or ClusterExtractionConfig()
    target = Path(cluster_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    token_rows = 0
    utterances = 0
    clusters = 0
    languages: Counter[str] = Counter()
    varieties: Counter[str] = Counter()

    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CLUSTER_COLUMNS)
        writer.writeheader()
        for utterance_id, rows in iter_utterances(token_path):
            utterances += 1
            token_rows += len(rows)
            for row in rows:
                languages[str(row.get("language", ""))] += 1
                varieties[str(row.get("variety", ""))] += 1

            for cluster in extract_utterance_clusters(utterance_id, rows, config):
                writer.writerow(cluster)
                clusters += 1

    return {
        "token_rows": token_rows,
        "utterances": utterances,
        "clusters": clusters,
        "languages": dict(languages),
        "varieties": dict(varieties),
    }


def extract_utterance_clusters(
    utterance_id: str,
    rows: list[dict[str, object]],
    config: ClusterExtractionConfig,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    current_indices: list[int] = []

    def flush() -> None:
        nonlocal current_indices
        if len(current_indices) >= config.min_verbs:
            records.append(make_cluster_record(utterance_id, rows, current_indices))
        current_indices = []

    for row_index, row in enumerate(rows):
        token_text = lower(row.get("token", ""))
        if is_verb_like(row):
            current_indices.append(row_index)
        elif current_indices and token_text in config.bridge_tokens:
            continue
        else:
            flush()
    flush()
    return records


def make_cluster_record(
    utterance_id: str,
    rows: list[dict[str, object]],
    verb_indices: list[int],
) -> dict[str, object]:
    verb_rows = [rows[index] for index in verb_indices]
    start = min(int(row["token_index"]) for row in verb_rows)
    end = max(int(row["token_index"]) for row in verb_rows)
    span_rows = [
        row for row in rows if start <= int(row["token_index"]) <= end
    ]

    verb_tokens = [str(row.get("token", "")) for row in verb_rows]
    verb_lemmas = [lower(row.get("lemma", "")) for row in verb_rows]
    span_tokens = [str(row.get("token", "")) for row in span_rows]
    span_lemmas = [lower(row.get("lemma", "")) for row in span_rows]
    forms = [
        infer_verb_form(row.get("pos", ""), row.get("verb_form", ""))
        for row in verb_rows
    ]
    head_info = head_info_from_rows(verb_rows, forms)

    return {
        "cluster_id": f"{utterance_id}:{start}-{end}",
        "utterance_id": utterance_id,
        "start_token_index": start,
        "end_token_index": end,
        "variety": most_common(row.get("variety", "") for row in verb_rows),
        "language": most_common(row.get("language", "") for row in verb_rows),
        "speaker_id": most_common(row.get("speaker_id", "") for row in verb_rows),
        "speaker_region": most_common(
            row.get("speaker_region", "") for row in verb_rows
        ),
        "component": most_common(row.get("component", "") for row in verb_rows),
        "genre": most_common(row.get("genre", "") for row in verb_rows),
        "register": most_common(row.get("register", "") for row in verb_rows),
        "cluster_length": len(verb_rows),
        "surface_tokens": " ".join(span_tokens),
        "surface_lemmas": " ".join(span_lemmas),
        "verb_tokens": " ".join(verb_tokens),
        "verb_lemmas": " ".join(verb_lemmas),
        "verb_forms": " ".join(forms),
        **head_info,
        "word_order": order_from_rows(verb_rows, forms),
        "finite_position": finite_position_from_forms(forms),
        "has_te": any(lower(row.get("token", "")) == "te" for row in span_rows),
        "has_modal": any(lemma in MODAL_LEMMAS for lemma in verb_lemmas),
        "has_auxiliary": any(lemma in AUXILIARY_LEMMAS for lemma in verb_lemmas),
    }


def head_info_from_rows(
    verb_rows: list[dict[str, object]],
    forms: list[str],
) -> dict[str, object]:
    ranks = [row.get("verb_rank", "") for row in verb_rows]
    head_index = head_index_from_forms_and_ranks(forms, ranks)
    if head_index is None:
        return {
            "head_position": "",
            "head_token": "",
            "head_lemma": "",
            "head_pos": "",
            "head_type": "unknown",
        }

    head_row = verb_rows[head_index]
    head_lemma = lower(head_row.get("lemma", ""))
    return {
        "head_position": head_index + 1,
        "head_token": str(head_row.get("token", "")),
        "head_lemma": head_lemma,
        "head_pos": str(head_row.get("pos", "")),
        "head_type": classify_head_lemma(head_lemma),
    }


def order_from_rows(verb_rows: list[dict[str, object]], forms: list[str]) -> str:
    ranks = []
    for row in verb_rows:
        raw_rank = row.get("verb_rank", "")
        if raw_rank in {"", None}:
            break
        try:
            ranks.append(int(float(str(raw_rank))))
        except ValueError:
            break
    if len(ranks) == len(verb_rows):
        return "-".join(str(rank) for rank in ranks)

    if len(forms) == 2 and forms.count("finite") == 1:
        return "1-2" if forms[0] == "finite" else "2-1"
    return "unknown"


def finite_position_from_forms(forms: list[str]) -> str:
    positions = [index for index, form in enumerate(forms) if form == "finite"]
    if not positions:
        return "none"
    if positions[0] == 0:
        return "first"
    if positions[0] == len(forms) - 1:
        return "last"
    return "medial"


def most_common(values: Iterable[object]) -> object:
    cleaned = [value for value in values if value not in {"", None}]
    if not cleaned:
        return ""
    return Counter(cleaned).most_common(1)[0][0]
