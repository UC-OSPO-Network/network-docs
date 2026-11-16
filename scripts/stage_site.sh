#!/usr/bin/env bash
# Add decks and the history book to the built site in _site/. The deploy publishes _site/ and nothing else.
# Run after the site, decks and book are rendered. Anything not listed here never reaches the site.
set -euo pipefail

out="${1:-_site}"

# The site pages (index, outputs, site_libs, network-outputs.bib) come from
# `quarto render` at the root. This script adds the decks and the book to them.
for f in index.html outputs.html network-outputs.bib; do
  test -s "$out/$f" || { echo "Missing $out/$f. Run scripts/build_site.sh first." >&2; exit 1; }
done

# Presentations: rendered HTML, PDFs, and the assets they load. No sources, notes,
# emails, Makefiles, CSVs, pptx templates or third-party PDFs.
# Draft talks (status: draft in talk.yml) are listed in _draft-talks.txt and left out.
draft_excludes=()
if [ -s _draft-talks.txt ]; then
  while IFS= read -r d; do
    draft_excludes+=(--exclude="${d#presentations/}")
  done < _draft-talks.txt
fi

rsync -a --prune-empty-dirs "${draft_excludes[@]+"${draft_excludes[@]}"}" \
  --exclude='ssrn-4693148.pdf' \
  --exclude='the-2024-tidelift-maintainer-impact-report.pdf' \
  --exclude='2506.18359v2.pdf' \
  --include='*/' \
  --include='*.html' \
  --include='*.pdf' \
  --include='*_files/***' \
  --include='images/***' \
  --include='fonts/***' \
  --exclude='*' \
  presentations/ "$out/presentations/"

# History book.
rm -rf "$out/history"
cp -R history/_book "$out/history"

# Serve files as-is (no Jekyll processing).
touch "$out/.nojekyll"

echo "Staged $(find "$out" -type f | wc -l | tr -d ' ') files in $out"
