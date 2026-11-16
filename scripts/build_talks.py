#!/usr/bin/env python3
"""Build the Talks and Home lists from presentations/*/talk.yml.

Every folder under presentations/ (except those starting with "_") needs a
talk.yml. The script writes:

  _talks-generated.md   all published talks, newest first (talks.qmd includes it)
  _talks-recent.md      the three newest published talks (index.qmd includes it)
  _draft-talks.txt      folders with status: draft, one per line; the workflow
                        does not render, export or publish them

It stops with an error when a talk.yml is missing or incomplete, or when a
published talk has no entry in network-outputs.bib.

Requires PyYAML. Run it from anywhere:  python3 scripts/build_talks.py
"""

from __future__ import annotations

import datetime
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRES = ROOT / "presentations"
BIB = ROOT / "network-outputs.bib"
REPO_TREE = "https://github.com/UC-OSPO-Network/network-docs/tree/main/presentations"
RECENT = 3
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def load_yaml(path: pathlib.Path) -> dict:
    return yaml.safe_load(path.read_text()) or {}


def date_parts(value) -> tuple[str, str, str] | None:
    """Return (year, month, day) strings from 2026, 2026-06 or 2026-06-04."""
    if value in (None, ""):
        return None
    if isinstance(value, (datetime.date, datetime.datetime)):
        return (f"{value.year:04d}", f"{value.month:02d}", f"{value.day:02d}")
    parts = (str(value).split("-") + ["00", "00"])[:3]
    return (parts[0], parts[1].zfill(2), parts[2].zfill(2))


def show_date(parts: tuple[str, str, str]) -> str:
    y, m, d = parts
    if m == "00":
        return y
    if d == "00":
        return f"{MONTHS[int(m) - 1]} {y}"
    return f"{MONTHS[int(m) - 1]} {int(d)}, {y}"


def people_from_cff(folder: pathlib.Path) -> list[str]:
    cff = folder / "CITATION.cff"
    if not cff.exists():
        return []
    names = []
    for a in load_yaml(cff).get("authors", []):
        names.append(f"{a.get('given-names', '')} {a.get('family-names', '')}".strip())
    return names


def doi_from_cff(folder: pathlib.Path) -> str | None:
    cff = folder / "CITATION.cff"
    if not cff.exists():
        return None
    for i in load_yaml(cff).get("identifiers", []):
        if i.get("type") == "doi":
            return i.get("value")
    return None


def bib_keys() -> set[str]:
    text = re.sub(r"(?m)^\s*%.*$", "", BIB.read_text())
    return set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", text))


def load_talks() -> list[dict]:
    errors, talks = [], []
    keys = bib_keys()
    for folder in sorted(p for p in PRES.iterdir() if p.is_dir() and not p.name.startswith("_")):
        slug = folder.name
        meta_path = folder / "talk.yml"
        if not meta_path.exists():
            errors.append(f"{slug}: no talk.yml. Add one, or the deck would be published without being listed.")
            continue
        t = load_yaml(meta_path)
        t["slug"] = slug
        for field in ("title", "event", "kind", "status"):
            if not t.get(field):
                errors.append(f"{slug}: talk.yml needs `{field}`")
        if t.get("status") not in ("published", "draft"):
            errors.append(f"{slug}: status must be `published` or `draft`")
        t["date_parts"] = date_parts(t.get("date"))
        t["people"] = t.get("people") or people_from_cff(folder)
        t["doi"] = t.get("doi") or doi_from_cff(folder)
        t["links"] = t.get("links") or []
        if t.get("status") == "published":
            if not t["date_parts"]:
                errors.append(f"{slug}: a published talk needs `date`")
            if not t["people"]:
                errors.append(f"{slug}: no people. Add `people:` or a CITATION.cff with authors")
            if not t["links"] and not t["doi"]:
                errors.append(f"{slug}: a published talk needs `links` or a `doi`")
            if not t.get("bib"):
                errors.append(f"{slug}: a published talk needs `bib:` (its key in network-outputs.bib)")
            elif t["bib"] not in keys:
                errors.append(f"{slug}: bib key `{t['bib']}` is not in network-outputs.bib")
        talks.append(t)
    if errors:
        sys.exit("build_talks.py:\n  " + "\n  ".join(errors))
    return talks


def link_list(t: dict) -> list[str]:
    out = []
    for link in t["links"]:
        href = str(link["href"])
        if not href.startswith(("http://", "https://")):
            href = f"presentations/{t['slug']}/{href}"
        out.append(f"[{link['label']}]({href})")
        # The workflow exports a PDF for every *slides*.html deck.
        if href.endswith(".html") and "slides" in href and not href.startswith("http"):
            out.append(f"[{link['label']} (PDF)]({href[:-5]}.pdf)")
    out.append(f"[Source]({REPO_TREE}/{t['slug']})")
    if t["doi"]:
        out.append(f"[DOI](https://doi.org/{t['doi']})")
    return out


def card(t: dict) -> str:
    when = show_date(t["date_parts"])
    people = ", ".join(t["people"])
    return (
        "::: {.resource-card}\n"
        f"### {t['title']}\n\n"
        f"**{when}** · {t['kind']} · {t['event']} · {people}\n\n"
        f"{' · '.join(link_list(t))}\n"
        ":::\n"
    )


def main() -> None:
    talks = load_talks()
    published = [t for t in talks if t["status"] == "published"]
    published.sort(key=lambda t: t["date_parts"], reverse=True)
    drafts = [t for t in talks if t["status"] == "draft"]

    (ROOT / "_talks-generated.md").write_text("\n".join(card(t) for t in published))
    (ROOT / "_talks-recent.md").write_text("\n".join(card(t) for t in published[:RECENT]))
    (ROOT / "_draft-talks.txt").write_text("".join(f"presentations/{t['slug']}/\n" for t in drafts))
    print(f"Wrote talks: {len(published)} published, {len(drafts)} draft")


if __name__ == "__main__":
    main()
