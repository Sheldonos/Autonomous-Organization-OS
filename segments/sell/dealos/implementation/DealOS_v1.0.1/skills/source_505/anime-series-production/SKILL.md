---
name: anime-series-production
description: Activate when the user requests creation of anime-style content — a series, season, episode, OVA, or anime short — from a concept, manga source, or series bible. Produces stylized, episodic animated content with locked character designs and genre-correct cinematography. Delegates the shot generation loop to script-to-film-production with anime parameterization.
---

# Skill 1: Anime Series Production

Anime production is a **style-parameterized specialization of the general film pipeline**. It uses the same narrative engine (Foundations F6–F7), the same Soul Cast identity discipline (F1–F2), and the same shot-generation kernel as `script-to-film-production`, but overrides the visual layer at every stage with an anime style contract.

## Prerequisites

| Requirement | Detail |
|---|---|
| Higgsfield.ai account | Soul Cast, Soul Cinema, Nano Banana Pro, Cinema Studio, SeedDance 2.0, Draw to Video, Lipsync Studio, Audio, Moodboard |
| Orchestration runtime | Paperclip / DeerFlow / LangGraph for the narrative agent hierarchy |
| Memory engine | Cognee or equivalent knowledge graph for the Series Bible and entity registry |
| Local environment | ffmpeg; `/production_assets/` directory tree |
| Input material | Concept document, manga/light-novel source, or existing series bible; target episode count and runtime |

---

## Step 1 — Establish the Anime Style Contract

Write the anime **Style Header** that will prefix every image and video prompt for the entire series. Define: animation lineage (e.g., 90s cel anime, modern digital sakuga, Ghibli-soft, seinen grit), line weight, shading style (cel-shaded two-tone vs. soft gradient), color palette discipline, aspect ratio, and frame-rate feel. Store the contract in the Moodboard and knowledge graph.

**Anime Style Header template (prepend to every generation):**

> "Style: 2D anime, [90s cel / modern digital] production. 16:9 widescreen. Clean line art with [thin/bold] outlines, cel-shaded two-tone shadows, flat color fills with painterly backgrounds. Color: saturated primaries with [palette]. Camera: virtual anime cinematography, limited animation timing on twos, held frames for emphasis. Physics: stylized but weight-respecting; hair and cloth follow motion with one-frame delay. Continuity: characters, outfits, and environments identical across every cut, matching @reference sheets exactly. No photorealism, no 3D render look."

## Step 2 — Generate the Series Bible

Run the narrative pipeline: the Story Architect Agent produces the **Series Bible** (world rules, power systems, tone, thematic mandates), **Character Arc documents** spanning the full season, and a **Director's Voice Profile** encoding the target studio aesthetic. Define **Checkpoints** at the end of each episode and season arc — outcome, Knowledge Map, Narrative Weight Distribution, Forbidden Moves — so episode-level agents cannot resolve arc material prematurely.

## Step 3 — Write Episode Screenplays via the Narrative Division

For each episode, run the parallel scene-drafting loop: spawn one Scene Writer Agent per scene, each receiving a scoped context packet (scene packet, relevant Series Bible sections, Character Arcs for present characters, the 2K-token Rolling Summary of all preceding scenes, and the episode's Checkpoint constraints). Every scene passes the **Critique-Correct-Verify loop** (Structural, Dialogue, Emotional Resonance, Director's Voice critics) plus the **Devil's Advocate anti-homogenization pass** — anime is especially prone to trope regression (generic power-up speeches, telegraphed tournament beats), so expect a high Devil's Advocate flag rate. The Continuity Guardian performs a full-episode pass before assembly.

## Step 4 — Design the Cast (Soul Cast in Anime Mode)

For each character: create in Soul Cast configuring Genre and Era to match the style contract, then generate the **anime character reference sheet** via Nano Banana Pro.

**Anime Character Reference Sheet Prompt (Nano Banana Pro):**

> "Create a professional anime character reference sheet based strictly on the uploaded reference image. Use a clean, seamless grey background and present the sheet as a settei-style model turnaround matching the exact anime art style of the reference. Arrange the composition into two horizontal rows. Top row: four full-body standing views — front, left profile, right profile, back — in a relaxed A-pose with consistent scale. Bottom row: three close-up face portraits — front, left profile, right profile — plus an expression strip (neutral, smiling, angry, surprised). Maintain perfect identity consistency across every panel: identical hair silhouette, eye design, and color palette. Consistent flat lighting across all panels. Output a crisp, print-ready anime production reference sheet."

Create a **separate locked reference sheet per outfit/form** (school uniform, battle form, transformed state). Apply the grey-background and single-face-lock rules. Save every sheet to the Elements Library tagged `@CharacterName` and, for forms, `@CharacterName_FormName`.

## Step 5 — Build Location and Prop Assets

