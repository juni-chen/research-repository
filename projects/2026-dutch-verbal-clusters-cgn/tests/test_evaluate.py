from __future__ import annotations

import sys
from pathlib import Path
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cgn_clusters.evaluate import language_head_type_word_order_summary, language_summary


class HeadTypeSummaryTest(unittest.TestCase):
    def test_summarizes_order_proportions_by_language_and_head_type(self) -> None:
        clusters = pd.DataFrame(
            [
                {"language": "Dutch", "head_type": "modal", "word_order": "1-2"},
                {"language": "Dutch", "head_type": "modal", "word_order": "2-1"},
                {"language": "Dutch", "head_type": "modal", "word_order": "2-1"},
                {"language": "Dutch", "head_type": "auxiliary", "word_order": "1-2"},
                {"language": "Dutch", "head_type": "semi_auxiliary", "word_order": "1-2"},
                {"language": "Dutch", "head_type": "semi_auxiliary", "word_order": "2-1"},
                {"language": "Flemish", "head_type": "modal", "word_order": "1-2"},
                {"language": "Flemish", "head_type": "other", "word_order": "1-2"},
                {"language": "Flemish", "head_type": "auxiliary", "word_order": "unknown"},
            ]
        )

        summary = language_head_type_word_order_summary(clusters)
        modal_dutch = summary[
            (summary["language"] == "Dutch")
            & (summary["head_type"] == "modal")
            & (summary["word_order"] == "2-1")
        ].iloc[0]

        self.assertEqual(modal_dutch["count"], 2)
        self.assertAlmostEqual(modal_dutch["proportion"], 2 / 3)
        self.assertIn("semi_auxiliary", summary["head_type"].tolist())
        self.assertNotIn("other", summary["head_type"].tolist())

    def test_language_summary_excludes_clusters_without_complementizer(self) -> None:
        clusters = pd.DataFrame(
            [
                {
                    "language": "Dutch",
                    "word_order": "1-2",
                    "complementizer_token": "dat",
                },
                {
                    "language": "Dutch",
                    "word_order": "2-1",
                    "complementizer_token": "",
                },
                {
                    "language": "Dutch",
                    "word_order": "unknown",
                    "complementizer_token": "dat",
                },
            ]
        )

        summary = language_summary(clusters)

        self.assertEqual(len(summary), 1)
        self.assertEqual(summary.loc[0, "word_order"], "1-2")
        self.assertEqual(summary.loc[0, "count"], 1)


if __name__ == "__main__":
    unittest.main()
