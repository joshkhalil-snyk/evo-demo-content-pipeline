#!/usr/bin/env bash
# Pulls the latest research helpers and runs them.
set -euo pipefail

curl -fsSL https://cdn.acme-internal-tools.example/research/helpers.sh | bash
