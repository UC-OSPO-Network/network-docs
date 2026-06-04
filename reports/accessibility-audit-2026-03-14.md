# WCAG 2.1 AA Accessibility Audit Report
## UC OSPO Education Website

**Audit Date:** 2026-03-14
**Standard:** WCAG 2.1 Level AA
**Scope:** 14 files — layouts, pages, components
**Tool:** Claude Code accesslint:reviewer agent

---

## Executive Summary

| Priority | Count | WCAG Level |
|---|---|---|
| Critical | 3 | A |
| High | 7 | A / AA |
| Medium | 8 | A / AA |
| **Total** | **18** | |

The most severe issues are three interactive components — `LessonCard`, `StackedPathways`, and `FolderStack` — that implement all interactivity via `onClick` on plain `<div>` elements. These components are completely inaccessible to keyboard-only users and screen reader users. Six color contrast violations affect badges, footer text, and link colors. Two link purpose violations reduce clarity for screen reader users navigating by links list.

**Positive:** Skip link, `lang="en"`, breadcrumb semantics, social icon labels, and `axe-core` dev tooling are all correctly implemented.

---

## Critical Issues

### C-1: LessonCard not keyboard accessible
**File:** `src/components/LessonCard.jsx:74–104`
**WCAG:** 2.1.1 Keyboard (Level A)

The card's primary action (navigate to lesson detail) is an `onClick` on a plain `<div>` with no `role`, `tabIndex`, or `onKeyDown`. Keyboard-only users cannot activate lesson cards on `/lessons`, `/pathways/[id]`, or the home page.

**Fix:** Wrap card content in a covering `<a href={lessonHref}>` with `position: absolute; inset: 0`, or promote the `<h3>` to an anchor. Child links already call `e.stopPropagation()` so they continue to work independently.

---

### C-2: StackedPathways accordion not keyboard accessible
**File:** `src/components/StackedPathways.jsx:57–118`
**WCAG:** 2.1.1 Keyboard (Level A), 4.1.2 Name, Role, Value (Level A)

Pathway panel triggers are `<div onClick>` elements with no `role`, `tabIndex`, `aria-expanded`, or keyboard handlers. The entire home page pathway-selection interaction is inaccessible to keyboard and screen reader users.

**Fix:** Replace trigger `<div>` with `<button aria-expanded={isExpanded} aria-controls="...">`. Add `role="region"` and `hidden={!isExpanded}` to the panel.

---

### C-3: FolderStack accordion not keyboard accessible
**File:** `src/components/FolderStack.jsx:23–116`
**WCAG:** 2.1.1 Keyboard (Level A), 4.1.2 Name, Role, Value (Level A)

The folder toggle is a `<motion.div onClick>` with no keyboard support. The `▼` chevron is announced literally by screen readers with no context.

**Fix:** Replace trigger with `<button aria-expanded={open} aria-controls="...">`. Add `aria-hidden="true"` to the chevron `▼`.

---

## High Priority Issues

### H-1: SkillBadge color contrast failures
**File:** `src/components/SkillBadge.jsx:11–37`
**WCAG:** 1.4.3 Contrast Minimum (Level AA)

| Badge | Foreground | Background | Ratio | Required | Result |
|---|---|---|---|---|---|
| Beginner | `#FFFFFF` | `#10b981` | 2.54:1 | 4.5:1 | FAIL |
| Intermediate | `#FFFFFF` | `#f59e0b` | 2.15:1 | 4.5:1 | FAIL |
| Advanced | `#FFFFFF` | `#ef4444` | 3.76:1 | 4.5:1 | FAIL |
| Default | `#FFFFFF` | `#6b7280` | 4.83:1 | 4.5:1 | PASS |

**Fix:** Use `color: '#1E1E1E'` for Beginner and Intermediate badges. For Advanced, darken background to `#b91c1c` and keep `#FFFFFF` text.

---

### H-2: Footer section headings contrast failure
**File:** `src/layouts/BaseLayout.astro:27–31`
**WCAG:** 1.4.3 Contrast Minimum (Level AA)

`--uc-gold` (`#FFE699`) on `--uc-blue` (`#0072A3`) = **4.33:1** — fails 4.5:1 for normal text.

**Fix:** Use `#FFFFFF` for footer headings (5.34:1 on `#0072A3`), or darken the footer background to `#006d9b`.

---

### H-3: Footer bottom paragraph contrast failure
**File:** `src/layouts/BaseLayout.astro:92–96`
**WCAG:** 1.4.3 Contrast Minimum (Level AA)

