# Stripe Billing Setup

1. Start in Stripe test mode.
2. Create a server-side secret/restricted key suitable for Customers, Invoices and Billing objects used by DealOS.
3. Set `STRIPE_SECRET_KEY`.
4. Add webhook `https://YOUR_DEALOS_DOMAIN/hooks/stripe`.
5. Store webhook signing secret as `STRIPE_WEBHOOK_SECRET`.
6. DealOS Core verifies the `Stripe-Signature` header with `STRIPE_WEBHOOK_SECRET`; test this before production.
7. Prefer draft invoice creation after commercial terms are approved/signed.
8. For recurring services, use Stripe subscriptions/Billing where appropriate; for large B2B invoices, consider ACH methods supported by your account.
9. Keep payouts, arbitrary transfers, refunds and bank-detail changes outside autonomous authority.

The included Core fails closed when Stripe is disabled or a webhook signature is invalid. It includes a draft-invoice endpoint; automatic finalization/payment remains outside v1 authority.
