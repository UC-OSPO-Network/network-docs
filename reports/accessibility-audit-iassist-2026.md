# Accessibility Audit: IASSIST 2026 Presentation
**Date:** 2026-05-31
**Auditor:** Claude Code (Anthropic) via accesslint skills
**Standard:** WCAG 2.1 Level A and AA
**Scope:** `/presentations/iassist-2026/`

## Files Audited

| File | Type |
|------|------|
| `iassist-2026-slides.qmd` | Quarto/Reveal.js presentation source |
| `ucospo-theme.scss` | Custom Reveal.js theme |
| `iassist-2026-handout.qmd` | Print handout |
| `iassist-2026-slides.html` | Rendered output (runtime check) |

## Executive Summary

| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 3 |
| Medium | 3 |
| Low / Positive | Several positives noted |

The presentation has a strong accessibility foundation: Atkinson Hyperlegible font, `.sr-only` utility, `prefers-reduced-motion` support, semantic list ARIA roles on the pipeline grid, and a well-implemented focus indicator. The critical issues are all fixable in under an hour. Most failures are in the handout rather than the slides.

---

## Critical Issues

### C1. Slide logo has no alt text

**Location:** `iassist-2026-slides.html:1073` (rendered output); source: `iassist-2026-slides.qmd:11` (YAML `logo:` key)

**WCAG:** 1.1.1 Non-text Content (Level A)

**Issue:** The persistent logo rendered by Reveal.js in the bottom-left corner has no `alt` attribute:

```html
<p><img src="images/uc-ospo-network-logo-light.svg" class="slide-logo"></p>
```

A missing `alt` attribute causes screen readers to fall back to the filename (`uc-ospo-network-logo-light`), which is not meaningful to a user.

**Impact:** Screen reader users hear a garbled filename on every slide as the logo is part of the persistent slide shell.

**Fix:** Quarto's `logo:` YAML key does not expose an `alt` attribute natively. The `logo-swap.txt` JavaScript already queries `.slide-logo` — extend it to also set `alt`:

In `logo-swap.txt`, add one line to the `updateLogo` function:

```js
function updateLogo(slide) {
  var logo = document.querySelector('.slide-logo');
  if (!logo) return;
  var bg = slide ? (slide.getAttribute('data-background-color') || '') : '';
  logo.src = bg === DARK_BG ? WHITE_LOGO : LIGHT_LOGO;
  logo.alt = 'UC OSPO Network';  // ADD THIS LINE
}
```

Also call it once on initial load at the bottom of the IIFE:

```js
window.addEventListener('load', function () {
  var firstSlide = document.querySelector('.reveal .slides section');
  updateLogo(firstSlide);
  // ...
});
```

**Priority:** Critical

---

### C2. QR code image has no alt text

**Location:** `iassist-2026-slides.qmd:798`

**WCAG:** 1.1.1 Non-text Content (Level A)

**Issue:** The QR code on the final "Learn more / connect" slide has no alt text:

```markdown
![](images/iassist2026-qr.svg){width="200px"}
```

An empty alt attribute (`alt=""`) would mark it as decorative, but the QR code is informative — it encodes the URL `tinyurl.com/iassist2026`. Without alt text, blind users have no access to the URL the QR code represents.

**Impact:** Blind users cannot access the slide URL from this image. (The URL does appear as visible text below the QR code, which partially mitigates the impact, but the image itself still violates 1.1.1.)

**Fix:** Add descriptive alt text including the encoded URL:

```markdown
![QR code linking to tinyurl.com/iassist2026 — slides for this presentation](images/iassist2026-qr.svg){width="200px"}
```

**Priority:** Critical

---

## High Priority Issues

### H1. Title slide background logo has no text alternative

**Location:** `iassist-2026-slides.qmd:24` (YAML `data-background-image:`)

**WCAG:** 1.1.1 Non-text Content (Level A)

**Issue:** The UC OSPO Network logo on the title slide is injected as a CSS background image via `data-background-image`, which has no mechanism for alt text:

