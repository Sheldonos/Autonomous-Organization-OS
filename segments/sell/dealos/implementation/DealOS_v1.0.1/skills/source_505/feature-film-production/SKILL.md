---
name: feature-film-production
description: Activate when the user requests a complete feature-length film from a concept, treatment, or draft script — end-to-end, from screenplay development through 4K delivered master. Chains the full eight-stage scriptwriting pipeline into the four-phase Higgsfield production workflow. Delegates the production phase to script-to-film-production once the screenplay is locked.
---

# Skill 3: Feature Film Production

Movie generation is the composition of the library's two largest subsystems. The **narrative half** runs the enterprise scriptwriting pipeline. The **production half** is the autonomous film director workflow — operating with "the discipline of a professional director who has one shot to deliver a final cut," making all creative decisions autonomously, and never asking for clarification except at hard blockers. The interface between the two halves is a locked, WGA-compliant screenplay plus a director's notes document; everything downstream of that interface is delegated to `script-to-film-production`.

## Prerequisites

| Requirement | Detail |
|---|---|
| Orchestration runtime | Paperclip / DeerFlow (LangGraph) for hierarchy, delegation, and budget control |
| LLM providers | OpenAI / Anthropic / Gemini / MiniMax; long-context model for assembly passes |
| Memory engine | Cognee knowledge graph + vector DB for Story Bible, arcs, entity tracking |
| Script tooling | pdfplumber/FDX parser for ingestion; Final Draft SDK or Fountain for output |
| Higgsfield.ai account | Full platform: Soul Cast, Soul ID, Soul Cinema, Nano Banana Pro, Cinema Studio 2.5, SeedDance 2.0, Kling 3.0, Lipsync Studio, Talking Avatar, Audio, Moodboard, Upscale |
| Local environment | ffmpeg/moviepy; `/production_assets/video/` and `/production_assets/audio/` trees |
| Observability | Langfuse/LangSmith/OTEL for trace, audit, cost analytics |
| Input material | Concept/treatment or draft script + director's cut notes; genre, target runtime (e.g., 110 minutes), director voice specification |

---

## Step 1 — Ingest and Decompose

The Executive Director Agent receives input material and director's notes and invokes a parsing sub-agent to produce the structured **scene manifest**: a JSON array with scene number, heading (INT./EXT., location, time of day), characters present, primary dramatic purpose, and the emotional beat each scene must land. This manifest is the master task queue for the entire pipeline.

If the input is a concept rather than a script, the Story Architect first expands it into a beat-sheet treatment and provisional manifest, which the Critique Panel approves before proceeding.

## Step 2 — Build the Source of Truth Layer

The Story Architect Agent synthesizes the manifest into authoritative Markdown artifacts:
- **Story Bible** (world rules, tone, what cannot happen, thematic mandates)
- **Character Arc documents** per major character (motivation, internal conflict, relationship edges, behavioral constraints)
- **Director's Voice Profile** (sentence rhythm preferences, forbidden tropes, subtext requirements, visual storytelling mandates)

Then define act-level **Checkpoints** — outcome, Knowledge Map, Narrative Weight Distribution, Forbidden Moves — as the API contract between the narrative plan and scene-level agents. Store all artifacts in the knowledge graph.

**Director's Voice Profile Template:**
> "Director's Voice Profile — [DIRECTOR/STYLE]. Action-line rhythm: [e.g., sparse, short lines (Villeneuve) / dense rapid-fire blocks (Sorkin)]. Dialogue rhythm patterns: [...]. Visual metaphor tendencies: [...]. Tonal boundaries — what this director will never do: [...]. Forbidden tropes and phrases: [...]. Subtext mandate: no character states their emotion directly when it can be shown. Reference scenes serving as stylistic anchors: [...]."

## Step 3 — Draft All Scenes in Parallel

The Executive Director spawns N Scene Writer Agents — exactly one per scene, never one per act, because "the overhead of spawning more agents is trivial compared to the quality degradation of overloading a single agent's context." Each receives: scene packet, relevant Story Bible sections, Character Arcs for present characters, the 2K-token Rolling Summary, and its act's Checkpoint constraints. Dialogue Specialist Sub-Agents are spawned for complex multi-character exchanges, one per character voice.

**Pipeline Initialization Prompt (Executive Director Agent):**
> "Act as a Principal Agentic Systems Architect, Master Screenwriter, and Chief Creative Officer of a next-generation AI film studio. Input: [SCRIPT_INPUT] with director's cut notes. Genre: [GENRE]. Target runtime: [TARGET_RUNTIME]. Director voice: [DIRECTOR_VOICE]. Take this input through the eight-stage pipeline — ingestion, story bible, checkpoints, parallel scene drafting, critique loops, continuity pass, assembly, panel review — producing a WGA-compliant screenplay that passes all four quality gates. Enforce per-agent token budgets and treat the Story Bible as sacred: all modifications go through the versioned update protocol."

