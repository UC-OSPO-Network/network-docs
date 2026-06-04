# UC OSPO Education Site — Feature Ideas for Prototyping
**Captured:** 2026-05-19  
**Audience:** UCLA-IMLS project team (prototyping and implementation)  
**Status:** Ideas for scoping — not yet in GitHub issues

---

## Idea 1: GitHub Repo Health Signals on Lesson Cards

Surface live data from each lesson's source GitHub repository directly in the lesson catalog.

### What to show
* Star count — community signal of interest/adoption
* Commit recency — last commit date as a freshness indicator
* Open issues / PRs — signals active maintenance or neglect
* Contributors count — signals community breadth

### Where to show it
* Lesson card in the catalog grid — compact health badge (stars + last updated)
* Lesson detail page — expanded health panel with full signals

### Implementation notes
* Each lesson JSON already has (or will have) a `repoUrl` field pointing to its GitHub repo
* GitHub REST API: `GET /repos/{owner}/{repo}` returns stars, updated_at, open issues
* Can be fetched at build time (static, cached) or client-side (live but rate-limited)
* Build-time fetch via Astro data fetch + `@astrojs/node` or a GitHub Action that writes a JSON snapshot — avoids rate limits, keeps the site static
* Consider a `lastHealthCheck` timestamp in the snapshot so users know data age

---

## Idea 2: User Interactions — Star and Teach

Let community members signal engagement with lessons without requiring a full account system.

### "Star this lesson"
* Lightweight bookmark/interest signal — not GitHub stars, but a site-native count
* Options: (a) proxy to opening a GitHub issue/reaction, (b) use a lightweight backend (Supabase, PocketBase), (c) use GitHub Discussions reactions as the store
* Show aggregate star count on lesson card and detail page

### "I taught this"
* Instructor self-report: a structured GitHub issue filed on behalf of the user via a pre-filled template modal
* Triggered by a button on the lesson detail page: "I taught this lesson"
* Opens a modal (no page navigation) with a short form

### Teaching report modal fields
| Field | Purpose |
|---|---|
| Who | Your name / institution |
| What | Lesson name (pre-filled) + any modifications |
| Where | Event / course / workshop name |
| When | Date taught |
| Why | Audience description — who were the learners? |
| How it went | Free text — what worked, what didn't |

* On submit: opens a pre-filled GitHub issue in `UC-OSPO-Network/education` using a `taught-report` issue template
* No auth required — user reviews and submits the issue themselves
* Teaching reports become a public record of usage and community feedback
* Aggregate taught count shown on lesson detail page (count of issues with `taught-report` label)

### Implementation path
* GitHub issue URL query string pre-filling: `https://github.com/org/repo/issues/new?template=taught-report.yml&title=...&body=...`
* Modal can be a simple React/Astro component that builds the URL and opens it in a new tab (or uses `window.open`)
* No backend needed for the filing step — GitHub handles auth

---

## Idea 3: Standards-Based Web Architecture

Move the site toward structured, machine-readable data that works for search engines, AI systems, and partner campus embeds.

### JSON-LD structured data (LearningResource schema)
* Add `<script type="application/ld+json">` blocks to each lesson detail page
* Schema: `https://schema.org/LearningResource` with fields: name, description, url, educationalLevel, teaches, author, dateModified, license, inLanguage
* Enables Google's learning resource rich results
* Makes lesson data consumable by AI assistants and research crawlers without scraping

### /llms.txt
* Static file at `/llms.txt` (and `/llms-full.txt`) following the llmstxt.org spec
* Plain-text index of the lesson catalog for AI system consumption — equivalent to a sitemap but for LLMs
* Format: site description + bulleted list of lesson titles, URLs, and one-line descriptions
* Almost no educational catalogs have this yet — early-mover advantage
* Low effort: generate at build time from the lesson JSON collection

### /api/lessons.json endpoint
* Static JSON endpoint at `/api/lessons.json` exposing the full lesson catalog as structured data
* Enables: partner campus embeds, external tools querying the catalog, programmatic access
* Schema: array of lesson objects with all metadata fields
* Generated at build time by Astro — no server needed

### Sitemap
* Add `@astrojs/sitemap` integration — one config line
* Ensures lesson detail pages and pathway pages are indexed by search engines
* Currently missing

### OpenGraph metadata
* Add OG tags to `BaseLayout.astro`: `og:title`, `og:description`, `og:image`, `og:url`
* Lesson detail pages get lesson-specific OG tags (title = lesson name, description = lesson summary)
* Enables rich previews when lessons are shared on Slack, LinkedIn, Bluesky, etc.

### Ontology / vocabulary alignment
* Align lesson metadata fields to established vocabularies: schema.org, Dublin Core, LRMI (Learning Resource Metadata Initiative)
* `audience` → `schema:educationalRole` values
* `domain` / `subTopic` → consider aligning to a controlled vocabulary (e.g., ACM CCS, or a UC OSPO-defined ontology)
* `license` → SPDX identifiers
* This makes the JSON-LD output interoperable with other educational catalogs and library systems

### campusOwner field
* Add `campusOwner` to the lesson JSON schema — which UC campus (or external org) owns/maintains this lesson
* Foundation for: filtering by campus, governance reporting, staleness attribution, future federated catalog work

### Staleness detection GitHub Action
* Quarterly CI job: for each lesson, check the source repo's last commit date
* If no commit in >12 months, auto-open a GitHub issue tagging the lesson owner: "This lesson may be stale — please review"
* Keeps the catalog honest without manual tracking

---

## Prioritization suggestion (for IMLS prototype scope)

| Feature | Effort | Impact | Suggested phase |
|---|---|---|---|
| Sitemap | Low | Medium | Now |
| OpenGraph tags | Low | Medium | Now |
| JSON-LD on lesson pages | Medium | High | Now |
| /llms.txt | Low | High | Now |
| /api/lessons.json | Medium | High | Soon |
| GitHub health signals (build-time) | Medium | High | Soon |
| campusOwner field | Low | Medium | Soon |
| "I taught this" modal | Medium | High | Prototype |
| Staleness detection Action | Medium | Medium | Prototype |
| Star/interest signal | Medium | Low-Medium | Later |
| Ontology alignment | High | High (long-term) | Later |

---

## Questions to resolve before prototyping

* For GitHub health signals: build-time snapshot vs. client-side live fetch? (Static preferred for rate limits)
* For "I taught this": do we want the count surfaced on the site, or is the GitHub issue record sufficient for now?
* For JSON-LD: which schema.org types cover all lesson types we have? (Course, LearningResource, or both)
* For campusOwner: what's the controlled list of valid values? (UC campuses + external partners)
* For ontology alignment: do we adopt an existing vocabulary or define our own for the OSPO domain?
