# DealOS Integration Contract

## Rule 1 — models do not own credentials
OpenAI and Manus generate structured recommendations. They cannot directly invoke Gmail, Calendar, Drive, Stripe or DocuSign with raw credentials.

## Rule 2 — all effects are queued
External effects go through `outbox` or `action_queue`.

## Rule 3 — policy before effect
`action_queue` evaluates action class and creates an approval record when required.

## Rule 4 — n8n is deterministic actuator
n8n reads only approved/eligible actions and uses configured OAuth/API credentials to perform the narrow operation.

## Rule 5 — audit everything
Each ingestion, suppression, approval, sent message and completed action creates an audit event.

## Rule 6 — fail closed
Unknown action types, missing credentials, unsigned webhooks and red-risk states do not execute.