## Step 4 — Run the Critique-Correct-Verify Loop

Every drafted scene passes the full panel: Structural, Dialogue, Emotional Resonance, and Director's Voice critics plus the **Devil's Advocate anti-homogenization pass**, iterating up to three cycles before human flagging. Then the **Continuity Guardian** performs its full-script pass — timeline consistency, state continuity (injuries, possessions, revealed secrets, relationship status), character knowledge gaps — returning flagged scenes for targeted revision.

## Step 5 — Assemble and Approve the Screenplay

The Story Architect assembles approved scenes, normalizes formatting and transitions, and applies the Director's Voice Profile globally. The assembled screenplay goes to full panel review, scored 1–10 on Plot Coherence, Character Authenticity, Dialogue Quality, and Directorial Vision, with human critiques ingested and weighted equally. The screenplay must pass all four automated gates before production:

**WGA Compliance Checklist:**
- Scene headings in INT./EXT. convention with location and time of day
- Action lines in present tense, active voice, never directing the camera (no "we see," no "the camera pans")
- Character names centered and capitalized on first introduction
- Dialogue properly indented; parentheticals used sparingly
- One page per minute of screen time, within the target runtime window

Output: locked FDX/PDF screenplay + `directors_notes.txt`.

## Step 6 — Execute Production

Hand the locked screenplay and director's notes to `script-to-film-production`, which executes the four Higgsfield phases in full: Phase 1 Film Bible (registries, Soul Cast characters, reference sheets, locations, Moodboard), Phase 2 shot-by-shot generation, Phase 3 audio (lipsync, score, SFX), Phase 4 assembly, credits, and 4K upscale.

Movie-specific parameterization: derive the Style Header from the Director's Voice Profile (e.g., a Villeneuve-profile film locks Silent Machine MoveSets, Anamorphic lens, Soft Cross/Practicals lighting). Establish the master color grade on the Moodboard before shot one.

**Production Handoff Prompt (to script-to-film-production):**
> "You are an autonomous AI Film Director operating inside a web browser. You have been given a movie script and a director's notes document. Your single objective is to produce a complete, export-ready feature film using exclusively the tools available on higgsfield.ai. The film must include all scenes in script order, synchronized dialogue, a music score, sound effects, and a closing credits sequence. You are not a chatbot. You do not ask for clarification unless you encounter a hard blocker. You make all creative decisions autonomously, guided by the script and director's notes."

## Step 7 — Final Review and Delivery

Run the delivered master through a final holistic QA: full-length watch-through evaluation by the Critique Panel, verification of every scene's presence in script order, dialogue sync spot-checks, and audio level verification. Human review is mandatory at this gate. Deliver the 4K master plus the complete document set.

---

## Quality Gates

| Gate | Threshold | Phase Boundary |
|---|---|---|
| Formatting Gate | Zero violations from a parser; page count within ±5% of target | Screenplay → production |
| Continuity Gate | Zero unresolved violations in the Continuity Guardian report | Screenplay → production |
| Voice Gate | Director's Voice Critic score ≥ 7.0/10 | Screenplay → production |
| Panel Gate | Average ≥ 7.5/10 across all four critique dimensions | Screenplay → production |
| Film Bible Gate | Every character, location, and prop locked as tagged Elements; Moodboard established | Pre-production → production |
| Shot QA Gate | Identity + motion + camera criteria per shot | Every shot |
| Sync Gate | Lip movement within one frame of audio | Audio → assembly |
| Delivery Gate | All scenes present in order; audio at −18/−12 dB spec; 4K upscale complete; human panel sign-off | Final delivery |

## Failure Protocols

Inherit all narrative failure protocols: critique deadlock → human flag after three cycles; Story Bible corruption → restore from versioned history; agent interruption → heartbeat resume.

Inherit all production failure protocols from `script-to-film-production`: character drift → re-verify `@tag` binding and regenerate with reference upload; three consecutive artifact failures → minimum viable prompt then re-complexify; lipsync failure after two attempts → Talking Avatar fallback; content policy block → indirect rephrasing.

**Movie-specific**: If the runtime gate fails (assembled film materially shorter/longer than target), do not stretch clips — return to the scene manifest, identify scenes whose dramatic purpose permits expansion or compression, and re-enter the pipeline at Step 3 for those scenes only.

## Output Specification

The final 4K film master (MP4, upscaled, with credits); final screenplay (FDX + PDF); Story Bible and Character Arc documents; continuity registry (CSV); panel review report (PDF); complete `/production_assets/` tree; pipeline audit log (JSON/OTEL trace); cost and token analytics dashboard.
