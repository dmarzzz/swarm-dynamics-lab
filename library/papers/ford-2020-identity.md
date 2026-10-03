---
id: ford-2020-identity
type: paper
title: "Identity and Personhood in Digital Democracy: Evaluating Inclusion, Equality, Security, and Privacy in Pseudonym Parties and Other Proofs of Personhood"
authors: ["Bryan Ford"]
year: 2020
venue: "arXiv preprint (cs.CY)"
url: https://arxiv.org/pdf/2011.02412
doi: null
arxiv: "2011.02412"
cite: "Ford, B. (2020). Identity and Personhood in Digital Democracy: Evaluating Inclusion, Equality, Security, and Privacy in Pseudonym Parties and Other Proofs of Personhood. arXiv preprint arXiv:2011.02412."
topics: [sybil-resistance, collective-decision]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "12 (OpenAlex, 2026-10-03); 22 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Ford separates identity (distinguishing people by attributes) from personhood (giving every real person one equal, inalienable participation right) and argues digital democracy needs the second first. He states four goals (inclusive, equal, secure, private), develops pseudonym parties for small, medium, large and federated events with cross-witnessing between organiser groups, and evaluates alternatives: government ID, biometrics, self-sovereign identity, proof of investment (PoW/PoS), social trust networks and threshold verification schemes such as HumanityDAO, BrightID, Duniter, Encointer and Idena.

## Contribution

The most complete argument for physical, synchronous, periodic personhood checks, together with a systematic critique of the alternatives in terms of which goal each one fails.

## Key results

- Conclusion: government, biometric and self-sovereign identity can be Sybil-resilient only by being highly privacy-invasive; proof of investment (work, stake) offers privacy but not equality; social-network and threshold-verification schemes "can potentially slow but cannot halt the creeping takeover of Sybil attackers".
- Two structural weaknesses of threshold verification (Section 4.7): profiles and verifications are fakeable by automated synthetic identities, and asynchronous verifications at a time of the participant's choosing are cumulable, so an attacker can get one profile verified, then another, and so on.
- Social trust "solves the wrong problem": PGP-style webs of trust bind names to keys but do not establish that a key holder has only one pseudonym (Section 4.6).
- Synchronised schemes (pseudonym parties, Encointer's randomly assigned meetups, Idena's simultaneous online ceremonies) resist time-shifting because one person cannot be in two places at once.
- Use cases for PoP tokens: CAPTCHA replacement, verified likes and follower counts, online voting and deliberation, sortition juries.

## Methods and models

Position and design paper; qualitative security analysis; no experiments. I read the goals, the pseudonym-party design overview, Sections 4.6 and 4.7, and the conclusion.

## Limitations and open questions

Physical events are costly and exclude people who cannot attend, which Ford discusses under inclusion and pandemic conditions. No quantitative model of attacker cost or of collusion among organisers.

## Relevance to us

The "cumulable asynchronous verification" argument is Douceur's Lemma 4 [[douceur-2002-sybil]] restated for humans and applies unchanged to agent onboarding: if each agent proves itself at a time of its choosing, a single operator can pass the check repeatedly. Synchronous, simultaneous challenges across the whole swarm are the generic fix, at a coordination cost. The critique of social trust also bears on agent reputation graphs: endorsements between agents establish key continuity, not uniqueness of the controlling principal. Related: [[borge-2017-proof-of-personhood]], [[siddarth-2020-who]], [[mukherjee-2023-sok]].
