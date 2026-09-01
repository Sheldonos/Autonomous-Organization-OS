# n8n Workflows

Import JSON files in `workflows/` and re-select credentials after import.

1. `01_gmail_inbox_triage.json` — Gmail Trigger -> DealOS Core -> mark read.
2. `02_outbox_dispatch.json` — polls DealOS outbox -> send/reply via Gmail -> mark sent.
3. `03_sam_opportunity_scan.json` — hourly SAM.gov scan -> normalize -> DealOS ingest.
4. `04_manus_research_dispatch.json` — queued high-value research -> Manus task -> mark submitted.
5. `04a_openai_research_dispatch.json` — ordinary qualified research with OpenAI web search -> deal/contact/outreach pipeline.
6. `05_weekly_owner_digest.json` — Monday 08:00 owner summary email.
7. `06_action_executor.json` — polls deterministic action queue; calendar action placeholder is routed here.
8. `07_error_handler.json` — workflow error notification path.

The JSON files avoid embedding live credential IDs. After import, assign `DealOS Gmail` / `DealOS Calendar` in the relevant nodes.

Before activation, use n8n's test-run UI and verify the payload mapping against the exact node version installed. n8n node schemas evolve, so production should pin a tested n8n version after initial commissioning.

9. `09_private_market_scans.json` — daily public-signal scans for AI transformation, mainframe modernization, AI governance and proposal/RFP demand.

Additional credentialed executors:
- `06a_calendar_executor.json` — approved calendar creation.
- `06b_stripe_executor.json` — approved/safe draft invoices only.
- `06c_docusign_executor.json` — template envelope creation; action policy governs approval.
