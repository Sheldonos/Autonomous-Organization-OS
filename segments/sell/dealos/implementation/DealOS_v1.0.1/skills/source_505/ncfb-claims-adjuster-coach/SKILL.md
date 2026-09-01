---
name: ncfb-claims-adjuster-coach
description: >
  Use when an NC Farm Bureau agent needs to evaluate a property damage, hail, auto, or
  home insurance claim. Walks through structured decision frameworks for roof damage, hail,
  and auto claims — covering coverage verification, functional vs. cosmetic damage,
  deductible math, escalation triggers, and documentation checklists. Activate on phrases
  like "how do I handle this claim", "is this covered", "hail damage", "roof claim",
  "ACV vs RCV", "functional damage", "when do I escalate", "what documents do I need",
  "total loss", "FNOL", or any NCFB claim evaluation question.
---

# NCFB Claims Adjuster Coach

This skill walks the agent through a structured claim evaluation. Follow every step in order.
Never skip a step. Never make a final coverage decision — guide the agent to make one.

---

## Step 1 — Open the Session

Ask the agent one opening question before proceeding:

> *"What type of claim are we working on today? (Roof damage, hail, auto, home, or something else?) Walk me through what you're seeing."*

Based on the answer, apply the matching framework below.

---

## Step 2 — Apply the Correct Decision Framework

### ROOF DAMAGE CLAIMS

**Step 2.1 — Verify Policy Coverage**
- Use `read_file` or ask the agent to confirm: Was the policy active on the date of loss?
- Confirm coverage type from the dec page: **ACV** (actual cash value, depreciation applied) or **RCV** (replacement cost value, full replacement paid).
- Check for any roof exclusions or age-related limitations on the policy.
- *New agent note: Always pull the dec page first. Never assume coverage.*

**Step 2.2 — Identify and Document Damage Type**
- Ask: What caused the damage? (Wind / Hail / Impact / Water / Age-Wear)
- Confirm it is a **covered peril** — normal wear and age is NOT covered.
- Identify what is damaged: roof deck, shingles, flashing, gutters, interior water intrusion.
- Confirm photos have been or will be taken **before any repairs begin**.

**Step 2.3 — Determine Functional vs. Cosmetic**
- Estimate the percentage of the total roof affected.
- Is the damage **functional** (affects ability to protect the home) or **cosmetic** (appearance only)?
  - Functional → covered, proceed.
  - Cosmetic only → `[CONFIRM WITH SUPERVISOR — NCFB POLICY ON COSMETIC DAMAGE]`

**Step 2.4 — Calculate Net Claim Value**
- Require a written estimate from a licensed contractor.
- Apply the deductible:
  - Repair cost ≤ deductible → **no payout** — document and close. Remind agent: filing when below deductible harms the policyholder's loss history.
  - Repair cost > deductible → net payout = estimate − deductible (− depreciation if ACV).
- For RCV policies: initial payment = ACV; recoverable depreciation paid after repairs complete + receipts submitted.

**Step 2.5 — Check Escalation Triggers** (see Step 3)

**Step 2.6 — Run Documentation Checklist** (see Step 4)

---

### HAIL DAMAGE CLAIMS

**Step 2.1 — Verify the Storm Event**
- Confirm storm date matches policy active period.
- Pull third-party weather verification (NOAA, CoreLogic, or Verisk) **at the specific property address** — not just "in the area."

**Step 2.2 — Verify Hail Size**
- Do NOT rely on the policyholder's description of hail size.
- Minimum size threshold: `[CONFIRM WITH SUPERVISOR — NCFB MINIMUM HAIL SIZE THRESHOLD]`
- Industry standard reference: ≥ 1 inch (quarter-size) for roof coverage.
- Source hail size from weather data only.

**Step 2.3 — Inspect for Functional Damage**
- Functional damage: granule loss exposing asphalt, dents to metal components (flashing, vents, gutters), cracked/fractured shingles.
- Cosmetic only: surface denting with no structural impact, minor paint marks.

**Step 2.4 — Apply Damage Density Test**
- Inspect a 10 sq ft test square. Count functional hail hits.
- Threshold: `[CONFIRM WITH SUPERVISOR — NCFB MINIMUM HIT DENSITY PER 10 SQ FT]`
  - Below threshold → cosmetic only → document and review for denial with supervisor.
  - At or above → functional damage → proceed to estimate.

**Step 2.5 — Distinguish by Property Type**
- Roof → apply functional damage test above.
- Siding → functional if denting compromises weather barrier.
- Vehicle → any hail denting on a covered vehicle is covered under comprehensive (auto policy, not homeowners).
- HVAC/AC → fin damage covered if it impacts unit performance.

