#!/usr/bin/env python3
"""Check history/_data/places.yml and write history/_data/places.json.

The book's pre-render step runs this. The `on-campus` and `places-map`
shortcodes (history/_filters/places.lua) read the JSON file.

  python3 scripts/build_places.py [history_dir]

Checks (any failure stops the render):
- every entry has the required fields, and ids are unique;
- a pinned entry has coordinates in California;
- a history entry names a chapter file, and that chapter has a heading with
  the id {#<id>}, so map popups and boxes link to a real section;
- every link has a label, an https URL, and a known kind.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

import yaml

REQUIRED = ("id", "layer", "pin", "name", "campus", "place", "links")
LAYERS = {"history", "today", "related"}
KINDS = {"project", "steward", "unit", "campus", "archive", "heritage"}
# A loose box around California. It catches swapped or mistyped coordinates.
LAT = (32.0, 42.5)
LON = (-124.6, -114.0)


def main() -> int:
    book = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent.parent / "history")
    src = book / "_data" / "places.yml"
    places = yaml.safe_load(src.read_text(encoding="utf-8"))
    errors: list[str] = []
    seen: set[str] = set()

    for p in places:
        pid = p.get("id", "?")
        for field in REQUIRED:
            if field not in p:
                errors.append(f"{pid}: missing {field}")
        if pid in seen:
            errors.append(f"{pid}: duplicate id")
        seen.add(pid)
        if p.get("layer") not in LAYERS:
            errors.append(f"{pid}: layer must be one of {sorted(LAYERS)}")
        if p.get("pin"):
            lat, lon = p.get("lat"), p.get("lon")
            if not (isinstance(lat, (int, float)) and isinstance(lon, (int, float))):
                errors.append(f"{pid}: pinned but has no lat/lon")
            elif not (LAT[0] <= lat <= LAT[1] and LON[0] <= lon <= LON[1]):
                errors.append(f"{pid}: lat/lon {lat},{lon} is outside California")
        if p.get("layer") == "history":
            chapter = p.get("chapter")
            if not chapter:
                errors.append(f"{pid}: history entry has no chapter")
            else:
                path = book / chapter
                if not path.exists():
                    errors.append(f"{pid}: chapter {chapter} not found")
                elif not re.search(r"^#+ .*\{#" + re.escape(pid) + r"\}", path.read_text(encoding="utf-8"), re.M):
                    errors.append(f"{pid}: no heading with {{#{pid}}} in {chapter}")
        for link in p.get("links") or []:
            if not link.get("label") or not str(link.get("url", "")).startswith("https://"):
                errors.append(f"{pid}: link needs a label and an https URL: {link}")
            if link.get("kind") not in KINDS:
                errors.append(f"{pid}: link kind {link.get('kind')!r} not in {sorted(KINDS)}")

    if errors:
        print(f"{src}: {len(errors)} problem(s)", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    keep = ("id", "layer", "pin", "name", "campus", "place", "place_at_time", "prior",
            "lat", "lon", "precision", "chapter", "links", "heritage_visit")
    out = [{k: p.get(k) for k in keep} for p in places]
    dest = book / "_data" / "places.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"places: {len(out)} entries checked, wrote {dest.relative_to(book)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
