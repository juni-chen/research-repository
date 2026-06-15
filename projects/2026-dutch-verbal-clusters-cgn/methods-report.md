# Methods Report: Dutch and Flemish Verbal-Cluster Word Order in CGN

## 1. Research Objective

This project examines which factors are associated with word-order variation in
spoken Dutch verbal clusters. The analysis treats **Dutch** and **Flemish** as
two separate languages. Therefore, the model is not one pooled Dutch-Flemish
model. Instead, the same procedure is applied separately to:

```text
Dutch   = CGN material labeled Netherlands
Flemish = CGN material labeled Flanders
```

The main dependent variable is verbal-cluster order:

```text
1-2 vs 2-1
```

where `1` represents the head verb under the current fallback annotation
procedure and `2` represents the dependent verb in a two-verb cluster.

## 2. Corpus and Data Conversion

The corpus source is the annotation package of the Corpus Gesproken Nederlands
(CGN):

```text
data/raw/CGNAnn_2.0.3.zip
```

The converter reads compressed CGN POS-tag XML files directly from the archive:

```text
CGNAnn_2.0.3/data/annot/xml/tag/...
```

Each XML file contains utterance units `<pau>` and token elements `<pw>` or
punctuation elements `<pl>`. The conversion script creates a normalized token
table:

```text
data/processed/cgn_tokens.csv
```

Each row represents one token:

```text
utterance_id, token_index, token, lemma, pos, variety, language,
speaker_id, component, source_file
```

The mapping from CGN path labels to analysis languages is:

| CGN Path Label | Variety | Analysis Language |
| --- | --- | --- |
| `nl` | `Netherlands` | `Dutch` |
| `vl` | `Flanders` | `Flemish` |

The converted table contains:

| Language | Tokens |
| --- | ---: |
| Dutch | 6,388,126 |
| Flemish | 3,705,947 |
| Total | 10,094,073 |

## 3. Token and Utterance Representation

Let the corpus be a set of utterances:

\[
\mathcal{U} = \{u_1, u_2, \ldots, u_N\}
\]

Each utterance \(u\) is an ordered sequence of tokens:

\[
u = (t_{u,1}, t_{u,2}, \ldots, t_{u,n_u})
\]

Each token has attributes:

\[
t_{u,i} =
(w_{u,i}, \ell_{u,i}, p_{u,i}, r_{u,i}, s_u, c_u)
\]

where:

- \(w_{u,i}\) is the surface token;
- \(\ell_{u,i}\) is the lemma;
- \(p_{u,i}\) is the POS tag;
- \(r_{u,i}\) is the token position;
- \(s_u\) is the speaker id;
- \(c_u\) is the CGN component.

## 4. Verbal-Cluster Extraction

A token is treated as verb-like if its POS tag indicates a verbal item. In CGN
this is mainly:

\[
V(t_{u,i}) = 1
\quad \text{if} \quad
p_{u,i} \text{ starts with } \texttt{WW}
\]

The code also accepts broader labels such as `VERB` or `AUX` if they are
present in a different normalized table.

A verbal cluster is extracted as a maximal sequence containing at least two
verb-like tokens, allowing the Dutch infinitival marker `te` to occur inside the
cluster span. Formally, for a candidate span:

\[
C = (t_{u,a}, \ldots, t_{u,b})
\]

the set of verb positions is:

\[
I_C = \{i : a \leq i \leq b,\ V(t_{u,i}) = 1\}
\]

The span is retained as a verbal cluster if:

\[
|I_C| \geq 2
\]

and any non-verbal material inside the span is limited to bridge material such
as:

\[
w_{u,i} = \texttt{te}
\]

For each extracted cluster, the project records:

```text
surface_tokens
verb_tokens
verb_lemmas
verb_forms
cluster_length
has_te
has_modal
has_auxiliary
```

The full extraction produced:

| Language | Total Extracted Clusters |
| --- | ---: |
| Dutch | 83,583 |
| Flemish | 57,573 |
| Total | 141,156 |

## 5. Verb Form Identification

The project assigns a simplified verb form from the POS tag:

\[
F(t) =
\begin{cases}
\text{finite} & \text{if } p(t) \text{ contains } \texttt{pv} \\
\text{infinitive} & \text{if } p(t) \text{ contains } \texttt{inf} \\
\text{participle} & \text{if } p(t) \text{ contains } \texttt{vd} \\
\text{unknown} & \text{otherwise}
\end{cases}
\]

This allows the extraction procedure to identify two-verb clusters where one
verb is finite and the other is non-finite.

## 6. Word-Order Labeling

If an independent `verb_rank` annotation is available, the order label is the
surface sequence of those ranks:

\[
y(C) = r_1-r_2-\cdots-r_k
\]

where \(r_j\) is the hierarchical rank of the \(j\)-th verb in surface order.

For the present CGN conversion, no independent `verb_rank` column is available.
Therefore, the project uses a fallback rule for two-verb clusters:

\[
y(C) =
\begin{cases}
1\text{-}2 & \text{if the finite verb precedes the non-finite verb} \\
2\text{-}1 & \text{if the non-finite verb precedes the finite verb} \\
\text{unknown} & \text{otherwise}
\end{cases}
\]