**Step 2.6 — Calculate Net Claim Value**
- Same deductible logic as roof damage.
- **Check for a SEPARATE hail deductible on the dec page** — this is a common mistake.

**Step 2.7 — Check Escalation Triggers** (see Step 3)

**Step 2.8 — Run Documentation Checklist** (see Step 4)

---

### AUTO DAMAGE CLAIMS

**Step 2.1 — Classify the Claim**
- **Collision** — vehicle struck another object or was struck.
- **Comprehensive** — non-collision: hail, flood, fire, theft, animal strike, glass.
- **Glass-only** — windshield/window only (may carry no deductible depending on policy).

**Step 2.2 — Verify Coverage**
- Is this vehicle listed on the policy on the date of loss?
- Is collision/comprehensive active? Not all policies carry both.
- What is the deductible for this coverage type?

**Step 2.3 — Determine Repair vs. Total Loss**
- Get an estimate from an approved appraiser or shop.
- Total loss threshold: `[CONFIRM WITH SUPERVISOR — NCFB TOTAL LOSS THRESHOLD %]`
  - If repair cost ≥ threshold % of ACV → total loss → pay ACV minus deductible, take title.

**Step 2.4 — Check Escalation Triggers** (see Step 3)

**Step 2.5 — Run Documentation Checklist** (see Step 4)

---

## Step 3 — Escalation Triggers

Stop the evaluation and instruct the agent to **immediately involve a senior adjuster** if ANY of these are true:

| Trigger | Why |
|---|---|
| Damage cause is disputed by policyholder | Coverage depends on cause — disputed cause = potential litigation |
| Pre-existing damage present alongside new damage | Must separate covered new from non-covered prior damage |
| Estimated loss exceeds `[CONFIRM — NCFB HIGH-VALUE THRESHOLD]` | Large claims require senior review before any commitment |
| Policyholder threatens legal action or mentions an attorney | Claims management must be notified immediately |
| Claim involves bodily injury alongside property damage | Liability exposure — requires separate handling |
| Cause of damage is ambiguous (could be covered or excluded) | Exclusion determinations carry legal risk |
| Policyholder disputes a cosmetic-only denial | Most common dispute category — senior review required before final denial |
| Unknown contractor with unusually high estimates | Fraud awareness — document and flag |

---

## Step 4 — Documentation Checklist

Before the agent closes any claim, confirm every applicable item is complete. Ask the agent to confirm each one.

**Required for every claim:**
- [ ] Date of loss confirmed and documented
- [ ] Policy verified active on date of loss
- [ ] Coverage type and deductible confirmed from dec page
- [ ] Cause of damage documented (covered peril confirmed)
- [ ] Photographs of all damage taken **before any repairs**
- [ ] Written repair estimate from licensed contractor or appraiser
- [ ] Deductible applied and net payout calculated
- [ ] Policyholder notified of decision in writing

**Additional — Hail claims:**
- [ ] Third-party weather verification attached (NOAA or equivalent)
- [ ] Hail size at property location documented
- [ ] Functional vs. cosmetic determination documented with reasoning
- [ ] Separate hail deductible checked and applied if applicable

**Additional — Total Loss (Auto):**
- [ ] ACV calculation documented with source
- [ ] Total loss threshold applied and documented
- [ ] Title transfer initiated
- [ ] Salvage value handled per NCFB procedure

---

## Step 5 — Quick Vocabulary Reference

Provide this when an agent asks about a term:

| Term | Definition |
|---|---|
| **ACV** | Actual Cash Value — replacement cost minus depreciation |
| **RCV** | Replacement Cost Value — full replacement cost, no depreciation |
| **Covered Peril** | A cause of damage specifically covered by the policy |
| **Excluded Peril** | A cause explicitly not covered (e.g., flood on standard homeowners, normal wear) |
| **Deductible** | Amount the policyholder pays before insurance covers the rest |
| **Dec Page** | Declarations page — summary of coverage, limits, and deductibles |
| **FNOL** | First Notice of Loss — the initial claim report from the policyholder |
| **Functional Damage** | Damage that impairs the property's ability to perform its purpose |
| **Cosmetic Damage** | Damage to appearance only, no functional impact |
| **Total Loss** | When repair cost exceeds a threshold % of the vehicle or property's value |
| **Recoverable Depreciation** | On RCV policies, withheld amount paid after repairs + receipts |
| **Subrogation** | NCFB's right to recover payout costs from an at-fault third party |
