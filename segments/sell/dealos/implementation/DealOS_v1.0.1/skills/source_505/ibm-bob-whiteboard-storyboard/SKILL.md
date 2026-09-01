---
name: ibm-bob-whiteboard-storyboard
description: Reverse-engineer reference visuals into a reusable IBM Bob whiteboard storyboard theme and apply it to presentations, infographics, one-pagers, enablement decks, and seller workspace packages. Use when the user asks to recreate, extend, standardize, or package the hand-drawn IBM Bob visual style; add slides to an existing IBM Bob deck; create Bob-ready theme prompts; or produce consistent whiteboard-style sales enablement assets.
---

# IBM Bob Whiteboard Storyboard

## Purpose

Use this skill to recreate the process of turning rough IBM Bob ideas, reference screenshots, seller enablement needs, and enterprise AI concepts into consistent **hand-drawn IBM Bob whiteboard storyboard** presentations, infographics, and reusable style systems.

This skill is especially useful when the user wants any of the following:

| User Need | Use This Skill To |
| --- | --- |
| “Create an IBM Bob presentation in this style.” | Build a slide deck using the whiteboard storyboard visual language. |
| “Add this slide/content into the Bob deck.” | Insert new content into an existing deck while preserving style continuity. |
| “Reverse engineer this into a theme.” | Produce a Bob-ready style guide and copy-paste theme prompt. |
| “Make a reusable package for sellers.” | Create AGENTS.md, templates, folder structures, scripts, and instructions for repeatable Bob workflows. |
| “Make this consistent across presentations and infographics.” | Use the same visual DNA, layout motifs, palette, prompt blocks, and QA checklist across formats. |

## Required Workflow

Follow these steps in order. If the user provides reference images, do not reinterpret them generically; extract a concrete visual system from them.

1. **Capture the intent.** Identify whether the user wants a new deck, an added slide, an infographic, a reusable theme, an enablement code package, or a reusable Manus skill.

1. **Preserve visual continuity.** Reuse the IBM Bob whiteboard storyboard DNA: off-white background, black marker outlines, IBM blue accents, rounded panels, hand-drawn icons, speech bubbles, checkmarks, and a friendly Bob mascot.

1. **Compress the content.** Convert dense ideas into one central insight, three to six panels, a visual metaphor, and a bottom takeaway or question bubble.

1. **Choose the correct output path.** Use slide tools for decks, document files for style guides, codebase folders and zip files for enablement packages, and skill-creator for reusable skills.

1. **Generate or edit assets.** For decks, initialize or organize slides first, then generate each slide in the established style. For packages, create folder structures, scripts, templates, and AGENTS.md files.

1. **Quality-check the result.** Verify that the output is not generic corporate design, does not use stock-photo aesthetics, avoids dense paragraphs, and retains the hand-drawn IBM Bob visual system.

1. **Deliver the finished artifact.** Present decks through the slide presentation tool; attach documents, zip packages, or SKILL.md files as appropriate.

## Visual System

For full style detail, read `references/style_system.md` when creating or revising visual outputs. The core style can be summarized as:

> Hand-drawn enterprise whiteboard storyboard, warm off-white background, thick black marker outlines, IBM blue underlines and arrows, rounded sketch panels, simple doodle icons, speech bubbles, checkmarks, and friendly IBM Bob mascot energy.

Use this style as a **visual operating system**, not as a suggestion. Avoid drifting into generic corporate PowerPoint, polished SaaS gradients, glassmorphism, or stock photography.

## Slide Creation Rules

When creating a deck, use this default structure unless the user specifies otherwise:

| Slide Type | Requirement |
| --- | --- |
| Cover | Large hand-lettered title, short subtitle, Bob mascot or simple icon cluster. |
| Second slide | “What You’ll Walk Away With” summary slide showing audience value in one whiteboard map. |
| Content slides | One central idea, short title, visual metaphor or panel map, bottom takeaway or question bubble. |
| Process slides | Numbered black circles, rounded panels, arrows, and checkmarks. |
| Comparison slides | Two to four panels, clear labels, simple icons, concise differences. |
| Closing slide | One memorable question or challenge. |

