# Issues to Raise
## UC OSPO Education Website — Audit Findings 2026-03-14

Consolidated from three audits:
* `accessibility-audit-2026-03-14.md` — WCAG 2.1 AA (accesslint:reviewer)
* `web-design-guidelines-audit-2026-03-14.md` — Vercel Web Interface Guidelines
* `react-best-practices-audit-2026-03-14.md` — Vercel React Best Practices

Overlapping findings (issues flagged by multiple audits) are merged into a single issue below.

---

## Critical

### Issue 1
**Title:** `[a11y] LessonCard not keyboard accessible — onClick on div`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit C-1, Web Design Guidelines

`LessonCard.jsx:74–104` — primary card action (`window.location.href` navigation) is implemented via `onClick` on a plain `<div>`. No `role`, `tabIndex`, or `onKeyDown`. Keyboard and screen reader users cannot activate lesson cards on `/lessons`, `/pathways/[id]`, or the home page.

**Fix:** Replace the outer `<div>` with `<article style={{ position: 'relative' }}>` and add a covering `<a href={lessonHref} aria-label={lessonName}>` with `position: absolute; inset: 0`. Child links already call `e.stopPropagation()` so they continue working independently. This also resolves the React best practice violation of using `window.location.href` in place of a native anchor.

---

### Issue 2
**Title:** `[a11y] StackedPathways accordion not keyboard accessible`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit C-2, Web Design Guidelines

`StackedPathways.jsx:57–118` — accordion panel triggers are plain `<div onClick>` with no `role`, `tabIndex`, `aria-expanded`, or keyboard handlers. The entire home page pathway-selection interaction is inaccessible to keyboard and screen reader users.

**Fix:** Replace trigger `<div>` with `<button aria-expanded={isExpanded} aria-controls={...}>`. Add `role="region"` and `hidden={!isExpanded}` to the panel content. Remove `transition: all` and add `prefers-reduced-motion` guard.

---

### Issue 3
**Title:** `[a11y] FolderStack accordion not keyboard accessible`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit C-3, Web Design Guidelines, React Best Practices

`FolderStack.jsx:23–116` — accordion toggle is a `<motion.div onClick>` with no keyboard support, `role`, or `aria-expanded`. Also: `framer-motion` is imported eagerly (~100KB+ gzipped), all animations lack `prefers-reduced-motion` guards, and height animation causes layout thrashing.

**Fix:** Replace trigger with `<button aria-expanded={open} aria-controls={...}>`. Replace Framer Motion height animation with a CSS `grid-template-rows: 0fr → 1fr` transition — this eliminates the heavy dependency, resolves the layout thrashing, and makes `prefers-reduced-motion` trivial to support.

---

## High Priority

### Issue 4
**Title:** `[a11y] SkillBadge color contrast failures — Beginner, Intermediate, Advanced`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit H-1, Web Design Guidelines

`SkillBadge.jsx:11–37` — three badge variants fail WCAG 4.5:1 contrast requirement for normal text:

| Badge | Ratio | Required |
|---|---|---|
| Beginner (`#FFF` on `#10b981`) | 2.54:1 | 4.5:1 |
| Intermediate (`#FFF` on `#f59e0b`) | 2.15:1 | 4.5:1 |
| Advanced (`#FFF` on `#ef4444`) | 3.76:1 | 4.5:1 |

**Fix:** Switch Beginner and Intermediate to `color: '#1E1E1E'` (dark text). For Advanced, darken background to `#b91c1c` and keep `#FFFFFF`. While fixing, also: hoist badge style map to a module-level constant (eliminates object allocation on every render), and add `aria-hidden="true"` to the SVG bar chart icon.

---

### Issue 5
**Title:** `[a11y] Footer heading and paragraph color contrast failures`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit H-2, H-3

* `BaseLayout.astro:27–31` — footer `<h3>` uses `--uc-gold` (`#FFE699`) on `--uc-blue` (`#0072A3`): **4.33:1**, fails 4.5:1
* `BaseLayout.astro:92–96` — footer bottom paragraph uses `--uc-light-gray` (`#CCCCCC`) on same blue: **3.32:1**, fails 4.5:1

**Fix:** Use `#FFFFFF` for both footer headings and bottom paragraph text (5.34:1 on `#0072A3`). Reserve gold for decorative accents only.

---

### Issue 6
**Title:** `[a11y] FolderStack lesson link color contrast failure`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit H-4, Web Design Guidelines

`FolderStack.jsx:91–95` — lesson title links use `color: '#007ACC'` on `#1E1E1E` background: **3.70:1**, fails 4.5:1.