```yaml
title-slide-attributes:
  data-background-image: images/uc-ospo-network-logo-white.svg
```

Background images are inherently inaccessible to screen readers.

**Impact:** The title slide logo is invisible to assistive technology. However, the text "UC OSPO Network" appears in the slide title content, partially compensating.

**Fix (Option A — preferred):** Add the logo as a foreground `<img>` in the title slide using a custom HTML block positioned absolutely, and set `data-background-image` to nothing. This requires custom Reveal.js title slide markup.

**Fix (Option B — simpler):** Add an `aria-label` to the title slide section via Quarto attributes. This is not directly supported by Quarto's YAML but can be done via a post-render script or a `data-aria-label` attribute that Reveal.js passes through.

**Fix (Option C — minimum viable):** Add a visually hidden span to the slide that names the logo. Since the title text already says "Open Source as Institutional Infrastructure" and "UC OSPO Network" appears in the institute field, this is partially addressed. At minimum, confirm the institute field renders with the network name visible to screen readers — it currently does via `.institute` text content.

**Priority:** High

---

### H2. Citation text on dark Jim Kent slide fails contrast (WCAG 1.4.3)

**Location:** `iassist-2026-slides.qmd:230`

**WCAG:** 1.4.3 Contrast Minimum (Level AA)

**Issue:** The citation footnote on the dark navy slide uses `rgba(255,255,255,0.6)` text on `#1f335e` navy background. The effective blended color is approximately `#8090af`, which yields a contrast ratio of **3.85:1** — below the 4.5:1 minimum for normal text.

```markdown
::: {style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.52em; margin-top: 1.8em;"}
Kent, J.W. (2002). BLAT - The BLAST-Like Alignment Tool. *Genome Research* 12, 656–664. · genome.ucsc.edu
:::
```

At 30px root font size, `0.52em` = approximately 15.6px normal weight — this is normal text, not large text, so the 4.5:1 threshold applies.

**Contrast check:**
- Current: `#8090af` on `#1f335e` = **3.85:1** — FAIL
- Required: 4.5:1

**Fix:** Raise opacity to approximately 0.78 or use an opaque compliant color:

```markdown
::: {style="text-align: center; color: rgba(255,255,255,0.78); font-size: 0.52em; margin-top: 1.8em;"}
```

Or use opaque `#919eba` which achieves 4.61:1 on `#1f335e`.

**Priority:** High

---

### H3. Four "link" resource links in handout are ambiguous (WCAG 2.4.4)

**Location:** `iassist-2026-handout.qmd:560–563`

**WCAG:** 2.4.4 Link Purpose (In Context) (Level A)

**Issue:** The "Resources for Your Researchers" panel contains four links whose visible text is simply "link". When a screen reader user browses the links list, they hear four identical announcements of "link" with no way to distinguish which resource each refers to:

```html
<div class="resource-row">
  <span class="resource-file">README.md</span> template + guide &middot;
  <a href="https://ucospo.net/oss-resources/template-guides/readme-guide/"
     style="font-size:7.5pt; color:var(--blue);">link</a>
</div>
<!-- three more identical "link" links follow -->
```

**Impact:** Screen reader users cannot identify individual resources without switching to linear reading mode.

**Fix:** Replace "link" with a descriptive resource name for each:

```html
<div class="resource-row">
  <span class="resource-file">README.md</span> template + guide &middot;
  <a href="https://ucospo.net/oss-resources/template-guides/readme-guide/"
     style="font-size:7.5pt; color:var(--blue);">README.md guide</a>
</div>

<div class="resource-row">
  <span class="resource-file">LICENSE</span> guide with UC-approved options &middot;
  <a href="https://ucospo.net/oss-resources/template-guides/license-guide/"
     style="font-size:7.5pt; color:var(--blue);">LICENSE guide</a>
</div>

<div class="resource-row">
  <span class="resource-file">CONTRIBUTING.md</span> template + guide &middot;
  <a href="https://ucospo.net/oss-resources/template-guides/contributing-guide/"
     style="font-size:7.5pt; color:var(--blue);">CONTRIBUTING.md guide</a>
</div>

<div class="resource-row">
  <span class="resource-file">CODE_OF_CONDUCT.md</span> Contributor Covenant &middot;
  <a href="https://ucospo.net/oss-resources/template-guides/code-of-conduct-guide/"
     style="font-size:7.5pt; color:var(--blue);">CODE_OF_CONDUCT.md guide</a>
</div>
```

