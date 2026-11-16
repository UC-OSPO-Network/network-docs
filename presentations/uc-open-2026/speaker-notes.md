# Speaker Notes — UC OSPO Education Activities
**UC Open | April 22–23 | UC Berkeley**
Tim Dennis | Director, Data Science Center, UCLA Library

*Target: 15 minutes. Rough pacing noted per slide. Slides marked ⚡ need the bridging language below — it's not on the slide, it's verbal only.*

---

## Slide 1 — Title
*~30 sec*

> "Thanks for having me. I'm Tim Dennis, Director of the Data Science Center at UCLA Library. What I want to share today is what a UC-wide OSPO education program actually looks like in practice — not the vision, but the built thing. We're in Year 2 of Sloan Foundation funding, all 6 ospo campuses are involved, and the platform is live. Let's dig in."

---

## Slide 2 — Open Source Literacy Isn't One-Size-Fits-All
*~1:30*

> "Here's the problem we started with. Open source literacy isn't a single thing. A faculty researcher applying for an NIH grant needs FAIR compliance and reproducibility documentation. A grad student needs Git basics and a portfolio. A tech transfer officer needs to know what 'commercializing open source' even means at a UC institution. A research computing admin needs to vet tools for P3/P4 data environments.

> These are real people with real, divergent needs. And nobody had mapped the right lesson to the right person at the right moment in their career. That's the mandate this project took on."

⚡ **Add verbally — "Why the Library" bridge (not on slide):**

> "And the reason the library is the right actor here: we sit outside any single department, we're already trusted infrastructure, and we've spent years building instructor networks through programs like UC Carpentries. We're not building this from scratch — we're connecting what already exists and filling what doesn't."

---

## Slide 3 — Built by a System-Wide Community
*~45 sec*

> "Before I go further — this is not a UCLA project. This is a distributed UC team. Reid Otsuji, Karla Padilla, and David Minor at UCSD anchored the education committee. Lauren Reyes at UCSD led the UI/UX work. Laura Langdon keeps the community coordinated. And student developers did the heavy engineering lift on the infrastructure side.

> No single campus owns this — which is exactly the point. Keep that in mind as I show you what we built."

*Move through this quickly — 45 seconds max. The team slide currently sits at #3; if you can reorder, consider moving it to after slide 9 so the problem-solution arc runs clean. If you can't reorder before tomorrow, just keep it brief and treat it as a quick acknowledgment.*

---

## Slide 4 — A Curated, Navigable Learning Experience
*~1:30*

> "The answer to the 'right lesson, right person, right time' problem is education.ucospo.net. It's live right now, go look at it on your phone.

> Three things make it work. First, role-based filtering — you tell it whether you're a maintainer, contributor, or consumer, and it filters the 56+ vetted lessons accordingly. Second, visual signposting — color-coded skill badges so you can immediately see if something is beginner, intermediate, or advanced. And third — and this one matters for the open science crowd — every lesson is tagged with Bioschemas Training Metadata. learningResourceType, timeRequired, mentions. That means these lessons are globally discoverable by systems like TeSS and schema.org scrapers, not just findable by people who already know we exist."

---

## Slide 5 — Structuring the Open Source Journey
*~1:00*

> "The 56 lessons are organized into six structured pathways — from 'Getting Started' for someone who's never heard of a pull request, all the way to 'Strategic Practices and Career Development' covering FAIR software, reproducibility, and grant alignment. The pathways are opinionated — we're not just a link dump. The sequence is designed so a learner can actually progress."

---

## Slide 6 — Eliminating Technical Debt Through Automation
*~1:30*

> "Here's something most curriculum projects don't talk about: the operational debt. We started with a Google Sheets inventory of lessons — fragmented URLs, missing tags, no time estimates, inconsistent dates. Classic.

> Our student developer built an automated pipeline to fix that. Slug generation, IETF language standardization, word-count-to-ISO-8601 time estimation, and automated scraping for author attribution and license info. The result: time estimate coverage went from zero to 98%. Author attribution from 57 to 88%. And we saved over 35 hours of manual labor that would have been someone's miserable afternoon.

> The infrastructure is Keystatic CMS feeding an Astro frontend deployed on GitHub Pages. Open, auditable, forkable."

---

## Slide 7 — [Section transition — GAP ANALYSIS]
⚡ **Verbal bridge before advancing to slide 8 (not on any slide):**

> "So we've built the platform. We've got the lessons, the filtering, the pathways, the metadata. But here's the honest problem: the content that exists globally doesn't cover what UC researchers actually run into day-to-day. Nobody has written a lesson on navigating UC tech transfer. Nobody's built a module on what P3/P4 data compliance means for your open source project. When we did the gap analysis, that's exactly what we found — and that's what the next section is about."

*Pause briefly here. This is the pivot point of the talk.*

