---
name: script-to-film-production
description: Activate when a finished, locked screenplay (plus optional director's notes) is provided and the request is to produce the film itself. This is the production kernel of the entire AI media library — the four-phase autonomous workflow (Film Bible → shot-by-shot generation → audio → assembly) executed on Higgsfield.ai. All other film-producing skills (anime-series-production, tv-series-production, feature-film-production, book-to-film-adaptation, music-video-production) delegate their shot generation phase to this skill.
---

# Skill 5: Script-to-Film Production (The Production Kernel)

This skill is a direct codification of the Master CUA Film Director workflow. The governing identity is absolute: the agent "operates with the discipline of a professional director who has one shot to deliver a final cut," makes all creative decisions autonomously, and **never asks for clarification except at hard blockers** such as login walls or account suspension.

This skill can run under either execution architecture:
- **Computer-Use Agent (CUA)**: drives the Higgsfield.ai web interface end-to-end
- **API-native**: programmatic API calls where the platform exposes access

## Prerequisites

| Requirement | Detail |
|---|---|
| Higgsfield.ai account | Logged in, with credits for the full production; access to Soul Cast, Soul Cinema, Nano Banana Pro, Cinema Studio, SeedDance 2.0, Kling 3.0, Lipsync Studio, Talking Avatar, Audio, Moodboard, Upscale |
| Input files | `script.txt` (locked screenplay) + `directors_notes.txt` (grades, tonal guidance, per-scene notes) |
| Local environment | ffmpeg (and optionally moviepy); `/production_assets/video/` and `/production_assets/audio/{score,sfx}/` directories |
| Working memory | Persistent character, location, scene, and dialogue registries; a shot log surviving across sessions |

---

## Phase 1.1 — Parse the Script into Registries

Read the full script and extract into working memory:
- **Character Registry**: every named character — physical description, age, dominant emotional state, first scene of appearance
- **Location Registry**: every distinct location — time of day, weather, visual atmosphere
- **Scene Registry**: every scene in order — number, characters present, location, emotional tone
- **Dialogue Registry**: every spoken line, attributed to character and scene

These four registries drive every subsequent phase. Do not proceed to asset creation until all four are complete.

## Phase 1.2 — Create the Cast (Soul Cast → Reference Sheets → Elements)

For each character:
1. Navigate to **Character > Soul Cast**. Configure Genre, Era, Archetype, Identity, Physical Appearance (height, eye color, hair, skin tone, facial structure), and Outfit from the script description. Generate and visually verify against the script — if generic or mismatched, regenerate with more specific descriptors before proceeding.
2. Upload the approved image to **Image > Nano Banana Pro** with the canonical character reference sheet prompt:

> "Create a professional character reference sheet based strictly on the uploaded reference image. Use a clean, neutral plain background and present the sheet as a technical model turnaround while matching the exact realistic visual style of the reference. Arrange the composition into two horizontal rows. Top row: four full-body standing views — front, left profile, right profile, back. Bottom row: three close-up portraits — front, left profile, right profile. Maintain perfect identity consistency across every panel. Keep the subject in a relaxed A-pose with consistent scale and alignment, accurate anatomy, and clear silhouette. Lighting should be consistent across all panels. Output a crisp, ultra-realistic, print-ready reference sheet."

3. Download the sheet. Return to Soul Cast, click "Save to Elements," and tag with the character name prefixed by `@` (e.g., `@Marcus`) — the **permanent recall token** for this production.
4. Apply grey-background and single-face-lock rules. Create a **separate locked reference sheet per outfit variant** (F2 discipline).

## Phase 1.3 — Create Locations and the Moodboard

For each location:
1. Generate the establishing shot in **Image > Soul Cinema** capturing atmosphere, time of day, and visual style — always at a **3/4 angle** for depth.
2. Run the canonical location reference sheet prompt through Nano Banana Pro:

> "Create a professional location reference sheet based strictly on the uploaded reference image. Match the exact realistic visual style, lighting quality, color treatment, and texture of the reference. Arrange into two horizontal rows. Top row: straight-on frontal view, left angled perspective, right angled perspective, reverse wide view. Bottom row: three detailed close-ups of key environmental elements. Maintain architectural consistency, accurate proportions, and consistent lighting across all panels. Output a crisp, ultra-realistic, print-ready location sheet."

3. Save to Elements with an `@Location` tag (e.g., `@Rooftop_Night`).
4. Create a **Moodboard** titled with the film's name and upload all approved character and location sheets. This is the visual anchor consulted before generating any shot.

---

## Phase 2 — The Shot Generation Loop

**Execute per shot, in strict script order, with no batching or skipping ahead.**

For every shot chronologically:

**2.1** Open **Cinema Studio 2.5**.

**2.2** **Summon Elements** — Add Character for every `@tag` in the shot; Add Location for the scene's `@Location` (location only for pure establishing shots).

**2.3** **Construct the prompt** using the cinematic formula: `[Shot Size & Angle] + [Subject & Action] + [Camera Movement] + [Mood & Lighting]` — one camera move maximum.

**Prompt Formula Reference Card:**

| Element | Options |
|---|---|
| Shot Size | Extreme close-up / Close-up / Medium close-up / Medium / Wide / Extreme wide / Aerial |
| Angle | Eye level / Low angle / High angle / Dutch angle / POV / Over-the-shoulder |
| Camera Move | Static / Slow dolly-in / Dolly-out / Pan left–right / Tilt up–down / Tracking shot / Crane up–down / Handheld |
| Lighting | Soft cinematic / Hard directional / Backlit silhouette / Neon-lit / Golden hour / Moonlit / Fluorescent interior |
| Mood | Tense / Melancholic / Euphoric / Ominous / Intimate / Epic / Comedic |

**Complete Shot Prompt Example:**
> "Medium close-up, low angle. @Marcus raises his weapon, scanning the corridor. Static camera. Hard directional lighting from above, deep shadows. Tense, ominous."

**Script-direction mapping:**

| Script Direction | Correct Prompt Language |
|---|---|
| Close-up on face | "Extreme close-up, eye level" |
| Following character walking | "Medium shot, tracking shot following subject" |
| Reveal of a location | "Wide establishing shot, slow crane up" |
| Tense confrontation | "Medium close-up, two-shot, static, shallow depth of field" |
| POV of character | "POV shot, handheld, slight camera shake" |

**2.4** **Select the engine**: SeedDance 2.0 by default for complex motion, multi-character scenes, environmental animation, and multi-shot continuity. Switch to Kling 3.0 only for close-up dialogue requiring precise facial performance and lip-sync fidelity.

**2.5** **Generate and QA** against three criteria — identity consistency with `@tag` sheets, motion quality (no warping, extra limbs, or physics violations), and camera logic (moves as instructed, no random drift). On failure, simplify the camera move or reduce subjects and regenerate, up to three times before escalating to a simpler prompt.

**2.6** **Color grade** the approved clip per the scene's directors_notes entry, or the master grade from the Moodboard if unspecified. Available parameters: Color Temperature, Contrast, Saturation, Sharpness, Highlights, Film Grain, Exposure.

**2.7** **Download and log** as `S[scene]_SH[shot].mp4` into `/production_assets/video/` and mark APPROVED in the shot log.

---

## Phase 3.1 — Dialogue Synchronization

For every shot with dialogue (from the Dialogue Registry):
1. Open **Video > Lipsync Studio**, upload the approved graded clip, enter the exact script lines, select the character's voice profile.
2. Generate and verify sync visually and aurally — if off by more than one frame, regenerate.
3. Download the lipsync-combined clip and overwrite the silent version.

## Phase 3.2 — Score and SFX

In the **Audio** tool:

**Score** — generate one music cue per distinct emotional beat (from the Scene Registry):
> "[Genre/instrumentation], [tempo BPM or descriptor], [emotional tone], [instrument inclusions/exclusions], [duration] seconds, [fade behavior]."

Example: `"Orchestral score, 60 BPM, slow and melancholic, strings and piano, no percussion, 45 seconds, fade out at end"`. Save to `/production_assets/audio/score/` named by scene.

**SFX** — generate ambient and action effects per scene:
> `"city traffic ambience, distant sirens, nighttime, 30 seconds loopable"` or `"gunshot, single, close range, reverb in concrete corridor, 1 second"`.
Save to `/production_assets/audio/sfx/`.

---

## Phase 4 — Assembly, Credits, and Export

**4.1 Concatenate** all approved shots in scene/shot order:
```
ffmpeg -f concat -safe 0 -i filelist.txt -c copy film_assembly_v1.mp4
```

**4.2 Mix**: overlay score at **−18 dB** and SFX at **−12 dB** relative to dialogue (dialogue is already embedded from Phase 3).

**4.3 Credits**: generate a cinematic title card in Soul Cinema:
> "Cinematic title card, black background, elegant serif typography, soft golden glow, film grain, anamorphic lens flare."

Add cards for: Directed by, Produced by, the AI Cast (all `@Character` tags and Soul Cast names), and the generation credit. Concatenate at 4 seconds per card with 1-second crossfades and append to the film.

**4.4 Upscale**: run the assembled film through **Edit > Upscale** at 4K and download the final master — this is the deliverable.

---

## Quality Gates

| Gate | Criteria | Blocking Behavior |
|---|---|---|
| Registry Gate | All four registries complete before any generation | Phase 1 cannot begin asset creation without them |
| Cast Lock Gate | Every character verified against script, reference sheet generated, `@tag` saved to Elements | No shot generation until every character and location is locked |
| Per-Shot QA Gate | Identity consistency + motion quality + camera logic — all three pass | "If any criterion fails, do not proceed" — the next shot never starts before the current one is APPROVED |
| Sync Gate | Lip movement within one frame of audio | Regenerate; fallback protocol after two failures |
| Assembly Gate | Every scene present in script order; audio levels at spec; credits appended | No upscale until verified |
| Delivery Gate | 4K upscale completed and downloaded | Final deliverable |

## Failure Protocols

| Failure | Protocol |
|---|---|
| **Character drift** (hair/face structure changes between shots) | Do not proceed. Verify the `@tag` is correctly bound to the original Soul Cast reference in the Elements Library; regenerate the drifted shot with an explicit reference image upload alongside the `@tag`. |
| **Severe artifacts** (melting faces, extra limbs, incoherent motion) ×3 consecutive attempts | Simplify to minimum viable prompt — one character, one action, one camera move, no complex lighting; generate the clean base, then add complexity via image editing on the still before animating. |
| **Lipsync failure** ×2 attempts | Fall back to **Talking Avatar**, animating a static portrait with the audio track — acceptable for close-up dialogue. |
| **Missing script information** (no camera angle/shot size specified) | Default to a medium shot at eye level with a slow dolly-in — the most cinematically neutral choice that cuts cleanly with adjacent shots. |
| **Content policy block** | Rephrase to describe the action indirectly (e.g., "violent confrontation" → "intense physical struggle, dramatic motion blur") and retry. |
| **Hard blockers** (login required, account suspended) | The only condition under which the agent halts and asks the user. |

## Output Specification

A complete, export-ready film: the final 4K upscaled master (MP4) containing all scenes in script order with synchronized dialogue, score, SFX, and a closing credits sequence; the complete `/production_assets/` tree (per-shot graded clips, score cues, SFX cues); the four registries and the APPROVED shot log; and the Elements Library of tagged characters and locations reusable for sequels, marketing, or `short-form-derivative-production`.
