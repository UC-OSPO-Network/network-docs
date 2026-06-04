# Web Interface Guidelines Audit
## UC OSPO Education Website

**Audit Date:** 2026-03-14
**Standard:** Vercel Web Interface Guidelines (100+ rules)
**Scope:** 13 files — layouts, pages, components

---

## src/layouts/BaseLayout.astro

`BaseLayout.astro:116` — no `<link rel="preconnect">` for any external origin; add if fonts or assets load from external hosts
`BaseLayout.astro:47` — no `prefers-reduced-motion` guard on any animation/transition
`BaseLayout.astro:179` — external GitHub link opens in new tab with no accessible new-tab warning
`BaseLayout.astro:184` — external RSS link opens in new tab with no accessible new-tab warning

---

## src/components/UnifiedNav.astro

`UnifiedNav.astro:179` — `transition: all 0.2s ease` on `.dropdown-menu` — never use `transition: all`; enumerate: `opacity, visibility, transform`
`UnifiedNav.astro:196` — `transition: all 0.2s` on `.dropdown-link` — enumerate: `background-color, color, padding-left`
`UnifiedNav.astro:349` — mobile menu button missing `aria-expanded="false"` in initial HTML
`UnifiedNav.astro:354` — `☰` symbol in button text not wrapped in `aria-hidden="true"` span
`UnifiedNav.astro:370` — `.dropdown-arrow` span missing `aria-hidden="true"`
`UnifiedNav.astro:397` — `.dropdown-arrow` span missing `aria-hidden="true"`
`UnifiedNav.astro:410` — `.dropdown-arrow` span missing `aria-hidden="true"`
`UnifiedNav.astro:308` — `<h1>` inside `<a>` logo link; every page gets two `<h1>` elements
`UnifiedNav.astro:319` — external GitHub link opens in new tab, no new-tab warning
`UnifiedNav.astro:334` — external RSS link opens in new tab, no new-tab warning
`UnifiedNav.astro:184` — dropdown reveal is hover-only; no `aria-haspopup` or `aria-expanded` on parent nav links

---

## src/pages/index.astro

`index.astro:46` — `.cta-primary:hover` and `.cta-secondary:hover` use `transform: translateY(-2px)` with no `prefers-reduced-motion` guard
`index.astro:47` — `transition: all 0.3s ease` on `.cta-primary` / `.cta-secondary` — enumerate properties
`index.astro:97` — `.browse-button` same: `transition: all 0.3s ease`
`index.astro:128` — hero `<h1>` text is all-caps in HTML content; use CSS `text-transform: uppercase` so screen readers announce it naturally
`index.astro:143` — "BROWSE ALL LESSONS" button text all-caps in content; use CSS instead

---

## src/pages/lessons/[slug].astro

