#!/usr/bin/env python3
"""Check the links in a built site.

Internal links (relative, or under https://ucospo.net/network-docs/) must point
at a file in the site. A broken internal link fails the run. External links are
fetched once each; failures are warnings, because other sites go down and block
robots.

  python3 scripts/check_links.py _site [--allow-missing-pdf] [--no-external]

--allow-missing-pdf skips internal links to *.pdf files. Pull requests do not run
decktape, so the slide PDFs exist only in the deploy run.
"""

from __future__ import annotations

import concurrent.futures
import html.parser
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

SITE_URL = "https://ucospo.net/network-docs/"
SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:", "blob:")
ATTRS = {"a": "href", "link": "href", "img": "src", "script": "src", "source": "src", "iframe": "src"}
BLOCKED = {401, 403, 429, 999}  # sites that refuse robots; not evidence of a dead link


class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.found: list[str] = []

    def handle_starttag(self, tag, attrs):
        want = ATTRS.get(tag)
        if want:
            for name, value in attrs:
                if name == want and value:
                    self.found.append(value.strip())


def resolve(site: pathlib.Path, page: pathlib.Path, link: str) -> pathlib.Path | None:
    """Return the local file a link points at, or None if the link is external."""
    if link.startswith(SITE_URL):
        link = link[len(SITE_URL):] or "./"
        base = site
    elif link.startswith(("http://", "https://", "//")):
        return None
    elif link.startswith("/"):
        return None  # root-absolute links depend on where the site is mounted
    else:
        base = page.parent
    path = urllib.parse.unquote(urllib.parse.urlsplit(link).path)
    target = (base / path).resolve()
    if path == "" or path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def fetch(url: str) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": "network-docs-link-check"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return None if r.status < 400 else f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        return None if e.code in BLOCKED or 300 <= e.code < 400 else f"HTTP {e.code}"
    except Exception as e:  # DNS, timeout, TLS
        return type(e).__name__


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    allow_pdf = "--allow-missing-pdf" in sys.argv
    external = "--no-external" not in sys.argv
    site = pathlib.Path(args[0] if args else "_site").resolve()

    broken: list[tuple[str, str]] = []
    externals: dict[str, str] = {}
    pages = [p for p in site.rglob("*.html") if "site_libs" not in p.parts and "_files" not in " ".join(p.parts)]
    for page in sorted(pages):
        parser = Links()
        parser.feed(page.read_text(errors="replace"))
        for link in parser.found:
            if link.startswith("#") or link.startswith(SKIP_SCHEMES):
                continue
            target = resolve(site, page, link)
            if target is None:
                if link.startswith(("http://", "https://")):
                    externals.setdefault(link.split("#")[0], str(page.relative_to(site)))
                continue
            if allow_pdf and target.suffix == ".pdf":
                continue
            if not target.exists():
                broken.append((str(page.relative_to(site)), link))

    for page, link in sorted(set(broken)):
        print(f"::error file={page}::broken internal link: {link}")

    dead = []
    if external:
        with concurrent.futures.ThreadPoolExecutor(16) as pool:
            for url, problem in zip(externals, pool.map(fetch, externals)):
                if problem:
                    dead.append((url, problem))
        for url, problem in sorted(dead):
            print(f"::warning::external link {problem}: {url} (on {externals[url]})")

    print(f"Checked {len(pages)} pages, {len(externals)} external links: "
          f"{len(set(broken))} broken internal, {len(dead)} external warnings")
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
