from __future__ import annotations

import sys
import tempfile
from pathlib import Path
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cgn_clusters.experiment import (
    ExperimentConfig,
    run_separate_language_experiments,
)


class SeparateLanguageExperimentTest(unittest.TestCase):
    def test_runs_same_experiment_for_dutch_and_flemish(self) -> None:
        clusters = pd.DataFrame(
            [
                language_cluster("Dutch", "1-2", "first", "conversation"),
                language_cluster("Dutch", "1-2", "first", "interview"),
                language_cluster("Dutch", "2-1", "last", "conversation"),
                language_cluster("Dutch", "2-1", "last", "interview"),
                language_cluster("Flemish", "1-2", "first", "conversation"),
                language_cluster("Flemish", "1-2", "first", "interview"),
                language_cluster("Flemish", "2-1", "last", "conversation"),
                language_cluster("Flemish", "2-1", "last", "interview"),
            ]
        )
        config = ExperimentConfig(iterations=20)

        with tempfile.TemporaryDirectory() as tmpdir:
            summary = run_separate_language_experiments(
                clusters,
                tmpdir,
                config=config,
            )

            self.assertEqual(summary["language"].tolist(), ["Dutch", "Flemish"])
            self.assertTrue((Path(tmpdir) / "dutch" / "metrics.json").exists())
            self.assertTrue((Path(tmpdir) / "flemish" / "metrics.json").exists())
            self.assertTrue((Path(tmpdir) / "dutch" / "coefficients.csv").exists())
            self.assertTrue((Path(tmpdir) / "flemish" / "coefficients.csv").exists())


def language_cluster(
    language: str,
    word_order: str,
    finite_position: str,
    genre: str,
) -> dict[str, object]:
    return {
        "cluster_id": f"{language}-{word_order}-{genre}",
        "language": language,
        "variety": "Netherlands" if language == "Dutch" else "Flanders",
        "word_order": word_order,
        "cluster_length": 2,
        "finite_position": finite_position,
        "has_te": False,
        "has_modal": True,
        "has_auxiliary": True,
        "component": "sample",
        "genre": genre,
        "register": "sample",
        "speaker_region": "sample",
    }


if __name__ == "__main__":
    unittest.main()
