# Google Workspace OAuth for n8n

## Recommended topology
Use one dedicated DealOS Workspace user, e.g. `deals@yourdomain.com`.

## Google Cloud
1. Create/select a Google Cloud project dedicated to DealOS.
2. Enable Gmail API, Google Calendar API and Google Drive API.
3. Configure OAuth consent.
4. If you control a Workspace organization, prefer the appropriate internal organizational configuration; otherwise follow Google's verification/publishing requirements for the scopes you request.
5. In n8n, start creating the Google credential and copy the exact **OAuth Redirect URL** n8n displays.
6. In Google Cloud Credentials, create an OAuth client of type **Web application** and add that redirect URL exactly.
7. Paste Client ID and Client Secret into n8n and connect the dedicated DealOS account.

## Least privilege
Gmail: practical default is `gmail.modify` for read/label/compose/reply/send workflows.
Calendar: request only the event/calendar access needed by the node.
Drive: prefer file-level access to the DealOS folder/files; broaden only if necessary.

Do not paste Google refresh tokens into prompts or `.env`; n8n's encrypted credential store owns them.
