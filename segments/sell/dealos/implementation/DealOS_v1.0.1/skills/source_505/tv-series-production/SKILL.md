---
name: tv-series-production
description: Activate when the user requests multi-episode serialized content — a television series, season, mini-series, or web series — in any live-action-style genre. Manages season-level narrative architecture, per-episode production, and cross-episode continuity. Delegates per-episode shot generation to script-to-film-production.
---

# Skill 2: TV Series Production

Television production is the **memory-stress-test of the skill library**. A single film must maintain continuity across ~50 scenes; a ten-episode season must maintain it across 400–600. This skill extends the film pipeline with a two-level narrative hierarchy (season arc above episode arc), persistent cast assets reused across the entire season, and an inter-episode continuity handoff protocol.

## Prerequisites

| Requirement | Detail |
|---|---|
| Higgsfield.ai account | Full platform access: Soul Cast, Cinema Studio, SeedDance 2.0, Kling 3.0, Lipsync Studio, Audio, Moodboard, Upscale |
| Orchestration + memory | Paperclip/DeerFlow/LangGraph + Cognee knowledge graph — mandatory at season scale |
| Long-context LLM | A 1M-token-class model (e.g., MiniMax-01) for full-season review passes |
| Local environment | ffmpeg; `/production_assets/S[season]E[episode]/` directory tree |
| Input material | Series concept or pilot script; season episode count; target per-episode runtime; genre and tonal references |

---

## Step 1 — Architect the Season

The Story Architect Agent produces the season-level Source of Truth before any episode work begins:
- **Series Bible** (world rules, tone, forbidden moves at the series level)
- **Season Arc document** (macro three-act structure mapped onto episodes)
- **Character Arc documents** spanning the season with per-episode waypoints
- **Director's Voice / Showrunner Profile**

Then define **Episode Checkpoints**: for each episode, the non-negotiable end-state — outcome, Knowledge Map, Narrative Weight Distribution, Forbidden Moves.

**Season Architecture Prompt (Story Architect Agent):**

> "Act as showrunner and story architect. From the attached series concept, produce: (1) a Series Bible in Markdown — world rules, tone, thematic mandates, and a 'what cannot happen' list; (2) a Season Arc mapping a three-act structure across [N] episodes; (3) Character Arc documents for each major character with per-episode waypoints (motivation, internal conflict, relationship edges, behavioral constraints); (4) Episode Checkpoints for every episode specifying: Outcome, Knowledge Map (who knows what by episode's end), Narrative Weight Distribution, and Forbidden Moves. These artifacts are the Source of Truth for all downstream agents."

## Step 2 — Write the Episode Grid

Decompose the season into an **Episode Manifest**: a JSON array where each element carries the episode number, logline, A/B/C plot assignments, characters featured, new entities introduced, and the emotional beat the episode must land. Validate against the Season Arc: verify escalation logic, subplot braiding (no thread dormant for more than two consecutive episodes), and that each episode ends on its Checkpoint. Pass the grid through the Critique Panel before any episode script is drafted.

## Step 3 — Draft Episode Screenplays (Serialized Pipeline)

For each episode in order, run the full scriptwriting pipeline scoped to that episode: ingestion of the episode packet, per-episode scene manifest, parallel Scene Writer Agents with scoped context packets, the Critique-Correct-Verify loop with all five critics plus the Devil's Advocate pass, Continuity Guardian pass, assembly, and panel review. Each episode's agents receive the **cross-episode Rolling Summary**: the previous episode's final state at high fidelity, the current act's beats at medium fidelity, prior acts at low fidelity, plus the Dynamic Entity Registry. An episode's scenes are never drafted before the preceding episode's Continuity Gate has passed.

## Step 4 — Build the Persistent Season Cast and World

Execute the Film Bible pre-production phase once for the entire season:
- Soul Cast creation and Nano Banana Pro reference sheets for every recurring character (using the canonical character turnaround prompt from `script-to-film-production` Phase 1.2)
- Location sheets for every standing set
- Prop sheets for signature objects
- **Per-episode wardrobe variants** as separately locked reference sheets
- **State variants** where the season arc demands them (e.g., `@Elena_S1_injured`, `@Elena_finale_scarred`)

Maintain one season Moodboard. Guest characters introduced mid-season are added to Elements at the top of their debut episode's production.

## Step 5 — Produce Each Episode via the Production Kernel

For each locked episode screenplay, invoke `script-to-film-production` with series-level parameterization: fix the Camera MoveSet Style palette per show (e.g., a prestige drama locks to Silent Machine and Classic Static; a found-footage thriller to Raw Chaos and Documentary Snap) and encode it in the series Style Header.

