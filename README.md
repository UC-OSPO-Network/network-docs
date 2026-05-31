# network-docs

Coordination documents for the UC OSPO Network: presentations, reports, a Quarto-rendered history, and planning drafts.

**GitHub:** [UC-OSPO-Network/network-docs](https://github.com/UC-OSPO-Network/network-docs)  
**Published site:** [ucospo.net/network-docs](https://ucospo.net/network-docs)

---

## Presentations

### IASSIST 2026 — Open Source as Institutional Infrastructure

A 10-minute talk making the case that open source software is research infrastructure, presenting the UC OSPO Network as a model for institutional support, and connecting OSPO work to data professionals' existing roles.

- **Slides:** [iassist-2026-slides.html](https://ucospo.net/network-docs/presentations/iassist-2026/iassist-2026-slides.html)
- **Handout:** `presentations/iassist-2026/iassist-2026-handout.html`
- **Source:** `presentations/iassist-2026/iassist-2026-slides.qmd`
- **Citation:** `presentations/iassist-2026/CITATION.cff`

Built with Quarto + Reveal.js. Includes a companion handout and a CSV of CURIOSS member institutions.

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

The history book and IASSIST slides are published via GitHub Actions to `ucospo.net`. See `.github/workflows/publish.yml` for the deployment configuration.
