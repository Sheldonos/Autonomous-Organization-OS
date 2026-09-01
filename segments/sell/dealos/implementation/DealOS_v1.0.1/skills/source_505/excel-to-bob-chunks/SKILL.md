---
name: excel-to-bob-chunks
description: >
  Use when a user wants to convert a large Excel (.xlsx/.xls) file into token-aware
  chunked Markdown files suitable for loading into IBM Bob's 200k context window.
  Triggers on phrases like "chunk this Excel file", "split my xlsx for Bob",
  "convert Excel to Markdown chunks", "my Excel file is too large for Bob",
  "prepare Excel data for Bob workspace", or any request to break up spreadsheet
  data so it fits within a context window.
---

# Excel to Bob Chunks

Convert a large Excel file into token-aware, self-contained Markdown chunk files
ready for sequential loading into IBM Bob's 200k context window.

## Step 1 — Check dependencies

Run the following to ensure all Python dependencies are installed:

```bash
pip install pandas tiktoken tabulate openpyxl
```

If `pip` is unavailable, instruct the user to install the packages manually before continuing.

## Step 2 — Collect inputs

Ask the user (using `ask_followup_question`) for any missing details:

- **Input file path** — the `.xlsx` or `.xls` file to process (required)
- **Output directory** — where to write chunks (default: `./bob_workspace_chunks`)
- **Max tokens per chunk** — default `150000` (leaves 50k headroom in a 200k window)
- **Sheet name or index** — default `0` (first sheet)
- **Include row index?** — default yes; pass `--no_index` to omit

Only ask if the user has not already provided the values.

## Step 3 — Run the chunker

Use `execute_command` to invoke the bundled script. Construct the command from the
user's inputs, for example:

```bash
python3 ~/.bob/skills/excel-to-bob-chunks/excel_to_bob_chunks.py \
  "<input_file>" \
  --output_dir "<output_dir>" \
  --max_tokens <max_tokens> \
  --sheet_name <sheet>
```

Append `--no_index` if the user chose to omit the row index column.

## Step 4 — Report results

After the command completes, summarise the output to the user:

- Number of chunks produced
- Output directory path
- Token limit applied per chunk
- Total rows and columns processed

Remind the user to load each `data_chunk_NNN.md` file into Bob **sequentially** — every
chunk contains the full column header so it is self-contained in any context window.

## Step 5 — Troubleshoot if needed

Common errors and fixes:

| Error | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install pandas tiktoken tabulate openpyxl` |
| Header alone exceeds token limit | Use `--max_tokens` with a higher value, or filter columns before chunking |
| Sheet not found | Check `--sheet_name` matches an actual tab name or use `0` for the first sheet |
| File not found | Confirm the absolute path to the `.xlsx` file |
