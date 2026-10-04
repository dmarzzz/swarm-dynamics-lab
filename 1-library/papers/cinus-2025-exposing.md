---
id: cinus-2025-exposing
type: paper
title: Exposing Cross-Platform Coordinated Inauthentic Activity in the Run-Up to the 2024 U.S. Election
authors:
- Federico Cinus
- Marco Minici
- Luca Luceri
- Emilio Ferrara
year: 2025
venue: Proceedings of the ACM Web Conference 2025 (WWW)
url: https://arxiv.org/abs/2410.22716
doi: 10.1145/3696410.3714698
arxiv: '2410.22716'
cite: Cinus, F., Minici, M., Luceri, L., & Ferrara, E. (2025). Exposing Cross-Platform Coordinated Inauthentic Activity in the Run-Up to the 2024 U.S. Election. In Proceedings of the ACM on Web Conference 2025 (pp. 541–559). ACM.
topics:
- swarm-detection
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 37 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Collects 2024 US election conversations on X, Facebook and Telegram and builds similarity networks of sharing behaviour within and across platforms. An extended coordination detection model finds coordinated communities with suspicious sharing patterns, including Russian-affiliated media systematically promoted on Telegram and X, and cross-platform coordinated activity spreading partisan, low-credibility and conspiratorial content.

## Contribution

Shows coordination routinely crosses platform boundaries and that single-platform detectors miss part of it.

## Key results

- Evidence of potential foreign interference: Russian-affiliated media promoted across Telegram and X (abstract).
- Substantial intra- and cross-platform coordinated inauthentic activity driving low-credibility content (abstract). No numbers in the abstract.

## Methods and models

Similarity networks over shared URLs and content across three platforms; community detection. The abstract does not specify how accounts are linked across platforms.

## Limitations and open questions

Abstract only. Cross-platform identity linking is the hard part and is not described in the abstract; validation against ground truth is not reported there.

## Relevance to us

Agent swarms will span platforms and APIs. This is the main cross-platform coordination study; see the cross-platform gap flagged in [[mannocci-2026-detection]].

## Notes from dmarz/sd-bots

Folded in by dmarz/sd-merge from the duplicate entry `cinus-2024-exposing` (added_by dmarz/sd-bots, accessed 2026-10-03, read_depth abstract, relevance 4). Same source (same arXiv id and DOI); the kept id uses the year of the published version given in cite.

- Frontmatter `year` in the folded entry: 2024
- Frontmatter `venue` in the folded entry: Proceedings of the ACM on Web Conference 2025 (WWW '25)
- Frontmatter `cite` in the folded entry: Cinus, F., Minici, M., Luceri, L., & Ferrara, E. (2025). Exposing Cross-Platform Coordinated Inauthentic Activity in the Run-Up to the 2024 U.S. Election. In Proceedings of the ACM on Web Conference 2025 (WWW '25), pp. 541-559. https://doi.org/10.1145/3696410.3714698
- Frontmatter `citations` in the folded entry: 14 (Crossref, 2026-10-03)

### Summary

Builds similarity networks over 2024 US election conversations on X, Facebook and Telegram to find coordinated communities within and across platforms. Finds evidence of potential foreign interference, with Russian-affiliated media systematically promoted across Telegram and X, and substantial cross-platform coordinated activity spreading partisan, low-credibility and conspiratorial content.

### Contribution

Shows coordination detection across platform boundaries, where a swarm's footprint is split.

### Key results

- Coordinated communities found within and across X, Facebook and Telegram (abstract).
- Russian-affiliated media systematically promoted across Telegram and X.

### Methods and models

Cross-platform similarity networks with a coordination model. Abstract-level read.

### Limitations and open questions

Attribution is inferred from content promoted, not confirmed operators.

### Relevance to us

A swarm operated across platforms needs cross-platform joins. Same group: [[minici-2024-uncovering]], [[luceri-2024-unmasking]].
