---
name: product-launch-architect
description: |End-to-end product launch planning workflow that transforms raw project documents or ideas into a full pre-build package — structured planning brief, research-backed technical specification, AI-generated UI mockup screens, user flow diagram, and a stakeholder briefing PPTX deck. Use when a user uploads project documents and wants to plan a new product, app, or platform before building it — especially when they need to align with investors, technical partners, or executives. Triggers on: "let's plan before we build", "help me prepare for a meeting about X", "turn these docs into a spec", "build a pitch deck for [product]", "create UI mockups for [idea]", "make a user flow for [platform]", "what should we clarify before building".
---

# Product Launch Architect

Turns raw project documents, ideas, or briefs into a complete pre-build package. Developed from the Sheldon AI Learning Platform planning workflow and reusable for any product, app, or platform.

## What This Skill Produces

1. **Planning Brief** — Synthesizes source docs into a structured brief with open questions

1. **Definitive Pre-Build Spec** — Research-backed decisions on tech stack, architecture, scope

1. **UI Mockup Screens** — 9 AI-generated screens covering key user flows

1. **User Flow Diagram** — D2-rendered diagram covering all designed + implied screens

1. **Stakeholder Briefing Deck** — PPTX tailored to a specific meeting or audience

Deliver all five or any subset based on what the user requests.

---

## Phase 1 — Intake & Planning Brief

Read every uploaded document before writing. Use the system file overview to prioritize. Extract: core vision, target users, key features, business model, tech stack (if specified), and ambiguities.

**Write the Planning Brief** → save to `{project_name}_planning_brief.md`:

```
1. Executive Summary (2-3 sentences)
2. Core Platform Pillars (3-5 pillars with descriptions)
3. Proposed Architecture (table: component | technology | purpose)
4. Critical Open Questions (numbered, grouped by: Scope, AI/Tech, Blockchain/Finance, Infrastructure, UX)
5. Next Steps
6. References (inline citations to source documents)
```

> Key principle: Surface open questions clearly — do not answer them yet. The user makes the decisions; you surface what needs deciding.

---

## Phase 2 — Research & Definitive Spec

For each unresolved technical decision, run targeted searches. Read at least 2 source URLs per decision — never rely on snippets alone.

Priority research areas:

- **Game/rendering engine**: `Unity vs Godot vs [engine] mobile [year]`

- **Blockchain network**: `[Polygon/Solana/Avalanche] rewards token compliance [year]`

- **AI architecture**: `RAG adaptive learning mobile offline edge AI [year]`

- **Compliance**: `COPPA GDPR FERPA [feature] EdTech minors`

**Write the Definitive Pre-Build Spec** → save to `{project_name}_prebuilt_spec.md`:

```
1. Executive Summary (decisions made)
2. MVP Scope & Phased Rollout
3. AI & LLM Architecture (RAG strategy, white-labeled backend, offline/edge plan)
4. Frontend / Game Engine (justified choice with trade-offs)
5. Blockchain & Tokenomics (network, compliance, wallet abstraction)
6. Development Roadmap (immediate next steps)
7. References (with URLs)
```

> Depth over width: always recommend starting with a single vertical slice (one grade, one subject, one user type) done deeply before expanding horizontally.

---

## Phase 3 — UI Mockup Screens

Generate 9 screens using `generate_image`. Use `aspect_ratio: "9:16"` for mobile-first, `"16:9"` for web/desktop. Save all to `{project_name}_ui/`.

### Standard 9-Screen Set

| # | Screen | Key Elements |
| --- | --- | --- |
| 1 | Splash / Onboarding | App name, tagline, CTA, brand aesthetic |
| 2 | Avatar / Profile Creation | Character or profile setup |
| 3 | Home Hub / Dashboard | Central nav, user stats, progress |
| 4 | World / Exploration Map | Content map, zones, categories |
| 5 | Core Activity Screen | Main value-delivery (lesson, game, tool) |
| 6 | Marketplace / Shop | In-app economy, purchases, rewards |
| 7 | Social / Leaderboard | Community, rankings, challenges |
| 8 | Progress / Learning Path | Curriculum overview, AI suggestions |
| 9 | Achievement / Reward | Certificate, badge, or milestone celebration |

Define the visual language once (color palette, style, theme) and reference it in every prompt for consistency. See `references/screen-prompts.md` for full prompt templates.

---

## Phase 4 — User Flow Diagram

### Always Include Implied Screens

Beyond the 9 designed screens, always include:

- Auth flows (sign in, sign up, SSO, password reset)

