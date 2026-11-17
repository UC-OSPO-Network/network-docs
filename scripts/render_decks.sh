#!/usr/bin/env bash
# Render every .qmd in every presentations/*/ folder, except draft talks.
# Run scripts/build_site.sh first: it writes _draft-talks.txt and the generated
# includes that the root project needs. Adding a talk needs no edit here.
set -euo pipefail
cd "$(dirname "$0")/.."
shopt -s nullglob
for dir in presentations/*/; do
  grep -qxF "$dir" _draft-talks.txt && continue
  qmds=("$dir"*.qmd)
  [ ${#qmds[@]} -eq 0 ] && continue
  echo "::group::Render ${dir}"
  for qmd in "${qmds[@]}"; do
    # Slide decks: render only revealjs for the site (skips pptx). Handouts and
    # other docs: default format.
    case "$qmd" in
      *slides*) quarto render "$qmd" --to revealjs ;;
      *)        quarto render "$qmd" ;;
    esac
  done
  echo "::endgroup::"
done