Generate every recurring location via Soul Cinema at a 3/4 angle for depth, then produce location reference sheets via Nano Banana Pro and save with `@Location` tags. Generate prop sheets (signature weapons, artifacts) with three views on grey. Upload all sheets to a series Moodboard.

## Step 6 — Storyboard Pass (Optional but Recommended)

For key sequences (action set pieces, emotional climaxes, openings), generate rough storyboard panels first, then use **Draw to Video** to convert storyboard sketches directly to motion. This gives explicit control over composition and timing for anime's highly graphic compositions.

## Step 7 — Execute the Shot Generation Loop

Invoke `script-to-film-production` Phase 2 with anime parameterization: summon `@Character` and `@Location` elements in Cinema Studio; construct the prompt as *Anime Style Header + [Shot Size & Angle] + [Subject & Action] + [Camera Movement] + [Mood & Lighting]* with one camera move maximum. Use SeedDance 2.0 by default, Kling 3.0 only for dialogue close-ups. Favor anime-idiomatic camera language: Classic Static and Dreamy Flow for dialogue, Epic Scale for action reveals.

**Combat Shot Template:**
> "[Anime Style Header] Wide shot, low angle. @Kaito lunges forward, blade trailing light, speed lines radiating from the impact point. Single fast tracking shot following subject. Contre-jour lighting from the explosion behind, silhouetted debris. Epic, desperate. Mass has real weight, correct contact shadows. No floating props."

**Dialogue Shot Template:**
> "[Anime Style Header] Medium close-up, eye level, two-shot. @Yuki turns away from @Kaito, clutching the pendant. Static camera, shallow depth of field, painterly bokeh background. Window lighting, soft fall-off, dusk tones. Melancholic, intimate."

## Step 8 — Audio Production

1. **Dialogue** — for every dialogue shot, use Lipsync Studio with exact script lines and a per-character voice profile. Talking Avatar fallback is broadly acceptable in anime.
2. **Score** — generate per-beat music cues in Higgsfield Audio specifying instrumentation, tempo, emotional tone, and duration. Generate a recurring theme per major character and reuse variations.
3. **SFX** — ambient and action effects per scene, including genre-specific cues (transformation shimmer, impact hits, cicadas for summer scenes).

## Step 9 — Assemble the Episode

Concatenate approved shots: `ffmpeg -f concat -safe 0 -i filelist.txt -c copy episode_v1.mp4`. Mix score at −18 dB and SFX at −12 dB relative to dialogue. Attach opening title sequence and closing credits (generated as title cards in Soul Cinema, 4 seconds per card with 1-second crossfades). Upscale master to 4K via Video Upscale.

## Step 10 — Serialize

After each approved episode: update the Rolling Summary and Dynamic Entity Registry with all state changes (injuries, revealed secrets, relationship shifts, new locations). Verify the episode's ending state matches its Checkpoint contract before beginning the next episode's scene drafting. For multi-episode orders, loop back to Step 3.

---

## Quality Gates

| Gate | Threshold | Enforced After |
|---|---|---|
| Script Gates | Zero formatting violations, zero continuity violations, Director's Voice ≥ 7.0/10, panel average ≥ 7.5/10 | Episode screenplay |
| Style Lock Gate | Every reference sheet matches the Style Contract; no photorealistic drift; grey background verified | Cast/location design |
| Shot QA Gate | Identity consistency with `@tag` sheets, stable motion, correct camera behavior — all three pass | Every shot |
| Episode Continuity Gate | Zero unresolved violations; Checkpoint end-state verified | Episode assembly |
| Delivery Gate | 4K upscale complete; audio at specified levels; OP/ED and credits attached | Final export |

## Failure Protocols

- **Style drift toward photorealism**: Strengthen the Style Header with explicit negative constraints ("no photorealism, no 3D render look"), re-anchor with reference sheet upload alongside the `@tag`, regenerate.
- **Character drift** (hair silhouette or eye design changes): Verify the `@tag` binding in Elements Library and regenerate with explicit reference image upload.
- **Three consecutive generation failures**: Simplify to minimum viable prompt — one character, one action, one camera move, no complex lighting — then add complexity via image editing on the still before animating.
- **Trope regression flagged repeatedly by Devil's Advocate**: Escalate to human review rather than exceeding three critique cycles.
- **Content policy block**: Rephrase indirectly (e.g., "intense clash, dramatic motion blur") and retry.

## Output Specification

Per episode: 4K master MP4 with synchronized dialogue, score, SFX, opening/closing sequences, and credits; episode screenplay (Markdown + Fountain); updated Series Bible, Character Arcs, Rolling Summary, and Entity Registry; complete Elements Library of tagged reference sheets; shot log (`S[scene]_SH[shot].mp4`); pipeline audit log with cost analytics.