- Onboarding sub-flows (role selection, parental consent for minors, placement/diagnostic)

- Settings (account, notifications, privacy, AI/LLM config, language/theme)

- Decision diamonds (correct/incorrect, locked/unlocked, sufficient balance)

- Error/empty states

- Role-specific portals (educator dashboard, parent view, admin panel)

### Write and Render the D2 Diagram

Write to `{project_name}_user_flow.d2`. Use `direction: right`, color-coded container groups per section, `shape: diamond` for decisions, `shape: oval` for entry/exit. See `references/d2-flow-template.d2` for a pre-wired starter.

Render:

```bash
d2 --layout=elk --theme=200 {input}.d2 {output}.svg
chromium --headless --disable-gpu --screenshot={output}.png --window-size=6000,3200 "file://{output}.svg"
```

If PNG exceeds PIL's pixel limit, resize with the script in `scripts/resize_diagram.py`.

---

## Phase 5 — Stakeholder Briefing Deck

### Research the Audience First

Before writing a single slide, search `[Name] [Company] LinkedIn role background` and read their profile. Identify: domain expertise, career history, patents, publications, what they have built. The deck must speak to what this specific person cares about — not a generic pitch.

**Slide 7 rule:** Always include a slide that explicitly maps the audience's background to the platform's specific technical needs. This is the most important slide for converting a technical expert into a collaborator.

**Slide 12 rule (The Three Asks):** Be specific. State the exact deliverable, exact compensation or exchange, and exact timeline for each ask. Vague asks get vague responses.

### 14-Slide Structure

See `references/deck-slide-stubs.md` for full manus-pptx XML stubs for each slide.

| Slide | Content |
| --- | --- |
| 1 | Cover — product name, tagline, meeting context |
| 2 | What You Will Walk Away With (4-card takeaway grid) |
| 3 | The Problem (3 pillars + market stat callout bar) |
| 4 | Meet [Product] (2×2 platform pillar grid with icons) |
| 5 | The Tech Stack (5-row table: layer / technology / purpose) |
| 6 | Core Architecture (3-step flow diagram) |
| 7 | The Layer Where [Audience Name] Comes In (2-column: what we built / why your background fits) |
| 8 | The Economy / Business Mechanics (flow + stat table) |
| 9 | The User Experience (9-screen grid overview) |
| 10 | Business Model (5-column revenue cards + validation bar) |
| 11 | Roadmap (3-phase horizontal timeline) |
| 12 | The Three Asks (3 tall cards with gold top borders) |
| 13 | Why Now (2×2 urgency driver grid) |
| 14 | Closing (centered CTA + 3 next steps + contact info) |

### PPTX Design Tokens (Dark Cyberpunk / Executive)

```xml
<color name="bg-dark"         value="#0B0F19"/>
<color name="surface"         value="#1A2235"/>
<color name="neon-teal"       value="#00F0FF"/>
<color name="electric-purple" value="#B026FF"/>
<color name="gold"            value="#F5D300"/>
<color name="text-light"      value="#FFFFFF"/>
<color name="text-muted"      value="#8B9BB4"/>
<color name="grid-line"       value="#2A3655"/>
<font name="display"  family="Space Grotesk" size="56"/>
<font name="heading"  family="Space Grotesk" size="32"/>
<font name="metric"   family="Space Grotesk" size="48"/>
<font name="body"     family="Inter"         size="18"/>
<font name="caption"  family="Inter"         size="14"/>
```

Recurring fixed elements on every slide:

- Corner bracket motif (top-left of content containers): two 34px L-shaped neon-teal lines

- Slide number bottom-right: `<text x="1180" y="680" width="40" height="24" font="caption" size="14" color="neon-teal" align="right">{n}</text>`

- Accent underline below title: `<shape type="line" x="60" y="{title_bottom+8}" width="120" height="0" stroke="neon-teal" stroke-width="3"/>`

Guardrails: max 2 neon accent colors per slide · no rounded corners · no glowing text shadows · no warm/light backgrounds · body min 15px · captions min 13px.

---

## Delivery Checklist

- [ ] Planning brief surfaces open questions (not answers)

- [ ] Pre-build spec resolves every open question with a cited source URL

- [ ] All 9 UI screens are consistent in aesthetic and saved to `{project}_ui/`

- [ ] User flow diagram includes both designed and implied screens

- [ ] Deck slide 7 explicitly maps audience background to platform needs

- [ ] Deck slide 12 (Three Asks) is specific: deliverable, compensation, timeline

- [ ] All files prefixed with `{project_name}` for easy identification

---

## psychopolitical-campaign-manager

