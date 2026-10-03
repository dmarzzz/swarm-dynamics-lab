---
id: lamb-2022-reproducible
type: paper
title: "Reproducible Builds: Increasing the Integrity of Software Supply Chains"
authors: ["Chris Lamb", "Stefano Zacchiroli"]
year: 2022
venue: "IEEE Software"
url: https://arxiv.org/pdf/2104.06020
doi: "10.1109/ms.2021.3073045"
arxiv: "2104.06020"
cite: "Lamb, C., & Zacchiroli, S. (2022). Reproducible Builds: Increasing the Integrity of Software Supply Chains. IEEE Software, 39(2), 62-70."
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "84 (Crossref, 2026-10-03)"
code: []
---

## Summary

An experience report from the Reproducible Builds project. Starting from Thompson's "Reflections on Trusting Trust" and the December 2020 SolarWinds Orion build-time compromise, it argues that reviewing source is not enough when users run binaries built by third parties. If a source tree always builds to bit-for-bit identical output, independent rebuilders can publish checksums and users can reject a vendor binary whose checksum disagrees. The paper sketches a verification scheme where semi-trusted builders announce checksums and the one reported by at least 50% of builders is trusted, so an attacker must take over at least half of the builder community. It reports that after seven years over 95% of the 30,000+ packages in Debian's development branch build reproducibly, and catalogues the sources of non-determinism (timestamps, build paths, file ordering, locale, randomness) and the tooling built to find them (adversarial rebuilding with varied environments, diffoscope). I read the abstract, introduction, the verification scheme, the Debian status and the non-determinism discussion.

## Contribution

Shows at distribution scale that "rebuild independently and compare" is feasible once non-determinism is engineered out, and frames it as a majority-vote defence for build integrity.

## Key results

- Over 95% of 30,000+ Debian development-branch packages reproducible after seven years (measured by the project).
- Majority-of-builders checksum rule: compromise requires at least 50% of builders (stated design, not a deployed measurement in the paper).
- Lists 174 documented supply-chain attacks in the literature (cited from other work) and SolarWinds as motivation.
- Adversarial rebuilding (deliberately varying build environment) is used to surface hidden non-determinism.

## Methods and models

Practitioner report and design argument; quantitative status from the Debian reproducibility infrastructure.

## Limitations and open questions

Requires source availability and deterministic toolchains; builder independence is assumed, not shown; the trusting-trust compiler problem is reduced, not removed.

## Relevance to us

Q2: the cleanest working example of a majority threshold on "did the part do what it should": n independent rebuilders must agree byte for byte. The transfer to sub-agents is limited by non-determinism, which the project had to engineer away for years; LLM sub-agents are non-deterministic by default, so any vote must compare semantic outputs or re-execute with fixed seeds. Q3: SolarWinds, which motivates the paper, is the case of corrupting the process that produces an artifact while the inputs stay clean, the analogue of corrupting a sub-agent's runtime or tools rather than its instructions. Related: [[crowdstrike-2021-sunspot]], [[torres-arias-2019-in-toto]], [[minsky-1996-cryptographic]], [[schneider-2005-implementing]].
