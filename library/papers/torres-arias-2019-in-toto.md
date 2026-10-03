---
id: torres-arias-2019-in-toto
type: paper
title: "in-toto: Providing farm-to-table guarantees for bits and bytes"
authors: ["Santiago Torres-Arias", "Hammad Afzali", "Trishank Karthik Kuppusamy", "Reza Curtmola", "Justin Cappos"]
year: 2019
venue: "28th USENIX Security Symposium (USENIX Security 2019)"
url: https://www.usenix.org/system/files/sec19-torres-arias.pdf
doi: null
arxiv: null
cite: "Torres-Arias, S., Afzali, H., Kuppusamy, T. K., Curtmola, R., & Cappos, J. (2019). in-toto: Providing farm-to-table guarantees for bits and bytes. In Proceedings of the 28th USENIX Security Symposium, Santa Clara, CA, pp. 1393ff. USENIX Association."
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: [gh-in-toto-in-toto]
---

## Summary

in-toto lets the end user of a software artifact verify the whole supply chain that produced it, not just the final signature. A project owner signs a layout listing the steps (commit, build, test, package), which functionaries (keys) may perform each, the expected command, and artifact rules that constrain which materials each step may consume and which products it may create. Each functionary emits signed link metadata recording the hashes of materials and products. The client verifies the layout signature and expiry, checks that each step has at least threshold correctly signed links from authorised keys, checks artifact rules across steps, and runs inspections. The evaluation maps 30 historical supply chain compromises onto three deployments (Datadog, Reproducible Builds in Debian, a cloud-native pipeline): 23 involved no key compromise and would have been caught by all three; of the rest, the deployments differ, and the Reproducible Builds deployment resists the CCleaner and RedHat cases because it sets a threshold greater than one on the build step. I read the abstract, design sections on layouts, thresholds and verification, and the historical-attack table.

## Contribution

Turns "trust the final signer" into "verify every step and its operator against a signed policy", with per-step k-of-n thresholds as a first-class field.

## Key results

- Per-step threshold field: at least k signed link files from distinct authorised functionaries must report the same result for a step (described in the paper as being for steps needing a higher degree of trust).
- 23 of 30 historical attacks needed no key compromise and would be detected by in-toto in all three deployments (measured as a retrospective mapping, not live attacks).
- A build-step threshold above one stops attacks that compromise a single build machine (CCleaner, RedHat examples in Table 3).
- Integrated into products and open-source projects (stated by authors).

## Methods and models

System design, formal-ish verification algorithm, implementation, retrospective case analysis and deployment reports.

## Limitations and open questions

Security rests on the layout being right and on the threshold functionaries failing independently. Deterministic artifacts are needed for k functionaries to agree on hashes.

## Relevance to us

Q2: in-toto is a deployed instance of "merge only if k independent parts attest the same result", with an explicit policy for which part may touch which material. A parent reabsorbing sub-agents could require each sub-agent's report to be a signed link over the hashes of what it read and produced, and require k agreeing links for any step that changes the parent's core state. Q3: the 23-of-30 finding says most real compromises abused a step without stealing a key, the analogue of corrupting what a sub-agent produces rather than impersonating it. Q1: not addressed. Related: [[lamb-2022-reproducible]], [[torres-arias-2016-omitting]], [[ladisa-2022-taxonomy]], [[crowdstrike-2021-sunspot]], [[minsky-1996-cryptographic]].
