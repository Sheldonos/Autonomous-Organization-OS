# Account and Knowledge Model

DealOS separates **knowledge** from **credentials**.

## What agents may know

- which legal entity is acting;
- approved brand/sender identity;
- approved capabilities and evidence references;
- public/non-secret account IDs and registrations (for example UEI/CAGE or Stripe/DocuSign account reference);
- authorized Gmail mailbox, Calendar, and Drive root;
- commercial floors and negotiation envelope;
- customers/partners explicitly entered as approved relationship context;
- deal history stored in Postgres;
- evidence/source URIs pointing to controlled Drive files.

These live in `config/business_profile.yaml`, `config/account_registry.yaml`, policy YAML, and Postgres.

## What agents may never know

- raw Gmail/Google OAuth tokens;
- passwords;
- API secrets;
- bank/routing/account numbers;
- card details;
- DocuSign private keys;
- Stripe secret keys or webhook signing secrets;
- server SSH private keys.

These remain in n8n credentials, container secrets, or the server environment.

## Source-of-truth order

1. signed agreement / authoritative source document;
2. approved business profile and account registry;
3. DealOS Postgres deal/relationship state;
4. evidence-backed current public research;
5. model inference (never treated as a fact).

If two higher-priority sources conflict, the system escalates rather than guessing.

## Initial knowledge load

1. Copy `config/business_profile.example.yaml` to `config/business_profile.yaml`.
2. Copy `config/account_registry.example.yaml` to `config/account_registry.yaml`.
3. Put supporting files in the controlled Drive folder structure documented in `TOOLING_AND_CONFIGURATION.md`.
4. Add only evidence-backed capabilities/case studies to the approved profile.
5. Keep secrets out of YAML and Drive whenever a credential vault/environment variable can be used instead.
