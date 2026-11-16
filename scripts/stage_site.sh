#!/usr/bin/env bash
# Assemble _site/ from built files only. The deploy publishes _site/ and nothing else.
# Run after every quarto render step. Anything not listed here never reaches the site.
set -euo pipefail

out="${1:-_site}"
rm -rf "$out"
mkdir -p "$out"

# Top-level built pages and the bibliography.
for f in index.html outputs.html network-outputs.bib; do
  cp "$f" "$out/$f"
done

# Presentations: rendered HTML, PDFs, and the assets they load. No sources, notes,
# emails, Makefiles, CSVs, pptx templates or third-party PDFs.
rsync -a --prune-empty-dirs \
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
cp -R history/_book "$out/history"

# Serve files as-is (no Jekyll processing).
touch "$out/.nojekyll"

echo "Staged $(find "$out" -type f | wc -l | tr -d ' ') files in $out"
