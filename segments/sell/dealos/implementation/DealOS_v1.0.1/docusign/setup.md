# DocuSign Setup

Goal: let DealOS prepare and route envelopes while keeping final owner signature human-controlled.

1. Start in a DocuSign developer account.
2. Create an Integration Key.
3. Configure OAuth/JWT for the server integration and grant the required one-time user consent.
4. Store the RSA private key only in `secrets/docusign_private_key.pem` (gitignored).
5. Configure integration key, user ID, account ID and demo base URLs in `.env`.
6. Build/test templates for NDA, MSA, SOW, teaming agreement as appropriate.
7. Move to production only after DocuSign production requirements are met.
8. Keep `OWNER_SIGNATURE_REQUIRED=true`.

Recommended pattern:
DealOS draft -> compliance gate -> owner approval if required -> DocuSign envelope prepared -> owner/signatory receives normal DocuSign signing flow -> completion webhook updates DealOS.
