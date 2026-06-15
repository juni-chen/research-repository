from __future__ import annotations

import sys
from pathlib import Path
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cgn_clusters.extract import extract_clusters
from cgn_clusters.schema import prepare_token_table


class ExtractClustersTest(unittest.TestCase):
    def test_extracts_ranked_orders_by_variety(self) -> None:
        tokens = pd.DataFrame(
            [
                {
                    "utterance_id": "nl1",
                    "token_index": 1,
                    "token": "wil",
                    "lemma": "willen",
                    "pos": "WW(pv,tgw,ev)",
                    "verb_form": "finite",
                    "verb_rank": 1,
                    "variety": "NL",
                },
                {
                    "utterance_id": "nl1",
                    "token_index": 2,
                    "token": "komen",
                    "lemma": "komen",
                    "pos": "WW(inf,vrij,zonder)",
                    "verb_form": "infinitive",
                    "verb_rank": 2,
                    "variety": "NL",
                },
                {
                    "utterance_id": "fl1",
                    "token_index": 1,
                    "token": "komen",
                    "lemma": "komen",
                    "pos": "WW(inf,vrij,zonder)",
                    "verb_form": "infinitive",
                    "verb_rank": 2,
                    "variety": "Flemish",
                },
                {
                    "utterance_id": "fl1",
                    "token_index": 2,
                    "token": "wil",
                    "lemma": "willen",
                    "pos": "WW(pv,tgw,ev)",
                    "verb_form": "finite",
                    "verb_rank": 1,
                    "variety": "Flemish",
                },
            ]
        )
        prepared, _ = prepare_token_table(tokens)
        clusters = extract_clusters(prepared)
        by_utterance = clusters.set_index("utterance_id")

        self.assertEqual(by_utterance.loc["nl1", "word_order"], "1-2")
        self.assertEqual(by_utterance.loc["nl1", "variety"], "Netherlands")
        self.assertEqual(by_utterance.loc["nl1", "language"], "Dutch")
        self.assertEqual(by_utterance.loc["nl1", "head_lemma"], "willen")
        self.assertEqual(by_utterance.loc["nl1", "head_type"], "modal")
        self.assertEqual(by_utterance.loc["fl1", "word_order"], "2-1")
        self.assertEqual(by_utterance.loc["fl1", "variety"], "Flanders")
        self.assertEqual(by_utterance.loc["fl1", "language"], "Flemish")
        self.assertEqual(by_utterance.loc["fl1", "head_lemma"], "willen")
        self.assertEqual(by_utterance.loc["fl1", "head_type"], "modal")

    def test_infers_simple_two_verb_order_without_rank(self) -> None:
        tokens = pd.DataFrame(
            [
                {
                    "utterance_id": "u1",
                    "token_index": 1,
                    "token": "komen",
                    "lemma": "komen",
                    "pos": "WW(inf,vrij,zonder)",
                    "verb_form": "infinitive",
                    "variety": "Flanders",
                },
                {
                    "utterance_id": "u1",
                    "token_index": 2,
                    "token": "kan",
                    "lemma": "kunnen",
                    "pos": "WW(pv,tgw,ev)",
                    "verb_form": "finite",
                    "variety": "Flanders",
                },
            ]
        )
        prepared, _ = prepare_token_table(tokens)
        clusters = extract_clusters(prepared)

        self.assertEqual(clusters.loc[0, "word_order"], "2-1")
        self.assertEqual(clusters.loc[0, "finite_position"], "last")
        self.assertEqual(clusters.loc[0, "head_type"], "modal")


if __name__ == "__main__":
    unittest.main()
