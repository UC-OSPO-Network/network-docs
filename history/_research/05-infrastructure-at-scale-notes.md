# Research notes: Infrastructure at Scale

Moved word for word from `history/05-infrastructure-at-scale.qmd` on 2026-11-17. Not rendered or published.
These notes are unverified. Do not write prose from them; write from the chapter's claims file.

## Ceph: The Dissertation That Funded an OSPO

*Draft - fill in: Sage Weil's dissertation at UCSC's SSRC under Prof. Scott A. Brandt; the design problem (exabyte-scale distributed storage without a central lookup table - using CRUSH algorithm for deterministic placement) [@weil2006ceph]; the Linux kernel merge in 2010; Weil founding Inktank to commercialize it; Red Hat acquiring Inktank in 2014; the Linux Foundation launching the Ceph Foundation in 2018 for neutral governance; crucially: the proceeds from Inktank's commercialization funding CROSS (Center for Research in Open Source Software) at UCSC - which became the first UC OSPO and the seed of the network this document represents.*

## RISC-V: The Summer Project in Ten Billion Devices

*Draft - fill in: Asanovic and Patterson wanting a clean, open instruction set for their graduate students to build chips without paying ARM royalties; the three-month summer project; the decision to make it fully open and royalty-free [@riscv2019]; the formation of the RISC-V Foundation; the dramatic relocation to Switzerland in 2020 to stay neutral in US-China trade tensions (both countries were adopting RISC-V for strategic hardware independence); the current scale: 350+ member organizations, 70 countries, 10 billion+ devices shipped.*

## Named Data Networking: Rethinking the Internet

*Draft - fill in: Lixia Zhang's background - growing up in rural China, driving tractors during the Cultural Revolution, earning her PhD at MIT under David Clark, working at Xerox PARC, joining UCLA. Zhang was the only woman and the only student at the very first IETF meeting in 1986. She coined "middlebox," designed RSVP (Resource Reservation Protocol), and is an inductee of the Internet Hall of Fame. NDN as a proposal to fundamentally rethink internet architecture: instead of routing by address (where data lives), route by name (what data is) [@zhang2014ndn]. The $14M NSF Future Internet Architecture project. The ongoing research and deployment work.*

## Ray: Two PhD Students and the OpenAI Stack

*Draft - fill in: The RISELab context (successor to AMPLab); Nishihara and Moritz as PhD students repeatedly rewriting Python code every time they needed to scale to more than one machine; Ray [@moritz2018ray] as a general-purpose distributed computing framework designed to make Python programs scale to clusters as easily as they run on a laptop; the adoption by OpenAI for their training and inference infrastructure; the Linux Foundation donation in 2025; the current scale of usage across AI and ML workloads.*
