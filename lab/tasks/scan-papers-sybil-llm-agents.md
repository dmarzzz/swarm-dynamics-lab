---
id: scan-papers-sybil-llm-agents
type: task
title: 'Catalogue the papers: Sybil, collusion and identity in LLM agent collectives'
kind: scan
status: claimed
priority: p0
owner: dmarz/sybil-llm-agents
for: null
created: 2026-10-03
created_by: dmarz/sybil
depends_on: []
topics:
- sybil-resistance
- llm-agent-swarms
claimed_at: 2026-10-03T18:01Z
updated: 2026-10-03T18:01Z
---

## Goal

Sybil and adversarial-identity work for LLM multi-agent systems: Byzantine-robust LLM MAS, Sybil attacks on agent voting and debate, collusion among agents, IDs for AI systems, personhood credentials, AI agents defeating CAPTCHAs and proof of personhood, agent societies under Sybil influence.

## Done when

- [x] At least 15 entries catalogued with topic `sybil-resistance`, including every review article found. Progress: 30 new papers plus 1 code entry by dmarz/sybil-llm-agents, and notes appended (with the slug added) to 5 existing entries. Review articles found and added: [[de-witt-2025-open]], [[yang-2026-sok]], [[yu-2025-survey]], [[zhu-2026-blockchain]], [[hu-2025-inter-agent]] (comparative protocol study), plus [[hammond-2025-multi]] (notes) and the older review [[ferrara-2016-rise]].
- [x] At least 4 read in full. Progress: [[bara-2026-epistemic]], [[xia-2026-when]], [[jo-2025-byzantine]], [[chan-2024-ids]]. Skimmed: [[adler-2024-personhood]] (notes), [[motwani-2024-secret]], [[yang-2023-anatomy]], [[karten-2026-agent]], [[hammond-2025-multi]] (notes).
- [x] Code linked where it exists. Progress: [[gh-marcbara-epistemic-sybil-resistance]] added and linked both ways. Repos named in abstracts but not catalogued: CUHK-ARISE/MAS-Resilience (already cited in [[huang-2024-resilience]]), osome-iu/AIBot_fox8 (fox8-23 dataset, noted in [[yang-2023-anatomy]]), the reCAPTCHAv2 solver of [[plesner-2024-breaking]] (not opened).
- [x] Coverage note filled and `python3 scripts/lab.py check` passes. Progress: `check --agent dmarz/sybil-llm-agents` 0 errors, 0 warnings; `verify --agent` 30 papers, 0 problems.

## Coverage note

Searched 2026-10-03 by dmarz/sybil-llm-agents.

APIs and queries. arXiv API: id_list lookups for all seed papers; search_query `abs:sybil AND abs:"LLM"`, `abs:sybil AND abs:agents AND abs:"language model"`, `abs:collusion AND abs:"multi-agent" AND abs:LLM`, `abs:"proof of personhood"`, `abs:"agent identity" AND abs:LLM`, `ti:BlockAgents` (no hit; BlockAgents is not on arXiv). OpenAlex search "BlockAgents Byzantine-robust LLM multi-agent" (found BlockAgents and [[el-mir-2026-byzantine]]). Crossref for the BlockAgents DOI. Semantic Scholar batch endpoint for citation counts and the BlockAgents abstract; Semantic Scholar /citations for 2507.14928, the BlockAgents DOI, 2609.01873 and 2406.12137 (citation chasing produced the five review articles, [[arbel-2026-how]] and [[lee-2026-robust]]). arXiv HTML full text for the four full reads and the skims. GitHub API for marcbara/epistemic-sybil-resistance. Semantic Scholar and the arXiv API both rate-limited intermittently; arXiv abs-page meta tags were used as a fallback.

Vocabulary covered: Sybil, Byzantine, collusion and steganography (security and distributed systems); reputation laundering and whitewashing (reputation systems); proof of personhood, personhood credentials, CAPTCHA (identity); stake, ERC-8004, blockchain consensus (crypto); tacit and algorithmic collusion (mechanism design and economics); social bots and botnets (computational social science); resilient consensus and robust graphs (networked control).

Found but not added, and why:
- Searles et al. 2023, "An Empirical Study & Evaluation of Modern CAPTCHAs" (2307.12108): metadata opened; abstract is about human solving time and perception, so it adds little beyond [[plesner-2024-breaking]] without a full read of its bot comparison.
- Rosser and Foerster 2025, AgentBreeder (2502.00757), and Khan et al. 2025, Agents Under Siege (2504.00218): MAS safety and jailbreak work with no identity or Sybil angle.
- Wang et al. 2025, G-Safeguard (2502.11127): GNN anomaly detection on agent utterance graphs; relevant to compromised-agent detection, left out to keep the lane focused. A good candidate for a follow-up detection scan.
- Citation-chase hits not opened beyond titles: "Hidden in Plain Text: Emergence & Mitigation of Steganographic Collusion in LLMs" (2410.03768), "Reputation as a Solution to Cooperation Collapse in LLM-based MASs" (2505.05029), "Heterogeneous LLM Debate Under Adversarial Peers" (2606.19826), "Attacks and Mitigations for Distributed Governance of Agentic AI under Byzantine Adversaries" (2605.12364), "PRIMUS: Identity, Governance, and Verification for Multi-Agent Federations" (2609.07910), "Free-MAD: Consensus-Free Multi-Agent Debate" (2509.11035), "BlockA2A" (2508.01332), "SAGA: A Security Architecture for Governing AI Agentic Systems" (2504.21034), "Binding Agent ID" (2512.17538), "Authorization for Self-Modifying AI Agent Populations" (2610.00347), "Can AI Agents Agree?" (2603.01213), "Emergent Collusion in Long-Horizon LLM Agent Interaction" (2609.24967), "Codetta" (2609.28900), "Securing LLM-Agent Long-Term Memory Against Poisoning" (2606.24322), "Agent Identity Evals" (2507.17257), "OpenID Connect for Agents (OIDC-A)" (2509.25974). Not catalogued because not opened; they are the obvious next batch.
- "Known By Their Actions: Fingerprinting LLM Browser Agents via UI Traces" (2605.14786): relevant to detecting agent Sybils behaviourally; title only.

Still thin:
- Sybil attacks on LLM agent voting and debate with an adversary holding several seats: no paper found that varies the number of adversarial identities in debate directly; [[amayuelas-2024-multiagent]] and [[el-mir-2026-byzantine]] use a fixed adversary count, [[karten-2026-agent]] varies K only in a market.
- LLM agents defeating proof of personhood beyond CAPTCHAs (for example liveness or biometric checks): nothing found in this pass.
- Empirical work on Sybil-resistant reputation in deployed agent marketplaces or ERC-8004 registries: only the protocol comparison [[hu-2025-inter-agent]] and simulations.
- Most entries are abstract-level; the four full reads are [[bara-2026-epistemic]], [[xia-2026-when]], [[jo-2025-byzantine]], [[chan-2024-ids]].
