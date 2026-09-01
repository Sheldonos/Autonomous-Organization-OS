---
name: music-video-production
description: Activate when the user provides a song (MP3 plus lyrics) and requests a music video. Executes the lyric-analysis → clip-sourcing → beat-sync → polish → export pipeline using Gemini as creative director and CapCut for editing. Supports Track A (no-code, free tools) and Track B (automated Python/yt-dlp). Optionally invokes script-to-film-production for original generative footage instead of sourced clips.
---

# Skill 6: Music Video Production

The core insight: the creative-direction problem can be delegated to an LLM acting as creative director — it "reads your lyrics the same way a creative director would," identifies the emotional core, and maps that emotion to specific iconic pop-culture moments. The pipeline then reduces editing to a beat-synchronization problem solved mechanically by CapCut's Auto Beat detection or Python/librosa for mathematically precise timestamps.

**Two tracks are supported:**
- **Track A (no-code)**: free web tools end-to-end — Gemini, Perplexity, cobalt.tools, CapCut
- **Track B (automated)**: Python, yt-dlp, and agentic tooling for batch production

## Prerequisites

| Requirement | Detail |
|---|---|
| Google account | Gemini (free) at gemini.google.com for lyric/theme analysis |
| Perplexity account | Free for clip research; Pro ($20/mo) unlocks agentic downloads via Perplexity Computer |
| CapCut Desktop | Free, from capcut.com — editing, Auto Beat Sync, effects, export |
| cobalt.tools | Free YouTube-to-MP4 downloads (Track A) |
| yt-dlp + Python/librosa | Track B only: automated downloads and precise beat detection |
| Optional generative branch | Higgsfield account if producing original footage via `script-to-film-production` |
| Input material | The MP3 and full lyrics; target platform(s) and aspect ratio |

---

## Step 1 — Analyze the Song's Theme (Gemini as Creative Director)

Submit the full lyrics to Gemini with the following prompt:

> "I am a music artist creating a thematic music video compilation. I want you to act as my creative director. Here are the full lyrics to my song: '[PASTE LYRICS]'. Please: (1) describe the core emotional theme in 2-3 sentences, (2) give me 15 iconic pop-culture video concepts that match the theme — including famous couples, sports moments, or historical figures as appropriate, and (3) for each concept, write the exact YouTube search term and one sentence explaining why it matches the song."

Save this brief as the production's Source of Truth. If output is generic, enrich with audience context: "My target audience is 18–30 year olds who love R&B and are familiar with classic romance films. Avoid generic suggestions."

## Step 2 — Source the Clips

**Track A**: Search each term on YouTube, select the best result, and download via cobalt.tools into a `Music_Video_Clips` folder.

**Track B**: Submit the concept list to Perplexity with the Clip Research prompt:
> "I am creating a transformative music video under Fair Use. For each of the following iconic moments, find the best YouTube clip (1–5 minutes, highest quality), give me the direct URL, and tell me the exact timestamp of the most iconic moment: [PASTE GEMINI'S LIST]."

With Perplexity Pro, follow up with the agentic download instruction:
> "Now use your computer-use tools to download all of these as MP4 files to a folder on my desktop called Music_Video_Clips."

Or drive yt-dlp directly from the URLs.

**Copyright discipline**: keep clips under 60 seconds each, ensure the original music is the dominant creative element, never re-upload raw clips without the music. Consider licensed routes (NBA Playmakers Creator Program, Storyblocks) for monetized use.

## Step 3 — Optional Generative Branch (Original Footage)

