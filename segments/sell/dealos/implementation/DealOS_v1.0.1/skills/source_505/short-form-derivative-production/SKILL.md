---
name: short-form-derivative-production
description: Activate when the user requests short-form social media content (TikToks, Instagram Reels, YouTube Shorts) derived from existing master videos, films, or anime produced by other skills in the library. Manages vertical reframing, hook optimization, and dynamic captioning. Triggers on phrases like "make TikToks from this", "create Reels from this film", "cut this for social media", "make Shorts from this anime episode".
---

# Skill 8: Short-Form Derivative Production

Short-form content requires a different editorial grammar than feature films or traditional music videos: the aspect ratio is 9:16, the **hook must land in the first three seconds**, and text overlays (captions) are mandatory for retention. This skill is the **terminal distribution node** of the library, turning long-form assets into social media marketing engines.

## Prerequisites

| Requirement | Detail |
|---|---|
| Source Asset | A master video produced by any skill in the library (`anime-series-production`, `tv-series-production`, `feature-film-production`, `book-to-film-adaptation`, `script-to-film-production`, or `music-video-production`) |
| CapCut Desktop | For Auto-Reframe, Auto-Captions, and dynamic text effects |
| Target Platform Specs | 9:16 aspect ratio, 1080p, 30/60fps, under 60 seconds (TikTok/Reels) |

---

## Step 1 — Select the Hook Segment

Review the source master video and select a 15–60 second segment that contains:
- A high-energy hook, a dramatic reveal, or a compelling dialogue exchange
- **The first 3 seconds must contain movement, a face, or an immediate audio hook**

Use an LLM to identify segments from a script or transcript if the master is long:

> "Review the attached script/transcript. Identify the 3 most compelling 30-second segments for TikTok. A compelling segment must start with a provocative statement or action, contain escalating tension, and end on a strong punchline or visual reveal. Provide the start and end dialogue lines for each."

## Step 2 — Auto-Reframe to Vertical

1. Import the segment into CapCut.
2. Change the project ratio to **9:16**.
3. Select the video clip and apply **Auto-Reframe**. The AI will track the primary subject and keep them centered in the vertical frame.
4. Review the tracking: if the AI chooses the wrong subject, manually keyframe the X-position to keep the intended action in frame.

## Step 3 — Generate Dynamic Captions

1. Click **Auto-Captions** to transcribe the dialogue or lyrics.
2. Apply a dynamic text template (word-by-word highlight, bouncy text, or karaoke style) to maximize visual retention.
3. Place captions in the safe zone — **middle-lower third of the screen** — ensuring they do not overlap with platform UI elements (buttons on the right, descriptions at the bottom).

## Step 4 — Pacing and Polish

Short-form audiences do not tolerate dead air:
- **Cut any pauses longer than 0.5 seconds** between dialogue lines.
- Add subtle zoom-ins (keyframing scale from 100% to 105% over a clip) to create artificial momentum during static shots.
- Ensure the color grade is punchy (high contrast, high saturation) to stand out on mobile screens.

## Step 5 — Export

Export at **1080p** (4K is often compressed aggressively by social platforms), 30fps (or 60fps for action), MP4.

For multiple clips from the same source, use **CapCut Batch Edit** or **Smart Highlights** to generate multiple vertical cuts automatically.

---

## Quality Gates

| Gate | Threshold | Enforced After |
|---|---|---|
| Hook Gate | Visual or audio hook occurs within the first 3 seconds | Step 1 |
| Framing Gate | Primary subject remains in the 9:16 frame at all times; no awkward cropping | Step 2 |
| Caption Gate | Captions are 100% accurate, clearly legible, and within the UI safe zone | Step 3 |

## Failure Protocols

- **Auto-Reframe failure** (e.g., a wide shot with two characters talking on opposite sides of the screen): Do not use pan-and-scan. Instead, use a **split-screen composition**: duplicate the video track, place character A on the top half of the vertical frame, character B on the bottom half.
- **No clear hook in any segment**: Return to the source screenplay or shot log; identify a moment with higher visual or dramatic stakes and regenerate a targeted clip via `script-to-film-production` before attempting reframing.
- **Caption inaccuracies**: Manually correct in the CapCut transcript editor — do not publish with errors; caption accuracy is the single most-flagged quality issue by short-form audiences.

## Output Specification

A 9:16 vertical video (MP4), 15–60 seconds in length, with dynamic captions, optimized for immediate social media distribution on TikTok, Instagram Reels, or YouTube Shorts.
