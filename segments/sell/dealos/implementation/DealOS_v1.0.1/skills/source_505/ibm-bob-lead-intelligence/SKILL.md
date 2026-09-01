---
name: ibm-bob-lead-intelligence
description: Generate comprehensive B2B lead databases with deep intelligence including decision maker contacts, pain points, IBM Automation solution mapping, ROI projections, and revenue potential. Use when prospecting for B2B sales, building lead lists, conducting market research, creating sales intelligence databases, preparing for outreach campaigns, or when a user requests lead generation with detailed business intelligence for IBM Project Bob.
---

# IBM Bob B2B Lead Intelligence Generator

This skill provides a complete workflow for generating deep, multi-level B2B lead intelligence databases specifically tailored for selling IBM Automation solutions (Turbonomic, Apptio, CP4I, watsonx, Verify) and ISV partners (e.g., Generate for Hospitals).

## Operating Modes

Before beginning, determine the appropriate mode based on the user's request:

1. **`new-account`**** Mode**: Use when the user provides a new list of target accounts or uploaded context documents. Focuses on initial ingestion and high-level C-suite mapping.

1. **`territory-filter`**** Mode**: Use when the user asks to filter an existing list by geography (e.g., "only Southeast territory"). Requires removing out-of-bounds accounts and rebuilding the database.

1. **`full-deep-analysis`**** Mode**: Use when the user requests "full deep analysis" or asks to find leads below the C-suite (VPs, Directors, Managers, Team Leads). Requires extensive parallel research across all organizational levels.

## The Workflow

Follow these steps sequentially based on the selected mode.

### Step 1: Context Ingestion (All Modes)

If the user uploads documents (e.g., Account Plans, ISV Enablement PDFs), read them thoroughly to extract account context, existing IBM footprint, and specific pain points.*Save key findings to a markdown file immediately to prevent context loss.*

### Step 2: Deep Parallel Research

Use the `map` tool to conduct parallel research on the target accounts.

**For ****`new-account`**** Mode:** Focus on C-suite and SVPs.**For ****`full-deep-analysis`**** Mode:** You MUST research all levels: C-Suite, SVPs, VPs, Directors, Managers, and Team Leads across IT, Finance, Clinical, Operations, Digital/AI, and Security departments.

*Research Requirements:*

- Identify named decision-makers and their exact titles.

- Identify specific account pain points (e.g., Epic on AWS cloud costs, M&A integration).

- Map pain points to IBM Solutions. See `references/ibm_automation_solutions.md` for the mapping guide.

### Step 3: Database Construction

Consolidate the research JSON output and build the master Excel workbook.

1. Write a Python script to build the Excel file. You can use or adapt the provided script:`python3 /home/ubuntu/skills/ibm-bob-lead-intelligence/scripts/build_excel_database.py <input_json> <output_excel>`

1. Ensure the workbook includes tabs for: Executive Dashboard, Master Lead Database, and Outreach Templates.

### Step 4: Executive Summary Generation

Create a strategic markdown playbook summarizing the findings.

1. Use the template provided at `templates/executive_summary.md`.

1. Calculate conservative 3-year TCV (Total Contract Value) pipeline estimates.

1. Highlight specific "Give-to-Get" offers (e.g., Complimentary Cloud Cost Assessment).

1. If healthcare accounts are included, you MUST include the "Generate for Hospitals" ISV play.

### Step 5: Deliverable Delivery

Deliver both the Excel workbook and the Markdown executive summary to the user via the `message` tool.

## Outreach Best Practices (Apply to Templates)

When generating outreach templates in the Excel file, adhere to these principles:

- **Consultative Tone:** Frame the message from a helpful perspective, emphasizing end-user value rather than a direct sales pitch.

- **Personalization:** Incorporate at least one personalization factor (public, private, personal, or professional connection).

- **Follow-up Protocol:** Explicitly state a 5-day follow-up plan (e.g., via email/call) if there is no immediate response.

---

## ibm-bob-requirements-orchestrator

