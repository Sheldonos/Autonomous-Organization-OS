---
name: ibm-bob-whiteboard-onepager
description: Create client-facing IBM Bob hand-drawn whiteboard one-pagers, seller-partner visuals, and reusable Bob enablement leave-behinds. Use when the user asks for IBM Bob graphics, one-pagers, client-facing explainers, Bob as a second brain/document system/control tower, modernization visuals, seller onboarding/account strategy/meeting notes/sales execution graphics, AGENTS-style seller partner harnesses, or reusable whiteboard-style sales/education collateral.
---

# IBM Bob Whiteboard One-Pager

Use this skill to turn an IBM Bob topic, client pain point, or briefing into a client-facing hand-drawn whiteboard one-pager. The output should match the friendly visual language used in the user’s Bob graphics: marker-style layout, six numbered panels, simple icons, blue accents, concise bullets, and a bottom benefit strip.

## Core Rule

Make the graphic **client-facing** by default. Do not include internal outreach language such as “email CTA,” “attach this one-pager,” “book a meeting,” or “Step 7” unless the user explicitly requests an internal sales enablement version.

## Workflow

1. **Classify the request.** Determine whether the user wants a new Bob use-case graphic, a revision to an existing graphic, a client-specific variant, or a reusable prompt/template.

1. **Condense the topic.** Convert the idea into a six-panel structure: context, explanation, plan, governed execution, validation/documentation, and scaling or handoff.

1. **Write visual copy first.** Keep each panel to one heading and three short bullets. Use client language, not internal sales language.

1. **Generate the image.** Use AI image generation/editing with the established whiteboard style and any user-provided reference image. If the user asks to modify an existing image, use image editing rather than deterministic image processing.

1. **Create supporting notes when useful.** Provide a short Markdown usage guide with positioning, conversation openers, and suggested follow-up language.

1. **Deliver the image and support file.** Attach final image files and any Markdown guide. Stop after delivery unless the user asks for revisions.

## Required Visual Pattern

| Component | Requirement |
| --- | --- |
| Format | 16:9 image, one client-facing one-pager |
| Layout | Exactly six numbered rounded panels; normally two rows of three |
| Style | Hand-drawn whiteboard, black marker outlines, IBM-like blue accents, light gray paper shadow |
| Character | Friendly builder mascot with blue hardhat is acceptable; do not copy blurred faces from references |
| Panel copy | One heading and three concise checkmarked bullets per panel |
| Bottom strip | Four outcome-focused benefits |
| Speech bubbles | Three plain-English diagnostic questions |
| Avoid | Step 7, internal CTA language, fake logos, QR codes, overclaiming, dense paragraphs, tiny text |

## Topic Templates

Read `/home/ubuntu/skills/ibm-bob-whiteboard-onepager/references/whiteboard_templates.md` when you need one of the general Bob use-case structures or need to convert a new topic into the six-panel format. Read `/home/ubuntu/skills/ibm-bob-whiteboard-onepager/references/seller_partner_visual_templates.md` when the request involves Bob as a seller partner, onboarding coach, account strategist, meeting notes engine, sales execution partner, confidence loop, or seller operating system. Read `/home/ubuntu/skills/ibm-bob-whiteboard-onepager/references/seller_partner_harness.md` only when the user asks for a full AGENTS.md-style harness or detailed seller workspace package.

| Topic | Use when |
| --- | --- |
| Second Brain | The user asks how Bob captures context, decisions, patterns, memory, or reusable team knowledge. |
| Document Management System | The user asks how Bob helps with documents, requirements, runbooks, summaries, version context, or documentation debt. |
| Knowledge Transfer Hub | The user asks about onboarding, handoffs, tribal knowledge, system understanding, or team learning. |
| SDLC Control Tower | The user asks about delivery visibility, governance, quality signals, risk, traceability, or control tower narratives. |
| Code + Runtime Modernization | The user asks about modernization, legacy code, runtime upgrades, refactoring, containers, dependency risk, or migration documentation. |
| Generic Topic Conversion | The user provides a new “Bob as…” or “Bob for…” idea not already listed. |
| Seller Partner | The user asks how Bob can help IBM sellers as a seller partner, onboarding coach, account strategist, or digital operations assistant. |
| Seller Onboarding Coach | The user asks for seller profile onboarding, Bob adoption guides, guided labs, or workspace setup graphics. |
| Account Strategist | The user asks about account profiles, stakeholder maps, opportunity maps, qualification, risks, or next-best actions. |
| Meeting Notes Engine | The user asks how Bob processes meeting notes, transcripts, follow-ups, action items, or account updates. |
| Sales Execution Partner | The user asks about discovery prep, demo prep, outreach, account plans, proposals, executive briefs, or why-change/why-IBM/why-now messaging. |
| Confidence Loop | The user asks about confidence scoring, MEDDICC/BANT gaps, evidence quality, missing information, or how Bob asks better questions before advising. |
| AGENTS Seller Harness | The user asks to create a full Bob seller partner workspace, AGENTS.md, operating harness, or reusable seller mode package. |

