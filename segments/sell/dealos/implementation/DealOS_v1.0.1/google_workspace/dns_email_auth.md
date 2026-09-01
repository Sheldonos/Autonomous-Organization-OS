# Sending-domain authentication

Before meaningful outbound volume:

1. Configure the SPF record required by your mail provider.
2. Enable Google Workspace DKIM and publish the generated DKIM DNS record.
3. Publish DMARC. Begin with monitoring if necessary, then tighten after legitimate send sources are understood.
4. Use a dedicated business mailbox and accurate identity.
5. Ramp from `initial_ramp_first_touch_per_day` rather than immediately using the maximum.

DealOS does not attempt to evade provider spam controls or rotate domains to bypass reputation enforcement.
