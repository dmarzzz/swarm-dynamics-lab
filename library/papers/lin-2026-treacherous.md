---
id: lin-2026-treacherous
type: paper
title: "The Treacherous Envoy Problem: Trust, Collusion, and Accountability in Multi-Agent Workflows [Blue Sky Paper]"
authors: [Zhiqiang Lin, Shuo Chen, Huan Sun]
year: 2026
venue: Proceedings of the 31st ACM Symposium on Access Control Models and Technologies (SACMAT '26), Waterloo, ON, Canada
url: https://zhiqlin.github.io/file/SACMAT26.pdf
doi: 10.1145/3750555.3811883
arxiv: null
cite: "Lin, Z., Chen, S., & Sun, H. (2026). The Treacherous Envoy Problem: Trust, Collusion, and Accountability in Multi-Agent Workflows [Blue Sky Paper]. In Proceedings of the 31st ACM Symposium on Access Control Models and Technologies (SACMAT '26), pp. 256-264. ACM. https://doi.org/10.1145/3750555.3811883"
topics: [sybil-resistance, llm-agent-swarms, fork-merge-security]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

A position ("Blue Sky") paper that names and formalises the Treacherous Envoy Problem (TEP): a principal delegates a task in natural language (the running example is "book me a refundable hotel for $487") to an LLM agent that interacts with other agents representing other principals (sellers, aggregators, affiliates), some of which may collude. An envoy is "treacherous" when the realised tool-side effects violate the principal's intent while every artifact it releases is locally consistent with every check the principal's disclosure policy allows. The paper argues detection is structurally hard because it needs three capabilities that cannot be maximised together: expressive negotiation (extracting an enforceable Scope from free-form text), verifiable conformance (checking realised Effects against Scope) and bounded disclosure (verifying without leaking private context). Two coupling edges get formal treatment: Proposition 1 (verification-leakage) uses Fano's inequality to show that a verifier with error at most delta must leak at least H(C|Z) - H_b(delta) bits of the provider's private state, i.e. at least one full bit in the balanced error-free case; Proposition 2 (hedge asymmetry) shows any complete, maximally sound deterministic scope extractor must emit a strictly more permissive constraint for a hedged phrase ("refundable (policy applies)") than an unhedged one ("fully refundable"), so an adversary widens scope by hedging with no extractor failure. The authors catalogue five tensions (T1-T5), five exploitation patterns (A1 misbinding drift, A2 proof laundering via over-disclosure pressure, A3 scope laundering through tool composition, A4 friction-driven policy evasion, A5 within-scope value degradation), a four-rung adversary ladder from a single envoy (S1) to cross-principal collusion (S4), and a four-layer reference architecture (scope-binding "lawyer", conformance-checking "inspector", evidence-brokering "escrow", accountability "licensing board"). No experiments; the contribution is the framing and the two propositions.

## Contribution

Reframes multi-agent LLM workflow security as a decision problem about joint behaviour under collusion and natural-language delegation, distinct from the confused deputy (one trust domain) and Lampson confinement (single principal, trusted monitor), and gives information-theoretic reasons why "log more" and "redact more" each break one side of the trilemma.

## Key results

- Proposition 1: for binary conformance label C = f(S) and verifier accuracy >= 1 - delta, I(S; Released | Z) >= H(C | Z) - H_b(delta). Error-free verification in the balanced case leaks at least one bit of private state beyond the public view. Proof chains Fano, the mutual-information identity and the chain rule.
- Proposition 2: hedge asymmetry is one-sided; narrowing scope requires adding explicit structure, widening only requires hedged phrasing. Design implication: require signed structured term sheets as a commitment device before execution.
- Threat model explicitly includes a Sybil dimension (one principal spawning ostensibly independent same-role agents, S3), partial collusion, and mid-workflow compromise via prompt injection while retaining delegated authority (cites Douceur [[douceur-2002-sybil]]).
- Table 1 maps each attack pattern to observable signals (late fee emergence, itemization requests beyond policy, split charges across merchants, escalation spikes, systematic steering with Conform = 1).
- Section 6.2 argues trusted infrastructure (payment processors, platform auditors, legal frameworks) shifts the frontier but does not remove it: A1 persists because disputes are semantic, A5 persists because it violates no rule.

## Methods and models

Formal setting: principals P, agents A, tools T, artifacts R; negotiation record N; Scope extracted from N as typed attribute constraints (price <= 487, refund_policy in {full, partial_with_fee}, cancel_deadline >= check_in); Effects with public projection Effects_pub; Released artifacts; per-principal Policy and an agreed evidence Profile. A workflow is unsafe iff Conform(Effects, Scope) = 0 or Disclose(Released, Profile, Policy) = 0. Graded conformance via a violation vector v in R^d. Dolev-Yao style trust-minimised baseline (no shared log, no trusted arbiter). No code, no benchmark; the paper proposes extending ToolBench and API-Bank with ground-truth scope, injected drift and collusion scenarios.

## Limitations and open questions

Authors: the attack catalogue is non-exhaustive; only two of three trilemma edges are formalised (conformance vs negotiation is sketched); recursive delegation is deferred; Conform and Disclose implemented by LLM judges create a circularity (the possibly compromised component decides whether compromise occurred). Mine: the propositions are short and the information-theoretic bound is loose in practice (it bounds leakage, not detectability of collusion); nothing is measured, so the "structural hardness" claim rests on argument. The Sybil dimension is named but not analysed beyond one sentence.

## Relevance to us

Useful vocabulary and formal scaffold for the fork-merge and sybil-resistance threads: "same-role multiplicity with a Sybil dimension" is exactly one-operator-many-agents, and the collusion ladder S1-S4 is a ready-made severity scale for swarm scenarios. The observable-signals column of Table 1 is a candidate feature list for detecting collusive agent coalitions from traces. Pairs with [[motwani-2024-secret]] and [[burianova-2025-secret]] on secret collusion, [[hammond-2025-multi]] on multi-agent risks, [[chan-2025-infrastructure]] on agent infrastructure (cited by the paper as [6]), [[marro-2025-permission]] and [[dash-2026-untrusted]] on agent authorization and untrusted components. Classic Sybil root: [[douceur-2002-sybil]].
