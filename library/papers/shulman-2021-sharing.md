---
id: shulman-2021-sharing
type: paper
title: Sharing the World with Digital Minds
authors: [Carl Shulman, Nick Bostrom]
year: 2021
venue: Rethinking Moral Status (Clarke, Zohny & Savulescu, eds.), Oxford University Press
url: https://nickbostrom.com/papers/digital-minds.pdf
doi: 10.1093/oso/9780192894076.003.0018
arxiv: null
cite: Shulman, C., & Bostrom, N. (2021). Sharing the World with Digital Minds. In S. Clarke, H. Zohny & J. Savulescu (Eds.), Rethinking Moral Status (pp. 306–326). Oxford University Press.
topics: [fork-merge-security, sybil-resistance, meta]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: null
code: []
---

## Summary

A philosophy chapter (read from the author-hosted draft, version 1.8, 2020) on digital minds whose claims to resources could exceed those of humans, either collectively because they are cheap to mass-produce or individually as "super-beneficiaries". It catalogues the relevant differences from humans: reproduction by copying, low cost of living, subjective speed-up, hedonic range, and the possibility of replacing a deleted mind with "a copy of a fully-fledged mind of the newest edition". Footnote 5 notes it "may be unclear" whether an exact copy is a new person or "an additional instantiation of the person whose mind served as the template". On institutions, the authors argue that if humans could "spawn arbitrary numbers of exact duplicates of themselves", constitutions would be adjusted to stop contests being decided by "voting-clones", for instance by requiring the creator "to share their own voting power with the copies they create".

## Contribution

Early statement in the digital-minds ethics literature that copying breaks one-person-one-vote institutions and that copies should split, not multiply, their creator's weight.

## Key results

- No empirical results; normative argument.
- The copy-identity question (new person or additional instance) is flagged and left open.
- Proposed remedy for clone-voting: copies share their creator's vote rather than each getting one.

## Methods and models

Conceptual analysis with simple illustrative numbers (for example, ten digital minds sustained for a year on one human-month of energy).

## Limitations and open questions

Concerned with moral status and resource claims, not with adversarial corruption. It does not discuss copies re-merging.

## Relevance to us

Bears on Q2 and the Sybil side of fork-merge. A k-of-n merge threshold only means something if the n children cannot be cheaply multiplied by the attacker; the authors' "share their own voting power with the copies" rule is the weight-splitting answer used in Sybil-resistant voting, applied to copies of one mind. In a fork-merge system it suggests that a child that forks further should split its merge weight among its descendants, so a corrupted child cannot inflate its vote by spawning. The copy-identity question in footnote 5 is the philosophical form of Q3's "the copy becomes the attacker's agent": when does a diverged copy stop being an instance of the parent? Companion to [[bostrom-2023-propositions]]; context for [[sutton-2025-father]].