**Fix:** Lighten to `#4DAADF` or use `var(--uc-light-blue)` (`#C8F0FF`, ratio 13.78:1).

---

### Issue 7
**Title:** `[a11y] LessonCard prerequisite label contrast borderline failure`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit H-5

`LessonCard.jsx:196–200` — "Prerequisites" label: `#9CA3AF` on `#3A3A3A` = **4.48:1**, misses 4.5:1 by 0.02.

**Fix:** Change to `#A1A8B4`.

---

### Issue 8
**Title:** `[a11y] Nav dropdown arrows not hidden from screen readers`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit H-6, Web Design Guidelines

`UnifiedNav.astro:370, 397, 411` — dropdown `▼` arrows inside nav links missing `aria-hidden="true"`. Screen readers announce "Black Down-Pointing Small Triangle" as part of the link name.

**Fix:** Add `aria-hidden="true"` to each `.dropdown-arrow` span. Also add `aria-expanded="false"` to mobile menu button initial HTML (`UnifiedNav.astro:349`) and wrap `☰`/`✕` symbols in `aria-hidden` spans.

---

### Issue 9
**Title:** `[a11y] Site title marked as h1 inside nav — duplicate h1 on every page`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit H-7, Web Design Guidelines

`UnifiedNav.astro:308–315` — site title is `<h1>` inside the logo `<a>`. Every page renders two `<h1>` elements, breaking the document outline.

**Fix:** Demote to `<span class="site-title">`. Add `aria-label="UC OSPO Network home"` to the logo anchor. Mark logo `<img>` as `aria-hidden="true"`.

---

## Medium Priority

### Issue 10
**Title:** `[a11y] Decorative emoji missing aria-hidden throughout`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit M-4, Web Design Guidelines

Decorative emoji rendered as plain text with no accessibility treatment in:
* `src/pages/pathways/[id].astro:146`
* `src/components/StackedPathways.jsx:85–90`
* `src/components/FolderStack.jsx:49`
* `src/components/LessonCard.jsx:138, 267, 343`
* `src/components/PathwayCard.astro:79`
* `src/components/SkillBadge.jsx:57` (SVG icon)

**Fix:** Add `aria-hidden="true"` to all decorative emoji containers and icon SVGs.

---

### Issue 11
**Title:** `[a11y] External links open in new tab without accessible warning`
**Labels:** `accessibility`, `enhancement`
**Source:** Accessibility audit M-8, Web Design Guidelines

`target="_blank"` used with no new-tab warning in:
* `src/components/LessonCard.jsx:219, 248`
* `src/components/FolderStack.jsx:84`
* `src/layouts/BaseLayout.astro:179, 184`
* `src/components/UnifiedNav.astro:319, 334`

**Fix:** Add visually hidden `(opens in new tab)` text or update `aria-label` to include the warning on each affected link.

---

### Issue 12
**Title:** `[a11y] LessonFilter result count not announced to screen readers`
**Labels:** `accessibility`, `enhancement`
**Source:** Accessibility audit M-6

`LessonFilter.tsx:242–244` — "Showing X of Y lessons" updates visually on filter change but has no `aria-live` region.

**Fix:** Add `aria-live="polite" aria-atomic="true"` to the results count `<p>`.

---

### Issue 13
**Title:** `[a11y] LessonFilter inputs lack explicit id/htmlFor label association`
**Labels:** `accessibility`, `enhancement`
**Source:** Accessibility audit M-7, Web Design Guidelines

`LessonFilter.tsx:148–238` — all four filter controls use implicit label wrapping with no `id`/`htmlFor`. Also missing `name` and `autocomplete` attributes on the search input. `<select>` elements missing `name`.

**Fix:** Add `id` to each input/select and `htmlFor` to each label. Add `name="search"` and `autocomplete="off"` to the search input.

---

### Issue 14
**Title:** `[a11y] Mobile menu button missing aria-expanded and aria-controls`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit M-2, Web Design Guidelines

`UnifiedNav.astro:349–355` — mobile menu toggle has no `aria-expanded` attribute in initial HTML; JS sets it only after first click. Also missing `aria-controls`.

**Fix:** Add `aria-expanded="false"` and `aria-controls="main-nav"` to the button in markup.

---

### Issue 15
**Title:** `[a11y] aria-disabled misused on active anchor in lesson detail`
**Labels:** `accessibility`, `bug`
**Source:** Accessibility audit M-5, Web Design Guidelines

