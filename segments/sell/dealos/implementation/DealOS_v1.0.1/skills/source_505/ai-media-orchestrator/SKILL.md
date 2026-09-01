---
name: ai-media-orchestrator
description: Use when the user wants to produce any AI-generated media — anime, TV series, feature film, book adaptation, music video, face swap, or short-form social content. Routes the request to the correct specialist skill (anime-series-production, tv-series-production, feature-film-production, book-to-film-adaptation, script-to-film-production, music-video-production, identity-replacement-pipeline, short-form-derivative-production) and enforces the 4-level agent hierarchy. Activate on phrases like "make a film", "create an anime", "produce a music video", "recast this character", "make TikToks from this", or any end-to-end media production request.
---

# AI Media Orchestrator

This skill is the **Master Media Orchestrator** — Level 1 of the four-level agent hierarchy. It never generates content directly. It reads the incoming request, matches it to the routing table, and activates exactly one specialist skill.

## Step 1 — Classify the Request

Use `ask_followup_question` to clarify if the request is ambiguous. Match against the routing table:

| Incoming Directive | Activate Skill |
|---|---|
| "Create an anime series/episode/OVA" | `anime-series-production` |
| "Produce a multi-episode TV show / season / mini-series" | `tv-series-production` |
| "Make a feature film from a concept or draft script" | `feature-film-production` |
| "Adapt this novel/book into a film" | `book-to-film-adaptation` |
| "Film this existing locked screenplay" | `script-to-film-production` |
| "Make a music video for my song" | `music-video-production` |
| "Recast this character / replace this face" | `identity-replacement-pipeline` |
| "Make TikToks / Reels / Shorts from this asset" | `short-form-derivative-production` |

## Step 2 — Enforce Prerequisites Before Delegation

Before activating the target skill, confirm the user has the minimum prerequisites:

- **Higgsfield.ai account** (required for Skills 1–5 and 7): confirm access to Soul Cast, Cinema Studio, SeedDance 2.0.
- **Input material**: screenplay, concept, manuscript, song MP3, or source video — whichever the skill requires.
- **Local environment**: ffmpeg installed for any skill that produces a video assembly (Skills 1–6).

If prerequisites are missing, instruct the user to satisfy them before proceeding. Do not skip this step.

## Step 3 — Delegate to the Skill

Activate the matched skill. Pass the full user context — input material, target runtime, genre, director voice, platform targets — so the specialist skill has everything it needs without asking again.

## Step 4 — Monitor and Re-route on Failure

If the activated skill encounters a **pipeline failure or identity drift** that cannot be resolved by its own failure protocols, return to this orchestrator:

- Identity/face drift across shots → route to `identity-replacement-pipeline` to re-lock the character, then resume the originating skill.
- Short-form derivative requested from a just-produced master → activate `short-form-derivative-production` without re-running the originating skill.
- Recasting required mid-production → activate `identity-replacement-pipeline` on the target shots, then return to the originating skill's shot loop.

## Step 5 — Enforce Cross-Cutting Guardrails

Apply these guardrails across every skill, regardless of which is active:

1. **Copyright / Fair Use**: Sourced clips (Skill 6) must stay under 60 seconds and be subordinated to original creative elements.
2. **Identity and Consent**: Face-swap requests (Skill 7) require explicit consent for real individuals. Reject requests to place non-consenting people in compromising, defamatory, or explicit situations.
3. **Content Policies**: When a generation prompt is blocked, rephrase indirectly (e.g., "intense physical struggle" instead of "violent assault") and retry.
4. **Attribution**: All AI cast members and generated assets must be credited in the closing credits sequence (Phase 4 of `script-to-film-production`).

## Skill Dependency Graph

```
book/novel ──► book-to-film-adaptation ──► locked screenplay ─┐
concept ──────► feature-film-production ────────────────────────┤
series bible ─► tv-series-production ───────────────────────────┼──► script-to-film-production (kernel)
anime bible ──► anime-series-production ────────────────────────┘           │
                                                                             │
song/MP3 ──────► music-video-production ◄── may invoke script-to-film-production for original footage
source video ──► identity-replacement-pipeline ◄─── invoked by any skill for recasting
any master ────► short-form-derivative-production ◄─── terminal distribution node
```

All composition decisions follow this graph. Skills 1–4 and 6 may invoke `script-to-film-production` as a sub-routine. Any skill may invoke `identity-replacement-pipeline` or `short-form-derivative-production` as post-processing steps.
