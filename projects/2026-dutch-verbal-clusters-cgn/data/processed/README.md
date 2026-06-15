# Processed Real CGN Data

The converter writes the normalized real CGN token table here as:

```text
cgn_tokens.csv
```

Create it from `data/raw/CGNAnn_2.0.3.zip` with:

```bash
python3 scripts/convert_cgn_annotations.py
```

The corpus table is ignored by Git so licensed CGN data is not accidentally
committed.
