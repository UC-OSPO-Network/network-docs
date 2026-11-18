#!/usr/bin/env python3
"""Build _outputs-generated.md from network-outputs.bib.

outputs.qmd includes the generated file. The script also writes
_catalog-recent.md (the newest entries, for index.qmd) and _talks-redirect.md (a
map from old Talks page anchors to catalog entries, for talks.qmd). Run it, then
render the pages:

    python3 scripts/build_outputs.py
    quarto render outputs.qmd

The script uses only the Python standard library and the pandoc that ships with
Quarto. It formats every entry with citeproc in APA style, groups the entries by
the first word in their `keywords` field, and sorts each group newest first.
Entries whose key is the `bib:` of a talk in presentations/*/talk.yml also get
that talk's slide, handout and source links.
"""

from __future__ import annotations

import html
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BIB = ROOT / "network-outputs.bib"
OUT = ROOT / "_outputs-generated.md"
RECENT_OUT = ROOT / "_catalog-recent.md"
REDIRECT_OUT = ROOT / "_talks-redirect.md"
RECENT = 3

sys.path.insert(0, str(ROOT / "scripts"))
import build_talks  # noqa: E402  (same folder; validates talk.yml)
CSL_URL = "https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl"

# (keyword, section heading). The order here is the order on the page.
SECTIONS = [
    ("lesson", "Lessons and curriculum"),
    ("software", "Software and data"),
    ("talk", "Talks, workshops, and events"),
    ("paper", "Papers"),
    ("press", "Press"),
]


def parse_fields(body: str) -> dict[str, str]:
    """Read `name = {value}` and `name = value` pairs from one entry body."""
    fields: dict[str, str] = {}
    pos = 0
    name_re = re.compile(r"\s*(\w+)\s*=\s*")
    skip_re = re.compile(r"[\s,]*")
    bare_re = re.compile(r"[^,\n]*")
    while True:
        m = name_re.match(body, pos)
        if not m:
            break
        name, pos = m.group(1).lower(), m.end()
        if pos < len(body) and body[pos] == "{":
            depth, start = 1, pos + 1
            pos += 1
            while depth and pos < len(body):
                if body[pos] == "{":
                    depth += 1
                elif body[pos] == "}":
                    depth -= 1
                pos += 1
            value = body[start : pos - 1]
        else:
            m2 = bare_re.match(body, pos)
            value, pos = m2.group(0), m2.end()
        fields[name] = value.strip()
        pos = skip_re.match(body, pos).end()
    return fields


def parse_bib(text: str) -> list[dict[str, str]]:
    text = re.sub(r"(?m)^\s*%.*$", "", text)  # drop comment lines
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        depth, i = 1, m.end()
        while depth and i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        fields = parse_fields(text[m.end() : i - 1])
        fields["_key"] = m.group(2)
        fields["_type"] = m.group(1).lower()
        entries.append(fields)
    return entries


def sort_key(entry: dict[str, str]) -> str:
    """ISO date padded to YYYY-MM-DD so that newer entries sort later."""
    raw = entry.get("date") or entry.get("year") or ""
    start = raw.split("/")[0]
    parts = (start.split("-") + ["00", "00"])[:3]
    return "-".join(parts)


def section_of(entry: dict[str, str]) -> str:
    words = [w.strip() for w in entry.get("keywords", "").split(",") if w.strip()]
    known = {token for token, _ in SECTIONS}
    if not words or words[0] not in known:
        sys.exit(
            f"{entry['_key']}: the first word in `keywords` must be one of "
            f"{', '.join(sorted(known))}"
        )
    return words[0]


