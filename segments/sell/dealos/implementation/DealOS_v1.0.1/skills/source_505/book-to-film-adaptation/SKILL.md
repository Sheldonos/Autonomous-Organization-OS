---
name: book-to-film-adaptation
description: Activate when the user provides a novel, novella, non-fiction book, or other long-form prose work and requests a film adaptation. Performs faithful narrative compression from prose (60,000–150,000+ words) to screenplay (15,000–20,000 words), then produces the film via feature-film-production and script-to-film-production. Triggers on phrases like "adapt this book", "turn this novel into a film", "make a movie from this manuscript".
---

# Skill 4: Book-to-Film Adaptation

Adaptation is the hardest narrative-engineering problem in the library. Instead of expanding a beat sheet into scenes, the system must **compress a work that is 5–10× longer than its target** while preserving what made the source resonate. Prose also carries information film cannot: interiority, narration, and authorial voice must be externalized into action, dialogue subtext, and visual language. This skill front-loads a dedicated adaptation phase onto `feature-film-production`; everything from parallel scene drafting onward is shared.

## Prerequisites

| Requirement | Detail |
|---|---|
| All feature-film-production prerequisites | Orchestration, LLM providers, Cognee memory, Higgsfield account, ffmpeg |
| Long-context LLM | **Mandatory**: a 1M-token-class model (MiniMax-01 or equivalent) to hold the full manuscript |
| Input material | The complete manuscript (EPUB/PDF/TXT); rights confirmation; target runtime; adaptation mandate (faithful / loose / "in the spirit of"); director voice specification |

---

## Step 1 — Ingest the Manuscript and Build the Source Fidelity Layer

Parse the book into a structured **Chapter Manifest** (chapter number, POV character, timeline position, events, characters present, structural function). Using the long-context model, extract:

- **Character Registry** with each character's arc as written
- **Interiority Register** cataloguing every significant internal monologue or narrated motivation that the film must externalize
- **Canonical Moments List** — the scenes, lines, and images readers most associate with the book (15–25 entries, ranked), which the adaptation must preserve or consciously justify cutting
- **Theme Statement** in the author's own terms

Store these artifacts in the knowledge graph alongside the Story Bible.

**Manuscript Ingestion Prompt (long-context model):**
> "You are the adaptation analyst for a film studio. Read the complete manuscript below. Produce: (1) a Chapter Manifest — for each chapter: number, POV character, timeline position, events, characters present, structural function; (2) a Character Registry — every named character with physical description quoted from the text, arc summary, and first/last appearance; (3) an Interiority Register — every significant internal monologue or narrated motivation, with chapter reference, that a film must externalize; (4) a Canonical Moments List — the 15–25 scenes, lines, or images most essential to this book's identity, ranked; (5) a Theme Statement in 2–3 sentences using the author's own terms. Output as structured Markdown."

## Step 2 — Make the Structural Adaptation Decisions

The Story Architect Agent, acting as adapting screenwriter, produces the **Adaptation Map**: a chapter-to-act mapping that assigns every chapter one fate:
- *DRAMATIZE* — becomes one or more scenes
- *COMPRESS* — merged with other material into a single scene (specify merge partners)
- *EXTERNALIZE* — interiority converted to invented action/dialogue (specify the device)
- *CUT* — with a written justification tested against the Canonical Moments List

Consolidate subplots and secondary characters per the target runtime. Decide POV structure (whose film is this?). Declare any invented connective scenes. A dedicated **Fidelity Critic** — an additional panel member for this skill — reviews the Adaptation Map before any scene writing.

**Adaptation Map Prompt (Story Architect):**
> "Act as the adapting screenwriter. Target runtime: [N] minutes. Using the Chapter Manifest and Canonical Moments List, assign every chapter one fate: DRAMATIZE, COMPRESS (specify merge partners), EXTERNALIZE (specify the visual/behavioral device), or CUT (justify against the Canonical Moments List). Consolidate subplots and secondary characters as needed, declaring every consolidation. Choose the POV structure and justify it. Declare any invented connective scenes. Output the Adaptation Map as a table: Chapter | Fate | Target Scene(s) | Act | Justification."

## Step 3 — Externalize Interiority

For every entry in the Interiority Register mapped to a kept scene, generate its cinematic externalization: a behavior, a visual metaphor, a line of subtext dialogue, or a reaction shot that conveys the internal state without narration. Action lines may only describe what is seen and heard — WGA rule. Voice-over is permitted only if the adaptation mandate explicitly allows it, and then only for prose whose language is itself a Canonical Moment.

