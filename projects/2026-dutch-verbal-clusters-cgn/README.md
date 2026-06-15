---
title: Dutch verbal clusters in CGN
type: project
status: seed
tags: [Dutch, Flemish, syntax, verbal-clusters, corpus, MaxEnt]
languages: [Dutch]
---

# Dutch And Flemish Verbal Clusters in CGN

This project studies which factors favor different word orders in Dutch verbal
clusters in the Corpus Gesproken Nederlands (CGN). For this experiment,
**Dutch** and **Flemish** are treated as two separate languages, not as one
pooled language with regional variation.

The first coding target is a reproducible pipeline:

1. read a CGN-derived token table;
2. extract verbal-cluster tokens;
3. assign a surface word-order label such as `1-2` or `2-1`;
4. split the extracted clusters into Dutch and Flemish;
5. run the same MaxEnt-style experiment separately for each language;
6. produce two independent result sets.

## Why CGN

CGN is appropriate here because it is spoken language data and was designed to
cover both the Netherlands and Flanders. In this project the CGN geographic
labels are used to assign the experimental language:

| CGN label | Experimental language |
| --- | --- |
| `Netherlands` | `Dutch` |
| `Flanders` | `Flemish` |

The tradeoff is that CGN exports may arrive in different formats. This project
therefore begins from a normalized token table. A later step can add a specific
converter for the exact CGN export format you obtain.

## Required Input

Create a CSV or TSV file with one row per token. Required columns:

| Column | Meaning |
| --- | --- |
| `utterance_id` | CGN utterance, sentence, or annotation-unit id. |
| `token_index` | Token order inside the utterance. |
| `token` | Surface token. |
| `lemma` | Lemma. |
| `pos` | POS tag, preferably CGN-style or UD-style. |
| `variety` | `Netherlands` or `Flanders`. |

Recommended columns:

| Column | Meaning |
| --- | --- |
| `verb_form` | `finite`, `infinitive`, `participle`, etc. |
| `verb_rank` | Hierarchical verb rank used to define orders like `1-2`. |
| `speaker_id` | Speaker id. |
| `speaker_region` | Region or province if available. |
| `component` | CGN component. |
| `genre` | Conversation, interview, broadcast, etc. |
| `register` | Informal, formal, broadcast, etc. |

If a `language` column is absent, the code derives it from `variety`.
`Netherlands` becomes `Dutch`; `Flanders` becomes `Flemish`.

`verb_rank` is important. If it is absent, the code can infer simple two-verb
orders from finite vs non-finite forms, but a real analysis should derive or
annotate hierarchy carefully.

## Run The Real CGN Experiment

From this project folder:

```bash
python3 scripts/run_pipeline.py
```

The default extraction path streams through `data/processed/cgn_tokens.csv`,
which is important for the full CGN table. The older in-memory extractor is
still available for debugging with `--use-pandas-extraction`, but it is not
recommended for the full corpus.

By default, the script expects the normalized real corpus table here:

```text
data/processed/cgn_tokens.csv
```

and writes the real experiment outputs here:

```text
outputs/cgn-run/
```

You can still provide another real CGN-derived table explicitly:

```bash
python3 scripts/run_pipeline.py \
  --tokens path/to/your/cgn_tokens.csv \
  --out outputs/cgn-run
```

Outputs:

| File | Meaning |
| --- | --- |
| `schema_report.json` | Columns, row count, and detected languages in the input table. |
| `all_clusters.csv` | All extracted verbal-cluster observations. |
| `language_summary.csv` | Counts of word orders by language. |
| `head_type_language_summary.csv` | `1-2`/`2-1` proportions by language and modal/auxiliary head type. |
| `experiment_summary.csv` | Compact overview of both model runs. |
| `dutch/clusters.csv` | Dutch-only cluster observations. |
| `dutch/metrics.json` | Dutch-only model evaluation. |
| `dutch/coefficients.csv` | Dutch-only MaxEnt feature weights. |
| `dutch/head_type_word_order_summary.csv` | Dutch-only `1-2`/`2-1` proportions by modal/auxiliary head type. |
| `flemish/clusters.csv` | Flemish-only cluster observations. |
| `flemish/metrics.json` | Flemish-only model evaluation. |
| `flemish/coefficients.csv` | Flemish-only MaxEnt feature weights. |
| `flemish/head_type_word_order_summary.csv` | Flemish-only `1-2`/`2-1` proportions by modal/auxiliary head type. |

## Real CGN Workflow

1. Obtain CGN data through the official access route.
2. Place `CGNAnn_2.0.3.zip` at:

```text
data/raw/CGNAnn_2.0.3.zip
```

3. Convert the CGN annotation XML into the normalized token table:

```bash
python3 scripts/convert_cgn_annotations.py
```

This reads the zip archive directly and writes:

```text
data/processed/cgn_tokens.csv
```

4. Run the experiment:

```bash
python3 scripts/run_pipeline.py
```

## Modeling Design

This project uses multinomial logistic regression as a MaxEnt model. The same
function is applied twice:

```text
run_language_experiment(clusters, "Dutch", ...)
run_language_experiment(clusters, "Flemish", ...)
```

Each model predicts `word_order` from factors such as:

- `cluster_length`
- `has_te`
- `has_modal`
- `has_auxiliary`
- `component`
- `genre`
- `speaker_region`

Because Dutch and Flemish are modeled separately, `language` and `variety` are
not used as predictors inside the individual models. The output is two sets of
weights, one for Dutch and one for Flemish.

`finite_position` is written to the extracted cluster table for inspection, but
it is not used as a default predictor because the current fallback `word_order`
label is inferred from finite/non-finite order when no independent `verb_rank`
annotation is available.

The extracted cluster table also includes `head_lemma`, `head_pos`,
`head_position`, and `head_type`. Head type is classified as `modal`,
`auxiliary`, `other`, or `unknown`. The modal/auxiliary order summaries use
only `modal` and non-modal `auxiliary` heads.

## Current Limits

This is a first experimental scaffold. Before using the results in a paper, the
project needs:

- a documented CGN conversion step for your exact data source;
- manual checking of verbal-cluster extraction;
- a principled definition of `verb_rank`;
- mixed-effects or speaker-aware validation if speaker imbalance is large;
- comparison of the two independently trained models.
