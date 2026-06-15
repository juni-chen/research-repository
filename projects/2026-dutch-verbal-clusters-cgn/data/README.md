# Data

Do not commit the full CGN corpus here unless your license explicitly allows
it. Keep raw corpus files outside version control or in a private local folder.

Expected working layout:

```text
data/
  raw/          # optional local CGN exports, not committed
  processed/    # normalized token tables used by the scripts
  sample/       # tiny artificial data for pipeline testing
```

The normalized file should contain one token per row. The separate Dutch and
Flemish analyses depend on the `variety` column, which must contain either
`Netherlands` or `Flanders`. The code derives the experimental `language`
column automatically:

| `variety` | `language` |
| --- | --- |
| `Netherlands` | `Dutch` |
| `Flanders` | `Flemish` |

See the project `README.md` for the complete input schema.