Only clusters with:

\[
y(C) \in \{1\text{-}2, 2\text{-}1\}
\]

are used for the MaxEnt analysis.

Known-order clusters:

| Language | Known 1-2/2-1 Clusters |
| --- | ---: |
| Dutch | 49,149 |
| Flemish | 33,722 |

## 7. Head Type: Modal vs Auxiliary

The project also classifies the verbal-cluster head. If `verb_rank` is
available, the head is the verb with rank 1:

\[
h(C) = \arg\min_j r_j
\]

If `verb_rank` is unavailable, the fallback head is the unique finite verb:

\[
h(C) = j
\quad \text{such that} \quad
F(v_j) = \text{finite}
\]

provided that there is exactly one finite verb in the cluster.

The head lemma is then classified into four possible head types:

\[
T(h) =
\begin{cases}
\text{modal} & \ell_h \in M \\
\text{auxiliary} & \ell_h \in A \setminus M \\
\text{other} & \ell_h \notin A \\
\text{unknown} & \text{if no head is identifiable}
\end{cases}
\]

where the modal set is:

\[
M =
\{
\text{kunnen}, \text{moeten}, \text{mogen},
\text{willen}, \text{zullen}, \text{hoeven}
\}
\]

and the auxiliary set is:

\[
A =
\{
\text{hebben}, \text{zijn}, \text{worden}, \text{gaan},
\text{blijven}, \text{komen}, \text{laten}, \text{doen}
\}
\cup M
\]

For the modal/auxiliary summary, only clusters with:

\[
T(h) \in \{\text{modal}, \text{auxiliary}\}
\]

are counted.

## 8. Descriptive Proportion Estimates

For each language \(\lambda\) and word order \(o\), the empirical proportion is:

\[
\hat{p}(o \mid \lambda)
=
\frac{n_{\lambda,o}}
{\sum_{o' \in \{1\text{-}2,2\text{-}1\}} n_{\lambda,o'}}
\]

where \(n_{\lambda,o}\) is the number of known-order clusters of language
\(\lambda\) with order \(o\).

The observed word-order proportions are:

| Language | Order | Count | Proportion |
| --- | --- | ---: | ---: |
| Dutch | 1-2 | 34,751 | 0.7071 |
| Dutch | 2-1 | 14,398 | 0.2929 |
| Flemish | 1-2 | 22,697 | 0.6731 |
| Flemish | 2-1 | 11,025 | 0.3269 |

For head-type summaries, the conditional proportion is:

\[
\hat{p}(o \mid \lambda, h)
=
\frac{n_{\lambda,h,o}}
{\sum_{o' \in \{1\text{-}2,2\text{-}1\}} n_{\lambda,h,o'}}
\]

where \(h \in \{\text{modal}, \text{auxiliary}\}\).

Observed proportions by head type:

| Language | Head Type | 1-2 Count | 1-2 Proportion | 2-1 Count | 2-1 Proportion |
| --- | --- | ---: | ---: | ---: | ---: |
| Dutch | auxiliary | 17,651 | 0.6341 | 10,186 | 0.3659 |
| Dutch | modal | 15,107 | 0.9498 | 798 | 0.0502 |
| Flemish | auxiliary | 10,518 | 0.5460 | 8,747 | 0.4540 |
| Flemish | modal | 10,946 | 0.9587 | 471 | 0.0413 |

## 9. MaxEnt Model

The project uses a MaxEnt classifier, implemented as multinomial logistic
regression. Dutch and Flemish are modeled separately.

For each language \(\lambda\), define the dataset:

\[
\mathcal{D}_{\lambda}
=
\{(x_i, y_i) : \text{language}(x_i)=\lambda,\ y_i \neq \text{unknown}\}
\]

where:

\[
\lambda \in \{\text{Dutch}, \text{Flemish}\}
\]

and:

\[
y_i \in \{1\text{-}2,2\text{-}1\}
\]

The feature vector is a one-hot encoding of categorical feature-value pairs:

\[
\phi(x_i) \in \{0,1\}^{d}
\]

The default predictors are:

```text
cluster_length
has_te
has_modal
has_auxiliary
component
genre
register
speaker_region
```

`language` and `variety` are not predictors, because the models are trained
separately for Dutch and Flemish.

`finite_position` is also not used as a predictor. This is important because
the fallback word-order label is itself inferred from finite/non-finite order.
Including `finite_position` would make the model partly circular.

## 10. MaxEnt Probability Equation

Let there be \(K\) possible labels. In this experiment:

\[
K = 2
\]

with labels:

\[
\mathcal{Y}=\{1\text{-}2,2\text{-}1\}
\]

The model augments the feature vector with a bias term:

\[
\tilde{\phi}(x_i) =
(1, \phi_1(x_i), \ldots, \phi_d(x_i))
\]

For each class \(k\), the model has a parameter vector:

\[
\theta_k \in \mathbb{R}^{d+1}
\]

The MaxEnt probability of class \(k\) is:

\[
P_{\Theta}(y_i=k \mid x_i)
=
\frac{\exp(\theta_k^\top \tilde{\phi}(x_i))}
{\sum_{m=1}^{K} \exp(\theta_m^\top \tilde{\phi}(x_i))}
\]

This is the softmax form of a maximum entropy classifier.

## 11. Objective Function

For each language-specific dataset \(\mathcal{D}_{\lambda}\), the model
minimizes regularized negative log-likelihood:

\[
\mathcal{L}(\Theta)
=
-
\frac{1}{n}
\sum_{i=1}^{n}
\log P_{\Theta}(y_i \mid x_i)
+
\frac{\alpha}{2}
\sum_{k=1}^{K}
\sum_{j=1}^{d}
\theta_{j,k}^{2}
\]

where:

- \(n\) is the number of training examples;
- \(\alpha = 0.01\) is the L2 regularization strength;
- the bias parameter is not regularized;
- \(\Theta\) is the full parameter matrix.

The model is trained with batch gradient descent. If \(X_b\) is the design
matrix including the bias column, \(P\) is the matrix of predicted
probabilities, and \(Y\) is the one-hot target matrix, then the gradient is:

\[
\nabla_{\Theta}\mathcal{L}
=
\frac{1}{n} X_b^\top(P-Y)
+
\alpha \Theta_{\text{non-bias}}
\]

The update rule is:

\[
\Theta^{(t+1)}
=
\Theta^{(t)}
-
\eta \nabla_{\Theta}\mathcal{L}
\]

with:

\[
\eta = 0.15
\]

The implementation uses:

```text
iterations = 1500
seed = 7
test_size = 0.25
```

The train/test split is stratified by word-order label.

## 12. Evaluation Metrics

The predicted class is:

\[
\hat{y}_i
=
\arg\max_{k \in \mathcal{Y}}
P_{\Theta}(y_i=k \mid x_i)
\]

Accuracy is:

\[
\text{Accuracy}
=
\frac{1}{n}
\sum_{i=1}^{n}
\mathbf{1}[\hat{y}_i = y_i]
\]

Log loss is:

\[
\text{LogLoss}
=
-
\frac{1}{n}
\sum_{i=1}^{n}
\log P_{\Theta}(y_i \mid x_i)
\]

The final model summaries were:

| Language | Total Clusters | Known-Order Clusters | Accuracy | Log Loss |
| --- | ---: | ---: | ---: | ---: |
| Dutch | 83,583 | 49,149 | 0.7481 | 0.4770 |
| Flemish | 57,573 | 33,722 | 0.7249 | 0.4862 |

## 13. Step-by-Step Reproducible Workflow

Step 1: Place the CGN annotation archive locally:

```text
data/raw/CGNAnn_2.0.3.zip
```

Step 2: Convert the CGN annotation XML into the normalized token table:

```bash
python3 scripts/convert_cgn_annotations.py
```

Step 3: Run verbal-cluster extraction and separate Dutch/Flemish models:

```bash
python3 scripts/run_pipeline.py
```

Step 4: Inspect the main extracted cluster file:

```text
outputs/cgn-run/all_clusters.csv
```

Step 5: Inspect separate language results:

```text
outputs/cgn-run/dutch/
outputs/cgn-run/flemish/
```

Step 6: Inspect the modal/auxiliary head-type summaries:

```text
outputs/cgn-run/head_type_language_summary.csv
outputs/cgn-run/dutch/head_type_word_order_summary.csv
outputs/cgn-run/flemish/head_type_word_order_summary.csv
```

## 14. Methodological Limitations

First, the current CGN conversion does not provide independent hierarchical
`verb_rank` values. For two-verb clusters, `1-2` and `2-1` are therefore
assigned by finite/non-finite order. This is useful for a first corpus-scale
experiment, but a stronger syntactic analysis would use independently parsed or
manually annotated hierarchy.

Second, clusters longer than two verbs are usually labeled `unknown` unless
rank information is available. This means the current MaxEnt analysis focuses
on two-verb cluster variation.

Third, some metadata fields such as genre, register, and speaker region are
included as possible model features, but the current converter primarily
extracts component, speaker id, language, and token-level annotation from the
CGN tag XML. A future converter could enrich the table using CGN IMDI metadata.

Fourth, the current model is speaker-unaware. A future extension could use
speaker-level grouping, mixed-effects modeling, or speaker-stratified
cross-validation.

## 15. Summary of the Method

The project follows this analytical sequence:

```text
CGN annotation zip
→ normalized token table
→ utterance-level streaming verbal-cluster extraction
→ Dutch/Flemish split
→ descriptive 1-2/2-1 proportions
→ modal/auxiliary head-type proportions
→ separate MaxEnt models for Dutch and Flemish
```

The central statistical model is:

\[
P_{\Theta}(y=k \mid x)
=
\frac{\exp(\theta_k^\top \tilde{\phi}(x))}
{\sum_{m=1}^{K} \exp(\theta_m^\top \tilde{\phi}(x))}
\]

This allows the project to estimate how linguistic and corpus factors change
the probability of each verbal-cluster word order separately for Dutch and
Flemish.
