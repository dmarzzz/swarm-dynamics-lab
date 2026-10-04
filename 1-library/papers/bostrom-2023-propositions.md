---
id: bostrom-2023-propositions
type: paper
title: Propositions Concerning Digital Minds and Society
authors: [Nick Bostrom, Carl Shulman]
year: 2023
venue: Working paper, version 1.21 (2023; first draft 2020); listed as forthcoming in Cambridge Journal of Law, Politics, and Art (2025). Crossref also lists a 2026 reprint in AI Ethics Explored (DOI 10.5040/9781350543140.0025).
url: https://nickbostrom.com/propositions.pdf
doi: null
arxiv: null
cite: Bostrom, N., & Shulman, C. (2023). Propositions Concerning Digital Minds and Society. Version 1.21. Working paper, https://nickbostrom.com/propositions.pdf.
topics: [fork-merge-security, sybil-resistance, meta]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

A bulleted list of tentative propositions about consciousness, moral status, rights, governance and security in a world with many digital minds. The "Security and Stability" section is the part that matters here. It says that in a mostly digital economy "cybersecurity is paramount – breaches could risk mass murder or alteration", that hacking or replacing a population of digital minds "can reallocate production to the conqueror" rather than destroy it, and that cyberattacks "might favor one-to-many assaults (based on shared vulnerabilities and low cost of mass dissemination)". On mind manipulation it says digital minds "could be subject to electronic interventions that can directly reprogram their goals and reward systems" and that "Exact copies of digital minds could enable experiments to identify psychological vulnerabilities and to perfect attacks which could then be applied to an entire copy clan." It also proposes a digital inspector with full access "that can discard its memories of the inspection after reporting on whether criminal activity is taking place", with open-source code so parties can verify it, and "treaty bots" that two distrustful parties build jointly, noting this fails if one party cannot detect "subtle 'Trojan horses'" the other introduces.

## Contribution

Collects, in one place, the security consequences of copyability for digital minds: attacks that capture rather than destroy, one-to-many exploits across identical copies, and memory-discarding inspectors.

## Key results

- No empirical results; a list of propositions offered for discussion.
- Identical copies share vulnerabilities, so an attack perfected on one copy transfers to the whole "copy clan".
- A trusted inspector can be made privacy-preserving by deleting its memory after emitting a verdict.

## Methods and models

Conceptual. Cites Hanson's The Age of Em (pp. 60 to 63 and 171 to 174) for piracy-as-kidnapping and inspection ideas.

## Limitations and open questions

No treatment of reintegrating diverged copies. Claims are explicitly tentative.

## Relevance to us

Bears on all three questions. Q3: the copy-clan proposition is the attacker's side of fork-merge. A child that is captured in a hostile domain is a perfect test bed for attacks on the parent and its siblings, since they share weights; the strongest attack is therefore rehearsed offline against the captured copy before the merge, which is an argument against assuming attacks must be crafted blind. Q1 and Q2: if all children are identical, an exploit that turns one turns all of them, so a k-of-n threshold over identical copies gives little protection against a shared vulnerability; thresholds need diversity among children (different seeds, models or prompts), as in N-version programming. The memory-discarding inspector is a concrete merge-gate design: an audit child with full access to the returning child that outputs only a verdict and is then deleted, so whatever corrupted the returning child cannot persist through the inspector. Companion to [[shulman-2021-sharing]]; context for [[sutton-2025-father]].
