# Overall Results Report: Dutch and Flemish Verbal-Cluster Word Order in CGN

## 1. Purpose of This Report

This report summarizes the final results of the CGN verbal-cluster experiment.
It reuses the methodological structure of `methods-report.md`, but focuses more
directly on the empirical findings and their interpretation.

The central research question is:

```text
Which factors are associated with 1-2 vs 2-1 word order in spoken Dutch and
spoken Flemish verbal clusters?
```

The analysis treats Dutch and Flemish as two separate languages:

```text
Dutch   = CGN material labeled Netherlands
Flemish = CGN material labeled Flanders
```

## 2. Corpus and Extraction Overview

The experiment uses the Corpus Gesproken Nederlands (CGN) annotation package.
The raw CGN annotation archive was converted into a normalized token table:

```text
data/processed/cgn_tokens.csv
```

The converted corpus contains:

| Language | Tokens |
| --- | ---: |
| Dutch | 6,388,126 |
| Flemish | 3,705,947 |
| Total | 10,094,073 |

The verbal-cluster extractor found the following diagnostic adjacent verb
sequences and target subordinate-clause clusters:

| Language | Total Extracted Clusters | Known Adjacent Sequences | Target Subordinate Clusters | Excluded Without Complementizer |
| --- | ---: | ---: | ---: | ---: |
| Dutch | 83,583 | 49,149 | 25,017 | 24,132 |
| Flemish | 57,573 | 33,722 | 17,773 | 15,949 |
| Total | 141,156 | 82,871 | 42,790 | 40,081 |

The actual MaxEnt experiment uses only the target subordinate-clause clusters:
known `1-2`/`2-1` clusters with a detected preceding subordinating
complementizer. Known-order adjacent verb sequences without a complementizer
are retained in `all_clusters.csv` only as diagnostic extraction output.

## 3. Word-Order Labeling

For two-verb clusters without independent `verb_rank` annotation, the project
uses the finite verb as the fallback head. The operational labels are:

\[
y(C) =
\begin{cases}
1\text{-}2 & \text{if the finite verb precedes the non-finite verb} \\
2\text{-}1 & \text{if the non-finite verb precedes the finite verb} \\
\text{unknown} & \text{otherwise}
\end{cases}
\]

This means that a cluster such as:

```text
kon pinnen
```

is labeled `1-2`, while:

```text
gelezen heeft
```

is labeled `2-1`.

## 4. Overall Word-Order Results

Across the target subordinate-clause clusters, both Dutch and Flemish favor
`1-2`. However, Flemish has a higher proportion of `2-1` than Dutch.

| Language | Order | Count | Proportion |
| --- | --- | ---: | ---: |
| Dutch | 1-2 | 18,521 | 0.7403 |
| Dutch | 2-1 | 6,496 | 0.2597 |
| Flemish | 1-2 | 12,196 | 0.6862 |
| Flemish | 2-1 | 5,577 | 0.3138 |

Main interpretation:

- Dutch: about 74.0% of target subordinate clusters are `1-2`.
- Flemish: about 68.6% of target subordinate clusters are `1-2`.
- Flemish therefore shows a stronger relative presence of `2-1` order.

## 5. Revised Head-Type Classification

The head classification was revised after inspection of the linguistic
categories. The final classification is:

| Head Type | Lemmas |
| --- | --- |
| `modal` | `kunnen`, `moeten`, `mogen`, `willen`, `zullen`, `hoeven` |
| `auxiliary` | `hebben`, `zijn`, `worden` |
| `semi_auxiliary` | `gaan`, `blijven`, `komen`, `laten`, `doen` |
| `other` | all remaining identifiable heads |
| `unknown` | no identifiable head |

The key correction is that `auxiliary` now contains only the core auxiliaries
`hebben`, `zijn`, and `worden`. Verbs such as `gaan`, `blijven`, `komen`,
`laten`, and `doen` are no longer counted as auxiliaries; they are treated as
semi-auxiliaries.

## 6. Results by Head Type

The head-type results show the most important contrast in the project.

| Language | Head Type | 1-2 Count | 1-2 Proportion | 2-1 Count | 2-1 Proportion |
| --- | --- | ---: | ---: | ---: | ---: |
| Dutch | auxiliary | 5,927 | 0.5171 | 5,534 | 0.4829 |
| Dutch | modal | 9,396 | 0.9815 | 177 | 0.0185 |
| Dutch | semi_auxiliary | 2,399 | 0.9520 | 121 | 0.0480 |
| Flemish | auxiliary | 2,901 | 0.3662 | 5,021 | 0.6338 |
| Flemish | modal | 6,872 | 0.9848 | 106 | 0.0152 |
| Flemish | semi_auxiliary | 1,841 | 0.9644 | 68 | 0.0356 |

