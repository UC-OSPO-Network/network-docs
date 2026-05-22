# React Best Practices Audit
## UC OSPO Education Website

**Audit Date:** 2026-03-14
**Standard:** Vercel React Best Practices v1.0.0 (62 rules, 8 categories)
**Scope:** 6 React/JSX components

---

## src/components/LessonFilter.tsx

**Re-render Optimization (MEDIUM)**

`LessonFilter.tsx:11–27` — `isLoading` state is set to `false` immediately in `useEffect` on every mount. This causes an unnecessary extra render cycle. Since Astro manages hydration via `client:load`, remove this pattern entirely or use `useSyncExternalStore`.
> Rule: `rerender-derived-state-no-effect`

`LessonFilter.tsx:29–49` — `filterOptions` `useMemo` iterates `lessons` three separate times (one forEach each for ossRoles, levels, categories). Combine into a single loop.
> Rule: `js-combine-iterations`

```tsx
// Current: 3 passes
lessons.forEach(l => ossRoles.add(...))
lessons.forEach(l => levels.add(...))
lessons.forEach(l => categories.add(...))

// Better: 1 pass
lessons.forEach(l => {
  if (l.oss_role) l.oss_role.split(',').forEach(r => ossRoles.add(r.trim()))
  if (l.educationalLevel) levels.add(l.educationalLevel)
  if (l.learnerCategory) categories.add(l.learnerCategory)
})
```

`LessonFilter.tsx:63–76` — `Fuse` index is rebuilt inside `useMemo` with `lessons` as a dependency. If `lessons` is a new array reference on every parent render, the entire Fuse index rebuilds each time. Verify the parent passes a stable reference, or stabilize with `useRef`.
> Rule: `rerender-dependencies`

`LessonFilter.tsx:295` — `key={index}` on lesson cards. Array index keys cause incorrect DOM reuse when results reorder after filtering. Use `lesson.slug` as the key.
> Rule: `rerender-memo`

---

## src/components/LessonCard.jsx

**JavaScript Performance (LOW-MEDIUM)**

`LessonCard.jsx:31–57` — `prerequisiteLinks` is built via `.map(...).filter(Boolean)` — two array iterations. Replace with `.flatMap()` for a single pass.
> Rule: `js-flatmap-filter`

```tsx
// Current: two passes
const prerequisiteLinks = dependencyRefs
  .map(token => { ...; return null })
  .filter(Boolean)

// Better: one pass
const prerequisiteLinks = dependencyRefs.flatMap(token => {
  const result = ...
  return result ? [result] : []
})
```

`LessonCard.jsx:59–63` — `feedbackUrl` is rebuilt by string concatenation + `encodeURIComponent` on every render. It's a pure function of `lessonName`. Wrap in `useMemo` or hoist the URL template to a utility function.
> Rule: `js-cache-function-results`

`LessonCard.jsx:101–103` — `onClick` assigns `window.location.href` directly. This bypasses native link behavior: middle-click, cmd/ctrl-click, right-click → "open in new tab", and browser history all stop working. Replace the outer `<div>` with an `<a>` element.
> Rule: semantic navigation / `rerender-no-inline-components`

`LessonCard.jsx:291` — `key={idx}` on role tag pills — use the role string as the key.
> Rule: `rerender-memo`

---

## src/components/FolderStack.jsx

**Bundle Size (CRITICAL)**

`FolderStack.jsx:2` — `framer-motion` is imported at the top level. This is a large library (~100KB+ gzipped) bundled eagerly on every page that includes `FolderStack`. The animations used (`height: 0 → auto`, `opacity`) can be replaced with a CSS `grid-template-rows: 0fr → 1fr` transition, eliminating the dependency entirely.
> Rule: `bundle-dynamic-imports`

If framer-motion must be kept, lazy-load it:

```tsx
const { motion, AnimatePresence } = await import('framer-motion')
```

**JavaScript Performance (LOW-MEDIUM)**

`FolderStack.jsx:66–70` — Framer Motion's `animate={{ height: 'auto' }}` requires JS measurement of element height on every animation frame (layout thrashing). Prefer a CSS-only expand pattern using `grid-template-rows`.
> Rule: `js-avoid-layout-thrashing`

`FolderStack.jsx:72` — `.slice(0, 5)` is performed inside the render. Pass only the 5 items needed from the parent to avoid serializing excess data through the component boundary.
> Rule: `server-serialization`

---

## src/components/StackedPathways.jsx

**Rendering Performance (MEDIUM)**