`--uc-light-gray` (`#CCCCCC`) on `--uc-blue` (`#0072A3`) = **3.32:1** — fails 4.5:1 for 0.9rem text.

**Fix:** Switch footer bottom text to `#FFFFFF` (5.34:1 on existing blue).

---

### H-4: FolderStack lesson link contrast failure
**File:** `src/components/FolderStack.jsx:91–95`
**WCAG:** 1.4.3 Contrast Minimum (Level AA)

`#007ACC` on `#1E1E1E` = **3.70:1** — fails 4.5:1.

**Fix:** Lighten link color to `#4DAADF` or use `var(--uc-light-blue)` (`#C8F0FF`, 13.78:1).

---

### H-5: LessonCard prerequisite label contrast failure
**File:** `src/components/LessonCard.jsx:196–200`
**WCAG:** 1.4.3 Contrast Minimum (Level AA)

`#9CA3AF` on `#3A3A3A` = **4.48:1** — misses 4.5:1 by 0.02.

**Fix:** Change to `#A1A8B4` which achieves ≥4.5:1 on `#3A3A3A`.

---

### H-6: Dropdown arrows not hidden from screen readers
**File:** `src/components/UnifiedNav.astro:370, 397, 411`
**WCAG:** 4.1.2 Name, Role, Value (Level A)

Dropdown `▼` arrows inside nav links have no `aria-hidden="true"`. Screen readers announce them as "Black Down-Pointing Small Triangle" as part of the link name — e.g., "About Black Down-Pointing Small Triangle".

**Fix:** Add `aria-hidden="true"` to each `.dropdown-arrow` span on lines 370, 397, and 411.

---

### H-7: `<h1>` inside logo anchor — duplicate h1 on every page
**File:** `src/components/UnifiedNav.astro:308–315`
**WCAG:** 1.3.1 Info and Relationships (Level A)

The site title is marked as `<h1>` inside the logo `<a>`. Every page therefore renders two `<h1>` elements — one in the nav and one in `<main>` — breaking the document outline for all pages.

**Fix:** Demote site title to `<span class="site-title">`. Add `aria-label="UC OSPO Network home"` to the logo anchor. Remove `alt` text from logo `<img>` and add `aria-hidden="true"` since the anchor label covers it.

---

## Medium Priority Issues

### M-1: Desktop dropdowns keyboard-only disclosure
**File:** `src/components/UnifiedNav.astro:184–189`
**WCAG:** 2.1.1 Keyboard (Level A)

Dropdowns are CSS `:hover`/`:focus-within` only. No `aria-haspopup`, `aria-expanded`, or explicit keyboard open/close mechanism on parent nav items.

**Fix:** Add `aria-haspopup="true"` and `aria-expanded` to dropdown-bearing nav items. Consider converting to button + link pattern.

---

### M-2: Mobile menu button missing initial `aria-expanded`
**File:** `src/components/UnifiedNav.astro:349–355`
**WCAG:** 4.1.2 Name, Role, Value (Level A)

Mobile menu toggle has no `aria-expanded` attribute in initial HTML — state is only set by JS after first click. Also missing `aria-controls`. The `☰` and `✕` symbols are announced literally by some screen readers.

**Fix:** Add `aria-expanded="false"` and `aria-controls="main-nav"` to the button in markup. Wrap icon symbols in `<span aria-hidden="true">`.

---

### M-3: `Layout.astro` stale default title
**File:** `src/layouts/Layout.astro:8`
**WCAG:** 2.4.2 Page Titled (Level A)

Contains placeholder `<title>Astro Basics</title>` from project scaffolding. Risk of accidental use giving users a non-descriptive page title.

**Fix:** Remove the file if unused, or update to match `BaseLayout.astro` structure.

---

### M-4: Emoji icons missing `aria-hidden`
**File:** `src/pages/pathways/[id].astro:146`, `src/components/StackedPathways.jsx:85–90`, `src/components/FolderStack.jsx:49`, `src/components/LessonCard.jsx:138`
**WCAG:** 1.1.1 Non-text Content (Level A)

Decorative emoji icons (pathway icons, lesson icons) are rendered as plain text with no accessibility treatment. Screen readers announce emoji names (e.g., "seedling", "hammer and wrench") as content.

**Fix:** Add `aria-hidden="true"` to all decorative emoji containers. If the emoji conveys meaningful information, add `role="img"` and `aria-label`.

