# network-docs

Presentations, reports, and project history from the UC OSPO Network.

**GitHub:** [UC-OSPO-Network/network-docs](https://github.com/UC-OSPO-Network/network-docs)  
**Published site:** [ucospo.net/network-docs](https://ucospo.net/network-docs)

---

## Presentations

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
- **Status:** draft, in preparation

### Other presentations

- `presentations/02-Dennis_Breakout-open-ed_WED.pptx` — UC Open breakout session slides
- `presentations/speaker_notes_uc_open.md` — Speaker notes for UC Open presentation

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
2. Add `<slug>-slides.qmd` (and `<slug>-handout.qmd` if you have one) plus its assets.
3. Add an entry to `index.qmd` so it shows on the site.
4. Push to `main`. The workflow renders and deploys it with no workflow edits.

Each folder can carry a `Makefile` (see `ucla-tlr-ospo-2026/`) for local `make all` / `make pdf` builds.

### DOI / archival: `zenodo-publish.yml`

Mints a Zenodo DOI for a presentation. Trigger it by pushing a tag:

- `publish/<slug>/v1.0` mints on production Zenodo (creates a draft for human review before publishing).
- `publish-test/<slug>/v1.0` mints on sandbox Zenodo (auto-publishes, for testing).

The deposit reads its file list from `presentations/<slug>/zenodo.yml` and its metadata from that folder's `CITATION.cff`. Every deposit is submitted to the [UC OSPO Network Zenodo community](https://zenodo.org/communities/uc-ospo-net/) (`uc-ospo-net`) by default; a community curator approves the request. Requires the `OSPO_ZENODO` and `OSPO_ZENODO_TEST` secrets.

> Records published before this default was added (such as the existing IASSIST deposit) are not pulled into the community automatically. Add those from the Zenodo record page using "Add to community," then approve the request in the community.
