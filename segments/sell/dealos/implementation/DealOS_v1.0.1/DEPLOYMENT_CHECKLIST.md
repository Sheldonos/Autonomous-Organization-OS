# Deployment Checklist

## Identity and authority
- [ ] dedicated legal business entity selected for DealOS transactions
- [ ] owner/delegated signatory identified
- [ ] `OWNER_EMAIL` set
- [ ] approved capability claims loaded to Drive
- [ ] approved pricing and negotiation floors set
- [ ] government registrations/certifications verified before referenced

## Infrastructure
- [ ] domain DNS configured
- [ ] VPS hardened
- [ ] Docker installed
- [ ] `.env` populated
- [ ] n8n encryption key generated
- [ ] DealOS internal API key generated
- [ ] Caddy HTTPS healthy
- [ ] database backups configured

## Google
- [ ] dedicated DealOS mailbox
- [ ] SPF
- [ ] DKIM
- [ ] DMARC
- [ ] Google OAuth project
- [ ] Gmail API enabled
- [ ] Calendar API enabled
- [ ] Drive API enabled
- [ ] n8n OAuth redirect URL registered
- [ ] Gmail credential connected
- [ ] Calendar credential connected
- [ ] Drive credential connected

## Government
- [ ] SAM API key
- [ ] NAICS filters reviewed
- [ ] set-aside filters reviewed
- [ ] prohibited contingent compensation remains disabled
- [ ] procurement counsel reviews any transaction-based federal brokerage compensation

## OpenAI / Manus
- [ ] OpenAI API key
- [ ] monthly model budget set
- [ ] high-value model threshold set
- [ ] Manus disabled initially or API key configured
- [ ] Manus webhook signature verification tested

## Closing
- [ ] DocuSign demo integration tested
- [ ] Stripe test mode tested
- [ ] owner signature required
- [ ] autonomous money movement disabled

## Autonomy validation
- [ ] unsubscribe test passes
- [ ] fake-certification test stops
- [ ] unknown bank-change instruction triggers red stop
- [ ] unusual indemnity triggers orange approval
- [ ] routine follow-up runs green
- [ ] normal calendar booking runs green/blue
- [ ] owner weekly digest generated
- [ ] owner approval email command works
- [ ] all actions appear in audit log
