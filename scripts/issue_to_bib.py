#!/usr/bin/env python3
"""Add an entry to network-outputs.bib from an "Add an output" issue form.

The issue body is untrusted input. Read it from a file, never from the command line:

    python3 scripts/issue_to_bib.py issue-body.md

The script appends the entry to the right section of network-outputs.bib and prints
the new key. It stops with an error when a required field is missing or malformed.
A maintainer still reviews the pull request that the workflow opens.
"""

from __future__ import annotations

import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
BIB = ROOT / "network-outputs.bib"
EMPTY = {"", "_No response_", "None"}

# category -> (BibTeX entry type, section marker the entry goes in)
CATEGORIES = {
    "lesson": ("misc", "lessons"),
    "software": ("software", "software and data"),
    "talk": ("misc", "talks, workshops and events"),
    "paper": ("misc", "papers"),
    "press": ("online", "press"),
}
MARKER = "% ---------------------------------------------------------------- "
STOP = {"a", "an", "the", "of", "and", "for", "to", "in", "on", "with", "from"}


def parse_form(text: str) -> dict[str, str]:
    """Return {heading: value} for each '### Heading' block of an issue form."""
    fields: dict[str, str] = {}
    for block in re.split(r"(?m)^### ", text)[1:]:
        heading, _, value = block.partition("\n")
        fields[heading.strip()] = value.strip()
    return fields


def clean(value: str) -> str:
    """Make a value safe inside {...}: one line, balanced braces, no backslashes."""
    value = " ".join(value.split())
    value = value.replace("\\", "").replace("{", "").replace("}", "")
    return value.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")


def get(fields: dict[str, str], name: str, required: bool = False) -> str:
    value = fields.get(name, "").strip()
    if value in EMPTY:
        value = ""
    if required and not value:
        sys.exit(f"Missing required field: {name}")
    return value


def ascii_word(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z]", "", text.lower())


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fields = parse_form(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))

    category = get(fields, "Category", True).split()[0]
    if category not in CATEGORIES:
        sys.exit(f"Unknown category: {category}")
    entry_type, section = CATEGORIES[category]

    title = clean(get(fields, "Title", True))
    date = get(fields, "Date", True)
    if not re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?(/\d{4}(-\d{2}(-\d{2})?)?)?", date):
        sys.exit(f"Date must be ISO (2026, 2026-04, 2026-04-22, or a range): {date}")

    people = []
    for line in get(fields, "Authors, speakers, or creators", True).splitlines():
        line = clean(line.strip(" -*"))
        if not line:
            continue
        people.append(line if "," in line else "{" + line + "}")
    if not people:
        sys.exit("No authors given")

    doi = get(fields, "DOI").removeprefix("https://doi.org/").strip()
    url = get(fields, "URL")
    if doi and not re.fullmatch(r"10\.\d{4,9}/\S+", doi):
        sys.exit(f"DOI does not look like a DOI: {doi}")
    if url and not re.fullmatch(r"https?://\S+", url):
        sys.exit(f"URL must start with http:// or https://: {url}")
    if not (doi or url):
        sys.exit("Give a DOI or a URL")

    first = people[0].strip("{}")
    family = ascii_word(first.split(",")[0]) if "," in first else ascii_word(first.split()[0])
    word = next((ascii_word(w) for w in title.split() if ascii_word(w) and ascii_word(w) not in STOP), "")
    base = f"{family}{date[:4]}{word}"
    text = BIB.read_text(encoding="utf-8")
    key, n = base, 0
    while re.search(r"@\w+\{" + re.escape(key) + ",", text):
        n += 1
        key = base + "abcdefghijklmnopqrstuvwxyz"[n - 1]

    tags = [t for t in (ascii_word(x) if " " not in x.strip() else clean(x.strip().lower()) for x in get(fields, "Tags").split(",")) if t]
    lines = [
        f"@{entry_type}{{{key},",
        f"  author = {{{' and '.join(people)}}},",
        f"  title = {{{{{title}}}}},",
        f"  type = {{{clean(get(fields, 'Kind of output', True))}}},",
    ]
    for field, name in [("eventtitle", "Event or series"), ("venue", "Location"), ("version", "Version")]:
        value = clean(get(fields, name))
        if value:
            lines.append(f"  {field} = {{{{{value}}}}}," if field == "eventtitle" else f"  {field} = {{{value}}},")
    publisher = clean(get(fields, "Publisher, repository, or journal"))
    if publisher:
        lines.append(f"  {'organization' if entry_type == 'online' else 'publisher'} = {{{publisher}}},")
    lines.append(f"  date = {{{date}}},")
    if doi:
        lines.append(f"  doi = {{{doi}}},")
    if url and not doi:
        lines.append(f"  url = {{{url}}},")
    lines.append(f"  keywords = {{{', '.join([category] + tags)}}}")
    lines.append("}")
    entry = "\n".join(lines) + "\n"

    issue = get(fields, "_issue")
    comment = f"% Added from issue #{issue}.\n" if issue else ""

    # Insert at the end of the section: before the next section marker, or at the end.
    start = text.find(MARKER + section)
    if start == -1:
        sys.exit(f"Section marker not found in {BIB.name}: {section}")
    nxt = text.find(MARKER, start + len(MARKER))
    block = "\n" + comment + entry
    text = text.rstrip("\n") + "\n" + block if nxt == -1 else text[:nxt] + block.lstrip("\n") + "\n" + text[nxt:]
    BIB.write_text(text, encoding="utf-8")
    print(key)


if __name__ == "__main__":
    main()
