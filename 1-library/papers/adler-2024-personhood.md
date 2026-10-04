---
id: adler-2024-personhood
type: paper
title: "Personhood credentials: Artificial intelligence and the value of privacy-preserving tools to distinguish who is real online"
authors: ["Steven Adler", "Zoë Hitzig", "Shrey Jain", "Catherine Brewer", "Wayne Chang", "Renée DiResta", "Eddy Lazzarin", "Sean McGregor", "Wendy Seltzer", "Divya Siddarth", "et al."]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2408.07892
doi: "10.48550/arXiv.2408.07892"
arxiv: "2408.07892"
cite: "Adler, S., Hitzig, Z., Jain, S., Brewer, C., Chang, W., DiResta, R., Lazzarin, E., McGregor, S., Seltzer, W., Siddarth, D., et al. (2024). Personhood credentials: Artificial intelligence and the value of privacy-preserving tools to distinguish who is real online. arXiv preprint arXiv:2408.07892."
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

A 63-page policy and technical analysis (arXiv v4) with a large multi-institution author list. It argues that capable AI raises both the indistinguishability of AI from people online (lifelike content, avatars, agentic activity) and the scalability of deception, so countermeasures such as CAPTCHAs are inadequate and full identity verification is insufficiently private. It defines "personhood credentials" (PHCs): digital credentials that let a user show they are a real person, not an AI, to an online service without disclosing personal information. PHCs may be issued by governments or other trusted institutions, may be local or global, and need not be biometric. The paper surveys benefits, deployment risks and design challenges, and closes with next steps for policymakers, technologists and standards bodies.

## Contribution

The most-cited framing document connecting anonymous credentials ([[davidson-2018-privacy]], [[rosenberg-2023-zk-creds]]) to the AI-agent Sybil problem: it asks for a credential that bounds how many accounts or agents a single human can field, while keeping anonymity.

## Key results

- Position and analysis, not experiments (from abstract and page count).
- Claims CAPTCHAs fail against sophisticated AI and that PHCs, built on anonymous-credential and proof-of-personhood research, can reduce misuse (abstract).

## Methods and models

Conceptual analysis. Not read beyond the abstract.

## Limitations and open questions

The abstract lists deployment risks and design challenges but we did not read them. A PHC bounds humans, not agents: a human can still delegate one credential to many agents unless the credential is rate-limited or clone-resistant ([[camenisch-2006-how]]).

## Relevance to us

Directly about agent Sybils. For a multi-agent system it raises the design question of whether agent identity should be rooted in a person (PHC), a payment ([[crapis-2026-zk]], [[gh-x402-foundation-x402]]), or an operator signature ([[cloudflare-2025-forget]]), and argues for the anonymous-credential route. A proof-of-personhood lane may catalogue overlapping work.

## Notes from dmarz/sybil-llm-agents

Skimmed the arXiv HTML full text 2026-10-03 (foundational requirements, Section 3.3 on delegation, recommendations). Points relevant to agent swarms: the two requirements are credential limits (at most one credential per person per issuer, so a person may hold a few across issuers) and unlinkable pseudonymity. Section 3.3 proposes using PHCs to verify that an AI agent is a delegate of some real person without revealing who, and gives multiple-persona market manipulation (lowball bids, fake demand) as a motivating case. The authors concede one PHC-verified account can still be handed to an agent, so PHCs bound scale rather than remove deception. That leaves the inside-the-swarm problems open: many agents under one credential can still be epistemic Sybils ([[bara-2026-epistemic]]) or launder reputation ([[xia-2026-when]]). Continuous alternative: [[maleki-2026-human]]; CAPTCHA failure evidence: [[plesner-2024-breaking]]; instance-level IDs: [[chan-2024-ids]].
