---
name: ibm-modes-to-skills
description: >-
  Converts all IBM BOB selling modes (ibm-pre-*, ibm-eng-*, ibm-qua-*, ibm-des-*,
  ibm-pro-*, ibm-neg-*, ibm-clo-*, ibm-dep-*, ibm-ado-*, ibm-exp-*, ibm-met-*,
  ibm-fw-*, ibm-sdr-workflow-*, ibm-atl-*) into standalone SKILL.md files under
  ~/.bob/skills/, preserving every field — roleDefinition, customInstructions,
  whenToUse, and groups — without any dilution. Use when asked to "convert IBM
  modes to skills", "create skills from IBM modes", or "run the IBM modes
  conversion script".
---

# IBM Modes → Skills Converter

This skill converts every IBM BOB selling mode defined in
`~/.bob/settings/custom_modes.yaml` into a fully-faithful `SKILL.md` file so
that each specialist cell is independently invocable as a Bob skill — either
via `/<slug>` or via Bob's auto-invocation when the `description` trigger
matches the user's request.

**No detail is lost.** The `roleDefinition`, `customInstructions`, `whenToUse`,
`groups`, `name`, and `slug` fields are all written verbatim into the output
`SKILL.md`. The skill description (which drives auto-invocation) is derived
directly from `whenToUse`.

---

## Prerequisites

The script requires [js-yaml](https://www.npmjs.com/package/js-yaml). Check
and install it before running.

```bash
node -e "require('js-yaml')" 2>/dev/null && echo "js-yaml present" || npm install -g js-yaml
```

---

## Step 1 — Verify the source file exists

```bash
ls -lh ~/.bob/settings/custom_modes.yaml
```

If the file is missing, stop and ask the user to confirm the correct path.

---

## Step 2 — Dry-run to preview what will be written

Always dry-run first so the user can confirm scope before touching disk.

```bash
node ~/.bob/skills/ibm-modes-to-skills/convert-ibm-modes.js --dry-run
```

Read the output. It will list every `ibm-*` mode slug and the target path.
Confirm with the user before proceeding.

**Optional — convert a single lane only (e.g. ATL):**

```bash
node ~/.bob/skills/ibm-modes-to-skills/convert-ibm-modes.js --dry-run --filter ibm-atl
```

---

## Step 3 — Run the full conversion

```bash
node ~/.bob/skills/ibm-modes-to-skills/convert-ibm-modes.js
```

The script will:

1. Load `~/.bob/settings/custom_modes.yaml`
2. Filter every mode whose `slug` starts with `ibm-`
3. For each mode, create `~/.bob/skills/<slug>/SKILL.md` containing:
   - A YAML frontmatter block with `name` and `description`
   - `## Role Definition` — the full `roleDefinition` verbatim
   - `## When To Use` — the full `whenToUse` verbatim
   - `## Custom Instructions` — the full `customInstructions` verbatim
   - `## Tool Groups` — the `groups` array serialised to YAML
   - `## Operating Protocol` — a fixed activation preamble that instructs
     Bob to adopt the specialist identity immediately
4. Print a summary of written / skipped / errors

---

## Step 4 — Validate a sample output

Pick any slug from the dry-run output and read its generated SKILL.md to
confirm nothing was truncated:

```bash
# Example: check ibm-atl-007
cat ~/.bob/skills/ibm-atl-007/SKILL.md | head -60
wc -l ~/.bob/skills/ibm-atl-007/SKILL.md
```

A correct SKILL.md for an IBM selling mode will be **350–500 lines**. If it is
shorter than 100 lines the roleDefinition was not written correctly — re-run
with the `--filter` flag on that slug to debug.

---

## Step 5 — Spot-check auto-invocation description

Open any generated `SKILL.md` and verify the `description:` field in the
frontmatter contains enough trigger phrases from `whenToUse` that Bob would
recognise the correct context for auto-invocation.

```bash
head -10 ~/.bob/skills/ibm-pre-001/SKILL.md
```

---

## Step 6 — Activate in the next Bob task

Skills become available in the **next new Bob task** (conversation). To invoke
any converted skill:

- **Explicit invocation:** type `/<slug>` e.g. `/ibm-pre-001`
- **Auto-invocation:** Bob activates the skill when the user's request matches
  the `description` trigger (e.g. "run company research on Accenture" →
  Bob activates `ibm-pre-001`)

---

## Filtering by lane

To convert only one lane at a time, pass `--filter` with the lane prefix:

| Lane | Filter flag |
|------|-------------|
| Pre-sales intelligence | `--filter ibm-pre` |
| Seller engagement | `--filter ibm-eng` |
| Qualification & discovery | `--filter ibm-qua` |
| Solution design & value | `--filter ibm-des` |
| Proposal & business case | `--filter ibm-pro` |
| Negotiation & objection handling | `--filter ibm-neg` |
| Closing coordination | `--filter ibm-clo` |
| Deployment & onboarding handoff | `--filter ibm-dep` |
| Adoption & value realization | `--filter ibm-ado` |
| Expansion & renewal | `--filter ibm-exp` |
| Sales method & quality | `--filter ibm-met` |
| Framework design | `--filter ibm-fw` |
| SDR workflow orchestration | `--filter ibm-sdr` |
| Account team leadership | `--filter ibm-atl` |

---

## Troubleshooting

**`Cannot find module 'js-yaml'`**
Run `npm install -g js-yaml` and re-run the script.

**A SKILL.md is shorter than expected**
The YAML block scalar in the source may have been parsed as `null`. Open the
source YAML around that mode's lines, verify the block scalar marker (`>-`)
is followed by indented content, and re-run.

**Skill does not appear in a new task**
Check the `name:` field in the frontmatter matches the regex
`^[a-z0-9]+(-[a-z0-9]+)*$`. IBM mode slugs (e.g. `ibm-pre-001`) already
satisfy this constraint.

**Script exits with "customModes array not found"**
The file at `SOURCE` may be a different YAML variant. Run:
```bash
head -5 ~/.bob/settings/custom_modes.yaml
```
It must begin with `customModes:`. Adjust the `SOURCE` constant in
`convert-ibm-modes.js` line 42 if needed.