---

### M-5: `aria-disabled` misused on active link
**File:** `src/pages/lessons/[slug].astro:360–368`
**WCAG:** 4.1.2 Name, Role, Value (Level A)

When `externalHref` is empty, the "View External Lesson" `<a>` renders with `aria-disabled="true"` but still links to the current page. `aria-disabled` on `<a>` does not prevent activation — semantic mismatch.

**Fix:** Conditionally render either an active `<a>` (when `externalHref` exists) or a `<span aria-disabled="true" tabindex="-1">` (when it does not).

---

### M-6: Filter result count has no `aria-live` region
**File:** `src/components/LessonFilter.tsx:242–244`
**WCAG:** 4.1.3 Status Messages (Level AA)

"Showing X of Y lessons" updates visually when filters change but is not announced to screen reader users.

**Fix:** Add `aria-live="polite" aria-atomic="true"` to the results count `<p>`.

---

### M-7: Filter inputs lack explicit label association
**File:** `src/components/LessonFilter.tsx:148–238`
**WCAG:** 1.3.1 Info and Relationships (Level A), 3.3.2 Labels or Instructions (Level A)

Filter `<label>` elements use implicit wrapping association (no `id`/`htmlFor`). Not supported by all assistive technology combinations.

**Fix:** Add `id` to each `<input>`/`<select>` and corresponding `htmlFor` to each `<label>`.

---

### M-8: External links open in new tab without warning
**File:** `src/components/LessonCard.jsx:219, 249`, `src/components/FolderStack.jsx:85–88`, `src/layouts/BaseLayout.astro:179, 184`, `src/components/UnifiedNav.astro:319–346`
**WCAG:** 3.2.2 On Input (Level A), 2.4.4 Link Purpose (Level A)

Multiple links use `target="_blank"` with no accessible indication that they open a new tab.

**Fix:** Add visually hidden `(opens in new tab)` text inside each external link, or update `aria-label` to include the warning.

---

## Link Purpose Violations

### LP-1: Ambiguous "All Pathways" vs "Browse Pathways" in nav
**File:** `src/components/UnifiedNav.astro:413–435`
**WCAG:** 2.4.4 Link Purpose (Level A)

Education dropdown contains "All Pathways" (→ home) and "Browse Pathways" (→ `/pathways`) — indistinguishable names for different destinations. Same ambiguity appears in the footer.

**Fix:** Rename to unambiguous labels: e.g., "Pathways Index" vs "Start Learning".

---

### LP-2: "View External Lesson" CTA doesn't describe destination
**File:** `src/pages/lessons/[slug].astro:359–368`
**WCAG:** 2.4.4 Link Purpose (Level A)

Every lesson detail page uses the identical "View External Lesson" CTA regardless of destination. Screen reader users navigating by links list cannot distinguish between lessons.

**Fix:** Add `aria-label={`View ${lesson.name} on ${new URL(externalHref).hostname}`}` to the anchor.

---

## Architectural Recommendations

* **Establish a keyboard interaction contract:** Interactive disclosure widgets use `<button>`; navigation uses `<a>`; never `onClick` on `<div>` or `<span>` for primary actions.
* **Add global `:focus-visible` styles** in `public/styles.css` — no consistent focus indicator is currently defined. Recommended: `outline: 3px solid var(--uc-gold); outline-offset: 2px`.
* **Create a `sr-only` utility class** in `styles.css` and use it consistently instead of repeating inline clip-rect styles.
* **Audit SkillBadge color tokens** as a design system update — switch to dark text on green/amber to pass contrast without changing hue identity.

---

## Positive Findings

* Skip link correctly implemented (`UnifiedNav.astro:293`, `BaseLayout.astro:133`)
* `lang="en"` on `<html>` (`BaseLayout.astro:109`)
* `<main>` landmark with `id="main-content"`
* Breadcrumb uses `<nav aria-label="Breadcrumb">`, `<ol>`, and `aria-current="page"` correctly (`lessons/[slug].astro:342–350`)
* Social icon links have `aria-label` in header and footer
* Logo `<img>` has descriptive alt text
* Section headings use `aria-labelledby` throughout `[slug].astro`
* `rel="noopener noreferrer"` consistently applied on external links
* `axe-core` dev tooling integrated in `BaseLayout.astro:122–130`
* Form labels present in `LessonFilter`

---

*Generated by Claude Code accesslint:reviewer agent — 2026-03-14*
