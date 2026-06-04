# IASSIST 2026 — Annotated Bibliography

Validation notes based on source fetches conducted 2026-06-04.
Status codes: ✅ confirmed · ⚠️ discrepancy or caveat · ❌ could not verify (URL inaccessible)

---

## Hettrick, S. et al. (2014). *UK Research Software Survey 2014*. Software Sustainability Institute. doi:10.5281/zenodo.14809

**Claims in talk:**
- 92% of researchers use software ✅ — confirmed from SSI blog post accompanying the survey
- 67% say their research would be impossible without it ⚠️ — **actual figure is 69%** ("it would not be practical"); slides should be corrected

**Notes:** Survey of 417 researchers at 15 UK Russell Group universities. The Zenodo record is the dataset; the blog post (software.ac.uk) is where the headline statistics are stated. The "(2014/2022)" attribution in the slides implies a US replication — the commonly cited US equivalent is Nangia & Katz (2017), which found similar numbers. If the 67% stat comes from a different survey year or geography, that source should be cited separately.

**Action:** Fix 67% → 69% in slide 2, or locate the source where 67% actually appears.

---

## Hoffmann, M. (HBS), Nagle, F. (HBS), & Zhou, Y. (University of Toronto). (2024). The value of open source software. Harvard Business School Working Paper 24-038. doi:10.2139/ssrn.4693148

**Claims in talk:**
- Open source software would cost $8.8 trillion to replace ✅ — confirmed from abstract: "the demand-side value is much larger at $8.8 trillion"
- Supply-side cost to recreate widely-used OSS: $4.15 billion ✅ — confirmed from abstract: "We estimate the supply-side value of widely-used OSS is $4.15 billion"
- Speaker notes ~2,000x ratio ($8.8T ÷ $4.15B ≈ 2,120x) ✅ — arithmetically correct

**Additional verified stats (not currently in slides, available if useful):**
- "Firms would need to spend 3.5 times more on software than they currently do if OSS did not exist" — cleaner for non-technical audiences than the $8.8T headline
- "96% of the demand-side value is created by only 5% of OSS developers"
- "Top six programming languages comprise 84% of the demand-side value"

**Notes:** PDF verified directly (ssrn-4693148.pdf). Zhou is at Rotman School of Management, University of Toronto — not HBS; bibliography entry should reflect this. Corrected author affiliation: Hoffmann (HBS), Nagle (HBS), Zhou (University of Toronto).

---

## Barker, M., Chue Hong, N. P., Katz, D. S., et al. (2022). Introducing the FAIR Principles for research software. *Scientific Data*, 9, 622. doi:10.1038/s41597-022-01710-x

**Claims in talk:**
- FAIR4RS extends FAIR principles to research software ✅ — this is the defining paper; Nature redirected to auth wall but the paper is well established and the DOI resolves correctly

**Notes:** Published by a large author group under the RDA/FORCE11/ReSA working group. The DOI is correct. Claim as stated is accurate.

---

## Ruff, N. (2026). The role of foundations in advancing open collaboration and innovation. *UC Open Summit*. youtu.be/eBriL3CDNeo

**Claims in talk (slides and notes):**
- "Neutral convener" framing — quoted at timestamp ~8:17–8:49 ❌ — YouTube not fetchable; could not confirm timestamp
- 70% of new AI PhDs go straight to industry (was 50/50 a decade ago) ❌ — in notes only (cut AI slide), not on current slides; not verified
- 90% of notable AI models come from a handful of companies ❌ — same

**Notes:** The "neutral convener" quote appears on the UC OSPO Network slide and is attributed to this talk. Timestamps in the speaker notes (6:15–7:15 and 8:17–8:49) give specific locations to verify if needed. The AI stats (70%/90%) are from the cut slide so are not currently in the deck — no action needed unless that slide is restored.

---

## Gomez, J., Lovell, E., Lieggi, S., Cardenas, A. A., & Davis, J. (2025). Recipe for discovery: A pipeline for institutional open source activity. arXiv:2506.18359

**Claims in talk:**
- 236,000+ repos scanned ✅ — paper reports 236,037 total (Table 2); "200,000+" in slides is technically correct but imprecise; updated to "236,000+"
- ~82,000 institutionally affiliated ✅ — paper reports 81,640 after LLM-based filtering (Table 4); slide previously said "~52,000" which was wrong and has been corrected
- 10 UC campuses ✅ — Table 1 lists all ten: UCB, UCD, UCI, UCLA, UCM, UCR, UCSB, UCSC, UCSD, UCSF
- Paper is UC-specific ✅ — all authors are at UC Santa Cruz; UC system is the explicit case study

**Additional verified stats (not in slides, available if useful):**
- 77.5% of affiliated repos have no explicit license
- 84.1% have a README; only 22.5% have a description; 6% have a Code of Conduct; 14% a Contributing Guide
- DEV (42.9%) and EDU (42.1%) dominate project types across the UC system
- UCSD has the largest absolute number of affiliated repos (18,163); UC Merced the lowest affiliation rate (23.7%)

**Notes:** PDF verified directly (2506.18359v2.pdf). The pipeline uses gpt-5-mini for LLM-based affiliation filtering.

---

## Scarlett, V., Curty, R. G., Gomez, J., Langdon, L., Janée, G., & Budden, A. E. (2025). A system-wide snapshot: A multi-campus survey of open source contributors at the University of California. SocArXiv. doi:10.31235/osf.io/p8bx6_v1

**Claims in talk:**
- 294 respondents ✅ — confirmed
- 58% of experienced contributors are also maintainers ✅ — confirmed (exact wording: "58% of experienced open source contributors have served as project maintainers")
- #1 challenge: finding time to write documentation ✅ — confirmed ("insufficient time, especially for documentation duties")
- What contributors asked for most: sustainability grants and computing infrastructure ✅ — confirmed ("robust computing infrastructure and sustainability-focused funding")

**Notes:** All claims verified. Strong source. DOI resolves correctly via CrossRef.

---

## Tidelift. (2024). *The 2024 state of the open source maintainer report*. Tidelift.

**Claims in talk (speaker notes only, not on slides):**
- 60% of maintainers are unpaid ❌ — Tidelift was acquired by SonarSource; the original URL redirects to a SonarSource product page with no survey data; could not verify
- 43% report burnout ❌ — same

**Notes:** These stats appear only in speaker notes for the sustainability slide, not on the slide itself, so they are low-risk for the presentation. However, since the original URL is dead, the citation as written is not resolvable by an audience member. Recommend either finding an archived version (the Internet Archive may have it) or replacing with a verifiable secondary source that cites these figures. The stats are consistent with other maintainer surveys and widely reproduced in press coverage of this report.
