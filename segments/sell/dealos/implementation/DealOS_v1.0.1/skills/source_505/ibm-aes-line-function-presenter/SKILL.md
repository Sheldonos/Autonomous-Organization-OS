---
name: ibm-aes-line-function-presenter
description: |A complete workflow for building client-facing IBM Agentic Engineering Suite (AES) sales presentationsthat map a prospect's confirmed dev tech stack (IDE, CI/CD, source control, testing), identify SDLCgaps, and position IBM AES solutions using the Line Function Presentation Strategist framework andAmir Mushich visual methodology. Produces a 14-slide deck that serves as a predecessor to a liveIBM Project Bob on IBM i demo. Use when a user asks to build, beautify, or generate an IBM AESsales deck, a predecessor to an IBM Bob demo, or any client-facing engineering modernizationpresentation — especially for IBM i / iSeries accounts. Triggers on IBM AES presentation,IBM Bob predecessor, line function deck, tech stack gap analysis slide, AES client deck,Sunbelt, iSeries sales deck.
---

# IBM AES Line Function Presenter

A repeatable workflow for building high-impact, client-facing IBM Agentic Engineering Suite presentations that:

- Map the client's **confirmed dev tech stack** (IDE, CI/CD, source control, testing, APM)

- Identify **SDLC velocity gaps** and match them to IBM AES solutions

- Anchor every technical slide to the client's **line function** (how they make money)

- Serve as a **predecessor** to a live IBM Project Bob on IBM i demo

---

## Workflow Overview

1. Ingest client artifacts and research the tech stack

1. Read the Line Function and Amir Mushich skills

1. Build the slide content plan (narrative + gap table)

1. Generate Amir Mushich hero visuals

1. Build and render the presentation

1. Deliver to user

---

## Step 1 — Ingest Client Artifacts & Research

**Inputs to collect:**

- Any existing PPTX/PDF decks from the client or prior engagements

- AES Persona Mapping PDF (if available)

- Client name and industry vertical

**Tech stack research sources (in priority order):**

1. RocketReach: `rocketreach.co/<company>-technology-stack`

1. BuiltWith / Wappalyzer for web-facing tools

1. LinkedIn job postings: search `<company> site:linkedin.com/jobs "RPG" OR "iSeries" OR "Bitbucket" OR "Azure DevOps"`

1. Existing PPTX/PDF artifacts from the user

**Minimum confirmed stack fields to populate before building slides:**

| SDLC Stage | Field to Confirm |
| --- | --- |
| Requirements | Ticketing tool (JIRA, Azure Boards, etc.) |
| Architecture/Design | Diagramming tool (Figma, Balsamiq, etc.) |
| IDE | Developer IDE (VS Code, RDi, Eclipse, etc.) |
| Source Control | Git platform (Bitbucket, GitHub, GitLab, ADO) |
| CI/CD | Pipeline tool (Bitbucket Pipelines, Jenkins, ADO Pipelines) |
| Database DevOps | DB platform (DB2, Oracle, SQL Server) |
| Testing | Test automation approach (manual, Selenium, Worksoft, etc.) |
| APM/Observability | Monitoring tool (Instana, Dynatrace, Datadog, Cognos, etc.) |
| Integration | API/ESB layer (MuleSoft, webMethods, none) |
| Agentic Layer | AI orchestration (none, watsonx, Copilot, etc.) |

Save all findings to a research notes markdown file before proceeding.

---

## Step 2 — Read Required Skills

Before building any content, read these two skills in full:

```
/home/ubuntu/skills/line-function-presentation-strategist/SKILL.md
/home/ubuntu/skills/amir-mushich-prompt-writer/SKILL.md
```

The **Line Function Strategist** governs the narrative: every slide must answer "how does this help the client make money?" — never lead with product features.

The **Amir Mushich** skill governs the visual direction for hero images: cinematic, high-contrast, industrial-meets-digital aesthetic.

---

## Step 3 — Build the Slide Content Plan

### Canonical 14-Slide Structure

| # | Slide Title | Purpose |
| --- | --- | --- |
| 1 | Cover | Client name + "IBM Agentic Engineering Suite" |
| 2 | Executive Summary | **Always a summary slide** — one-slide value proposition for C-suite |
| 3 | How [Client] Makes Money | Client's line function map (revenue drivers, not org chart) |
| 4 | The Engineering Bottleneck | Current SDLC friction and its direct business cost |
| 5 | Dev Tech Stack Gap Table | Confirmed stack + gaps + IBM AES fills |
| 6 | The IBM AES Overview | Suite overview as an outcome map, not a feature list |
| 7 | IBM Project Bob on IBM i | The iSeries/RPG entry point — bridge to the Bob demo |
| 8 | Persona Map | Key stakeholders and their pain points |
| 9 | Use Case 1 | Agentic intervention → line function impact |
| 10 | Use Case 2 | Agentic intervention → line function impact |
| 11 | Use Case 3 | Agentic intervention → line function impact |
| 12 | The Outcome Chain | Engineering velocity → field execution → revenue |
| 13 | Complete AES Solution Map | All strategic pillars × IBM AES tools |
| 14 | The Demo Starts Here | Bridge to live IBM Bob on IBM i demo |