**Interiority Externalization Prompt (Scene Writer sub-task):**
> "The book states the character's internal state as: '[QUOTED PASSAGE].' Film may only show what is seen and heard — action lines must not narrate thought. Propose three externalizations of this internal state: (a) a physical behavior or business, (b) a subtext line of dialogue that implies but never states it, (c) a visual composition or camera choice (using the lighting and lens vocabulary of the platform). Rank them for this scene and justify."

## Step 4 — Generate the Adaptation Story Bible and Checkpoints

Synthesize the Story Bible, Character Arcs, and Director's Voice Profile as in `feature-film-production` Step 2, with two additions:
- Each Character Arc records deviations from the book version with justification.
- Act Checkpoints cross-reference the Adaptation Map: every Forbidden Moves list includes "do not reveal earlier than the book's own information order" unless a deviation was approved.

## Step 5 — Draft, Critique, and Lock the Screenplay

Execute `feature-film-production` Steps 3–5 (parallel scene drafting, five-critic loop, Continuity Guardian, assembly, panel review) with the **Fidelity Critic added to the panel**. The Fidelity Critic scores each scene on: preservation of Canonical Moments, character consistency with the source, and theme fidelity. Scenes scoring below 7.0 are revised with the relevant book passages injected verbatim into the revising agent's context. The locked screenplay must pass the standard four gates **plus** the Fidelity Gate.

## Step 6 — Cast from the Page

In pre-production (`script-to-film-production` Phase 1), Soul Cast characters are configured from the book's own physical descriptions, quoted verbatim in the generation prompt. Where the author is non-specific, the Character Council Agent for that character proposes a design consistent with era, region, and archetype, approved against the Fidelity Critic. Locations described in the book are generated in Soul Cinema with the author's descriptive language incorporated into the prompt, always at the 3/4 angle.

## Step 7 — Produce the Film

Hand the locked screenplay and adaptation-aware director's notes to `script-to-film-production` for the full four-phase production.

**Adaptation-specific parameterization**: period and setting details from the book override generic defaults in every shot prompt (era-correct props, costume, architecture). The Canonical Moments List drives shot-priority — canonical scenes receive the highest regeneration budgets and the most careful camera design.

## Step 8 — Fidelity Review

Before final delivery, run a source-versus-screen pass: the Fidelity Critic (long-context model holding the full manuscript) reviews the assembled film's scene summaries against the book, confirming every Canonical Moment is present and every approved deviation is intentional. Human review by a reader of the book is strongly recommended at this gate.

---

## Quality Gates

| Gate | Threshold | Enforced After |
|---|---|---|
| Ingestion Gate | Chapter Manifest, registries, Canonical Moments List, and Theme Statement complete and internally consistent | Step 1 |
| Adaptation Map Gate | Every chapter assigned a fate; every CUT justified; runtime math validates (dramatized scenes ≈ target ±10%); Fidelity Critic approval | Step 2 |
| Standard Script Gates | Formatting, Continuity, Voice ≥ 7.0, Panel ≥ 7.5 | Step 5 |
| Fidelity Gate | Fidelity Critic score ≥ 7.0: Canonical Moments preserved or justified; character and theme fidelity | Steps 5 and 8 |
| Production Gates | All script-to-film-production gates (Film Bible, per-shot QA, sync, delivery) | Steps 6–8 |

## Failure Protocols

- **Runtime overflow** (too much book survives the Map): Re-enter Step 2 with a stricter consolidation mandate rather than uniformly shortening scenes — adaptation fails by dilution, not by cutting.
- **Fidelity Critic deadlock with the Director's Voice Critic**: The adaptation mandate declared in prerequisites is the tiebreaker; if ambiguous, escalate to human decision — this is a creative-rights decision, not a technical one.
- **Externalization failure** (an interiority beat resisting three proposed devices): Permit a minimal voice-over line as last resort and log the exception.
- **Canonical scene generation failure** (high-priority scene failing shot QA repeatedly): Apply the simplification protocol but never silently downgrade a Canonical Moment — flag for human review if the simplified version loses the moment's essence.

## Output Specification

Everything in `feature-film-production`'s output specification, plus the adaptation document set: Chapter Manifest, Interiority Register, Canonical Moments List with preservation status, the approved Adaptation Map, the deviation log, and the final Fidelity Review report.
