---
name: markdown-chunker
description: Splits a large Markdown file (like the IBM Data Driven Sales Play Heat Map, territory data exports, or any large .md document) into numbered chunk files that fit safely inside a context window. Use when a user references a .md file that is too large to process in one shot, asks to "chunk a markdown", wants to break down a large file before analysis, or needs to split any large table/data markdown into sequentially-numbered micro-chunks without losing content. Produces YAML-front-matter chunk files matching the existing `chunk_NNNN_rows_XXXXXX-YYYYYY.md` naming convention used in data_lake/02_territory_data/.
---

# Markdown Chunker

Splits a large `.md` file into sequentially-numbered chunk files, each small enough for a single context window pass. Mirrors the naming and structure already used in `data_lake/02_territory_data/`.

## When to Use

- Input file is larger than ~500 KB or ~1 000 lines and must be processed section-by-section.
- User says "chunk this file", "break it down", "split the markdown", or asks to process a heat map / territory export.
- Preparing a large data file so downstream agent modes can read one chunk per turn.

## Key Facts from the Existing Pattern

| Property | Value |
|---|---|
| Naming convention | `chunk_NNNN_rows_XXXXXX-YYYYYY.md` (4-digit chunk, 6-digit row range) |
| Typical chunk size | ~128 KB / ~200 data rows per chunk |
| Default max rows/chunk | **200 rows** (configurable via `--rows-per-chunk`) |
| Default max bytes/chunk | **150 000 bytes** — whichever limit is hit first |
| Front matter | YAML block with `source`, `type`, `role`, `tags`, `converted` |
| Chunk header | `# Micro-Markdown Chunk: <source> / Chunk N of T` |
| Metadata table | `Field | Value` table (source, worksheet, range, rows, SHA-256, prev, next) |
| Content block | Fenced ` ```tsv ``` ` for tab-separated data OR raw markdown table rows |

## Workflow

### Step 1 — Identify the input

Ask the user to confirm (or detect from context):
- **File path** of the large `.md` to split.
- **Output directory** (default: same directory as input).
- **Rows per chunk** (default: 200; override if user specifies).
- **Source label** (e.g. workbook name, sheet name) — used in chunk headers.

### Step 2 — Run the script

```bash
python /Users/sheldonibm/.bob/skills/markdown-chunker/scripts/chunk_markdown.py \
  --input  "<path/to/large_file.md>" \
  --output "<output_dir>" \
  --rows-per-chunk 200 \
  --source-label  "SheetName or file label" \
  --role  "SE"
```

All flags except `--input` are optional and fall back to defaults.

### Step 3 — Verify output

After the script runs it prints a manifest table. Confirm:
- Total chunks created equals `ceil(data_rows / rows_per_chunk)`.
- Each chunk file opens cleanly and shows correct YAML front matter.
- `next` / `previous` links chain correctly.

### Step 4 — Update INDEX / MANIFEST if present

If the output directory contains an `INDEX.md` or `MANIFEST.md`, append each new chunk entry:

```markdown
| chunk_NNNN_rows_XXXXXX-YYYYYY.md | rows XXXXXX–YYYYYY | <source-label> |
```

## Script Reference

Script: `/Users/sheldonibm/.bob/skills/markdown-chunker/scripts/chunk_markdown.py`

Key options:

| Flag | Default | Description |
|---|---|---|
| `--input` | *(required)* | Path to the source `.md` file |
| `--output` | Same dir as input | Directory to write chunk files |
| `--rows-per-chunk` | `200` | Max data rows per chunk |
| `--max-bytes` | `25000000` | Hard byte ceiling per chunk (rows-per-chunk governs for wide tables) |
| `--source-label` | Filename stem | Label used in chunk header / metadata table |
| `--role` | `SE` | YAML `role` tag written into each chunk |
| `--sheet` | `""` | Worksheet name (optional metadata) |

## Naming Formula

```
chunk_{NNNN}_rows_{RSTART:06d}-{REND:06d}.md
```

- `NNNN` — 4-digit chunk sequence number, zero-padded (0001, 0002, …)
- `RSTART` / `REND` — 6-digit first and last row numbers in that chunk (1-based, data rows only, header row excluded)

## Wide-Table Files (Heat Map, Territory Data)

The IBM heat map has rows of ~98 KB each (hundreds of columns). For such files the `--max-bytes` ceiling is irrelevant — `--rows-per-chunk` is the only limit that matters. The default `--max-bytes` of 25 MB is large enough to never interfere with row grouping.

## Error Cases

| Symptom | Fix |
|---|---|
| `No data rows found` | File has only header/metadata lines; check that data lines don't start with `#` or `>` |
| Chunks much larger than expected | Wide table rows; reduce `--rows-per-chunk` to 50–100 |
| 1 row per chunk | Old `--max-bytes 150000` may have been used; omit the flag to use default 25 MB |
| Chunk files written but SHA mismatch | Re-run with `--no-sha` flag if SHA is not needed |
