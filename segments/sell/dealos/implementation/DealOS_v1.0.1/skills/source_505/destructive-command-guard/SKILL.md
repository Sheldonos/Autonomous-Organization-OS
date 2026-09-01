---
name: destructive-command-guard
description: Use when Bob is about to run any shell command that could cause irreversible data loss or system damage — file deletion, database drops, disk wipes, or destructive git operations. Activates automatically before executing commands matching high-risk patterns. Also activates when the user says "check this command", "is this safe to run", or "guard my shell commands".
---

# Destructive Command Guard

Intercepts high-risk shell commands before they execute, surfaces the risk to the user, and requires explicit typed confirmation before proceeding. If the user does not confirm, the command is **not run**.

---

## Step 1 — Classify the Command

Before running any shell command with `execute_command`, scan the command string against the pattern table below.

| Category | Patterns to match (case-insensitive) |
|---|---|
| **File deletion** | `rm -rf`, `rm -r`, `rmdir`, `unlink`, `shred` |
| **Database drop / truncate** | `DROP TABLE`, `DROP DATABASE`, `DROP SCHEMA`, `TRUNCATE`, `DELETE FROM` without a `WHERE` clause |
| **Git destructive ops** | `git reset --hard`, `git push --force`, `git push -f`, `git clean -f`, `git clean -fd`, `git clean -fx` |
| **Disk wipe / format** | `mkfs`, `dd if=`, `diskutil eraseDisk`, `format`, `fdisk` |
| **Dangerous redirects** | Any command ending in `> /dev/` or overwriting a file with `>` (not `>>`) on a path outside the current project directory |

If **no pattern matches** → proceed with `execute_command` normally, no gate needed.

If **one or more patterns match** → go to Step 2.

---

## Step 2 — Surface the Risk

**Do not run the command yet.** Instead, present this block to the user:

```
⚠️  DESTRUCTIVE COMMAND DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Command:  <exact command string>
Category: <matched category from Step 1>
Risk:     <one-sentence plain-language description of what could be lost or broken>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type  confirm  to proceed, or anything else to cancel.
```

**Risk descriptions by category:**

| Category | Risk sentence |
|---|---|
| File deletion | "This will permanently delete files or directories — no Trash, no undo." |
| Database drop / truncate | "This will permanently destroy database objects or all rows in a table." |
| Git destructive ops | "This will rewrite or discard commits and cannot be undone without a backup ref." |
| Disk wipe / format | "This will erase the entire disk or partition — all data will be unrecoverable." |
| Dangerous redirects | "This will overwrite a file outside the current project — existing content will be lost." |

---

## Step 3 — Wait for Confirmation

Use `ask_followup_question` to prompt the user. Do **not** proceed until a response is received.

- If the user types exactly `confirm` (case-insensitive) → go to Step 4.
- If the user types anything else, or dismisses → go to Step 5 (cancel).

---

## Step 4 — Execute with Logging

Run the command using `execute_command`. After it completes, append a one-line log entry to `~/.bob/command-guard-log.md` (create the file if it does not exist):

```
| <ISO timestamp> | <command> | CONFIRMED | <exit code> |
```

Use `execute_command` to append:
```bash
echo "| $(date -u +"%Y-%m-%dT%H:%M:%SZ") | <command> | CONFIRMED | <exit_code> |" \
  >> ~/.bob/command-guard-log.md
```

Report the result to the user normally.

---

## Step 5 — Cancel and Explain

If the user did not confirm, **do not run the command**. Tell the user:

```
🛑 Command cancelled — not executed.
```

Then offer alternatives if applicable:
- For `rm -rf`: suggest `mv` to a temp directory instead of deleting
- For `git reset --hard`: suggest `git stash` or creating a backup branch first
- For `DROP TABLE`: suggest `RENAME TABLE ... TO _backup_...` before dropping
- For disk operations: suggest verifying the target device with `lsblk` or `diskutil list` first

---

## Notes

- This skill is a **pre-execution gate**, not a post-execution rollback. It cannot undo a command that already ran.
- If Bob is chaining multiple commands (e.g., a pipeline script), classify **each individual command** in the chain separately.
- For commands that are destructive only depending on flags (e.g., `rm` without `-r` vs. `rm -rf`), only gate the dangerous variant.
- The log at `~/.bob/command-guard-log.md` is append-only — do not truncate or delete it during normal operation.
