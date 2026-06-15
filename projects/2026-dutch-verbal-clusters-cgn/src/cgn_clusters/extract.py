"""Extract verbal-cluster observations from CGN-derived token tables."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable

import pandas as pd


BRIDGE_TOKENS = {"te"}
MODAL_LEMMAS = {
    "kunnen",
    "moeten",
    "mogen",
    "willen",
    "zullen",
    "hoeven",
}
AUXILIARY_LEMMAS = {
    "hebben",
    "zijn",
    "worden",
    "gaan",
    "blijven",
    "komen",
    "laten",
    "doen",
} | MODAL_LEMMAS
NON_MODAL_AUXILIARY_LEMMAS = AUXILIARY_LEMMAS - MODAL_LEMMAS


@dataclass(frozen=True)
class ClusterExtractionConfig:
    min_verbs: int = 2
    bridge_tokens: frozenset[str] = frozenset(BRIDGE_TOKENS)


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def lower(value: object) -> str:
    return clean_text(value).lower()


def infer_verb_form(pos: object, explicit: object = None) -> str:
    if explicit is not None and not pd.isna(explicit) and clean_text(explicit):
        return lower(explicit)

    tag = lower(pos)
    if "pv" in tag or "finite" in tag or "fin" in tag:
        return "finite"
    if "inf" in tag:
        return "infinitive"
    if "vd" in tag or "part" in tag or "participle" in tag:
        return "participle"
    return "unknown"


def is_verb_like(row: pd.Series) -> bool:
    pos = lower(row.get("pos", ""))
    upos = lower(row.get("upos", ""))
    verb_form = lower(row.get("verb_form", ""))

    if upos in {"verb", "aux"}:
        return True
    if pos.startswith("ww") or pos.startswith("verb") or pos.startswith("aux"):
        return True
    if "verb" in pos or "aux" in pos:
        return True
    return verb_form in {"finite", "infinitive", "participle", "gerund"}


def most_common(values: Iterable[object]) -> object:
    cleaned = [value for value in values if not pd.isna(value) and clean_text(value)]
    if not cleaned:
        return pd.NA
    return Counter(cleaned).most_common(1)[0][0]


def order_from_ranks(verb_rows: pd.DataFrame) -> str:
    if "verb_rank" not in verb_rows.columns:
        return "unknown"
    ranks = pd.to_numeric(verb_rows["verb_rank"], errors="coerce")
    if ranks.isna().any():
        return "unknown"
    return "-".join(str(int(rank)) for rank in ranks.tolist())


def order_from_forms(verb_rows: pd.DataFrame) -> str:
    forms = [
        infer_verb_form(row.get("pos", ""), row.get("verb_form", ""))
        for _, row in verb_rows.iterrows()
    ]
    if len(forms) == 2 and forms.count("finite") == 1:
        return "1-2" if forms[0] == "finite" else "2-1"
    return "unknown"


def finite_position(verb_rows: pd.DataFrame) -> str:
    forms = [
        infer_verb_form(row.get("pos", ""), row.get("verb_form", ""))
        for _, row in verb_rows.iterrows()
    ]
    positions = [index for index, form in enumerate(forms) if form == "finite"]
    if not positions:
        return "none"
    if positions[0] == 0:
        return "first"
    if positions[0] == len(forms) - 1:
        return "last"
    return "medial"


def classify_head_lemma(lemma: object) -> str:
    normalized = lower(lemma)
    if not normalized:
        return "unknown"
    if normalized in MODAL_LEMMAS:
        return "modal"
    if normalized in NON_MODAL_AUXILIARY_LEMMAS:
        return "auxiliary"
    return "other"


def head_index_from_forms_and_ranks(
    forms: list[str],
    ranks: Iterable[object] | None = None,
) -> int | None:
    rank_values: list[int] = []
    if ranks is not None:
        for raw_rank in ranks:
            if pd.isna(raw_rank) or not clean_text(raw_rank):
                break
            try:
                rank_values.append(int(float(clean_text(raw_rank))))
            except ValueError:
                break
        if len(rank_values) == len(forms) and rank_values:
            minimum = min(rank_values)
            if rank_values.count(minimum) == 1:
                return rank_values.index(minimum)

    finite_indices = [index for index, form in enumerate(forms) if form == "finite"]
    if len(finite_indices) == 1:
        return finite_indices[0]
    return None


def head_info_from_rows(
    verb_rows: pd.DataFrame,
    forms: list[str],
) -> dict[str, object]:
    ranks = verb_rows["verb_rank"].tolist() if "verb_rank" in verb_rows.columns else None
    head_index = head_index_from_forms_and_ranks(forms, ranks)
    if head_index is None:
        return {
            "head_position": pd.NA,
            "head_token": "",
            "head_lemma": "",
            "head_pos": "",
            "head_type": "unknown",
        }

    head_row = verb_rows.iloc[head_index]
    head_lemma = lower(head_row.get("lemma", ""))
    return {
        "head_position": head_index + 1,
        "head_token": clean_text(head_row.get("token", "")),
        "head_lemma": head_lemma,
        "head_pos": clean_text(head_row.get("pos", "")),
        "head_type": classify_head_lemma(head_lemma),
    }


def extract_clusters(
    tokens: pd.DataFrame,
    config: ClusterExtractionConfig | None = None,
) -> pd.DataFrame:
    config = config or ClusterExtractionConfig()
    records: list[dict[str, object]] = []

    for utterance_id, group in tokens.groupby("utterance_id", sort=False):
        group = group.sort_values("token_index").reset_index(drop=True)
        current_indices: list[int] = []
        pending_bridge_indices: list[int] = []

        def flush() -> None:
            nonlocal current_indices, pending_bridge_indices
            if len(current_indices) >= config.min_verbs:
                add_cluster_record(records, utterance_id, group, current_indices)
            current_indices = []
            pending_bridge_indices = []

        for row_index, row in group.iterrows():
            token_text = lower(row.get("token", ""))
            if is_verb_like(row):
                current_indices.append(row_index)
                pending_bridge_indices = []
            elif current_indices and token_text in config.bridge_tokens:
                pending_bridge_indices.append(row_index)
            else:
                flush()
        flush()

    return pd.DataFrame.from_records(records)


def add_cluster_record(
    records: list[dict[str, object]],
    utterance_id: object,
    utterance: pd.DataFrame,
    verb_indices: list[int],
) -> None:
    verb_rows = utterance.loc[verb_indices].copy()
    start = int(verb_rows["token_index"].min())
    end = int(verb_rows["token_index"].max())
    span = utterance[
        (utterance["token_index"] >= start) & (utterance["token_index"] <= end)
    ]

    verb_lemmas = [lower(value) for value in verb_rows["lemma"].tolist()]
    verb_tokens = [clean_text(value) for value in verb_rows["token"].tolist()]
    span_lemmas = [lower(value) for value in span["lemma"].tolist()]
    span_tokens = [clean_text(value) for value in span["token"].tolist()]
    forms = [
        infer_verb_form(row.get("pos", ""), row.get("verb_form", ""))
        for _, row in verb_rows.iterrows()
    ]
    word_order = order_from_ranks(verb_rows)
    if word_order == "unknown":
        word_order = order_from_forms(verb_rows)
    head_info = head_info_from_rows(verb_rows, forms)

    record = {
        "cluster_id": f"{utterance_id}:{start}-{end}",
        "utterance_id": utterance_id,
        "start_token_index": start,
        "end_token_index": end,
        "variety": most_common(verb_rows["variety"]),
        "language": most_common(verb_rows["language"]),
        "speaker_id": most_common(verb_rows.get("speaker_id", [])),
        "speaker_region": most_common(verb_rows.get("speaker_region", [])),
        "component": most_common(verb_rows.get("component", [])),
        "genre": most_common(verb_rows.get("genre", [])),
        "register": most_common(verb_rows.get("register", [])),
        "cluster_length": len(verb_rows),
        "surface_tokens": " ".join(span_tokens),
        "surface_lemmas": " ".join(span_lemmas),
        "verb_tokens": " ".join(verb_tokens),
        "verb_lemmas": " ".join(verb_lemmas),
        "verb_forms": " ".join(forms),
        **head_info,
        "word_order": word_order,
        "finite_position": finite_position(verb_rows),
        "has_te": any(lower(value) == "te" for value in span["token"].tolist()),
        "has_modal": any(lemma in MODAL_LEMMAS for lemma in verb_lemmas),
        "has_auxiliary": any(lemma in AUXILIARY_LEMMAS for lemma in verb_lemmas),
    }
    records.append(record)