`lessons/[slug].astro:360–368` — when `externalHref` is empty, the CTA renders as `<a aria-disabled="true">` still pointing to the current page. `aria-disabled` on `<a>` does not prevent keyboard activation.

**Fix:** Render conditionally — an `<a>` when `externalHref` exists, or a `<span aria-disabled="true" tabindex="-1">` when it does not.

---

### Issue 16
**Title:** `[ux] transition: all used in 6+ places — enumerate CSS properties`
**Labels:** `enhancement`
**Source:** Web Design Guidelines

`transition: all` used in `UnifiedNav.astro:179, 196`, `index.astro:47`, `PathwayCard.astro:16`, `StackedPathways.jsx:65, 77`, and `LessonCard.jsx:47`. This forces the browser to check every animatable property on each frame.

**Fix:** Replace with explicit property lists, e.g. `transition: background-color 0.2s, color 0.2s`.

---

### Issue 17
**Title:** `[ux] Hover transforms lack prefers-reduced-motion guard`
**Labels:** `accessibility`, `enhancement`
**Source:** Web Design Guidelines

`transform: translateY` and `scale` animations used in `index.astro:46`, `PathwayCard.astro:40`, `LessonCard.jsx:90`, `StackedPathways.jsx:66`, `FolderStack.jsx:66`, `lessons/[slug].astro:194, 283` with no `prefers-reduced-motion` guard.

**Fix:** Add a global rule to `public/styles.css`:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
And in JS components, check `window.matchMedia('(prefers-reduced-motion: reduce)').matches` before applying inline transform animations.

---

### Issue 18
**Title:** `[ux] All-caps text hardcoded in HTML content`
**Labels:** `enhancement`
**Source:** Web Design Guidelines

`index.astro:128` hero `<h1>` and `index.astro:143` CTA button both use all-caps text in HTML content. Screen readers may spell out characters rather than reading them as words.

**Fix:** Use CSS `text-transform: uppercase` and write source text in mixed case.

---

### Issue 19
**Title:** `[perf] framer-motion imported eagerly in FolderStack`
**Labels:** `performance`
**Source:** React Best Practices (CRITICAL)

`FolderStack.jsx:2` — `framer-motion` (~100KB+ gzipped) is imported at module level. It loads on every page that renders `FolderStack`, including the home page.

**Fix:** Replace `motion.div`/`AnimatePresence` with a CSS `grid-template-rows: 0fr → 1fr` transition. This eliminates the dependency entirely, resolves the layout-thrashing height animation, and makes `prefers-reduced-motion` support trivial.

---

### Issue 20
**Title:** `[perf] LessonFilter re-renders: isLoading pattern, triple forEach, unstable keys`
**Labels:** `performance`
**Source:** React Best Practices

Three issues in `LessonFilter.tsx` that cause unnecessary renders or poor list reconciliation:
* `:11` — `isLoading` useEffect causes an extra render on every mount for no benefit
* `:29–49` — `filterOptions` iterates `lessons` three times; combine into one `forEach`
* `:295` — `key={index}` on lesson cards; use `lesson.slug` for stable reconciliation

---

### Issue 21
**Title:** `[perf] Static style objects and keyframes recreated on every render`
**Labels:** `performance`
**Source:** React Best Practices

* `StackedPathways.jsx:56–119` — all inline style objects created as new literals on every render; hoist static portions to module-level constants
* `StackedPathways.jsx:121–131` — `@keyframes fadeIn` defined in a JSX string inside the component; move to `public/styles.css`
* `SkillBadge.jsx:8–37` — badge style map returns new objects on every call; hoist to a module-level constant

---

### Issue 22
**Title:** `[perf] ErrorBoundary retry reloads page instead of resetting state`
**Labels:** `enhancement`
**Source:** React Best Practices

`ErrorBoundary.jsx:24` — retry button calls `window.location.reload()`, losing all React state. Also: errors are only logged to `console.error` and silently swallowed in production.

**Fix:** Reset via `this.setState({ hasError: false })`. Add error reporting to a tracking service or expose a reportable error message to users.

---

## Suggested Label Setup

If these labels don't exist yet, create them before filing:

| Label | Color | Use for |
|---|---|---|
| `accessibility` | `#0075ca` | WCAG violations, ARIA issues |
| `performance` | `#e4e669` | Bundle size, render cost |
| `enhancement` | `#a2eeef` | UX improvements, non-breaking fixes |
| `bug` | `#d73a4a` | Broken behavior |

---

*Generated 2026-03-14 — based on accesslint, web-design-guidelines, and vercel-react-best-practices audits*
