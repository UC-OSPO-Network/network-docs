#!/usr/bin/env bash
# Build the site pages into _site/. Quarto resolves {{< include >}} before its
# pre-render hook runs, so the generated Outputs file must exist first.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_outputs.py
quarto render "$@"