---

## Slide 8 — Identifying the UC-Specific Curriculum Gaps
*~1:30*

> "The left column is what exists globally — and it's good. Version control, Python and R workflows, contribution guides, license overviews. Solid material.

> The right column is what doesn't exist for UC specifically. Institutional security policy guidance for P3/P4 environments. Licensing and compliance in the UC context — not generic, but navigating UC's actual policies. Tech transfer and patents. And honestly, the one I think is most important: an extreme-beginner framing of open source for non-technical academic staff. The people who work in research administration, grants offices, department operations — they encounter open source constantly and have no on-ramp whatsoever.

> These aren't hypothetical gaps. They came directly from the learner persona work and the gap analysis the education committee ran."

---

## Slide 9 — Filling the Gaps: Collaborative Lesson Development
*~1:30*

> "So how do we fill them? The model is a four-step cohort cycle. We identify an institutional gap — say, licensing and compliance. We assemble a cross-functional team of about four subject matter experts from across campuses. They collaborate using the Carpentries Incubator framework and markdown templates, so the output is immediately publishable and peer-reviewable. Then we pilot it — beta testing at events like UC Love Data Week — before it goes live on the platform.

> We're actively running this right now. The Licensing and Compliance lesson is in draft, and it's being built with domain-specific episodes so individual campuses can adapt it for their context."

---

## Slide 10 — Workforce Enhancement: Training the Trainers
*~1:30*

> "The platform and the curriculum only work if people are actually teaching the material. That's where the Carpentries partnership comes in.

> We have 60+ certified instructors across all 10 UC campuses right now. Last year UC Carpentries reached over 500 learners system-wide. The Sloan funding includes a Platinum Carpentries membership specifically to provide dedicated instructor training seats and lesson development support.

> The key framing here is 'training the trainers.' We're not trying to teach every UC researcher ourselves — we're building the human infrastructure so that local experts at each campus can deliver the material. That's what makes this scalable across a 10-campus system."

---

## Slide 11 — A Living, Interconnected Ecosystem
*~1:00*

> "Zoom out and here's what this actually looks like. The Library and UC OSPO sit at the center as the neutral, interdisciplinary hub. UC Carpentries deploys the instructors. UC Love Data Week pilots new beta workshops — like the Citable Discoverable Software lesson we ran last year. CKG groups handle cross-campus knowledge sharing. Academic departments integrate open source into formal research.

> None of these spokes would talk to each other without a neutral convener. That's the structural argument for why this lives in the library."

---

## Slide 12 — Built for Continuous Evolution
*~1:00*

> "We built this to keep running after the grant ends. Three mechanisms. First, downloadable curriculum packages — any campus lead can download a lesson and run it locally without asking us. Second, GitHub Issues integration directly from the website — learners and instructors can flag friction points and request content without needing to know our workflow. Third, system-wide tracking of lesson lifecycle status so we know what's active, what needs updating, and what's retired.

> The goal is a platform the community maintains, not one that requires a dedicated team to babysit."

---

## Slide 13 — Let's Build Together (CTA)
*~1:00*

⚡ **Open with this line before reading the three bullets:**

> "If you're in this room, you're not a beginner — so let me be specific about what I'm actually asking for."

> "**Learn:** Go to education.ucospo.net this week. Browse it. And if you find a gap we missed, open a GitHub issue — that's a direct line to us.

> **Teach:** Pick one lesson that fits your campus's needs and run it this quarter. We want the feedback from real delivery more than we want perfect lessons.

> **Build:** We're forming the next cohort for the Licensing and Compliance lesson right now. If your campus has a subject matter expert — a tech transfer officer, a research compliance person, a licensing librarian — I want to talk to you today. Come find me.

> The platform is live, the infrastructure is real, the gaps are documented. What we need now is your campus's expertise in the room."

---

## Timing Summary

| Slide | Topic | Target |
|-------|-------|--------|
| 1 | Title / framing | 0:30 |
| 2 | Problem + why the library ⚡ | 2:00 |
| 3 | Team | 0:45 |
| 4 | Platform — navigable experience | 1:30 |
| 5 | Six pathways | 1:00 |
| 6 | Automation / technical debt | 1:30 |
| ⚡ | Gap analysis bridge (verbal) | 0:20 |
| 7 | UC curriculum gaps | 1:30 |
| 8 | Collaborative lesson development | 1:30 |
| 9 | Workforce / Carpentries + 500+ stat | 1:30 |
| 10 | Ecosystem diagram | 1:00 |
| 11 | Continuous evolution | 1:00 |
| 12 | CTA ⚡ | 1:00 |
| **Total** | | **~15:05** |

---

*⚡ = bridging language that's verbal only, not on the slide. Don't look at the screen when you say these — make eye contact with the room.*