Main interpretation:

- Modal heads strongly favor `1-2` in both Dutch and Flemish.
- Semi-auxiliary heads also strongly favor `1-2` in both languages.
- Core auxiliary heads are much more balanced.
- Flemish core auxiliary heads show more `2-1` than `1-2`.

This is the clearest Dutch-Flemish contrast:

```text
Dutch auxiliary heads:   51.71% 1-2, 48.29% 2-1
Flemish auxiliary heads: 36.62% 1-2, 63.38% 2-1
```

So, once the broad auxiliary category is split into core auxiliaries and
semi-auxiliaries and non-complementizer cases are excluded, the Flemish
auxiliary pattern becomes noticeably different from the Dutch one. Dutch core
auxiliary heads are close to balanced, while Flemish core auxiliary heads
strongly favor `2-1`.

## 7. Head-Type Distribution

Among target subordinate-clause clusters, the distribution of head types is:

| Language | Head Type | Count | Share of Target Clusters |
| --- | --- | ---: | ---: |
| Dutch | auxiliary | 11,461 | 0.4581 |
| Dutch | modal | 9,573 | 0.3827 |
| Dutch | semi_auxiliary | 2,520 | 0.1007 |
| Dutch | other | 1,463 | 0.0585 |
| Flemish | auxiliary | 7,922 | 0.4457 |
| Flemish | modal | 6,978 | 0.3926 |
| Flemish | semi_auxiliary | 1,909 | 0.1074 |
| Flemish | other | 964 | 0.0542 |

The two languages are similar in the overall distribution of head types. The
main difference is not how often core auxiliaries occur, but how those
auxiliary-headed clusters are ordered.

## 8. Complementizer-to-Cluster Length

The sentence-length feature measures the amount of non-verbal material between
a preceding subordinating complementizer and the verbal cluster. It is not the
total length of the CGN utterance.

\[
\text{sentence\_length\_type}(C) =
\begin{cases}
\text{short} & \text{if a complementizer is found and } B(C) \leq 4 \\
\text{long} & \text{if a complementizer is found and } B(C) > 4 \\
\text{no\_complementizer} & \text{if no preceding complementizer is found}
\end{cases}
\]

Here \(B(C)\) is the number of non-punctuation non-verbal words between the
nearest preceding subordinating complementizer, such as `dat`, `omdat`, `als`,
or `of`, and the beginning of the verbal cluster.

The threshold assumes that an essentially short subordinate clause contains a
subject NP and an object NP, with each NP approximated as a determiner plus
noun:

\[
2 \times (\text{determiner}+\text{noun}) = 4
\]

Observed results:

| Language | Length Type | 1-2 Count | 1-2 Proportion | 2-1 Count | 2-1 Proportion |
| --- | --- | ---: | ---: | ---: | ---: |
| Dutch | long | 9,645 | 0.7594 | 3,055 | 0.2406 |
| Dutch | short | 8,876 | 0.7206 | 3,441 | 0.2794 |
| Flemish | long | 5,583 | 0.7016 | 2,375 | 0.2984 |
| Flemish | short | 6,613 | 0.6738 | 3,202 | 0.3262 |

With the corrected definition, subordinate clauses with more than four
non-verbal words before the verbal cluster show a stronger `1-2` tendency than
shorter subordinate clauses.

## 9. Cluster Position

Cluster position was encoded as:

\[
\text{cluster\_position}(C) =
\begin{cases}
\text{final} & \text{if no non-punctuation material follows the cluster} \\
\text{nonfinal} & \text{if material follows the cluster}
\end{cases}
\]

Observed results:

| Language | Cluster Position | 1-2 Count | 1-2 Proportion | 2-1 Count | 2-1 Proportion |
| --- | --- | ---: | ---: | ---: | ---: |
| Dutch | final | 8,221 | 0.7667 | 2,501 | 0.2333 |
| Dutch | nonfinal | 10,300 | 0.7205 | 3,995 | 0.2795 |
| Flemish | final | 5,081 | 0.7111 | 2,064 | 0.2889 |
| Flemish | nonfinal | 7,115 | 0.6695 | 3,513 | 0.3305 |

Clusters at the end of the utterance show a stronger `1-2` tendency than
clusters followed by additional material. Nonfinal clusters have relatively
more `2-1` order in both languages.

## 10. MaxEnt Model

The project uses a MaxEnt classifier, implemented as multinomial logistic
regression. Dutch and Flemish are modeled separately.

The model estimates:

\[
P_{\Theta}(y=k \mid x)
=
\frac{\exp(\theta_k^\top \tilde{\phi}(x))}
{\sum_{m=1}^{K} \exp(\theta_m^\top \tilde{\phi}(x))}
\]