**Priority:** High

---

## Medium Priority Issues

### M1. Hover link color fails contrast on white backgrounds (WCAG 1.4.3)

**Location:** `ucospo-theme.scss:137`

**WCAG:** 1.4.3 Contrast Minimum (Level AA)

**Issue:** The hover state for links changes color to `$uc-orange` (`#ff9100`) on white backgrounds. This orange achieves only **2.26:1** against `#ffffff` — well below both the 4.5:1 normal text threshold and the 3:1 large text threshold.

```scss
.reveal a:hover {
  color: $uc-orange;  // #ff9100 on #ffffff = 2.26:1 — FAIL
}
```

This is a transient state (only active while hovering), but it still must meet contrast requirements. Users with low vision who hover and pause to read a link will see illegible text.

**Fix:** Replace the orange hover color with a darker amber that passes at 4.5:1:

```scss
.reveal a:hover {
  color: #af6300;  // 4.56:1 on #ffffff — PASS, preserves orange hue
}
```

Note: The orange remains appropriate for hover color on dark backgrounds (`#1f335e`) where it achieves 5.49:1.

**Priority:** Medium

---

### M2. Empty `<h2>` on the Jim Kent narrative slide (WCAG 1.3.1, 2.4.6)

**Location:** `iassist-2026-slides.qmd:215`; rendered at `iassist-2026-slides.html:432`

**WCAG:** 1.3.1 Info and Relationships (Level A); 2.4.6 Headings and Labels (Level AA)

**Issue:** The Jim Kent story slide uses a headingless dark background layout:

```markdown
## {background-color="#1f335e"}
```

This renders as `<h2></h2>` in the HTML — an empty heading element. Screen readers announce "heading level 2, empty" or skip it, then present the slide content without a navigable label. A screen reader user scanning headings will encounter a blank entry for this slide in the outline.

**Rendered HTML:**
```html
<section id="section" class="slide level2" data-background-color="#1f335e">
  <h2></h2>
  ...
```

**Impact:** The slide has no accessible name. Users navigating by headings cannot identify this slide in the document outline.

**Fix:** Add a visually hidden heading that names the slide content:

```markdown
## [Summer 2000: The Human Genome]{.sr-only} {background-color="#1f335e"}
```

The `.sr-only` class is already defined in the SCSS, so this renders the heading text for screen readers while keeping the slide visually headingless.

**Priority:** Medium

---

### M3. Timeline links in handout have no underline (WCAG 1.4.1)

**Location:** `iassist-2026-handout.qmd:186–188`, `271–272`

**WCAG:** 1.4.1 Use of Color (Level A)

**Issue:** Two link classes in the handout suppress underlines, leaving color as the sole visual indicator that they are links:

```css
.tl-link {
  color: var(--blue);
  text-decoration: none;   /* color is the only link indicator */
}

.learn-link {
  display: block;
  color: var(--blue);
  text-decoration: none;   /* color is the only link indicator */
}
```

Users with deuteranopia or protanopia (red-green color blindness) or those printing in black and white may not distinguish these links from surrounding text.

**Fix:**

```css
.tl-link {
  color: var(--blue);
  text-decoration: underline;
  text-underline-offset: 2px;
}
.tl-link:hover { color: var(--orange); }

.learn-link {
  display: block;
  color: var(--blue);
  text-decoration: underline;
  text-underline-offset: 2px;
}
.learn-link:hover { color: var(--orange); }
```

**Priority:** Medium

---

## Low Priority / Minor Issues

### L1. Micro-text attribution color fails contrast in handout stat cards

