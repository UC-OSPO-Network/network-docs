# network-docs

A public record of the UC OSPO Network's talks and outputs. The site is the catalog: [ucospo.net/network-docs](https://ucospo.net/network-docs). This repo holds its sources.

## What is here

- `presentations/<slug>/`: one folder per talk (slides, handout, `talk.yml`, `CITATION.cff`). Shared theme, fonts and templates are in `presentations/_shared/`.
- `network-outputs.bib`: every public output (lessons, software, talks, papers, press). One source for the Outputs page.
- `history/`: the Quarto book "UC Open Source: A System History". It is published at `/history/` but not linked from the site while it is under review.
- `handout.qmd`: "UC Open Source at a Glance", a one-page printable handout.
- `index.qmd`, `outputs.qmd` (the Catalog), `handout.qmd` (At a Glance), `_quarto.yml`: the site pages. `talks.qmd` only redirects old Talks links to the matching catalog entry.
- `drafts/`, `reports/`, `presentation-proposals/`: working files. They are in the repo and are not published.
- `scripts/`: build and check scripts.

## Add a talk

Create `presentations/<slug>/` with the deck source and a `talk.yml`, and add the talk to `network-outputs.bib`. Its links appear under that entry in the Catalog with no other edit.

```yaml
title: "Short title for the listing"
date: 2026-09-23          # 2026, 2026-09 or 2026-09-23
event: Event name
kind: Workshop            # Conference talk, Workshop, Meetup, ...
status: published         # draft = not listed, rendered or published
bib: dennis2026example    # key in network-outputs.bib (required when published)
people: [Tim Dennis]      # optional if CITATION.cff lists the authors
doi: 10.5281/zenodo.0     # optional; also read from CITATION.cff
links:                    # relative to the folder, or full URLs
  - {label: Slides, href: example-slides.html}
```

In the deck front matter use `theme: ../_shared/ucospo-theme.scss`, `include-after-body: ../_shared/logo-swap.txt` and `reference-doc: ../_shared/ucospo-reference.pptx`. A `*slides*.html` link also gets a PDF link, because the workflow exports a PDF for every such deck.

## Add an output

Anyone can suggest an output with the [Add an output issue form](https://github.com/UC-OSPO-Network/network-docs/issues/new?template=add-output.yml). A maintainer checks it and adds the `approved` label. The `issue-to-bib.yml` workflow then runs `scripts/issue_to_bib.py` and opens a pull request with the entry. Review the entry against the record before merging.

To add an entry by hand, edit `network-outputs.bib`. The header of that file explains the fields. The first word in `keywords` picks the section on the Outputs page.

## How the catalog works

The Catalog page lists every entry in `network-outputs.bib`, grouped by category, newest first. When a talk's `talk.yml` names an entry with `bib:`, its slides, PDF, handout and source links appear under that entry. Each entry also gets a DOI or web page link and a permanent link (`outputs.html#<key>`). Home shows the three newest entries.

There are no filters yet. Grouping and the site search are enough at this size. Revisit at 75 to 100 entries, or sooner if people cannot find known items: first title and speaker search, or a "slides available" filter.

## Build

Needs Quarto, Python 3 with PyYAML, and decktape for PDFs.

```
scripts/build_site.sh        # Talks and Outputs lists, then the site pages
scripts/render_decks.sh      # every deck except drafts
quarto render history/       # the book
scripts/stage_site.sh        # copy decks and book into _site/
scripts/check_site.sh        # working files, missing pages, broken links
```

`scripts/build_site.sh` must run first: the pages include generated files. If you change a font file in `presentations/_shared/fonts/`, run `python3 scripts/embed_fonts.py`. If you change a font file in `presentations/_shared/fonts/`, run `python3 scripts/embed_fonts.py`.

## How it publishes

- Pull requests: `check.yml` builds the site and runs the checks. It does not deploy.
- Push to `main`: `publish.yml` builds everything, exports the slide PDFs, and deploys `_site/` to `gh-pages`. Only built files reach the site.
- DOI: push a tag `publish/<slug>/v1.0` (production, creates a draft) or `publish-test/<slug>/v1.0` (sandbox). `zenodo-publish.yml` reads the file list from `presentations/<slug>/zenodo.yml` and the metadata from that folder's `CITATION.cff`, and submits to the [UC OSPO Network Zenodo community](https://zenodo.org/communities/uc-ospo-net/). It needs the `OSPO_ZENODO` and `OSPO_ZENODO_TEST` secrets.
