# Action Executor Configuration

`06_action_executor.json` is the generic fail-closed watcher. The package also includes dedicated deterministic executor workflows for Calendar, Stripe, DocuSign, and Drive. Keep the generic `06_action_executor.json` **inactive in production**; it is a fail-closed reference/catch-all, not a credentialed executor. Configure credentials in those workflows and leave the generic executor fail-closed as a catch-all. Supported action contracts:

## `calendar_create`
Google Calendar Create Event using `DealOS Calendar` credential. Required payload:
`summary,start,end,attendees,description`. Validate start/end against scheduling policy, then POST `/actions/{id}/complete`.

## `drive_write`
Implemented by `06d_drive_executor.json` with Google Drive **File → Create From Text**. It always writes to `GOOGLE_DRIVE_DEALOS_FOLDER_ID` and converts the text to a Google Doc. Required payload: `name,content`. Re-select the `DealOS Drive` credential after import.

## `docusign_template_envelope`
Only after DocuSign credentials/templates are configured. Prepare an envelope; do **not** impersonate owner signature. Owner/signatory receives normal DocuSign flow.

## `stripe_draft_invoice`
Only after Stripe webhook verification is implemented and commercial terms are approved/signed. Create a **draft** invoice by default.

Unknown action types must remain unexecuted. Do not add a generic arbitrary-HTTP action that lets a model call any URL.
