#!/usr/bin/env bash
# Check the staged site in _site/ before it is deployed (or, on a pull request,
# before it is merged). Fails on working files, missing pages and broken
# internal links. Broken external links are reported as warnings.
#   scripts/check_site.sh [_site] [--allow-missing-pdf]
set -euo pipefail
cd "$(dirname "$0")/.."
site="${1:-_site}"
shift || true

bad=$(find "$site" -type f \( -name '*.md' -o -name '*.qmd' -o -name '*.scss' -o -name '*.py' -o -name '*.sh' -o -name 'Makefile' -o -name '*.yml' -o -name '*.csv' -o -name '*.pptx' -o -name '.gitignore' -o -name '*.txt' \) ! -path "$site/history/*" ! -path '*_files/*')
if [ -n "$bad" ]; then
  echo "::error::Working files in $site:"; echo "$bad"; exit 1
fi

for f in index.html talks.html outputs.html network-outputs.bib history/index.html; do
  test -s "$site/$f" || { echo "::error::Missing $site/$f"; exit 1; }
done

# Unverified research notes live in history/_research/ and must never reach the book.
if [ -d "$site/history" ] && grep -rlE 'Draft - (fill in|develop)|\*Draft - ' "$site/history" >/dev/null; then
  echo "::error::Draft research notes found in $site/history:"; grep -rlE 'Draft - (fill in|develop)' "$site/history"; exit 1
fi

python3 scripts/check_links.py "$site" "$@"
