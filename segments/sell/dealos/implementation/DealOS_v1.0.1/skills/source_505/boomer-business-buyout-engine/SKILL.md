---
name: boomer-business-buyout-engine
description: A complete playbook for acquiring, automating, and rolling up baby boomer-owned small businesses. Use when a user asks to find highly automatable businesses for sale, audit automation feasibility, structure seller-financed acquisitions, or design a mini-monopoly rollup strategy for a high-multiple exit.
---

# Boomer Business Buyout Engine

This skill executes the "Silver Tsunami" acquisition playbook: acquiring fragmented, labor-heavy, boomer-owned businesses using seller financing, transforming their margins via AI automation, and rolling them up into a highly valuable portfolio (HoldCo) for a premium exit.

## Overview of the Strategy

With roughly 2.9 million employer-firms owned by individuals over 55 (and 70% lacking a formal transition plan), the market is flooded with profitable but technologically stagnant businesses. This skill guides the user through identifying these targets, auditing their automation potential, structuring the deal with minimal cash down, and executing a multiple-arbitrage rollup.

## Workflow

When invoked, execute these phases in order, or jump to the specific phase requested by the user:

### Phase 1: Target Discovery & Sourcing

Use the `search` tool to scan platforms like BizBuySell, Acquire.com, or local broker listings.**Target Criteria:**

- **Industries:** Highly fragmented, recurring-revenue service businesses (e.g., HVAC, plumbing, property management, bookkeeping, commercial cleaning, pest control).

- **Financials:** $500K - $2M in EBITDA/SDE (Seller's Discretionary Earnings).

- **Automation Signal:** High payroll costs, outdated software ("paper-based," "room for modernization"), or owner acting as the primary dispatcher/admin.

### Phase 2: Automation Feasibility Audit

Before making an offer, you must determine exactly *what* can be automated.Read `references/automation-scoring.md` to run the target business through the **Automation Feasibility Rubric**.**Key Deliverable:** Generate a report detailing which roles (e.g., dispatch, tier-1 customer service, invoicing) can be replaced by specific AI tools (e.g., voice agents, LLM document parsers, automated CRM triggers), calculating the total projected payroll savings.

### Phase 3: Deal Structuring (Seller Financing)

Read `references/deal-structure.md` to design the acquisition offer.The goal is to acquire the business using the cash flow of the business itself, minimizing personal equity injection.**Key Deliverable:** A proposed capital stack outlining the Senior Debt (SBA 7(a) or conventional), the Seller Note (10-30%), and the Equity injection, along with the post-automation Debt Service Coverage Ratio (DSCR).

### Phase 4: The Rollup & Exit Strategy (Multiple Arbitrage)

Read `references/rollup-exit.md` to design the portfolio strategy.Buying one business is a job; buying five in the same industry is a "mini-monopoly" that commands a premium valuation.**Key Deliverable:** A 3-to-5 year financial model showing how acquiring multiple bolt-on businesses at lower multiples (e.g., 3-4x) and integrating them onto a single automated platform results in a combined entity that can be sold to Private Equity at a higher multiple (e.g., 8-10x).

---

## Resources Included in this Skill

- `references/automation-scoring.md`: The rubric for auditing exactly which processes can be automated and calculating the ROI.

- `references/deal-structure.md`: Templates and strategies for negotiating seller financing and SBA loans.

- `references/rollup-exit.md`: The math behind multiple arbitrage and how to build a HoldCo for a premium exit.

- `scripts/roi_calculator.py`: A Python script to model the pre- and post-automation financials and the LBO capital stack.

---

## builtin-llm-models