def format_entries(csl_path: pathlib.Path) -> dict[str, str]:
    """Run citeproc once over the whole file and return {key: entry html}."""
    metadata = f"---\nbibliography: {BIB}\ncsl: {csl_path}\nnocite: '@*'\n---\n"
    result = subprocess.run(
        ["quarto", "pandoc", "--from=markdown", "--to=html", "--citeproc"],
        input=metadata,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        sys.exit(result.stderr)
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    found = {}
    for m in re.finditer(
        r'<div id="ref-([^"]+)" class="csl-entry"[^>]*>\s*(.*?)\s*</div>',
        result.stdout,
        re.S,
    ):
        found[m.group(1)] = m.group(2)
    return found


def heading_id(text: str) -> str:
    """The anchor Quarto gives a heading, as on the old Talks page cards."""
    text = re.sub(r"[^\w\s.-]", "", text.lower())
    return re.sub(r"\s+", "-", text.strip())


def actions(e: dict[str, str], talk: dict | None, page: str = "") -> str:
    """One row of labelled links. Only links that really exist are shown."""
    links: list[tuple[str, str]] = []
    if talk:
        for label, href in build_talks.link_pairs(talk):
            links.append((label, href))
    hrefs = {h for _, h in links}
    doi = e.get("doi", "")
    url = e.get("url", "")
    if doi and f"https://doi.org/{doi}" not in hrefs:
        links.append(("DOI", f"https://doi.org/{doi}"))
    if url and not doi:
        local = url.replace("https://ucospo.net/network-docs/", "")
        if local not in hrefs and url not in hrefs:
            if url.lower().endswith(".pdf"):
                label = "Slides (PDF)" if "slides" in e.get("type", "").lower() else "PDF"
            else:
                label = "Web page"
            links.append((label, url))
    parts = [f'<a href="{html.escape(h)}">{html.escape(label)}</a>' for label, h in links]
    parts.append(
        f'<a class="permalink" href="{page}#{html.escape(e["_key"])}" '
        f'title="Link to this entry">Link to entry</a>'
    )
    return '<span class="entry-actions">' + " · ".join(parts) + "</span>"


def item(e: dict[str, str], rendered: dict[str, str], talks: dict, page: str = "") -> str:
    attr = "" if page else f' id="{html.escape(e["_key"])}"'
    return f'<li{attr}>{rendered[e["_key"]]}<br>{actions(e, talks.get(e["_key"]), page)}</li>'


def main() -> None:
    entries = parse_bib(BIB.read_text(encoding="utf-8"))
    if not entries:
        sys.exit(f"No entries found in {BIB}")
    with tempfile.TemporaryDirectory() as tmp:
        csl_path = pathlib.Path(tmp) / "apa.csl"
        with urllib.request.urlopen(CSL_URL, timeout=30) as resp:
            csl_text = resp.read().decode("utf-8")
        # APA adds year suffixes (2026a, 2026b) when authors and year repeat. A list
        # page does not need them, so turn that off.
        csl_text = csl_text.replace('disambiguate-add-year-suffix="true"', "")
        csl_path.write_text(csl_text, encoding="utf-8")
        rendered = format_entries(csl_path)

    missing = [e["_key"] for e in entries if e["_key"] not in rendered]
    if missing:
        sys.exit(f"citeproc produced no output for: {', '.join(missing)}")

    talks = {
        t["bib"]: t for t in build_talks.load_talks() if t.get("status") == "published"
    }

    note = "<!-- Generated by scripts/build_outputs.py from network-outputs.bib. Do not edit. -->"
    groups = []
    for token, heading in SECTIONS:
        group = sorted((e for e in entries if section_of(e) == token), key=sort_key, reverse=True)
        if group:
            groups.append((heading, group))

    jump = " · ".join(f"[{h}](#{heading_id(h)}) ({len(g)})" for h, g in groups)
    lines = [note, "", "::: {.catalog-jump}", f"Jump to: {jump}", ":::", ""]
    for heading, group in groups:
        lines += [f"## {heading}", "", "```{=html}", '<ul class="outputs">']
        lines += [item(e, rendered, talks) for e in group]
        lines += ["</ul>", "```", ""]
    OUT.write_text("\n".join(lines), encoding="utf-8")

    newest = sorted(entries, key=sort_key, reverse=True)[:RECENT]
    RECENT_OUT.write_text(
        "\n".join([note, "", "```{=html}", '<ul class="outputs">']
                  + [item(e, rendered, talks, "outputs.html") for e in newest]
                  + ["</ul>", "```", ""]),
        encoding="utf-8",
    )

    # Old Talks page links (talks.html#<card heading> or #<folder>) go to the entry.
    mapping = {}
    for key, t in talks.items():
        mapping[heading_id(t["title"])] = key
        mapping[t["slug"]] = key
    REDIRECT_OUT.write_text(
        "\n".join([note, "", "```{=html}", "<script>",
                   f"const talkAnchors = {json.dumps(mapping, sort_keys=True)};",
                   "const want = decodeURIComponent(location.hash.slice(1));",
                   "location.replace('outputs.html#' + (talkAnchors[want] || 'talks-workshops-and-events'));",
                   "</script>", "```", ""]),
        encoding="utf-8",
    )
    print(f"Wrote {OUT.name}: {len(entries)} entries; {RECENT_OUT.name}; {REDIRECT_OUT.name}")


if __name__ == "__main__":
    main()
