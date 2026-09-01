# Air-gap Transfer Procedure

1. Build and validate the release in a connected staging environment.
2. Export the application image and every approved dependency image by immutable digest into the transfer package.
3. Run `python deployment/airgap/make_transfer_manifest.py <transfer-directory>`.
4. Sign the resulting manifest using the organization's approved signing system.
5. Move through the guarded-transfer/malware-inspection process.
6. In the enclave, verify every hash before importing images or files.
7. Run with `deployment/docker-compose.airgap.yml` or the tenant's equivalent internal-only orchestrator profile.
8. Do not configure external MCP URLs, telemetry endpoints, package repositories or public model endpoints.

The cold-room environment needs a locally approved agent/model executor for autonomous reasoning. Without one, FAOS continues to route, queue, hydrate and maintain state but returns jobs as ready for an executor rather than leaking them outward.