`StackedPathways.jsx:56–119` — Each pathway card's style objects are created as new object literals on every render. Six pathways × multiple style objects = significant allocation on each state change. Extract static styles to module-level constants; keep only dynamic values (isExpanded) inline.
> Rule: `rendering-hoist-jsx`

`StackedPathways.jsx:121–131` — `@keyframes fadeIn` CSS is defined as a JSX string inside the component body. It is recreated on every render. Move to `public/styles.css` or a module-level constant.
> Rule: `rendering-hoist-jsx`

**Re-render Optimization (MEDIUM)**

`StackedPathways.jsx:43` — `useState('getting-started')` initial value is a string literal — fine. ✓

`StackedPathways.jsx:59` — `onClick={() => setExpandedId(pathway.id)}` creates a new arrow function on every render for each of the 6 pathway items. Extract to a stable callback with `useCallback` or use a data attribute approach.
> Rule: `rerender-functional-setstate`

---

## src/components/SkillBadge.jsx

**Rendering Performance (MEDIUM)**

`SkillBadge.jsx:8–37` — `getBadgeStyle()` returns new object literals on every render call. Since it's a pure mapping from a fixed set of strings to a fixed set of styles, hoist the style map to a module-level constant for O(1) lookup with zero object allocation.
> Rule: `js-cache-function-results`

```tsx
// Current: new objects on every render
const getBadgeStyle = (level) => {
  if (normalizedLevel.includes('beginner')) return { background: '...', color: '...' }
}

// Better: module-level constant, zero allocation
const BADGE_STYLES: Record<string, BadgeStyle> = {
  beginner: { background: 'linear-gradient(...)', color: '#1E1E1E', label: 'Beginner' },
  intermediate: { background: 'linear-gradient(...)', color: '#1E1E1E', label: 'Intermediate' },
  advanced: { background: 'linear-gradient(...)', color: '#FFFFFF', label: 'Advanced' },
}
```

`SkillBadge.jsx:57–61` — The SVG bar chart icon is recreated as new JSX on every render. Extract as a module-level constant `const BarIcon = <svg .../>` or a named component.
> Rule: `rendering-hoist-jsx`

---

## src/components/ErrorBoundary.jsx

`ErrorBoundary.jsx:13–15` — `componentDidCatch` only logs to `console.error`. Errors are silently swallowed in production. Forward to an error tracking service or surface a reportable error ID to users.

`ErrorBoundary.jsx:24` — `window.location.reload()` on retry loses all React state. Reset `hasError` via `setState({ hasError: false })` to let React re-render the subtree without a full page reload.
> Rule: `rerender-functional-setstate`

`ErrorBoundary.jsx` — Correct use of class component for error boundary (required — no functional alternative). Overall implementation is minimal but correct. ✓

---

## Summary by Priority

| Priority | Issue | File | Rule |
|---|---|---|---|
| CRITICAL | framer-motion imported top-level (~100KB) | `FolderStack.jsx:2` | `bundle-dynamic-imports` |
| MEDIUM | Extra render from `isLoading` useEffect pattern | `LessonFilter.tsx:11` | `rerender-derived-state-no-effect` |
| MEDIUM | filterOptions iterates lessons 3× | `LessonFilter.tsx:29` | `js-combine-iterations` |
| MEDIUM | Fuse index rebuilt on unstable `lessons` ref | `LessonFilter.tsx:63` | `rerender-dependencies` |
| MEDIUM | `key={index}` on lesson cards and role pills | `LessonFilter.tsx:295`, `LessonCard.jsx:291` | `rerender-memo` |
| MEDIUM | Style objects recreated on every render | `StackedPathways.jsx:56`, `SkillBadge.jsx:8` | `rendering-hoist-jsx` |
| MEDIUM | `@keyframes` defined inside component | `StackedPathways.jsx:121` | `rendering-hoist-jsx` |
| MEDIUM | New arrow function per pathway per render | `StackedPathways.jsx:59` | `rerender-functional-setstate` |
| LOW-MEDIUM | `prerequisiteLinks` uses map+filter (2 passes) | `LessonCard.jsx:31` | `js-flatmap-filter` |
| LOW-MEDIUM | `feedbackUrl` rebuilt every render | `LessonCard.jsx:59` | `js-cache-function-results` |
| LOW-MEDIUM | Height animation causes layout thrashing | `FolderStack.jsx:66` | `js-avoid-layout-thrashing` |
| LOW | ErrorBoundary retry reloads page | `ErrorBoundary.jsx:24` | `rerender-functional-setstate` |

---

*Generated by Claude Code vercel-react-best-practices skill — 2026-03-14*