where:

- \(x\) is one verbal-cluster observation;
- \(y\) is the word-order label;
- \(k\) is one possible order, here `1-2` or `2-1`;
- \(\tilde{\phi}(x)\) is the feature vector with a bias term;
- \(\theta_k\) is the weight vector for class \(k\).

The final model results were:

| Language | Target Subordinate Clusters | Accuracy | Log Loss |
| --- | ---: | ---: | ---: |
| Dutch | 25,017 | 0.7864 | 0.4008 |
| Flemish | 17,773 | 0.8118 | 0.3761 |

The model performs above a simple majority-class baseline, especially for
Flemish. This indicates that the included features contain useful information
about word-order choice.

## 11. Coefficient Interpretation

For interpretation, it is useful to compare each feature's weight for `1-2`
against its weight for `2-1`:

\[
\Delta_j =
\theta_{j,1\text{-}2}
-
\theta_{j,2\text{-}1}
\]

If \(\Delta_j > 0\), the feature favors `1-2` relative to `2-1`. If
\(\Delta_j < 0\), it favors `2-1` relative to `1-2`.

Strongest Dutch predictors toward `1-2`:

| Feature | Delta Toward 1-2 |
| --- | ---: |
| `has_modal=True` | 1.3915 |
| `component=comp-k` | 1.0645 |
| `<bias>` | 0.8748 |
| `has_te=True` | 0.6791 |
| `has_semi_auxiliary=True` | 0.6423 |
| `has_auxiliary=False` | 0.5296 |
| `component=comp-o` | 0.2998 |

Strongest Flemish predictors toward `1-2`:

| Feature | Delta Toward 1-2 |
| --- | ---: |
| `has_modal=True` | 1.4988 |
| `component=comp-o` | 0.9045 |
| `has_auxiliary=False` | 0.8700 |
| `<bias>` | 0.8529 |
| `has_semi_auxiliary=True` | 0.7089 |
| `has_te=True` | 0.6084 |
| `component=comp-k` | 0.2884 |

Main interpretation:

- Modal clusters strongly favor `1-2` in both languages.
- Clusters containing `te` also favor `1-2`.
- Semi-auxiliary clusters favor `1-2`.
- The corrected complementizer-to-cluster length feature is weaker than head
  type, but longer subordinate pre-cluster spans show a somewhat stronger
  `1-2` tendency than shorter ones.
- Final cluster position favors `1-2`, especially in Dutch.

Because this is an observational corpus model, coefficients should be
interpreted as associations rather than causal effects.

## 12. Main Findings

The final results support five main conclusions.

1. Both Dutch and Flemish prefer `1-2` overall.

2. Flemish has a higher overall proportion of `2-1` than Dutch.

3. Head type matters strongly. Modal and semi-auxiliary heads overwhelmingly
favor `1-2`, while core auxiliary heads are much more balanced.

4. The strongest Dutch-Flemish difference appears with core auxiliary heads:
Dutch auxiliary-headed clusters still favor `1-2`, but Flemish
auxiliary-headed clusters strongly favor `2-1`.

5. Under the corrected definition, longer subordinate pre-cluster spans and
utterance-final clusters tend to show more `1-2` order than shorter
subordinate spans or nonfinal contexts.

## 13. Limitations

The main limitation is that `verb_rank` is not independently available in the
current converted CGN table. Therefore, two-verb `1-2` and `2-1` labels are
currently inferred from finite/non-finite order. This is workable for a first
large-scale experiment, but a stronger syntactic analysis would require
independent hierarchy annotation or parsing.

Second, the corrected sentence-length feature depends on automatic detection
of a preceding subordinating complementizer. Some subordinate clauses may be
missed if the complementizer is absent, disfluent, or tagged differently, and
the excluded no-complementizer diagnostic cases may mix true main-clause
adjacency with undetected subordinate contexts.

Third, the model is not speaker-aware. Future work should consider
speaker-stratified evaluation or mixed-effects modeling, because some speakers
or components may contribute many more clusters than others.

Finally, the head-type classification is lemma-based. This is transparent and
reproducible, but it does not distinguish every possible lexical vs auxiliary
use of a verb in context.

## 14. Output Files

The relevant generated outputs are:

```text
outputs/cgn-run/language_summary.csv
outputs/cgn-run/head_type_language_summary.csv
outputs/cgn-run/experiment_summary.csv
outputs/cgn-run/dutch/coefficients.csv
outputs/cgn-run/flemish/coefficients.csv
outputs/cgn-run/dutch/head_type_word_order_summary.csv
outputs/cgn-run/flemish/head_type_word_order_summary.csv
```

The raw CGN archive and converted corpus table are not included in the
repository, because CGN data access is subject to corpus licensing conditions.