**Location:** `iassist-2026-slides.qmd:525`; `iassist-2026-handout.qmd:506, 535`

**WCAG:** 1.4.3 Contrast Minimum (Level AA)

**Issue:** Attribution lines inside stat cards use `color:#888` on `#f0f4fa`, yielding **3.21:1** — a fail for normal text. The font size at this scale (~12–13px) is normal text.

```html
<div style="font-size:0.42em; color:#888; margin-top:0.5em;">
  Tidelift (2024) State of the Open Source Maintainer Report
</div>
```

Similarly, the handout uses `color:#777` (line 506) on `#ffffff`, which yields **4.48:1** — technically a fail (the threshold is 4.5:1, missing by 0.02).

**Fix:**
- Change `color:#888` on `#f0f4fa` → `color:#6e6e6e` (4.62:1 — PASS)
- Change `color:#777` on `#ffffff` → `color:#767676` (4.54:1 — PASS, visually identical)

**Priority:** Low

---

### L2. Era labels in handout timeline use color as sole structural cue

**Location:** `iassist-2026-handout.qmd:109–119`

**WCAG:** 1.4.1 Use of Color (Level A)

**Issue:** `.era-label` elements ("Open Source Foundation", "Universal Infrastructure", etc.) use `color: var(--orange)` as their primary distinguishing visual property to signal category breaks in the timeline. Bold and uppercase are present, which partially compensates, but at 6pt these cues are weak.

**Fix:** Add a left border rule to reinforce structure without color alone:

```css
.era-label {
  color: var(--orange);
  font-size: 6pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border-left: 2px solid currentColor;  /* adds non-color structural cue */
  padding-left: 0.4em;
}
```

**Priority:** Low

---

### L3. Map dot legend in slides uses color-coded emoji

**Location:** `iassist-2026-slides.qmd:301`

**WCAG:** 1.4.1 Use of Color (Level A)

**Issue:** The world map legend uses `🟠` and `🔵` emoji, which rely entirely on color to distinguish the two dot categories:

```markdown
[🟠 UC OSPO Network &nbsp;·&nbsp; 🔵 CURIOSS member]{.small}
```

The map dots themselves also use only color to differentiate UC vs. CURIOSS institutions.

A `.sr-only` block (lines 303–305) provides a text alternative for the map, which mitigates the issue significantly. The legend emoji are still a color-only indicator for sighted colorblind users.

**Fix:** Replace emoji with text markers:

```markdown
[UC OSPO Network (orange) &nbsp;·&nbsp; CURIOSS member (blue)]{.small}
```

Or use shape-based differentiation in the Plot.js code (circle vs. square) alongside color.

**Priority:** Low

---

### L4. `tl-year` color (#999) at 6pt fails contrast

**Location:** `iassist-2026-handout.qmd:136–141`

**WCAG:** 1.4.3 Contrast Minimum (Level AA)

**Issue:** Year labels use `color: #999` at 6pt font. At this size, the text is normal text (requires 4.5:1). `#999` on `#ffffff` yields approximately **2.85:1** — a clear fail.

```css
.tl-year {
  font-size: 6pt;
  font-weight: 700;
  color: #999;
}
```

**Note:** This is a print-at-6pt handout, and the years are supplementary to the entry title. They are also redundant (years appear in the era-label sections), reducing impact. But technically it is a contrast failure.

**Fix:**

```css
.tl-year {
  font-size: 6pt;
  font-weight: 700;
  color: #767676;  /* 4.54:1 on white — PASS */
}
```

**Priority:** Low

---

## Recommendations

### Architecture

1. **Extend `logo-swap.txt`** to always set `alt="UC OSPO Network"` on the slide logo element — one line of JS covers every slide.

2. **Create a standard alt text pattern for QR codes.** Any future QR code image should include the encoded URL in the alt text: `alt="QR code for [URL]"`.

3. **Reserve `$uc-orange` for decorative and dark-background use only.** On white or muted light backgrounds, orange text and hover states will always fail contrast. Consider adding a comment to `ucospo-theme.scss` documenting this constraint.