### The Gap Table (Slide 5) — Most Important Slide

This slide is the primary selling tool. It must:

- Use the client's **confirmed** tools only (never assumed)

- Show gaps in **orange** — these are the selling opportunities

- Show existing tools IBM integrates with in **green** — IBM coordinates, not replaces

- Map each gap to a specific IBM AES product

**Column structure:**

```
SDLC STAGE | WHAT [CLIENT] RUNS TODAY | THE GAP | IBM AES FILLS IT WITH
```

See `references/gap-table-template.md` for a pre-built HTML pattern.

### Use Case Slides (Slides 9–11)

Each use case follows a strict 3-column layout:

- **Left (40%):** THE SITUATION — business context, not technical

- **Center (60%):** THE AGENTIC INTERVENTION — 5 numbered steps

- **Right panel or embedded:** LINE FUNCTION IMPACT — revenue/margin outcomes, no jargon

Footer: A single provocative statement anchoring the slide to the business.

See `references/use-case-template.md` for the HTML pattern.

---

## Step 4 — Generate Amir Mushich Hero Visuals

Generate **3 hero images** using the Amir Mushich prompt methodology (read the skill first):

**Cover Image:** Cinematic isometric render of the client's core physical asset (equipment, infrastructure, product) overlaid on an IBM data grid. Dark background, high contrast, orange and blue accent lighting.

**IBM i / Bob Slide Image:** IBM Power server rack in a dark data center, cinematic depth of field, blue IBM accent lighting, code overlays suggesting AI-assisted development on green-screen terminals.

**Closing Slide:** Optional. A bold typographic layout (no image) works well for the demo bridge slide.

Save all images to the project directory before building slides.

---

## Step 5 — Build the Presentation

### Visual Design System

| Element | Value |
| --- | --- |
| Background (content slides) | `#0A0A0A` |
| Background (cover/closing) | `#001141` |
| Top accent bar | `#FF6B00` (8px height) |
| Primary accent | `#0F62FE` (IBM Blue) |
| Secondary accent | `#FF6B00` (client orange) |
| Highlight text | `#FFD100` |
| Body text | `#CCCCCC` |
| Font family | IBM Plex Sans (Google Fonts) |
| Mono font | IBM Plex Mono (step numbers, code) |
| Vertical rule | `border-left: 4px solid #0F62FE` |

### Layout Rules

- **No rounded corners** — IBM design language is angular and structural

- **No CSS animations** — slides are static

- **No padding-bottom** on any container — use padding-top only

- **No absolute positioning** on main containers

- **Always use ****`min-height: 720px`** not `height: 720px`

- **Vary column ratios** per slide to avoid monotony (e.g., 40/60, 33/33/33, 25/25/25/25)

- **Footer anchor** on every content slide — one bold business statement

### Build Order

Build slides sequentially using `slide_edit`. Do not batch or parallelize. After completing all slides, run `slide_present` to render and deliver.

---

## Step 6 — IBM i / Project Bob Entry Point (Slide 7)

This slide is the bridge to the live demo. It must:

1. Acknowledge that the client runs active RPG/CL development on IBM i

1. Name the specific IDE they use today (RDi, green-screen, VS Code with IBM i extension)

1. Show the gap: no AI-native coding agent for iSeries

1. Position IBM Project Bob as the solution

1. End with: "We will show you this live."

**Key IBM i talking points:**

- Bob understands RPG IV, CL, and DDS natively

- Bob integrates with existing Bitbucket/Git workflows — no migration required

- Bob can modernize legacy RPG to free-format and generate REST APIs from existing programs

- DBmaestro governs DB2 for i schema changes in the CI/CD pipeline

---

## Adapting for Non-Sunbelt Clients

When using this skill for a different client:

1. Replace all references to "Sunbelt Rentals" with the client name

1. Replace the **line function** (how they make money) — this is the most critical customization

1. Replace the **physical asset** in the cover hero image prompt

1. Replace the **strategic pillars** with the client's business units or priorities

1. Keep the visual design system identical — it is IBM-branded, not client-branded

The gap table, use case structure, and outcome chain are universal — they require only content substitution.

---

## Reference Files

- `references/gap-table-template.md` — Pre-built gap table HTML pattern

- `references/use-case-template.md` — 3-column use case slide HTML pattern

- `references/ibm-aes-products.md` — Full IBM AES product catalog with one-line descriptions

---

## ibm-bob-demo-generator

