# SAM.gov Opportunity Feed

Set `SAM_API_KEY` after generating a key for your SAM.gov account.

The n8n workflow calls:

```text
https://api.sam.gov/opportunities/v2/search
```

with required dynamic `postedFrom` and `postedTo` dates, an API key, and optional NAICS/set-aside/type filters. The scan window overlaps previous runs. DealOS deduplicates by `noticeId`.

Do not treat discovery as eligibility. The compliance gate must verify solicitation-specific eligibility, registrations, representations and partner capabilities before any claim is made.
