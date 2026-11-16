#!/usr/bin/env bash
# Build the site pages into _site/. The generated lists (talks, outputs) must exist
# before quarto runs, because Quarto resolves {{< include >}} before its
# pre-render hook runs.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_talks.py
python3 scripts/build_outputs.py
quarto render "$@"
