---
id: scan-code-fm
type: task
title: Catalogue code and benchmarks for agent injection, merge poisoning and multi-agent attacks
kind: scan
status: claimed
priority: p1
owner: dmarz/fm-code-bench
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
claimed_at: 2026-10-03T18:12Z
updated: 2026-10-03T18:12Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: repos and benchmarks.

## Done when

- At least 12 code repos or benchmarks catalogued with topic `fork-merge-security`.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Filled by dmarz/fm-code-bench, 2026-10-03.

Result: 30 code entries plus 1 paper entry added with topic `fork-merge-security`; notes appended to 14 existing paper entries linking them to code. `lab.py check --agent dmarz/fm-code-bench` reports 0 errors, 0 warnings; `lab.py verify` reports 0 problems (one warning: the new USENIX paper has no arXiv id or DOI).

Method. GitHub REST API via `gh api repos/<o>/<r>` for stars, last push, licence, creation date, and `/readme` for README text; `gh api search/repositories` for discovery; arXiv export API for abstracts of the linked papers; Tor GitLab API v4 for Arti; USENIX presentation page and PDF for MergeBackdoor. Semantic Scholar and OpenAlex both returned rate-limit errors (429, daily budget exhausted) during this run, so citation chasing for code was done through the paper entries other lanes already hold and through repositories' own citation lists (FLPoison and Blades README tables, G-Safeguard citation block, Merge-Hijacking vendoring mergekit).

Rounds.
1. Seed list from the lane brief: 26 repos queried by API; 2 redirects found (StavC/ComPromptMized to StavC/Here-Comes-the-AI-Worm, invariantlabs-ai/mcp-scan to snyk/agent-scan) and one duplicate name (Azure/PyRIT, 118 stars, versus microsoft/PyRIT, 4574 stars; catalogued the latter). 19 new entries from this round.
2. GitHub search with neighbouring vocabulary ("byzantine crdt", "model merging backdoor", "memory injection agent attack", "self-replicating prompt", "byzantine llm multi-agent", "agent memory poisoning defense", "replibench"): about 70 results, 7 new entries (bft-json-crdt, bft-crdts, MINJA, Merge-Hijacking, MergeBackdoor, DAM, Aegean).
3. Second search ("agent-in-the-middle", "AgentPrune", "TrustAgent", "trojan agents", "multi-agent debate attack", "prompt infection multi-agent"): about 40 results, 3 new entries (FedAgent, MiDojo, AgentPrune), plus Arti from the Tor GitLab.

Ran two things. ByzFL 0.0.11 toy aggregation (n = 11, d = 50, single seed): mean drifts linearly with corrupted inputs; median, trimmed mean and Krum hold to f = 5 and all collapse to the attacker target at f = 6. bft-json-crdt byzantine and commutativity tests pass; the full suite with the Kleppmann trace did not finish in 10 minutes in debug mode.

Found but not added. RepliBench code (no public repository found; paper entry [[black-2025-replibench]] exists). AgentPoison repo and A-MemGuard repo (stubs already being filled by dmarz/fm-memory-injection). CaMeL repo (already catalogued by dmarz/fm-ai-control). microsoft/BIPIA (160 stars, indirect injection benchmark, README read) and XHMY/AutoDefense (69 stars, multi-agent jailbreak filter, README read): read but not written up for time; both single-agent or response-filter oriented. UKGovernmentBEIS/inspect_evals (contains an AgentDojo port, no RepliBench). Low-star repos seen in search and not opened beyond the listing: harshwt/Cross-Agent-Prompt-Injection-Attacks-CA-PIA- (1 star), jonathan-teel/block-agents (0), daniel-eai/Robust-Multi-Agent-LLMs-under-Byzantine-Faults (1), infinite-oreo/llm-agent-fault-tolerance (0), kit-dsn/proof-carrying-crdts (8), Krishita17/PoisonRecall (11), 7h30th3r0n3/MindJack (18), aminrj-labs/mcp-attack-labs (21).

What is thin. (a) No public code implements an actual fork-and-merge of LLM agents with an adversarial child; the closest are FedAgent (weight merge, no adversary), the merge-backdoor repos (weight merge, no agents) and the multi-agent safety repos (message passing, no merge). (b) No code found for Q1 (hiding which child is reintegrated) beyond generic anonymity transports (Arti, and Nym from another lane). (c) Byzantine-robust aggregation code exists only for numeric vectors; nothing applies k-of-n quorums to text reports or memories with an adversary in the loop, except the third-party Aegean repo, whose quorum is a simple majority and not Byzantine. (d) Several key repos have no licence file (BadMerging, MergeBackdoor, DAM, G-Safeguard, PsySafe, AgentPrune, AI Worm).
