#!/usr/bin/env bash
set -euo pipefail
if [[ ! -f .env ]]; then echo 'Missing .env. Copy .env.example -> .env and fill REQUIRED values.' >&2; exit 1; fi
python scripts/validate_package.py
docker compose up -d --build
echo "DealOS started. Check: https://${DEALOS_DOMAIN:-your-dealos-domain}/health"
