# Private-Market Autonomous Origination Loop

When `PRIVATE_MARKET_SCANS_ENABLED=true`, `HUNTER_ENABLED=true`, `OUTREACH_AUTONOMOUS_ENABLED=true`, and a lane in `config/business_profile.yaml` is enabled:

1. daily n8n scan calls DealOS lane scanner;
2. OpenAI web search returns current, cited public buying/need signals;
3. opportunities are deduplicated and queued for deeper research;
4. research identifies verified organization/domain/decision-maker candidates and a 0–100 qualification score;
5. qualified opportunities become Deal records;
6. Hunter is called only for a qualified named decision maker missing a professional email;
7. suppressed contacts are excluded;
8. OpenAI drafts a short first-touch email using **only** approved offer text + verified facts;
9. message enters DealOS outbox;
10. n8n sends through the dedicated Gmail account;
11. replies return through the inbox workflow, which handles opt-outs/routine replies and escalates exceptions.

The system will not send autonomous private-market first touch until the business profile is completed and the corresponding lane is explicitly enabled. This prevents a fresh install from sending placeholder claims.
