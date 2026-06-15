from __future__ import annotations

import sys
from pathlib import Path
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cgn_clusters.evaluate import language_head_type_word_order_summary


class HeadTypeSummaryTest(unittest.TestCase):
    def test_summarizes_order_proportions_by_language_and_head_type(self) -> None:
        clusters = pd.DataFrame(
            [
                {"language": "Dutch", "head_type": "modal", "word_order": "1-2"},
                {"language": "Dutch", "head_type": "modal", "word_order": "2-1"},
                {"language": "Dutch", "head_type": "modal", "word_order": "2-1"},
                {"language": "Dutch", "head_type": "auxiliary", "word_order": "1-2"},
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
        self.assertNotIn("other", summary["head_type"].tolist())


if __name__ == "__main__":
    unittest.main()
