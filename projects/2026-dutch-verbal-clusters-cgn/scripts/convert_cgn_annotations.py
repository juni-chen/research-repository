#!/usr/bin/env python3
"""Convert CGN annotation XML into the normalized token table."""

from __future__ import annotations

import argparse
import csv
import gzip
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARCHIVE = PROJECT_ROOT / "data" / "raw" / "CGNAnn_2.0.3.zip"
DEFAULT_OUT = PROJECT_ROOT / "data" / "processed" / "cgn_tokens.csv"
TAG_PREFIX = "CGNAnn_2.0.3/data/annot/xml/tag/"

OUTPUT_COLUMNS = [
    "utterance_id",
    "token_index",
    "token",
    "lemma",
    "pos",
    "variety",
    "language",
    "speaker_id",
    "component",
    "source_file",
]

LANGUAGE_BY_PATH_CODE = {
    "nl": ("Netherlands", "Dutch"),
    "vl": ("Flanders", "Flemish"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--archive",
        default=str(DEFAULT_ARCHIVE),
        help="CGNAnn_2.0.3.zip annotation archive.",
    )
    parser.add_argument(
        "--out",
        default=str(DEFAULT_OUT),
        help="Normalized token CSV to create.",
    )
    parser.add_argument(
        "--limit-files",
        type=int,
        default=None,
        help="Optional debugging limit; omit for the full corpus.",
    )
    return parser.parse_args()


def tag_files(zip_file: ZipFile) -> list[str]:
    names = [
        name
        for name in zip_file.namelist()
        if name.startswith(TAG_PREFIX) and name.endswith(".tag.gz")
    ]
    return sorted(names)


def path_metadata(member_name: str) -> tuple[str, str, str]:
    parts = member_name.split("/")
    try:
        tag_index = parts.index("tag")
        component = parts[tag_index + 1]
        language_code = parts[tag_index + 2]
    except (ValueError, IndexError) as exc:
        raise ValueError(f"Unexpected CGN tag path: {member_name}") from exc

    if language_code not in LANGUAGE_BY_PATH_CODE:
        raise ValueError(f"Unknown CGN language code {language_code!r} in {member_name}")
    variety, language = LANGUAGE_BY_PATH_CODE[language_code]
    return component, variety, language


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def token_rows(zip_file: ZipFile, member_name: str) -> list[dict[str, object]]:
    component, variety, language = path_metadata(member_name)
    rows: list[dict[str, object]] = []

    current_utterance_id = ""
    current_speaker_id = ""
    token_index = 0

    with zip_file.open(member_name) as compressed_member:
        with gzip.GzipFile(fileobj=compressed_member) as xml_file:
            for event, elem in ET.iterparse(xml_file, events=("start",)):
                name = local_name(elem.tag)
                if name == "pau":
                    current_utterance_id = elem.attrib.get("ref", "")
                    current_speaker_id = elem.attrib.get("s", "")
                    token_index = 0
                elif name in {"pw", "pl"}:
                    token_index += 1
                    rows.append(
                        {
                            "utterance_id": current_utterance_id,
                            "token_index": token_index,
                            "token": elem.attrib.get("w", ""),
                            "lemma": elem.attrib.get("lem", ""),
                            "pos": elem.attrib.get("pos", ""),
                            "variety": variety,
                            "language": language,
                            "speaker_id": current_speaker_id,
                            "component": component,
                            "source_file": Path(member_name).name,
                        }
                    )
                elem.clear()

    return rows


def convert_archive(archive_path: Path, out_path: Path, limit_files: int | None) -> int:
    if not archive_path.exists():
        raise FileNotFoundError(archive_path)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    total_rows = 0

    with ZipFile(archive_path) as zip_file:
        members = tag_files(zip_file)
        if limit_files is not None:
            members = members[:limit_files]
        if not members:
            raise ValueError(f"No CGN tag files found under {TAG_PREFIX}")

        with out_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
            writer.writeheader()
            for file_index, member in enumerate(members, start=1):
                rows = token_rows(zip_file, member)
                writer.writerows(rows)
                total_rows += len(rows)
                if file_index % 500 == 0:
                    print(
                        f"converted {file_index}/{len(members)} files; "
                        f"{total_rows:,} tokens",
                        file=sys.stderr,
                    )

    return total_rows


def main() -> None:
    args = parse_args()
    archive_path = Path(args.archive)
    out_path = Path(args.out)
    total_rows = convert_archive(archive_path, out_path, args.limit_files)
    print(f"Wrote {total_rows:,} tokens to {out_path}")


if __name__ == "__main__":
    main()
