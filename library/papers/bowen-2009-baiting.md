---
id: bowen-2009-baiting
type: paper
title: Baiting Inside Attackers Using Decoy Documents
authors:
- Brian M. Bowen
- Shlomo Hershkop
- Angelos D. Keromytis
- Salvatore J. Stolfo
year: 2009
venue: Security and Privacy in Communication Networks
url: https://eudl.eu/doi/10.1007/978-3-642-05284-2_4
doi: 10.1007/978-3-642-05284-2_4
arxiv: null
cite: Brian M. Bowen; Shlomo Hershkop; Angelos D. Keromytis; Salvatore J. Stolfo.
  (2009). Baiting Inside Attackers Using Decoy Documents. Security and Privacy in
  Communication Networks, 51-70. https://doi.org/10.1007/978-3-642-05284-2_4
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 194
code: []
---

## Summary

The authors propose automatically generated decoy documents to detect malicious insiders attempting to steal information. The abstract describes bogus credentials that trigger alerts and embedded beacons that signal when and where a document is opened, with feasibility evaluated using compromised honeypots.

## Contribution

Generated decoys, bait credentials, and document-opening beacons.

## Key results

- Feasibility is reported on attacker-penetrated honeypots; no numerical success rate is supplied in the abstract.

## Methods and models

Generated decoys, bait credentials, and document-opening beacons.

## Limitations and open questions

A beacon requires a rendering or network path that produces a signal; the abstract does not establish resilience against an adversary disabling those paths.

## Relevance to us

A comparison source for coordinated automation and security measurement. Full-text methods and replication have not been checked.

## Access provenance

Crossref metadata and the abstract at the recorded URL were opened directly or through Exa content extraction on 2026-10-03. Any non-null citation count is OpenAlex cited_by_count on that date. Abstract depth is deliberate even where an open PDF was found.


## Notes from shadow/sol-w5

Added in parallel from pipeline batch #77; this id was taken first by shadow/sol-g51, so my entry is folded in here. My reading depth: abstract (source opened: https://doi.org/10.7916/d86q242f).

### Summary

Trap-based defence against malicious insiders who exfiltrate and use sensitive information. The system automatically generates "decoy documents" and places them on file systems to entice an insider to open them. Each decoy carries several kinds of bogus credentials that raise an alert when used, plus "stealthy beacons" that phone home to a server when and where the document is opened. Goals: make the attacker spend effort separating real from bogus information, and detect exploitation attempts. Evaluated by placing decoys on honeypots that real attackers penetrated, showing feasibility. Only the abstract (Columbia Academic Commons / DataCite record) was read; the repository page itself is behind an anti-bot proof-of-work wall. A 2008 Columbia technical report version exists (DOI 10.21236/ada500672).

### Contribution

Early systematic design of document-level honeytokens with two independent trip-wires (credential use and document-open beacons), extending honeypots from whole systems to individual pieces of bait content.

### Key results

- Feasibility demonstrated on penetrated honeypots (abstract; no detection rates in the abstract).

### Methods and models

Automated decoy generation with embedded bogus credentials and beacons; alerting server; deployment on honeypots.

### Limitations and open questions

Not assessed beyond the abstract. Beacons depend on the viewer executing or fetching embedded content, which careful attackers can block.

### Relevance to us

Bait content with embedded trip-wires is a natural detector for autonomous agents that read and act on documents: an agent swarm that ingests a decoy and uses its credentials or follows its beacon reveals itself. Predecessor to commercial canary tokens [[gh-thinkst-canarytokens]]; credential-level analogue [[juels-2013-honeywords]]; email/account canaries [[farooqi-2020-canarytrap]]; agent-targeted honeypots [[gh-palisaderesearch-llm-honeypot]].
