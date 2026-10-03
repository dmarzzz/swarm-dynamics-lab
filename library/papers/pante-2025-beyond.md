---
id: pante-2025-beyond
type: paper
title: "Beyond Interaction Patterns: Assessing Claims of Coordinated Inter-State Information Operations on Twitter/X"
authors: ["Valeria Pantè", "David Axelrod", "Alessandro Flammini", "Filippo Menczer", "Emilio Ferrara", "Luca Luceri"]
year: 2025
venue: "Companion Proceedings of the ACM Web Conference 2025 (WWW Companion)"
url: https://arxiv.org/html/2502.17344
doi: "10.1145/3701716.3715575"
arxiv: "2502.17344"
cite: "Pantè, V., Axelrod, D., Flammini, A., Menczer, F., Ferrara, E., & Luceri, L. (2025). Beyond Interaction Patterns: Assessing Claims of Coordinated Inter-State Information Operations on Twitter/X. In Companion Proceedings of the ACM on Web Conference 2025 (pp. 1234–1238). ACM."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "10 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

A negative result. An earlier study had reported coordination between state-run influence operations of different countries from aggregated state-to-state interaction networks. The authors re-test this on 26 X-attributed campaigns from 16 states, adding a control set of organic users who discussed the same topics in the same period. For each state pair they compare IO and control distributions of five similarity traces (co-retweet, co-URL, co-hashtag, fast retweet within 10 seconds, text similarity) and an interaction suspiciousness score, using one-sided Mann-Whitney tests with Bonferroni correction.

## Contribution

Shows that apparent group-level coordination can be an artefact of skipping a control baseline. Across 197 tests no inter-state edge was significant, so the earlier inter-state coordination claim did not replicate.

## Key results

- 197 state-pair by trace experiments; none significant after Bonferroni correction.
- Pairs that looked coordinated in aggregate networks (Egypt-UAE with Qatar, Iran with Cuba, Russia-China-Iran on similarity traces) gave p = 0.49 (Qatar to Egypt-UAE retweets) and 0.44 (Egypt-UAE to Qatar replies); the lowest p in the table was 0.39 (Armenia-Russia co-retweet).
- Data sizes: from 11 IO users (Bangladesh) to 5,902 (Iran); control sets from 929 to 80,108 users per state.

## Methods and models

TF-IDF user vectors per trace, cosine similarity networks ([[pacheco-2021-uncovering]], [[luceri-2024-unmasking]]); interaction suspiciousness = (share of a user's retweets or replies going to the other state) times (share of the other state's original posts the user engaged with). The IO and control distributions are compared per state pair. Data from [[seckin-2024-labeled]].

## Limitations and open questions

A 4-page companion paper. The control set is sampled by hashtag and may be broader or narrower than the IO conversation. Control data exists only for some campaigns. Absence of evidence at the state level does not rule out coordination through channels X did not log.

## Relevance to us

The methodological warning for any swarm-detection claim: test against matched organic controls, not against zero. Any claim that "these agents are one swarm" from co-activity alone should report the control distribution. Cross-check with [[panayiotou-2026-setting]] on window sensitivity and [[mannocci-2026-detection]] on missing null models.