`[slug].astro:362` — `target="_blank"` on "View External Lesson" with no new-tab warning in label
`[slug].astro:364` — `aria-disabled="false"` on active `<a>` is redundant; `aria-disabled="true"` on a functional link is a semantic mismatch (CSS `pointer-events: none` doesn't prevent keyboard activation)
`[slug].astro:194` — `.primary-button` `transition: transform 0.15s ease` — no `prefers-reduced-motion` guard
`[slug].astro:283` — `.related-card:hover` uses `transform: translateY(-2px)` — no `prefers-reduced-motion` guard

---

## src/pages/pathways/[id].astro

`[id].astro:146` — pathway icon emoji in `<div class="pathway-icon">` missing `aria-hidden="true"`

---

## src/components/LessonCard.jsx

`LessonCard.jsx:74` — primary card action is `onClick` on `<div>` — no `role`, `tabIndex`, or keyboard handler; not keyboard accessible
`LessonCard.jsx:47` — `transition: all 0.3s ease` — enumerate properties
`LessonCard.jsx:90` — `onMouseEnter`/`onMouseLeave` `transform: translateY(-4px)` — no `prefers-reduced-motion` guard
`LessonCard.jsx:138` — emoji icon in plain `<div>` missing `aria-hidden="true"`
`LessonCard.jsx:219` — prerequisite links open in new tab with no new-tab warning
`LessonCard.jsx:248` — feedback link opens in new tab with no new-tab warning
`LessonCard.jsx:267` — `💬` emoji not wrapped in `aria-hidden="true"` span
`LessonCard.jsx:343` — `✨` emoji not wrapped in `aria-hidden="true"` span
`LessonCard.jsx:297` — `key={idx}` on mapped role pills — use stable key (role string)

---

## src/components/LessonFilter.tsx

`LessonFilter.tsx:149` — `<label>` wraps `<input>` with no `htmlFor`/`id` — use explicit association
`LessonFilter.tsx:170` — OSS Role `<label>` same issue
`LessonFilter.tsx:194` — Skill Level `<label>` same issue
`LessonFilter.tsx:218` — Pathway `<label>` same issue
`LessonFilter.tsx:152` — search `<input>` missing `name` and `autocomplete` attributes
`LessonFilter.tsx:173` — `<select>` elements missing `name` attribute
`LessonFilter.tsx:242` — filter result count `<p>` missing `aria-live="polite"` and `aria-atomic="true"`
`LessonFilter.tsx:295` — `key={index}` on lesson cards — use `lesson.slug`

---

## src/components/PathwayCard.astro

`PathwayCard.astro:79` — emoji icon in `<span class="pathway-icon">` missing `aria-hidden="true"`
`PathwayCard.astro:16` — `.pathway-card` uses `transition: all 0.3s ease` — enumerate properties
`PathwayCard.astro:40` — `.pathway-card:hover` uses `transform: translateY(-4px)` — no `prefers-reduced-motion` guard

---

## src/components/SkillBadge.jsx

`SkillBadge.jsx:57` — bar chart `<svg>` missing `aria-hidden="true"`
`SkillBadge.jsx:13` — Beginner: `#ffffff` on `#10b981` — contrast 2.54:1, fails AA (4.5:1 required)
`SkillBadge.jsx:18` — Intermediate: `#ffffff` on `#f59e0b` — contrast 2.15:1, fails AA
`SkillBadge.jsx:23` — Advanced: `#ffffff` on `#ef4444` — contrast 3.76:1, fails AA

---

## src/components/FolderStack.jsx

`FolderStack.jsx:23` — `<motion.div onClick>` accordion trigger — no `role`, `tabIndex`, keyboard handler, or `aria-expanded`
`FolderStack.jsx:49` — emoji icon in plain `<span>` missing `aria-hidden="true"`
`FolderStack.jsx:57` — chevron `▼` missing `aria-hidden="true"`
`FolderStack.jsx:84` — lesson links open in new tab with no new-tab warning
`FolderStack.jsx:92` — `color: '#007ACC'` on `#1E1E1E` — contrast 3.70:1, fails AA
`FolderStack.jsx:66` — Framer Motion animate — no `prefers-reduced-motion` guard

---

## src/components/StackedPathways.jsx

`StackedPathways.jsx:57` — `<div onClick>` accordion trigger — no `role`, `tabIndex`, keyboard handler, or `aria-expanded`
`StackedPathways.jsx:65` — `transition: all 0.3s` — enumerate properties
`StackedPathways.jsx:66` — `transform: scale(0.98)` — no `prefers-reduced-motion` guard
`StackedPathways.jsx:77` — inner div `transition: all 0.3s ease` — enumerate properties
`StackedPathways.jsx:85` — emoji icon in plain `<span>` missing `aria-hidden="true"`
`StackedPathways.jsx:109` — `animation: 'fadeIn 0.3s ease'` inline — no `prefers-reduced-motion` guard
`StackedPathways.jsx:121` — `@keyframes fadeIn` defined inline with no `prefers-reduced-motion` media query

---

## Recurring Issues (apply globally)

* `transition: all` used in 6 places — always enumerate specific CSS properties
* `prefers-reduced-motion` not guarded in any transform/animation — add `@media (prefers-reduced-motion: reduce)` globally in `styles.css`
* External links with `target="_blank"` missing new-tab warnings — 8+ locations
* Decorative emoji not hidden from assistive technology — 7+ locations
* `key={index}` used instead of stable keys in 3 components

---

*Generated by Claude Code web-design-guidelines skill — 2026-03-14*
