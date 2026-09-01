---
name: ibm-bob-ibmi-office-hours
description: Create client-ready IBM Bob for IBM i office-hours assets. Use when asked to prepare or revise an IBM Bob / IBM i / RPG modernization presentation, align to a client-provided agenda, research attendees, create hand-drawn Bob-style slides, produce client leave-behind master prompts, or generate presentation scripts for IBM i modernization meetings.
---

# IBM Bob for IBM i Office-Hours Workflow

Use this skill to convert a raw IBM Bob for IBM i client meeting into a complete engagement package: attendee intelligence, agenda-aligned presentation, client leave-behind prompt sheet, and presenter script. It is optimized for IBM i / RPG modernization conversations with enterprise clients such as logistics, banking, insurance, manufacturing, or distribution accounts.

## Core Principle

Anchor every asset to the client’s requested agenda and audience composition. Do not replace the client’s agenda with a generic product pitch. Use IBM Bob as a practical work partner that helps IBM i teams **explain, test, document, and propose safe changes** with humans in review.

## Standard Workflow

### 1. Ingest Inputs

Collect and preserve these inputs when available:

| Input | How to Use It |
| --- | --- |
| Client agenda screenshot or text | Make the deck follow it exactly, especially section titles and timing. |
| Existing IBM Bob intro deck or screenshots | Reuse tone, visual style, and expected agenda structure. |
| Attendee list | Research roles and map each audience segment to proof points. |
| Client public technology context | Tie IBM i/Bob use cases to real client operating systems, integrations, APIs, and business model. |
| Requested style reference | Use it as the presentation visual system. If the user asks for hand-drawn Bob style, use image slides. |

If the user provides images, respect any instruction not to re-open or re-view them. Use already-visible content from the conversation as source context.

### 2. Research the Client and Attendees

Research enough to answer: who is in the room, what they do, and what they care about. Use public sources only and mark uncertainty clearly.

Produce an attendee briefing with this structure:

| Person | Likely Role | What They Likely Do | What They Care About | Engagement Angle | Question to Ask | Confidence |
| --- | --- | --- | --- | --- | --- | --- |

Segment the room into practical groups:

| Audience Segment | Likely Concern | Message That Lands |
| --- | --- | --- |
| Application delivery leaders | Safe adoption, pilot value, governance, delivery metrics | Bob creates repeatable, reviewable work products. |
| RPG / iSeries practitioners | Accuracy, RPG/CL/Db2 nuance, tests, no hype | Bob explains first and changes only after expert review. |
| Integration / API owners | EDI/API lineage, compatibility, interface modernization | Bob maps IBM i logic to EDI/API behavior and tests. |
| IBM product/account team | Proof path, product feedback, next step | One client workflow becomes a credible Bob-for-i proof. |

### 3. Align to the Client Agenda

Create a slide outline that mirrors the requested agenda. For the ODFL-style agenda used to derive this skill, the canonical flow is:

| Agenda Section | Slide Purpose |
| --- | --- |
| Intro to Bob | Explain what Bob does for IBM i. |
| How to get it working | Show safe setup/adoption flow using sanitized artifacts. |
| Limitations | State guardrails and trust boundaries plainly. |
| Impactful RPG use cases | Map Bob to business-relevant RPG workflows. |
| Premium Package for i GA + capabilities | Present as capabilities to validate, not unsupported claims. |
| Modernization best practices | Explain, map, test, then modernize incrementally. |
| Example prompts | Give senior-developer-context prompt recipes. |
| Bug analysis | Start with symptoms, rank causes, generate tests. |
| Action items + next steps | Ask for one workflow, one code slice, one proof review. |

Always include a second slide that summarizes what each audience segment should get from the session.

### 4. Build the IBM i Narrative

Use these positioning rules:

| Do | Avoid |
| --- | --- |
| “Bob helps IBM i teams explain, test, document, and plan safe changes.” | “Bob will rewrite the system.” |
| “Modernization can happen in place with preserved behavior.” | “Modernization means leaving IBM i.” |
| “Use sanitized artifacts for the pilot.” | “Connect Bob directly to production for the first proof.” |
| “RPG experts validate Bob’s reasoning.” | “AI replaces senior RPG knowledge.” |
| “Tie use cases to freight, billing, EDI, APIs, and operational workflows.” | “Talk about generic developer productivity only.” |

For logistics/LTL clients, prioritize these use cases:

| Use Case | Why It Works |
| --- | --- |
| Shipment-status defect analysis | Connects RPG logic to customer visibility, tracking, and EDI/API outputs. |
| EDI 214 / 210 mapping | Interface-heavy, business-critical, and testable. |
| Pickup / eBOL validation | Customer-facing workflow with downstream billing and operational impact. |
| Billing/rating exceptions | High-control workflow with revenue and audit implications. |
| RPG-to-Java/mobile modernization | Good for mixed IBM i + modern app teams. |
| SOAP-to-REST support | Strong integration modernization proof. |

### 5. Generate the Presentation

Use slide tools for slide decks. Use `slide_initialize` once for a new deck. Use image mode when the user requests a visually illustrated or hand-drawn Bob style.

For hand-drawn Bob-style decks, use this design direction:

> Hand-drawn whiteboard storyboard with thick black marker lines, IBM-blue sketch highlights, green checkmarks, light gray pencil shading, friendly Bob robot wearing a blue hard hat, handwritten headings, doodle icons, dashed connector lines, and workshop-ready diagrams.

Keep slides concise. The slide itself should be easy to read; detailed explanation belongs in speaker notes or the leave-behind.

### 6. Create the Client Leave-Behind

Create a client-facing Markdown cheat sheet with extended master prompts and use cases. Include at least these prompts:

| Master Prompt | Purpose |
| --- | --- |
| IBM i / RPG code comprehension | Explain legacy RPG/CL/Db2 workflows before changes. |
| Production defect triage | Rank likely causes and produce investigation tests. |
| EDI/API data lineage | Map internal events to EDI/API outputs. |
| SOAP-to-REST modernization | Preserve behavior while drafting REST contracts. |
| RPG modernization plan | Convert/refactor safely with behavior-preserving tests. |
| Billing/rating/invoice logic review | Treat revenue and audit workflows as high-control changes. |

Each prompt should include required inputs, the master prompt text, required output format, and tags such as `#ibmi #rpg #defecttriage #edi #apimodernization`.

### 7. Generate Speaker Notes

After the deck is complete, use notes generation for all slides. The tone should be practical, consultative, and client-facing. Include transition lines and questions to ask the room.

Speaker notes should reinforce:

- The meeting follows the client’s agenda.

- Bob is a governed work partner, not a rewrite button.

- IBM i experts remain the reviewers.

- The goal is one sanitized workflow proof.

### 8. Deliver Package

Deliver, at minimum:

| Deliverable | Purpose |
| --- | --- |
| Presentation link | Client-facing deck. |
| PowerPoint export if available | Offline editable/shareable deck. |
| Attendee briefing | Internal IBM preparation. |
| Client leave-behind prompt sheet | Practical client artifact. |
| Speaker notes / script | Presenter readiness. |

If PowerPoint export times out, still deliver the slide presentation link and all supporting files. Do not claim the PPTX was created unless the file exists.

## Quality Checklist

Before delivery, verify that:

- The client’s requested agenda is visibly represented.

- The second slide summarizes what the audience gains.

- Attendee research informs, but does not overcrowd, the deck.

- IBM i / RPG practitioners are treated as validators, not replaceable resources.

- The deck ends with a concrete ask: one sanitized workflow, one code slice, one proof.

- Leave-behind prompts are copy-paste ready and include constraints and output formats.

- Speaker notes include practical presenter language and room questions.

## Reusable Prompt for Slide Generation

When generating image slides in the hand-drawn Bob style, adapt this base prompt:

```
Create a polished hand-drawn whiteboard storyboard slide in 16:9 with thick black marker border, white background, friendly Bob robot wearing an IBM-blue hard hat, black handwritten typography, IBM-blue sketch highlights and underlines, green checkmarks, light gray pencil shading, and simple enterprise doodle icons. Keep all text legible and presentation-ready. Avoid photorealism, dark UI, and generic corporate slide styling.
```

## Common Pitfalls

Do not turn the meeting into a generic IBM Bob overview if the client provided a specific agenda. Do not overstate Premium Package for i capabilities; phrase them as capabilities to validate unless confirmed by source material. Do not bury the practical next step. Do not use attendee research to make private or sensitive claims; use it only to tailor the conversation.

## Suggested File Names

Use predictable working filenames:

| File | Purpose |
| --- | --- |
| `attendee_briefing.md` | Internal attendee research and engagement strategy. |
| `agenda_aligned_deck_outline.md` | Slide narrative before deck creation. |
| `client_leavebehind_ibmi_prompts.md` | Client prompt/use-case cheat sheet. |
| `slide_notes.md` | Presentation script generated from final deck. |

---

## ibm-bob-lead-intelligence