## Seller Partner Harness Pattern

When the request is based on a seller partner operating harness, use the pattern from `seller_partner_visual_templates.md`: **ask, capture, score, improve, save, and teach reuse**. Treat Bob as a seller partner, onboarding coach, account strategist, and digital operations assistant.

| Seller-Partner Area | Required Treatment |
| --- | --- |
| Seller onboarding | Show staged profile creation, safe capture, confidence scoring, and reusable Markdown memory. |
| Account onboarding | Show account profile creation, stakeholder mapping, opportunity mapping, qualification gaps, and next-best actions. |
| Meeting notes intake | Show confidentiality confirmation, recap, stakeholder signals, account updates, actions, follow-up drafts, and confidence changes. |
| Sales execution | Show evidence review, confidence display, discovery/demo/proposal/account-plan support, and reusable prompt teaching. |
| Mode creation | Show repeated workflow detection, mode proposal, approval gate, and reusable prompt shortcut. |
| Confidence scoring | Show what Bob knows, what is missing, the confidence score, and the next best question before high-impact recommendations. |
| Privacy and approvals | Always include approval boundaries for sensitive seller, customer, pipeline, pricing, personal, meeting, CRM, or external-action data. |

If the user asks for a full `AGENTS.md`, seller workspace package, or harness rather than a visual one-pager, produce a Markdown operating harness with the sections listed in `seller_partner_visual_templates.md` and use `seller_partner_harness.md` as the detailed reference. Do not edit an existing AGENTS.md or imply system-of-record updates without explicit user approval.

## Copywriting Standards

Write the visual copy as if it will be shown directly to a client executive, product leader, engineering leader, transformation stakeholder, or IBM seller audience, depending on the request. Favor outcome words such as **visibility**, **governance**, **traceability**, **rework reduction**, **readiness**, **knowledge reuse**, **faster understanding**, **account confidence**, **next-best action**, and **seller memory**.

Keep claims grounded. Prefer “helps,” “supports,” “can assist,” and “makes it easier to” over absolute claims such as “eliminates,” “guarantees,” or “fully automates.” If the user provides specific numbers or ROI claims, treat them as briefing assumptions unless externally verified.

## Standard Generation Prompt Requirements

When generating a one-pager, include all of the following in the image prompt:

- The exact title and subtitle.

- A six-panel instruction with exact headings and bullets.

- “Do not include internal email CTA language, salesy wording, QR codes, fake logos, or any Step 7.”

- “Exclude any blurred-face details from the reference.”

- A bottom strip with four exact benefits.

- Three speech-bubble questions.

- A request for large, legible, client-facing text.

## Revision Rules

When a user requests a change to an existing one-pager, edit the existing image and change only the requested content where possible. Preserve the whiteboard style, layout, mascot, icons, panel structure, colors, and non-target text. For example, if the user says “remove Step 7,” remove the full Step 7 panel and rebalance into six panels, rather than cropping or leaving a blank space.

## Supporting Markdown Guide Pattern

For client-facing series or strategic graphics, create a short Markdown guide with this table:

| Graphic | Best Use | Conversation Opener |
| --- | --- | --- |
| [Title] | [When to use it] | [One diagnostic question] |

Then add a short paragraph titled “Suggested Positioning” and one “Suggested Follow-Up Line.” Do not include author attribution.

---

## ibm-bob-whiteboard-storyboard

