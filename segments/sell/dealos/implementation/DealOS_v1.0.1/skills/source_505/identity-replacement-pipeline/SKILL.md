---
name: identity-replacement-pipeline
description: Activate when the user requests recasting, identity replacement, or face-swapping an existing video with a new digital actor, historical figure, or user-provided face. Executes the three-step identity replacement pipeline — extract master frame, replace face in still (Nano Banana Pro), synthesize motion (Kling Motion Control). Triggers on phrases like "recast this character", "replace this face", "put [person] in this video", "swap the actor in this clip".
---

# Skill 7: Identity Replacement Pipeline

The pipeline **separates identity from motion**: it extracts the best frame, replaces the face in the still image using an image-generation model, and then uses a motion-control model to re-animate that new still using the motion of the original video. This overcomes the temporal instability of traditional deepfake approaches — it is much easier to generate a perfect still image than a perfect video, but video models are excellent at transferring motion from one source to another.

## Prerequisites

| Requirement | Detail |
|---|---|
| Target Identity | A trained Soul ID (20+ photos of the target face) or a high-quality reference image |
| Source Video | The original video clip containing the motion and performance to be replaced |
| LastFrame.ai | For precision frame extraction (free) |
| Higgsfield Nano Banana Pro | For high-fidelity face replacement on the still image |
| Kling Motion Control | For synthesizing the new still with the original video's motion |

---

## Step 1 — Extract the Master Frame

Upload the source video to LastFrame.ai (or use `ffmpeg` with `ffmpeg -i input.mp4 -vf "select='eq(n,FRAME_NUM)'" -vframes 1 frame.png`).

Scrub through the video to find the **Master Frame**: the single frame where the subject's face is most clearly visible, well-lit, and facing forward (or closest to it). Download this frame in maximum resolution. This frame is the anchor for the entire process.

**Master Frame selection criteria:**
- Face is unblurred and unobstructed
- Lighting is representative of the hardest lighting condition in the clip
- Head angle is as close to straight-on as possible
- Expression is the most neutral frame (minimizes distortion in the replacement)

## Step 2 — Replace Identity in the Still

Upload the Master Frame to **Higgsfield > Image > Nano Banana Pro**.

Use the Identity Replacement Prompt, referencing the target identity via their `@tag` (if a trained Soul ID) or by uploading the target reference photo:

> "Replace the face of the subject with the identity provided in the reference [@tag or uploaded image]. Maintain the exact lighting, shadows, skin texture, and environmental reflections of the original image. The new face must seamlessly integrate into the existing head structure and match the emotional expression of the original subject perfectly. Photorealistic, 8K, cinematic."

Because this is an image-to-image process, the model can dedicate all its compute to matching the lighting, skin texture, and geometry of the original frame without worrying about temporal consistency.

**Review the output**: the new face must match the original's lighting direction, shadows, and color temperature exactly. Download the approved **Anchor Image**.

## Step 3 — Synthesize Motion

Open **Kling Motion Control**:
1. Upload the Anchor Image as the visual source.
2. Upload the original source video as the motion source.
3. Kling will map the facial landmarks and body pose of the source video onto the Anchor Image, driving the new identity through the exact performance of the original actor.
4. Generate the video.

## Step 4 — Audio and Color Polish

The resulting video from Kling will be silent.
1. In CapCut or ffmpeg, align the new video track with the original source video's audio track.
2. Apply a light unifying color grade (subtle film grain and contrast adjustment) to blend any minor artifacting at the edges of the face replacement.
3. Upscale to 4K if required.

**ffmpeg audio alignment:**
```
ffmpeg -i new_video.mp4 -i original_audio.mp4 -c:v copy -map 0:v -map 1:a final_output.mp4
```

---

## Quality Gates

| Gate | Threshold | Enforced After |
|---|---|---|
| Master Frame Gate | Frame is clear, unblurred, and represents the hardest lighting condition of the shot | Step 1 |
| Anchor Image Gate | Lighting direction matches; skin tones blend seamlessly; identity is recognizable | Step 2 |
| Motion Synthesis Gate | No severe warping during rapid head turns; micro-expressions (blinks, lip movements) map correctly | Step 3 |

## Failure Protocols

- **Lighting mismatch** in the Anchor Image: Add explicit lighting instructions to the Nano Banana Pro prompt (e.g., "match the hard red neon rim light on the left cheek").
- **Motion warping during extreme head turns** (e.g., profile to straight-on): The motion model fails because it lacks data for the occluded side of the face. Split the source video into two clips at the turn, extract a Master Frame for each half, run the pipeline twice, and cut them together.
- **Multiple subjects in frame**: Isolate the target subject before Step 1 — mask or crop to the target face before sending to Nano Banana Pro to prevent the model from replacing the wrong identity.

## Ethical Guardrails

This skill **requires explicit consent** for real individuals. The orchestrator (`ai-media-orchestrator`) will reject requests to face-swap non-consenting real individuals into compromising, defamatory, or explicit situations. For historical figures or public figures in parody contexts, evaluate the request against platform content policies before proceeding.

## Output Specification

A photorealistic video clip matching the exact duration, motion, and audio of the source video, but featuring the new target identity — ready for insertion into any production pipeline or use as a standalone clip.
