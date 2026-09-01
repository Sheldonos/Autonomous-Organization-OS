# n8n Credential Map

| Name | Node | Secret location |
|---|---|---|
| DealOS Gmail | Gmail / Gmail Trigger | n8n encrypted credential store |
| DealOS Calendar | Google Calendar | n8n encrypted credential store |
| DealOS Drive | Google Drive | n8n encrypted credential store |
| DealOS Core | HTTP Header Auth (optional) | n8n encrypted credential store or env |

Internal HTTP calls may use expression header:

```text
X-DealOS-Key: {{$env.DEALOS_API_KEY}}
```

Never put OAuth refresh tokens in workflow JSON.
