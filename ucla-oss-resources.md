# UCLA Open Source Resource Cheat Sheet

Working campus inventory for the UC OSPO Network  
Last verified: July 23, 2026

> **Status key:** **Confirmed** means an authoritative UCLA page or policy supports the entry. **Verified & Updated** indicates where decentralized or unconfirmed items have been clarified with specific campus pathways.

---

# Facet 1: Discoverability

## Scholarly preservation

### Does UCLA have premium subscriptions to scholarly data repositories? Where can people get assistance?

**Confirmed.** UCLA researchers have access to:

- [UCLA Dataverse](https://dataverse.ucla.edu/), an institutional repository managed by the UCLA Library Data Science Center (DSC) for publishing and preserving research data.  
- [Protocols.io](https://www.library.ucla.edu/help/services-resources/open-science-services/).  
- [Dryad](https://datadryad.org/), available across the UC system.  
- Other supported preservation and dissemination resources include [eScholarship](https://escholarship.org/), Vivli, and discipline-appropriate repositories.

The best starting point is the UCLA Library’s [Open Science Services](https://www.library.ucla.edu/help/services-resources/open-science-services/). UCLA Library staff can help with repository selection, data publication, data management, persistent identifiers, and open-science workflows.

### Does UCLA have a software catalog where people can list or promote open source projects?

**Needs campus confirmation.** UCLA does not currently operate a single, centralized, campus-wide public catalog of open source research software. Project repositories remain distributed across individual GitHub organizations (e.g., `ucla-data-archive`, `ucla-oarc`), lab sites, and centers. The UC OSPO Network software-discovery initiative represents the primary active effort working toward unified discovery.

### Are there other groups, educational resources, or services for scholarly software management, preservation, or archival?

**Confirmed.**

- The UCLA Library [Data Science Center](https://www.library.ucla.edu/about/programs/data-science-center/) supports reproducible research, open science, research data stewardship, software-based methods, and project consultations.  
- The [Office of Advanced Research Computing (OARC)](https://oarc.ucla.edu/) provides research computing, software development, data science, cloud, and high-performance computing expertise.  
- [OARC Research Software Development](https://oarc.ucla.edu/get-help/areas-expertise/research-software-development) supports simulation, containerization (Docker/Apptainer), full-stack development, APIs, cloud deployment, and Hoffman2-based software.  
- [UCLA Carpentries](https://ucla-data-archive.github.io/ucla-carpentries/) provides foundational, hands-on training in reproducible computing, version control (Git/GitHub), and data skills.  
- UCLA Library [Open Science Services](https://www.library.ucla.edu/help/services-resources/open-science-services/) supports integrations including GitHub-to-Zenodo archiving, OSF, ORCID, DMPTool, and eScholarship.

### Are there resources or workshops to help researchers articulate software impact for tenure and promotion?

**Verified & Updated.** No formal, central UCLA program explicitly targets software citation or software metrics in academic personnel reviews. However, practical guidance is available through:
- **UCLA Library DSC & Open Science Services:** Guidance on minting DOIs for code (via Zenodo/Dataverse) to enable proper academic citation.
- **UC OSPO Network:** Emerging consultations on tracking software dependencies, altmetrics, and contributor attribution for tenure portfolios.

---

## Licensing

### Who is UCLA’s technology transfer office?

**Confirmed.** UCLA’s technology transfer office is the [Technology Development Group (TDG)](https://tdg.ucla.edu/).

### Does TDG have resources of interest to open source software or hardware creators?

**Confirmed & Detailed.**

- TDG outlines [open source and software-sharing options](https://tdg.ucla.edu/about/faq/open-source-other-software-sharing-options).  
- TDG provides [source-available licenses for sharing software code for noncommercial use](https://tdg.ucla.edu/about/faq/open-source-other-software-sharing-options/licenses-sharing-software-code-non).  
- **Required Workflow:** Creators *must* submit a **Software Disclosure Form** to TDG (`software@tdg.ucla.edu`) prior to applying standard open-source licenses (MIT, Apache 2.0, GPL) if the code:
  1. Contains potentially patentable algorithms or hardware designs.
  2. Was developed under sponsored research or industry agreements with third-party IP obligations.
  3. Has direct commercialization potential.

---

## Documentation

### Does UCLA have resources to help researchers write software documentation?

**Confirmed.** While UCLA lacks a standalone "documentation clinic," structured support exists across units:

- **UCLA Carpentries & DSC:** Hands-on workshops covering README best practices, Markdown, and static site generation (e.g., GitHub Pages) for code repositories.
- **OARC Research Software Development:** Direct consultations for structuring user documentation, API references, and developer contribution guides.  
- **[UCLA Writing Programs](https://wp.ucla.edu/):** Supports general technical writing, though not tailored for open-source codebases.

---

# Facet 2: Funding

### Who is UCLA’s Sponsored Projects Office?

**Confirmed.** The [Office of Contract and Grant Administration (OCGA)](https://ocga.research.ucla.edu/) reviews, approves, and submits proposals to government and nonprofit sponsors and supports post-award administration.

### Does UCLA have a central office for grant-writing assistance?

**Confirmed.** The [Research Enhancement Office (REO)](https://www3.research.ucla.edu/reo) provides research development, funding search assistance, limited-submission coordination, and proposal-writing workshops.

### What tool does UCLA recommend for finding grant opportunities, and where can people get help?

**Confirmed.** UCLA provides institutional access to the [SPIN funding opportunity database](https://www3.research.ucla.edu/reo/fundopps). REO maintains lists of federal, foundation, and internal opportunities and provides search assistance.

### Where can researchers recruit student interns or find student-research matching programs?

**Confirmed.**

- [Undergraduate Research Portal](https://sciences.ugresearch.ucla.edu/courses/srp/): Posts faculty research listings for academic credit (SRP 99/199).  
- [Undergraduate Research Center–Sciences](https://sciences.ugresearch.ucla.edu/): Manages STEM undergraduate research pipelines.  
- [Undergraduate Research Center–Humanities, Arts, and Social Sciences](https://hass.ugresearch.ucla.edu/): Serves non-STEM disciplines.  
- **Project & Capstone Channels:** UCLA Data Science Union (DSU), Computer Science student organizations, and departmental capstone courses (e.g., CS 188 / Stats capstones).

### Who is UCLA’s Office of Development?

**Confirmed.** [UCLA Development](https://www.uclafoundation.org/about/development) and the [UCLA Foundation](https://www.uclafoundation.org/) handle campus fundraising, major gifts, and philanthropic accounts.

### Are there development programs of interest to open source creators, such as crowdfunding or gift sponsorship?

**Verified & Updated.** **[UCLA Spark](https://giving.ucla.edu/html/Spark/Student.html) is active** as UCLA’s official crowdfunding platform. 
- **Eligibility:** Projects must be explicitly sponsored by an official UCLA academic department, research lab, center, or registered student organization (RSO). Unaffiliated individuals cannot run independent campaigns.
- **Gift Processing:** Departmental development officers must establish dedicated gift funds before receiving corporate or individual donor gifts for software projects.

### Does UCLA have a Corporate Relations Office?

**Confirmed.** Corporate engagement is handled jointly by **UCLA Corporate Financial Partnerships** (External Affairs) and **TDG Corporate Relations**, acting as gateways for industry-sponsored research and technology partnerships.

### Does UCLA have industry consortia?

**Confirmed.** Major campus consortia with industry affiliate models include:
- **Samueli School of Engineering Industry Affiliates Program** (computer science, AI, systems).
- **California NanoSystems Institute (CNSI)** Innovation/Industry Partners Program.
- **Institute for Digital Research and Education (IDRE)** industry activities managed via OARC.

### Does UCLA have legal clinics relevant to open source creators?

**Verified & Updated.** UCLA School of Law does **not** host a dedicated open-source software legal clinic. 
- Official university-owned software IP matters are handled exclusively by **TDG** and **UC Office of the General Counsel (OGC)**.
- For independent student or founder startups, pro-bono legal office hours are periodically provided through the **UCLA Anderson Venture Accelerator**.

### What incubator or accelerator programs are available?

**Confirmed.**

- [UCLA Anderson Venture Accelerator](https://www.anderson.ucla.edu/about/centers/price-center-for-entrepreneurship-and-innovation/anderson-venture-accelerator): Cohort-based founder programming, workspace, and mentoring.  
- [Magnify at CNSI](https://www.cnsi.ucla.edu/magnify/): Incubator space and instruments for physical-science, bio, and software/hard-tech startups.  
- [UCLA Biodesign](https://biodesign.ucla.edu/): Health-tech, medical device, and digital health software innovation.  
- [UCLA Technology Development Group (TDG)](https://tdg.ucla.edu/): Startup formation guidance, commercialization grants, and pitch showcases.

### Does UCLA have an entrepreneur-in-residence program?

**Verified & Updated.** UCLA does not maintain a single, campus-wide EIR registry. Instead, Executives- and Entrepreneurs-in-Residence (EIRs) are embedded within specific units:
1. **TDG Advisory Board / Innovation Fund** (technology commercialization focus).
2. **Magnify at CNSI** (deep-tech and hardware focus).
3. **UCLA Anderson Center for Entrepreneurship** (general startup and venture creation focus).

### Does UCLA have internal seed grants that may fund software development?

**Confirmed.**

- REO [Internal Funding Opportunities database](https://www3.research.ucla.edu/reo/internalfunding/database).  
- [UCLA Innovation Fund](https://tdg.ucla.edu/ucla-researchers/ucla-innovation-fund): Provides seed grants to advance UCLA technologies toward commercial readiness or public release.  
- Academic Senate Council on Research (COR) grants and UCLA DataX seed funding.

---

# Facet 3: Community

### Where can maintainers get guidance on governance or conflict resolution?

**Confirmed.**

- **Interpersonal & Workplace Disputes:** [UCLA Office of Ombuds Services](https://ombuds.ucla.edu/) (confidential, neutral consulting) and [UCLA Equity, Diversity and Inclusion](https://equity.ucla.edu/).  
- **Open Source Project Governance:** Consultations on contributor agreements, Codes of Conduct enforcement, and sustainable project maintenance models are provided through the **UC OSPO Network**, **UCLA Library DSC**, and **OARC Software Developers**.

### Does UCLA subscribe to self-guided learning platforms?

**Confirmed.** UCLA employees have full access to **LinkedIn Learning** via institutional single sign-on. Additional technical training modules are provided via OARC workshops and Library tutorials.

---

# Facet 4: Product Design & Infrastructure

### Does UCLA have research computing or HPC consulting for optimization, containerization, and scaling?

**Confirmed.** [OARC](https://oarc.ucla.edu/) manages the **Hoffman2 Cluster** and provides high-performance computing consultations. Its Research Software Development team specifically assists with:
- Containerization using **Apptainer (Singularity)** and **Docker** for HPC environments.
- Code profiling, parallelization, GPU acceleration, and cloud deployment (AWS/GCP/Azure).

The UCLA Library Data Science Center complements OARC with reproducible workflow education and data management methods.

### Does UCLA have an accessibility office that supports software and documentation?

**Confirmed.** The [Disabilities and Computing Program (DCP)](https://dcp.ucla.edu/) within OARC leads digital accessibility efforts. Its **[UCLA Web Accessibility Initiative (UWAI)](https://dcp.ucla.edu/uwai)** provides:
- Audits and testing for web software interfaces and documentation.
- Guidance on WCAG 2.1 AA compliance and accessible design practices.

### What UCLA resources exist for AI usage?

**Verified & Updated.**

- **Central Guidance:** All AI platform use must comply with UC Systemwide Procurement and IT Security policies regarding data classification (P1–P4). Sensitive research or institutional data must not be entered into unvetted public models.
- **Enterprise Tools:** Main campus Google Workspace provides managed access to Google AI tools under enterprise privacy protections.
- **Health System:** **UCLA Health** operates under strict, isolated HIPAA-compliant governance rules separate from main campus.
- **Custom Research AI:** **OARC** and **UCLA DataX** assist researchers with hosting local, private open-weights models (e.g., Llama, Mistral) on Hoffman2 GPU nodes for secure data processing.

---

# Miscellaneous

### Key Campus Contacts Summary

| Focus Area | Primary Entry Point | Secondary / Specialist Contact |
| :--- | :--- | :--- |
| **Data & Open Science** | UCLA Library Data Science Center (DSC) | UCLA Library Open Science Services |
| **Advanced Software & HPC** | OARC Research Software Development | Hoffman2 Consulting |
| **IP & OSS Releases** | Technology Development Group (TDG) | UC OSPO Network Representative |
| **Accessibility Compliance** | Disabilities & Computing Program (DCP) | UCLA Web Accessibility Initiative (UWAI) |
| **Commercialization & Incubators** | TDG Startup Group | Anderson Venture Accelerator / Magnify |