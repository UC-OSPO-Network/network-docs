# network-docs

Presentations, reports, and project history from the UC OSPO Network.

**GitHub:** [UC-OSPO-Network/network-docs](https://github.com/UC-OSPO-Network/network-docs)  
**Published site:** [ucospo.net/network-docs](https://ucospo.net/network-docs)

---

## Presentations

### UC Carpentries Fall 2026: Making Research Software Citable & Discoverable

Slides for the Sep 23, 2026 session of the UC Carpentries Workshop Series, co-presented by the UC OSPO Network and UC Carpentries. They accompany the lesson [Making Research Software Citable & Discoverable](https://ucospo.net/research-software-citable-discoverable/). Learners add a license, a CITATION.cff, a release with a DOI, and better metadata to their own fork of a demo repository.

- **Intro deck:** [uc-carpentries-sharing-software-2026-slides.html](https://ucospo.net/network-docs/presentations/uc-carpentries-sharing-software-2026/uc-carpentries-sharing-software-2026-slides.html). Welcome, why software citation matters, the UC OSPO Network, forking the demo repo
- **Improving Metadata and Discoverability:** [improving-metadata-discoverability-slides.html](https://ucospo.net/network-docs/presentations/uc-carpentries-sharing-software-2026/improving-metadata-discoverability-slides.html). Topics, README, Zenodo metadata, getting involved
- **Source:** `presentations/uc-carpentries-sharing-software-2026/`

### IASSIST 2026 — Open Source as Institutional Infrastructure

A 10-minute talk making the case that open source software is research infrastructure, presenting the UC OSPO Network as a model for institutional support, and connecting OSPO work to data professionals' existing roles.

- **Slides:** [ucospo.net/network-docs/presentations/iassist-2026/iassist-2026-slides.html](https://ucospo.net/network-docs/presentations/iassist-2026/iassist-2026-slides.html) · shortlink: [tinyurl.com/iassist2026](https://tinyurl.com/iassist2026)
- **Handout:** [ucospo.net/network-docs/presentations/iassist-2026/iassist-2026-handout.html](https://ucospo.net/network-docs/presentations/iassist-2026/iassist-2026-handout.html) · shortlink: [tinyurl.com/iassist2026-handout](https://tinyurl.com/iassist2026-handout)
- **Source:** `presentations/iassist-2026/iassist-2026-slides.qmd`
- **Full version** (19 slides, for other venues): `presentations/iassist-2026/iassist-2026-slides-full.qmd`
- **Annotated bibliography:** `presentations/iassist-2026/iassist-2026-bibliography.md`
- **Citation:** `presentations/iassist-2026/CITATION.cff`

Built with Quarto + Reveal.js. Includes a companion handout and a CSV of CURIOSS member institutions.

### UCLA Library Brown-bag: Open Source as Institutional Infrastructure *(draft)*

An internal adaptation of the IASSIST talk for the UCLA Library Teaching, Learning & Research department. Reframes the case for a library audience: software is where research data was a decade ago, and scholarly communication is the library's seat at the OSPO table. Co-authored with Leigh Phan.

- **Source:** `presentations/ucla-tlr-ospo-2026/ucla-tlr-ospo-2026-slides.qmd`
- **Status:** draft (`status: draft` in its `talk.yml`), so it is not listed or published

### UC Open 2026: UC OSPO Education Activities

Breakout talk at UC Open 2026 (Apr 22, 2026). Slides are on Zenodo ([10.5281/zenodo.19710413](https://doi.org/10.5281/zenodo.19710413)). The pptx and speaker notes are in `presentations/uc-open-2026/` and are not published on the site.

### Add a talk

The Talks page and the home page are generated. To add a talk, create `presentations/<slug>/` with the deck source and a `talk.yml`. No other file needs an edit.

```yaml
title: "Short title for the listing"
date: 2026-09-23          # 2026, 2026-09 or 2026-09-23
event: Event name
kind: Workshop            # Conference talk, Workshop, Meetup, ...
status: published         # draft = not listed, not rendered, not published
bib: dennis2026example    # key in network-outputs.bib (required when published)
people: [Tim Dennis]      # optional if CITATION.cff lists the authors
doi: 10.5281/zenodo.0     # optional; also read from CITATION.cff
links:                    # relative to the folder, or full URLs
  - {label: Slides, href: example-slides.html}
```

Decks share one theme, set of fonts, logo swap and pptx reference in `presentations/_shared/`. In a deck's front matter use `theme: ../_shared/ucospo-theme.scss`, `include-after-body: ../_shared/logo-swap.txt` and `reference-doc: ../_shared/ucospo-reference.pptx`. Rendered HTML is built by the workflow and is not committed.

A link to a `*slides*.html` deck also gets a PDF link, because the workflow exports a PDF for every such deck. `python3 scripts/build_talks.py` checks every `talk.yml`. It fails when a folder has no `talk.yml`, a required field is missing, or a published talk has no entry in `network-outputs.bib`. Build the site locally with `scripts/build_site.sh`.

---

## History book — UC Open Source: A System History

A Quarto book tracing UC research software from BSD Unix through Jupyter, Ceph, Spark, RISC-V, and beyond. Covers the origin stories, the pattern of open release, and what it means for institutional support today.

- **Published:** [ucospo.net/network-docs/history](https://ucospo.net/network-docs/history)
- **Source:** `history/` (Quarto book project)

Chapters are organized in two parts: *The Record* (project histories) and *The Analysis* (pattern, stakes, and the network). Appendix covers individual projects in detail.

---

## Reports

Internal and working documents in `reports/`:

- `education-activity-report.md` — UC OSPO education activity summary
- `accessibility-audit-2026-03-14.md` / `ACCESSIBILITY_AUDIT_REPORT.md` — accessibility audits of network sites
- `web-design-guidelines-audit-2026-03-14.md` / `react-best-practices-audit-2026-03-14.md` — design and code quality reviews
- `meeting-agenda-2026-03-10.md` / `issues-to-raise-2026-03-14.md` — meeting records
- `metadata-learningresource.csv` — schema.org metadata for learning resources

---

## Drafts

Working drafts in `drafts/`:

- `feature-ideas-2026-05.md` — feature ideas backlog
- `lesson-dev-appeal.md` — draft appeal for lesson development support

---

## Publishing

Two GitHub Actions workflows handle publishing. Both rely on one convention: **one folder per presentation under `presentations/`, named `<slug>/`, containing `<slug>-slides.qmd`** (and optionally `<slug>-handout.qmd`). For example, `presentations/iassist-2026/iassist-2026-slides.qmd`.

### Site (HTML + PDF): `publish.yml`

Runs on every push to `main` that touches `presentations/`, `history/`, `index.qmd`, or the site styles. It renders the index, **every `.qmd` in every `presentations/*/` folder**, and the history book; exports a PDF for each reveal.js deck (any `*slides*.html`) with decktape; and deploys to the `gh-pages` branch behind `ucospo.net/network-docs`.

Each presentation deploys into its own subdirectory with `keep_files: true`, so distinct presentations sit side by side and never overwrite each other. A deck publishes to `ucospo.net/network-docs/presentations/<slug>/<slug>-slides.html`.

**To add a new presentation:**

1. Create `presentations/<slug>/` with a dated slug (e.g. `acrl-2027`).
2. Add `<slug>-slides.qmd` (and `<slug>-handout.qmd` if you have one) plus its assets. Set `embed-resources: true` on the deck's `revealjs` format so it renders to one self-contained HTML file (rendered `*_files/` directories are git-ignored and won't deploy).
3. Add an entry to `index.qmd` so it shows on the site.
4. Push to `main`. The workflow renders and deploys it with no workflow edits.

Each folder can carry a `Makefile` (see `ucla-tlr-ospo-2026/`) for local `make all` / `make pdf` builds.

### DOI / archival: `zenodo-publish.yml`

Mints a Zenodo DOI for a presentation. Trigger it by pushing a tag:

- `publish/<slug>/v1.0` mints on production Zenodo (creates a draft for human review before publishing).
- `publish-test/<slug>/v1.0` mints on sandbox Zenodo (auto-publishes, for testing).

The deposit reads its file list from `presentations/<slug>/zenodo.yml` and its metadata from that folder's `CITATION.cff`. Every deposit is submitted to the [UC OSPO Network Zenodo community](https://zenodo.org/communities/uc-ospo-net/) (`uc-ospo-net`) by default; a community curator approves the request. Requires the `OSPO_ZENODO` and `OSPO_ZENODO_TEST` secrets.

> Records published before this default was added (such as the existing IASSIST deposit) are not pulled into the community automatically. Add those from the Zenodo record page using "Add to community," then approve the request in the community.

## Outputs page

`network-outputs.bib` lists the Network's public outputs: lessons, software and data, talks and workshops, papers, and press. `outputs.qmd` renders it as the Outputs page at [ucospo.net/network-docs/outputs.html](https://ucospo.net/network-docs/outputs.html). `references.bib` is a different file. It holds the works that the history book and the slides cite.

To add an entry, edit `network-outputs.bib`. The header of that file lists the fields. The first word in `keywords` picks the section. To preview the page:

```sh
python3 scripts/build_outputs.py
quarto render outputs.qmd
```

The script needs only Python 3 and Quarto. `_outputs-generated.md` is built from the bibliography and is not committed. The publish workflow runs the same two commands.