4. **Add `text-decoration: underline` to `.tl-link` and `.learn-link`** in the handout. The global link underline in the slides SCSS (`ucospo-theme.scss:131`) does not carry over to the handout's inline CSS, where the reset (`* { margin: 0; padding: 0 }`) strips default browser underlines.

### Testing

- Run VoiceOver (Mac: Cmd+F5) on the rendered `iassist-2026-slides.html` and tab through all slides. Pay attention to the logo, QR code, and the empty heading on the Jim Kent slide.
- Use the VoiceOver rotor (VO+U, then arrow to "Links") on the handout to hear all links read in isolation — this will immediately surface the four "link" link-text violations.
- Use [contrast.tools](https://contrast.tools) to spot-check any inline color values not covered here.
- The Observable/Plot.js maps require manual colorblind simulation — use the Chrome DevTools "Vision Deficiencies" emulator (DevTools > Rendering > Emulate vision deficiencies) to check the world map dot differentiation.

### Documentation

- Add a comment to `ucospo-theme.scss` noting which colors are safe on white vs. navy backgrounds.
- The `.sr-only` utility and `role="list"` + `aria-label` pattern on the pipeline grid are worth documenting as templates for future slides.

---

## Positive Findings

The following accessibility features are well-implemented and should be preserved as patterns:

| Feature | Location | Notes |
|---------|----------|-------|
| Atkinson Hyperlegible font | `ucospo-theme.scss:27` | Designed specifically for low-vision readers |
| `.sr-only` utility class | `ucospo-theme.scss:162–172` | Correct implementation — used on both map slides |
| `prefers-reduced-motion` | `ucospo-theme.scss:261–267` | Suppresses all transitions and animations |
| Focus indicator | `ucospo-theme.scss:177–181` | 3px solid orange outline, 3px offset — exceeds minimum |
| `role="list"` + `aria-label` on pipeline grid | `iassist-2026-slides.qmd:126` | Correctly marks the campus/project grid as a semantic list |
| Map text alternatives | `iassist-2026-slides.qmd:303–305, 395–397` | Both OJS maps have `.sr-only` fallback descriptions |
| Logo alt text in handout | `iassist-2026-handout.qmd:292` | `<img alt="UC OSPO Network">` — correctly named |
| `keyboard: true` in Reveal config | `iassist-2026-slides.qmd:22` | Keyboard navigation explicitly enabled |
| `controls: true` | `iassist-2026-slides.qmd:20` | Navigation controls present for mouse/touch users |
| Image alt text on all logos | `iassist-2026-slides.qmd:55–67, 131–180` | All tool logos have descriptive alt text |
| Link underlines in slides | `ucospo-theme.scss:131–134` | `text-decoration: underline` on all slide links |
| XKCD image alt text | `iassist-2026-slides.qmd:542` | Full descriptive caption used as alt — exemplary |

---

## Quick Fix Checklist

Ordered by effort and impact:

- [ ] **`logo-swap.txt`** — add `logo.alt = 'UC OSPO Network'` in `updateLogo()` function
- [ ] **`iassist-2026-slides.qmd:798`** — add alt text to QR code image
- [ ] **`iassist-2026-handout.qmd:560–563`** — replace four "link" texts with resource names
- [ ] **`iassist-2026-slides.qmd:230`** — raise opacity from `0.6` to `0.78` on citation text
- [ ] **`iassist-2026-slides.qmd:215`** — add `[Summer 2000: The Human Genome]{.sr-only}` to empty heading
- [ ] **`iassist-2026-handout.qmd:186–188, 271–272`** — add `text-decoration: underline` to `.tl-link` and `.learn-link`
- [ ] **`ucospo-theme.scss:137`** — change hover link color from `#ff9100` to `#af6300`
- [ ] **`iassist-2026-handout.qmd:136`** — change `.tl-year` color from `#999` to `#767676`
- [ ] **`iassist-2026-slides.qmd:525` / handout:506, 535** — change `#888`/`#777` micro-text to `#6e6e6e`/`#767676`
