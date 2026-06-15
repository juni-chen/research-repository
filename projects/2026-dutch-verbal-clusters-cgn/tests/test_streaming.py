from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cgn_clusters.extract import ClusterExtractionConfig
from cgn_clusters.streaming import extract_clusters_to_csv


class StreamingExtractionTest(unittest.TestCase):
    def test_extracts_clusters_from_token_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            token_path = Path(tmpdir) / "tokens.csv"
            cluster_path = Path(tmpdir) / "clusters.csv"
            with token_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "utterance_id",
                        "token_index",
                        "token",
                        "lemma",
                        "pos",
                        "variety",
                        "language",
                        "speaker_id",
                        "component",
                    ],
                )
                writer.writeheader()
                writer.writerows(
                    [
                        token("u1", 1, "dat", "dat", "VG()", "Netherlands", "Dutch"),
                        token(
                            "u1",
                            2,
                            "wil",
                            "willen",
                            "WW(pv,tgw,ev)",
                            "Netherlands",
                            "Dutch",
                        ),
                        token(
                            "u1",
                            3,
                            "komen",
                            "komen",
                            "WW(inf,vrij,zonder)",
                            "Netherlands",
                            "Dutch",
                        ),
                        token("u2", 1, "dat", "dat", "VG()", "Flanders", "Flemish"),
                        token(
                            "u2",
                            2,
                            "komen",
                            "komen",
                            "WW(inf,vrij,zonder)",
                            "Flanders",
                            "Flemish",
                        ),
                        token(
                            "u2",
                            3,
                            "wil",
                            "willen",
                            "WW(pv,tgw,ev)",
                            "Flanders",
                            "Flemish",
                        ),
                    ]
                )

            report = extract_clusters_to_csv(
                token_path,
                cluster_path,
                ClusterExtractionConfig(),
            )

            self.assertEqual(report["token_rows"], 6)
            self.assertEqual(report["clusters"], 2)
            with cluster_path.open(newline="", encoding="utf-8") as handle:
                clusters = list(csv.DictReader(handle))
            self.assertEqual(clusters[0]["language"], "Dutch")
            self.assertEqual(clusters[0]["word_order"], "1-2")
            self.assertEqual(clusters[0]["head_type"], "modal")
            self.assertEqual(clusters[1]["language"], "Flemish")
            self.assertEqual(clusters[1]["word_order"], "2-1")
            self.assertEqual(clusters[1]["head_type"], "modal")


def token(
    utterance_id: str,
    token_index: int,
    token_text: str,
    lemma: str,
    pos: str,
    variety: str,
    language: str,
) -> dict[str, object]:
    return {
        "utterance_id": utterance_id,
        "token_index": token_index,
        "token": token_text,
        "lemma": lemma,
        "pos": pos,
        "variety": variety,
        "language": language,
        "speaker_id": "speaker",
        "component": "comp-a",
    }


if __name__ == "__main__":
    unittest.main()