If editing an existing slide deck, do not reinitialize it. Add, delete, reorder, or edit slides in the existing project. When adding a slide, place it where it strengthens the narrative and use prior generated slides as style references.

## Infographic Rules

When creating one-page infographics or whiteboard one-pagers, use this structure:

| Region | Requirement |
| --- | --- |
| Top band | Large title and one-sentence subtitle. |
| Main body | Six rounded panels in a 3x2 grid or horizontal workflow. |
| Panel structure | Number circle, short heading, simple icon, and two or three short notes. |
| Connectors | Black or IBM-blue arrows between panels. |
| Decision framing | Two or three speech bubbles with practical audience questions. |
| Footer strip | Three or four outcome benefits with simple icons and short phrases. |

## Theme Reverse-Engineering Workflow

When the user asks to reverse-engineer a theme/style, produce both a detailed guide and a short prompt.

1. Identify visual DNA: composition, palette, typography, motif library, icon language, emotional tone, and content density.

1. Turn observations into enforceable rules, not vague adjectives.

1. Create a full Markdown style guide using `templates/theme_guide_template.md` as the default structure.

1. Create a short copy-paste prompt using `templates/short_style_prompt_template.txt`.

1. Include negative constraints that prevent style drift.

1. Include example topic translations showing how abstract ideas become whiteboard diagrams.

## Seller Enablement Package Workflow

When the user asks for a reusable seller or Bob workspace package, create a zip-ready folder with:

| Component | Purpose |
| --- | --- |
| `AGENTS.md` | Operating manual telling Bob how to behave in the workspace. |
| `README.md` | Human-facing quick start. |
| `account_workspace/` | Structured folders for personal context, account lists, transcripts, notes, email exports, Slack exports, Sales Cloud exports, decks, documents, converted Markdown, briefs, plans, and proposals. |
| `scripts/` | Deterministic utilities, such as converters that transform Excel, PowerPoint, Word, PDF, email, Slack JSON, and CSV exports into Markdown. |
| `templates/` | Dave Mobley file, account brief, opportunity plan, and prompt templates. |
| `docs/` | Workflow guide and copy-paste Bob prompts. |

The AGENTS.md should instruct Bob to interview the seller first, build a **Dave Mobley file**, analyze account evidence, create account briefs, inspect opportunities, draft follow-ups, and maintain approval boundaries.

## Prompt Templates

Use bundled templates when helpful:

| Template | When To Use |
| --- | --- |
| `templates/deck_style_prompt.txt` | Give Bob instructions for creating a presentation in this style. |
| `templates/infographic_style_prompt.txt` | Give Bob instructions for creating a one-page infographic in this style. |
| `templates/short_style_prompt_template.txt` | Provide a compact style block for quick reuse. |
| `templates/theme_guide_template.md` | Create a complete reverse-engineered theme guide. |

## Quality Checklist

Before delivery, verify:

| Check | Pass Criteria |
| --- | --- |
| Style fidelity | Output looks like a hand-drawn enterprise whiteboard, not a generic deck. |
| Palette discipline | Off-white, black, IBM blue, and only rare secondary accents. |
| Readability | Short text, large headings, and scan-friendly panels. |
| Structure | Clear visual logic through panels, arrows, icons, and a metaphor. |
| Bob usage | Mascot is helpful, not decorative clutter. |
| Enterprise credibility | Content is practical, governed, and business-relevant. |
| Output completeness | Decks are presented, packages are zipped, and skills are validated before delivery. |

## Tooling Notes

For slide decks, use the presentation workflow rather than creating raw HTML manually. For image-based style matching, use generated image slides when the user asks for the same visual look. For reusable skill creation or updates, read and follow `/home/ubuntu/skills/skill-creator/SKILL.md` before editing any skill files.

---

## ibm-patent-architect

