"""Schema helpers for CGN-derived token tables."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


REQUIRED_COLUMNS = [
    "utterance_id",
    "token_index",
    "token",
    "lemma",
    "pos",
    "variety",
]

OPTIONAL_COLUMNS = [
    "language",
    "verb_form",
    "verb_rank",
    "speaker_id",
    "speaker_region",
    "component",
    "genre",
    "register",
]

COLUMN_ALIASES = {
    "id": "utterance_id",
    "sentence_id": "utterance_id",
    "sent_id": "utterance_id",
    "annotation_unit": "utterance_id",
    "au_id": "utterance_id",
    "word": "token",
    "form": "token",
    "orth": "token",
    "orthography": "token",
    "position": "token_index",
    "index": "token_index",
    "token_id": "token_index",
    "word_id": "token_index",
    "speaker_country": "variety",
    "country": "variety",
    "language_area": "variety",
    "variety_label": "variety",
    "region": "speaker_region",
    "speaker_variety": "variety",
    "cgn_component": "component",
    "text_type": "genre",
    "register_type": "register",
    "rank": "verb_rank",
    "hierarchy_rank": "verb_rank",
}

VARIETY_ALIASES = {
    "nl": "Netherlands",
    "nld": "Netherlands",
    "netherlands": "Netherlands",
    "the netherlands": "Netherlands",
    "nederland": "Netherlands",
    "nederlands": "Netherlands",
    "northern dutch": "Netherlands",
    "be": "Flanders",
    "bel": "Flanders",
    "belgium": "Flanders",
    "belgian dutch": "Flanders",
    "flanders": "Flanders",
    "flemish": "Flanders",
    "vlaanderen": "Flanders",
    "vlaams": "Flanders",
}

LANGUAGE_BY_VARIETY = {
    "Netherlands": "Dutch",
    "Flanders": "Flemish",
}

LANGUAGE_ALIASES = {
    "nl": "Dutch",
    "nld": "Dutch",
    "dutch": "Dutch",
    "netherlands": "Dutch",
    "netherlands dutch": "Dutch",
    "northern dutch": "Dutch",
    "be": "Flemish",
    "bel": "Flemish",
    "flemish": "Flemish",
    "belgian dutch": "Flemish",
    "flanders": "Flemish",
    "vlaams": "Flemish",
}


@dataclass(frozen=True)
class SchemaReport:
    """A compact report about schema normalization."""

    rows: int
    columns: list[str]
    varieties: list[str]
    languages: list[str]


def normalize_column_name(name: str) -> str:
    normalized = name.strip().lower().replace("-", "_").replace(" ", "_")
    return COLUMN_ALIASES.get(normalized, normalized)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {column: normalize_column_name(column) for column in df.columns}
    return df.rename(columns=renamed)


def normalize_variety(value: object) -> str:
    if pd.isna(value):
        raise ValueError("Missing variety value. Expected Netherlands or Flanders.")
    raw = str(value).strip()
    key = raw.lower()
    if key in {"netherlands", "flanders"}:
        return raw[0].upper() + raw[1:].lower()
    if key in VARIETY_ALIASES:
        return VARIETY_ALIASES[key]
    raise ValueError(
        f"Unknown variety value {raw!r}. Use Netherlands/Flanders or a known alias."
    )


def normalize_language(value: object) -> str:
    if pd.isna(value):
        raise ValueError("Missing language value. Expected Dutch or Flemish.")
    raw = str(value).strip()
    key = raw.lower()
    if key in {"dutch", "flemish"}:
        return raw[0].upper() + raw[1:].lower()
    if key in LANGUAGE_ALIASES:
        return LANGUAGE_ALIASES[key]
    raise ValueError(f"Unknown language value {raw!r}. Use Dutch or Flemish.")


def ensure_columns(df: pd.DataFrame, required: Iterable[str] = REQUIRED_COLUMNS) -> None:
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(missing)}")


def prepare_token_table(df: pd.DataFrame) -> tuple[pd.DataFrame, SchemaReport]:
    prepared = normalize_columns(df).copy()
    ensure_columns(prepared)

    prepared["variety"] = prepared["variety"].map(normalize_variety)
    if "language" in prepared.columns:
        prepared["language"] = prepared["language"].map(normalize_language)
    else:
        prepared["language"] = prepared["variety"].map(LANGUAGE_BY_VARIETY)
    prepared["token_index"] = pd.to_numeric(prepared["token_index"], errors="raise")

    for column in OPTIONAL_COLUMNS:
        if column not in prepared.columns:
            prepared[column] = pd.NA

    prepared = prepared.sort_values(["utterance_id", "token_index"]).reset_index(drop=True)
    report = SchemaReport(
        rows=len(prepared),
        columns=list(prepared.columns),
        varieties=sorted(prepared["variety"].dropna().unique().tolist()),
        languages=sorted(prepared["language"].dropna().unique().tolist()),
    )
    return prepared, report
