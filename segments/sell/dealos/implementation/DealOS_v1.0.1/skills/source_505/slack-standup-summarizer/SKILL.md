---
name: slack-standup-summarizer
description: Use when the user wants to generate a Slack-ready daily standup summary from a meeting transcript, recording link, or follow-up notes. Triggers on phrases like "summarize the standup", "generate a standup summary", "create a standup recap", "write up the standup", or any request to turn a transcript or meeting notes into a Slack standup post.
---

# Slack Standup Summarizer

Generate a Slack-ready daily standup summary from a meeting transcript and optional follow-up material. Follow every step below in order.

## Step 1 — Gather inputs

If the user has not yet provided the inputs below, ask for them using `ask_followup_question`:

- **Project name** — the name of the project this standup is for (e.g. "Qisbob")
- **Date** — the date of the standup (YYYY.MM.DD)
- **Transcript** — raw transcript text, or a link to a transcript document
- **Recording link** *(optional)* — link to the meeting recording
- **Transcript link** *(optional)* — direct link to the transcript document
- **Follow-up material** *(optional)* — any post-meeting notes, screenshots, or Slack posts shared after the standup

If the user has already pasted all of this in their message, skip asking and proceed directly to Step 2.

## Step 2 — Normalize project name variants

Before processing, scan the transcript for any phonetic or transcription mis-spellings of the project name (e.g. for "Qisbob": "Kiss Bob", "Kids Bob", "KissBob", "KizBob", "KizVab"). Silently replace every occurrence with the correct project name in your output. Never let a mis-transcription appear in the summary.

## Step 3 — Determine whether follow-up material is present

If the user provided post-meeting follow-ups (screenshots, Slack posts, new artifacts shared after the standup), you will add an optional **📋 Post-standup** section in Step 4. If not, omit it entirely.

## Step 4 — Produce the summary

Output the summary using exactly the structure below. Use plain Markdown that renders cleanly in Slack (`**bold**`, `- bullets`, `#` headings). Do not add inline citations, footnotes, or reference tags.

---

```
# [Project Name] Daily Standup — YYYY.MM.DD

*TL;DR: [One sentence capturing the most important outcome, decision, or direction from the meeting.]*

**📼 Resources**
- Recording: [link if provided; otherwise "[link to be added]"]
- Transcript: [link if provided; otherwise "[link to be added]"]

**👥 Attendees**
- [Full Name]
- [Full Name]
(Bulleted, alphabetical by first name. Include only people who actually spoke or were clearly present per the transcript.)

**🚀 Progress & decisions**
- [Concise bullet. Attribute progress and decisions to specific people. Bold key terms or decision headlines where it helps skimmability.]

**📋 Post-standup: [short label]**
(Include ONLY if post-meeting follow-up material was provided. Capture it as bullets here, between "Progress & decisions" and "Blockers / friction". Omit this section entirely if no follow-up material was provided.)

**⚠️ Blockers / friction**
- [Concise bullet on blockers, dependencies, unclear ownership, tool issues, or open questions. Write "None flagged" if genuinely empty. Do not pad.]

**➡️ Next steps**
- [Owner] — [action] — [by when, if stated]
```

---

## Hard rules — apply to every output

1. **No inline citations, footnotes, or reference tags.** Slack does not render them cleanly.
2. **Be concise.** Attribute specific progress, decisions, and next steps to specific people by name.
3. **Focus on what actually moved** — progress and decisions, not just "topics discussed."
4. **Include small friction** (dependencies, unclear ownership, tool weirdness), not only hard blockers. Use "None flagged" if genuinely empty; do not pad.
5. **If a section has nothing to report**, write "None flagged" or omit the bullet. Do not invent content.
6. **Attendees** must be alphabetical by first name. The user will convert names to Slack handles manually.
7. **Do not proactively regenerate prior outputs**, offer templates, or suggest next actions unless explicitly asked.
8. **If follow-up material is included**, add a short italicized note directly below the TL;DR clarifying that the recap covers both the meeting discussion and post-meeting follow-ups.

## Style notes

- Professional but approachable. No jargon padding, no AI-tell phrases.
- Prefer concrete verbs and specific artifacts (e.g., "Rynne stood up an MCP server that connects to…" rather than "the team discussed servers").
- Keep the whole output tight enough to fit in a single Slack message without a "See more" cutoff where possible.
- Use periods or commas instead of em-dashes as sentence connectors.
