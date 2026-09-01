---
name: bob-executive-competitive-deck-builder
description: Build executive compare-and-contrast presentations that position IBM Bob or another target solution against named competitors. Use when asked to create reusable Bob modes, CLI workflows, or skill-driven competitive decks with source-backed research, business-value differentiation, decision matrices, and a visual style derived from a provided reference graphic.
---

# Bob Executive Competitive Deck Builder

Use this skill to turn a one-off competitive presentation request into a repeatable Bob mode or CLI-driven skill workflow. The output should help executives compare a target solution against competitors by business value, use-case fit, risk, governance, modernization impact, and adoption path.

## Default Workflow

Follow these steps in order.

| Step | Action | Output |
| --- | --- | --- |
| 1. Intake | Normalize the target solution, competitors, audience, business lens, visual style reference, and constraints. | Structured brief. |
| 2. Research | Gather public, source-backed facts for the target and each competitor. | Research notes with URLs and proof points. |
| 3. Position | Convert facts into differentiators, executive risks, best-fit use cases, and business outcomes. | Positioning matrix. |
| 4. Story | Build a presentation narrative that moves from executive problem to competitive landscape to recommendation. | Slide content outline. |
| 5. Visualize | Translate the visual reference into reusable style rules: palette, typography, motifs, layouts, image usage, and density limits. | Visual style guide. |
| 6. Generate | Create the final presentation using slide tooling when available, or produce files/prompts that a Bob CLI workflow can execute. | Finished deck or generation package. |
| 7. QA | Validate factual support, source citations, executive relevance, competitive fairness, and style consistency. | QA checklist and final package. |

## Intake Requirements

Collect or infer the following. Ask only if a missing item would block the work.

| Field | Guidance |
| --- | --- |
| Target solution | The hero product or platform, such as IBM Bob. |
| Competitors | Named alternatives to compare against. |
| Audience | Executives, technical leaders, sellers, architects, security leaders, public sector, or client-specific roles. |
| Business lens | Benefit, use-case differentiation, modernization, governance, cost, risk, productivity, competitive analysis, or adoption strategy. |
| Visual reference | A screenshot, brand asset, deck, one-pager, website, or explicit design direction. |
| Output form | Slide deck, Markdown outline, Bob mode prompt, CLI package, or all of the above. |
| Constraints | Slide count, citation strictness, required tools, forbidden image actions, export format, or preferred language. |

If the user provides an image and says not to view it again, reuse the existing contextual description and do not inspect the file.

## Research Rules

Research must distinguish public facts from strategic interpretation. Use official product pages, documentation, press releases, analyst reports, customer stories, or reputable industry coverage. Never fabricate numerical claims. If a claim is not source-backed, phrase it as interpretation rather than fact.

For each product, capture:

| Research Field | Description |
| --- | --- |
| Official positioning | How the vendor describes the product. |
| Primary user | Developer, architect, enterprise platform team, security leader, or business leader. |
| Core capabilities | Specific public capabilities relevant to the comparison. |
| Proof points | Public metrics, customer stories, adoption data, certifications, governance claims, or architecture claims. |
| Gaps or limits | Fair, evidence-based limitations or likely implementation considerations. |
| Best-fit use case | Where the product should win. |

## Executive Positioning Pattern

Avoid feature dumps. Translate product features into business outcomes.

| Feature-Level Claim | Executive Translation |
| --- | --- |
| Code completion | Developer productivity and faster iteration. |
| Multi-agent execution | Throughput and parallel engineering capacity. |
| Multi-model routing | Cost control, quality tuning, and model optionality. |
| Human checkpoints | Risk management and accountable approvals. |
| Audit trails | Compliance evidence and production governance. |
| Legacy modernization | Faster transformation with lower rework and institutional knowledge recovery. |
| Security scanning | Earlier defect detection and reduced downstream incident risk. |

When positioning IBM Bob, use this default thesis:

> IBM Bob is not merely another coding assistant. It is a governed SDLC delivery partner for enterprises that need AI speed with modernization depth, security controls, auditability, human oversight, and cost-aware model orchestration.

Adapt this thesis when the target solution is not IBM Bob.

## Default Competitive Deck Structure

Use this structure unless the user requests something else. The second slide must always summarize what the audience will gain.

| Slide | Purpose |
| --- | --- |
| Cover | Title, subtitle, audience, and visual identity. |
| Executive Gain | All-in-one summary of what the audience will learn and decide. |
| Enterprise Problem | Reframe the buyer issue as delivery, governance, modernization, or business friction. |
| Competitive Landscape | Categorize competitors into useful executive groups. |
| Target Solution Differentiator | Explain the hero product’s distinctive operating model. |
| Proof Points | Show source-backed metrics, customer evidence, and credibility anchors. |
| Head-to-Head Slides | Compare the target against each competitor by promise, strengths, best fit, and risk. |
| Decision Matrix | Summarize where each product is strongest and where the target wins. |
| Adoption Pattern | Recommend how a large organization should adopt the target solution. |
| Takeaway | Close with the executive decision thesis. |

For a six-competitor request, a 14–15 slide deck is usually appropriate. For shorter executive briefings, combine competitors into category slides.

## Visual Style Extraction

When a user provides a style reference, extract reusable design rules rather than copying blindly.

| Style Dimension | Examples |
| --- | --- |
| Palette | Background, text, accent, secondary line, success/check colors. |
| Typography | Headline font feel, body font feel, scale, density. |
| Layout motifs | Whiteboard panels, numbered steps, split boards, decision matrices, flow lanes. |
| Icon language | Checkmarks, arrows, target symbols, badges, mascots, role icons. |
| Texture | Hand-drawn, corporate, cinematic, technical, data-heavy, workshop, etc. |
| Restrictions | Use only local images; do not re-view prohibited images; avoid non-existent links. |

For IBM Bob whiteboard visuals, use this default direction:

> Hand-drawn IBM whiteboard workshop: off-white canvas, thick black marker panels, IBM blue hard-hat accents, numbered bubbles, checklist ticks, simple icons, and friendly Bob mascot moments.

## Bob Mode / CLI Packaging

When the user asks for something Bob could have made through a mode and skill in the CLI, include or generate a mode prompt from `templates/bob-mode-prompt.md`. The mode prompt should be copy-paste ready and should instruct Bob to:

1. Read the intake brief.

1. Create a working directory.

1. Produce `research_notes.md`, `positioning_matrix.md`, `visual_style.md`, `slide_content.md`, and `qa_checklist.md`.

1. Use public sources for all factual claims.

1. Generate the deck or hand off to the available slide generation workflow.

1. Validate the output before delivery.

If the environment cannot create slides directly, output the complete slide content and HTML/PPT generation prompts so another slide tool can execute them.

## Quality Gate

Before delivery, verify that:

- The deck is audience-specific and not a generic product pitch.

- The second slide summarizes what executives gain.

- Every numerical or factual claim is source-backed.

- Competitors are represented fairly and not dismissed with strawman language.

- The target solution’s differentiation is framed as business value.

- The decision matrix is qualitative unless backed by measured data.

- Visual style is consistent with the provided reference.

- Local images are referenced only when they exist and are permitted.

- The closing slide gives a clear executive takeaway.

## Bundled Templates

Use these files when generating repeatable packages:

| Template | When to Use |
| --- | --- |
| `templates/intake-brief.md` | Start every reusable deck workflow. |
| `templates/slide-content-template.md` | Build a structured slide outline before slide generation. |
| `templates/bob-mode-prompt.md` | Create a reusable Bob mode or CLI instruction block. |
| `templates/qa-checklist.md` | Validate final readiness before delivery. |

---

## boblore