Where sourced footage is unavailable, unlicensed, or the artist wants a narrative video:
1. Convert the Gemini concept list into a micro-screenplay (one scene per concept, 15–30 seconds each).
2. Invoke `script-to-film-production` to generate original clips: Soul Cast the artist via Soul ID (trained from the artist's photos), lock reference sheets, and shoot each concept with a music-video style header — bold grades, Dreamy Flow or Raw Chaos MoveSets per genre.
3. Generated clips then enter the same beat-sync flow as sourced clips.

## Step 4 — Beat Synchronization in CapCut

1. Import the MP3 and all clips into a new CapCut project.
2. Drag the MP3 to the audio track and clips onto the video track in rough order.
3. Select the MP3 and click **Auto Beat / Beat Sync** — CapCut marks every heavy beat with yellow diamond markers.
4. Select all clips and apply **Sync to Beat / AutoCut** — trims and repositions every clip so each cut lands exactly on a beat marker.
5. Preview, trim edges (they snap to beat markers), and mute all video-clip audio so only the music is heard.

*Track B alternative*: compute exact beat timestamps with `librosa.beat.beat_track` and cut programmatically for frame-accurate sync.

## Step 5 — The 10-Minute Polish Pass

Apply the professional finishing layer:
- **Transitions** matched to genre: Dissolve/Fade to Black for cinematic-romantic; Flash/Glitch/Zoom Blur for hype or sports. Apply to all cuts at once via "Apply to All."
- **Effects** by vibe: Soft Glow/Film Grain/Vignette for romance; Motion Blur/Shake/Glitch for hype; Old Film/VHS for nostalgia.
- **Color grade**: Contrast +15, Saturation +10, Vignette +20, copied to all clips via Copy Style / Paste Style.
- **Optional lower-third text** naming each moment (thin serif for romance, bold sans-serif for hype) for an editorial feel.

## Step 6 — Editorial Quality Pass

Apply the professional principles that separate a music video from a fan edit:
- **Match energy, not just theme**: move any clip whose energy contradicts its musical moment (a tender scene must not land on a bass drop).
- **Use the best 10 seconds**: scrub every clip to its most iconic frame — the single biggest quality improvement available.
- **Vary clip lengths**: let clips breathe 3–4 beats in melodic sections; cut on every beat in the hook.
- **Keep the total under 3 minutes**: edit the song down to a radio edit if needed.

## Step 7 — Export and Publish

Export at 1080p (or 4K), 30fps (60fps for high-frame-rate sports sources), MP4.

For vertical platform derivatives, hand the master to `short-form-derivative-production`.

For batch production across multiple songs: use CapCut Batch Edit / Smart Highlights, or the Perplexity Computer batch prompt:
> "Act as my automated video production assistant. For each song below, analyze the lyrics, generate 10 iconic video concepts, find the best YouTube URL for each, and compile a production brief. Songs: [PASTE SONG TITLES AND LYRICS]."

---

## Quality Gates

| Gate | Criteria | Enforced After |
|---|---|---|
| Brief Gate | Theme analysis is specific (not generic); all 15 concepts have search terms and emotional justifications | Step 1 |
| Clip Gate | Every concept has a downloaded clip; each under 60 seconds; quality sufficient (HD source) | Steps 2–3 |
| Sync Gate | Every cut lands on a beat marker; original clip audio fully muted | Step 4 |
| Polish Gate | Consistent grade on all clips; intentional transitions; energy-matched clip placement; best-10-seconds selection done | Steps 5–6 |
| Export Gate | Correct resolution/frame rate/format for target platform; total runtime under 3 minutes | Step 7 |

## Failure Protocols

- **Generic Gemini output**: Re-prompt with audience and genre context rather than accepting median suggestions.
- **Unfindable or low-quality clips**: Return the concept to Perplexity for alternates, or route that concept through the generative branch (Step 3).
- **Copyright risk** (clips too long, music not dominant): Re-trim below 60 seconds, add transformative layers (effects, text overlays that add new meaning), or substitute licensed/generated footage.
- **Energy mismatch discovered in preview**: Manually reorder clips before touching effects — structure precedes polish.
- **Takedown of a published video**: Rebuild the affected sections from the generative branch and re-publish; keep the CapCut project file for exactly this contingency.

## Output Specification

A finished music video master (MP4, 1080p or 4K, beat-synchronized, graded, with transitions and optional lower-thirds), ready for YouTube, TikTok, or Instagram Reels; the saved production brief (theme analysis + concept list) filed in the brief library; the `Music_Video_Clips` source folder and the CapCut project file; and in batch mode, one brief and one video per song.
