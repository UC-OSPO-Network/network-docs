# Help Build the Next Round of OSPO Education Lessons

*We're recruiting authors and reviewers for four lessons in active development this summer.*

---

Four lessons are moving through development this July through September. Each one fills a gap in the current open source education landscape. We're looking for people from the broader OSS community to join as co-authors or peer reviewers.

Here's what's on the table:

| Lesson | Status | License | Target audience |
| --- | --- | --- | --- |
| UC Licensing Module | In development | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Researchers, developers, institutional staff |
| [Research Software: Citable and Discoverable](https://tim-dennis.com/research-software-citable-discoverable/) | Pre-alpha (8 episodes) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Researchers who code |
| Librarians as Open Source Stewards | Concept stage (5 episodes) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Library and information professionals |
| Open Source AI | In development (OSAID framing) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Researchers, practitioners, educators |

All materials are licensed CC BY 4.0. Everything built here is freely reusable by anyone.

---

## Two ways to get involved

### 1. Join the authoring team — with Carpentries Lesson Development Training

This is the deeper commitment and the more rewarding one.

Authoring team members join a [Carpentries Collaborative Lesson Development Training (CLDT)](https://carpentries.org/lesson-development/) cohort alongside lesson development. CLDT runs across three full days or six half-day online sessions (roughly 18 hours of instruction total) and teaches you to:

* Identify and characterize a target audience
* Write SMART learning objectives
* Design authentic exercises for formative assessment
* Structure lessons with cognitive load in mind
* Publish and maintain a lesson using the Carpentries Workbench on GitHub

By the end of training, each team has a live lesson website, a configured GitHub repository, a Lesson Design Notes document, and a complete lesson outline with episode-level objectives and exercises. The remaining work is writing the explanatory content — that happens in the async weeks that follow.

The whole arc from first session to a teachable draft is roughly 10-14 weeks.

**Prerequisites:** Markdown basics and the GitHub web interface. No command-line required.

**What you'll get:**
* Named co-authorship in the lesson metadata (CC BY attribution persists permanently)
* Co-author credit on the JOSE ([Journal of Open Source Education](https://jose.theoj.org/)) submission
* A citable Zenodo DOI through the UC OSPO Zenodo community before lab review
* A slot to co-teach the lesson at the next UC Open conference

---

### 2. Peer review a draft episode

Not ready for a full authoring commitment? Reviewers are just as important.

Structured peer review happens after a first draft exists, roughly mid-cycle. Reviewers work through one or two episodes using the Carpentries peer review rubric — checking for clarity, accuracy, audience fit, and exercise design. One or two review rounds, async, on your schedule.

**What you'll get:**
* Acknowledgment in the lesson's `CONTRIBUTORS` file and Zenodo record
* Invitation to co-teach the lesson if you want it

---

## Two more ways to plug in

**Beta teaching.** If your institution runs Carpentries workshops or similar, pilot one of these lessons after the first draft is ready. Debrief feedback directly shapes the final version. You'd be listed as a pilot instructor in the lesson notes.

**Subject matter expert consultation.** One 60-minute conversation — we bring a draft episode, you push back on the framing, the audience assumptions, or the tool choices. No ongoing commitment. You'll be acknowledged in the lesson notes.

---

## About these lessons

**UC Licensing Module** builds on the existing [Understanding Software Licensing](https://intersect-training.org/software-licensing/) lesson with UC-specific policy content. The existing lesson is strong but explicitly needs "to be supplemented with UC Policies" — this development cycle does that.

**Research Software: Citable and Discoverable** targets researchers who share code but haven't made it findable or reusable. Eight episodes covering CITATION.cff files, licensing, pixi environments, and metadata for discoverability. Pre-alpha draft already exists at [tim-dennis.com/research-software-citable-discoverable](https://tim-dennis.com/research-software-citable-discoverable/).

**Librarians as Open Source Stewards** makes the case that librarians already practice the core OSPO functions — cataloging is project discovery, copyright consulting is license guidance, collection development is dependency evaluation. The lesson gives library and information professionals the vocabulary and tools to act in an OSPO role, whether or not their institution has a formal OSPO. Targets the Library Carpentry track and Carpentries Incubator.

**Open Source AI** addresses the gap in structured education around open source AI practices. Development follows the [Open Source AI Definition (OSAID)](https://opensource.org/ai/open-source-ai-definition) framing. Scope is still being refined — this is a good moment to shape it.

---

## What this leads to

Finished lessons go through the [Carpentries Incubator](https://carpentries-incubator.org/) and Lab review process. Lessons that reach Lab status are teachable by any certified Carpentries instructor globally. Authors retain CC BY attribution throughout.

Reach out directly or open an issue on the [UC OSPO Education repo](https://github.com/UC-OSPO-Network/education) if you want to learn more about a specific lesson or contribution type.

---

---

# NotebookLM Prompt

Use this prompt after uploading the following sources to NotebookLM:
* This blog post draft
* The full CLDT curriculum (https://carpentries.github.io/lesson-development-training/instructor/aio.html)
* GitHub issue #121 (Librarians as Open Source Stewards) — paste the text directly
* The Research Software: Citable and Discoverable lesson index (https://tim-dennis.com/research-software-citable-discoverable/)
* The Open Source AI Definition (OSAID) document from opensource.org

---

**Prompt:**

You are helping design a community-facing lesson development recruitment campaign for the UC OSPO Education Network. The goal is to recruit co-authors and peer reviewers from the broader open source, research software, and library communities for a July-September 2026 development cycle.

Using the uploaded sources, help me work through the following:

1. **Audience mapping.** For each of the four lessons (UC Licensing Module, Research Software: Citable and Discoverable, Librarians as Open Source Stewards, Open Source AI), identify the most specific community that would have both the subject matter expertise and a practical stake in the lesson existing. Name 3-5 concrete communities, mailing lists, Slack workspaces, or events where this appeal should be distributed.

2. **Commitment calibration.** Based on the CLDT structure (four 4-hour sessions plus async writing) and a 10-14 week development arc, draft a one-paragraph "what's the actual ask" description for each contribution track (author, reviewer, beta teacher, SME consultation) that would hold up under scrutiny from a busy RSE or librarian who has been burned by underestimated volunteer asks before.

3. **Gaps and risks.** What topics or perspectives are currently missing from the four lessons that a potential co-author might notice and flag? What assumptions in the current lesson designs (audience, tool choices, prerequisite knowledge) are most likely to be challenged in peer review?

4. **UC Open workshop pitch.** Draft a 150-word proposal for a hands-on workshop at the next UC Open conference built around one of these lessons. Assume 60 minutes, 20-30 participants, mixed backgrounds.

5. **Follow-up questions.** After reviewing the sources, what 3-5 questions should I be prepared to answer when potential contributors ask about the lessons, the development process, or the credit and recognition structure?
