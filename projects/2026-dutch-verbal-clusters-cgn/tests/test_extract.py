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
        self.assertEqual(
            by_utterance.loc["nl1", "sentence_length_type"],
            "no_complementizer",
        )
        self.assertTrue(by_utterance.loc["nl1", "cluster_final"])
        self.assertEqual(by_utterance.loc["nl1", "post_cluster_word_count"], 0)
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

    def test_counts_nonverbal_words_between_complementizer_and_cluster(self) -> None:
        tokens = pd.DataFrame(
            [
                token("short", 1, "dat", "dat", "VG(onder)"),
                token("short", 2, "de", "de", "LID()"),
                token("short", 3, "man", "man", "N()"),
                token("short", 4, "het", "het", "LID()"),
                token("short", 5, "boek", "boek", "N()"),
                token("short", 6, "wil", "willen", "WW(pv,tgw,ev)", "finite"),
                token("short", 7, "lezen", "lezen", "WW(inf,vrij,zonder)", "infinitive"),
                token("long", 1, "dat", "dat", "VG(onder)"),
                token("long", 2, "de", "de", "LID()"),
                token("long", 3, "oude", "oud", "ADJ()"),
                token("long", 4, "man", "man", "N()"),
                token("long", 5, "gisteren", "gisteren", "BW()"),
                token("long", 6, "het", "het", "LID()"),
                token("long", 7, "boek", "boek", "N()"),
                token("long", 8, "wil", "willen", "WW(pv,tgw,ev)", "finite"),
                token("long", 9, "lezen", "lezen", "WW(inf,vrij,zonder)", "infinitive"),
            ]
        )
        prepared, _ = prepare_token_table(tokens)
        clusters = extract_clusters(prepared).set_index("utterance_id")

        self.assertEqual(clusters.loc["short", "complementizer_token"], "dat")
        self.assertEqual(clusters.loc["short", "pre_cluster_nonverbal_count"], 4)
        self.assertEqual(clusters.loc["short", "sentence_length_type"], "short")
        self.assertEqual(clusters.loc["long", "pre_cluster_nonverbal_count"], 6)
        self.assertEqual(clusters.loc["long", "sentence_length_type"], "long")

    def test_classifies_core_and_semi_auxiliary_heads(self) -> None:
        tokens = pd.DataFrame(
            [
                {
                    "utterance_id": "aux",
                    "token_index": 1,
                    "token": "gelezen",
                    "lemma": "lezen",
                    "pos": "WW(vd,vrij,zonder)",
                    "verb_form": "participle",
                    "variety": "Netherlands",
                },
                {
                    "utterance_id": "aux",
                    "token_index": 2,
                    "token": "heeft",
                    "lemma": "hebben",
                    "pos": "WW(pv,tgw,ev)",
                    "verb_form": "finite",
                    "variety": "Netherlands",
                },
                {
                    "utterance_id": "semi",
                    "token_index": 1,
                    "token": "gaat",
                    "lemma": "gaan",
                    "pos": "WW(pv,tgw,ev)",
                    "verb_form": "finite",
                    "variety": "Flanders",
                },
                {
                    "utterance_id": "semi",
                    "token_index": 2,
                    "token": "werken",
                    "lemma": "werken",
                    "pos": "WW(inf,vrij,zonder)",
                    "verb_form": "infinitive",
                    "variety": "Flanders",
                },
            ]
        )
        prepared, _ = prepare_token_table(tokens)
        clusters = extract_clusters(prepared).set_index("utterance_id")

        self.assertEqual(clusters.loc["aux", "head_type"], "auxiliary")
        self.assertTrue(clusters.loc["aux", "has_auxiliary"])
        self.assertFalse(clusters.loc["aux", "has_semi_auxiliary"])
        self.assertEqual(clusters.loc["semi", "head_type"], "semi_auxiliary")
        self.assertFalse(clusters.loc["semi", "has_auxiliary"])
        self.assertTrue(clusters.loc["semi", "has_semi_auxiliary"])


if __name__ == "__main__":
    unittest.main()


def token(
    utterance_id: str,
    token_index: int,
    token_text: str,
    lemma: str,
    pos: str,
    verb_form: str = "",
) -> dict[str, object]:
    return {
        "utterance_id": utterance_id,
        "token_index": token_index,
        "token": token_text,
        "lemma": lemma,
        "pos": pos,
        "verb_form": verb_form,
        "variety": "Netherlands",
    }