**Series Style Header Template:**

> "Style: prestige television drama, 4K, 16:9. Photorealistic. Lighting: motivated practicals and window light, low-key contrast. Color: desaturated teal-slate with warm skin preservation, 60:30:10. Camera: Silent Machine MoveSet — slow, precise, invisible trajectories; 35mm and 50mm natural perspective; f/4 moderate depth. Skin: pore-level realism. Acting: Hollywood — micro-pauses before reactions. Physics: gravity and inertia respected. Continuity: characters, wardrobe, and standing sets identical across every cut and every episode, matching @reference sheets."

## Step 6 — Series-Level Assembly Conventions

Assemble each episode with ffmpeg, then attach standing series elements:
- Cold open (if the format uses one)
- Main title sequence (generated once in Soul Cinema and reused)
- **"Previously on" recap** (auto-cut from prior episodes' approved shots using Rolling Summary high-fidelity beats as the selection criterion)
- End credits with AI cast list

**"Previously On" Recap Selection Prompt:**
> "From the Rolling Summary's high-fidelity beats for episodes 1–[N−1], select the 4–6 moments a first-time viewer must see to understand episode [N]. Return the shot IDs (S/SH naming) for each moment, ordered for a 30–45 second recap. Prefer moments that plant this episode's payoffs; exclude anything that spoils an unrevealed twist per the Forbidden Moves list."

Mix: score at −18 dB, SFX at −12 dB relative to dialogue. Upscale to 4K.

## Step 7 — Inter-Episode Continuity Handoff

After each episode's delivery gate, execute the handoff protocol:
1. The Continuity Guardian writes the episode's **State Delta** (every change to character knowledge, possessions, injuries, relationships, world state) into the knowledge graph and Entity Registry.
2. The Rolling Summary is re-tiered: the just-finished episode compresses to medium fidelity, older episodes to low.
3. The next episode's Checkpoint is re-validated against actual (not planned) end-state. If approved deviations occurred, the Story Architect amends downstream Checkpoints through the versioned update protocol.

This handoff is a **hard blocker** — the next episode's scene drafting cannot begin until it is complete.

## Step 8 — Season Finale Review

After the final episode, run a full-season holistic pass using the long-context model: evaluate against season-level payoff — every Checkpoint honored, every planted setup paid off, every character arc landed. Human critiques are ingested as structured feedback and weighted equally with AI panel scores. Flagged episodes return to targeted re-production before the season is declared final.

---

## Quality Gates

| Gate | Threshold | Enforced After |
|---|---|---|
| Season Architecture Gate | Series Bible, Season Arc, Character Arcs, and all Episode Checkpoints approved; braiding logic verified | Steps 1–2 |
| Episode Script Gates | Zero formatting/continuity violations; Voice ≥ 7.0/10; Panel ≥ 7.5/10 | Each episode screenplay |
| Cast Lock Gate | Every recurring character, wardrobe variant, and standing set saved to Elements with verified `@tags` | Step 4 |
| Per-Shot QA Gate | Identity + motion + camera criteria pass | Every shot |
| Episode Delivery Gate | Assembly with titles/recap/credits; audio at spec; 4K master | Each episode |
| Handoff Gate | State Delta written; Rolling Summary re-tiered; next Checkpoint re-validated | Between episodes — hard blocker |
| Season Gate | Full-season holistic review passed; all setups paid off; human critique integrated | Season delivery |

## Failure Protocols

- **Cross-episode continuity violation discovered mid-season**: Halt downstream drafting. Trace to source episode. Prefer forward-fix (scene amendment in current episode) over re-producing a delivered master. Record decision in knowledge graph.
- **Character drift across episodes**: Re-anchor via Elements Library `@tag` verification and regenerate drifted shots with explicit reference upload.
- **Critique deadlock** (episode failing panel review after three full cycles): Flag for human showrunner review.
- **Budget escalation**: Orchestrator's budget engine pauses new episode spawning and reports. Per-agent budgets are never silently raised.
- **Agent interruption**: Resume from the last heartbeat checkpoint — never re-draft completed scenes.

## Output Specification

One 4K master MP4 per episode with cold open, titles, recap, synchronized audio, and credits; complete season screenplay set (FDX/Fountain + PDF); Series Bible, Season Arc, Character Arc documents, and per-episode Checkpoint records; season Entity Registry and continuity spreadsheet (CSV); full Elements Library; panel review reports per episode and per season; pipeline audit log with cost analytics per episode.
