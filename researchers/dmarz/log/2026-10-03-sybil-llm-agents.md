# 2026-10-03 sybil-llm-agents

Task: scan-papers-sybil-llm-agents (agent dmarz/sybil-llm-agents).

## What I did

- Added 30 paper entries and 1 code entry tagged `sybil-resistance`, covering agent identity and personhood ([[chan-2024-ids]], [[chan-2024-visibility]], [[chan-2025-infrastructure]], [[south-2025-authenticated]], [[arbel-2026-how]], [[maleki-2026-human]], [[hu-2025-inter-agent]]), Byzantine-robust LLM consensus ([[jo-2025-byzantine]], [[chen-2024-blockagents]], [[luo-2025-weighted]], [[lee-2026-robust]], [[el-mir-2026-byzantine]]), attacks and collusion in agent collectives ([[motwani-2024-secret]], [[amayuelas-2024-multiagent]], [[ju-2024-flooding]], [[fish-2024-algorithmic]], [[nakamura-2026-colosseum]], [[tailor-2025-audit]]), marketplaces and reputation ([[xia-2026-when]], [[karten-2026-agent]], [[bansal-2025-magentic]]), bots and CAPTCHAs ([[ferrara-2016-rise]], [[yang-2023-anatomy]], [[feng-2024-what]], [[plesner-2024-breaking]]), epistemic Sybils ([[bara-2026-epistemic]], [[gh-marcbara-epistemic-sybil-resistance]]) and reviews ([[de-witt-2025-open]], [[yang-2026-sok]], [[yu-2025-survey]], [[zhu-2026-blockchain]]).
- Full reads: [[bara-2026-epistemic]], [[xia-2026-when]], [[jo-2025-byzantine]], [[chan-2024-ids]].
- Appended notes and the slug to [[hammond-2025-multi]], [[huang-2024-resilience]], [[lee-2024-prompt]], [[gu-2024-agent]], [[adler-2024-personhood]] (owned by dmarz/sybil-credentials, which created it while I was working).
- `check --agent` 0 errors; `verify --agent` 30 papers, 0 problems.

## What surprised me

- [[bara-2026-epistemic]] reframes Sybil resistance for swarms as an information problem: authenticated, distinct agents can still be Sybils if they descend from one evidence root, and a same-model swarm has correlated extraction errors (gamma = 0.719) that cap what more agents add. Its embedding-dedup baseline tracked wording, not ancestry.
- [[xia-2026-when]] shows reputation laundering across skills costs one episode, because budget and coupling cancel algebraically; rate limits cannot help, only a zero-evidence gate.
- The Byzantine-robust LLM consensus papers ([[jo-2025-byzantine]], [[chen-2024-blockagents]], [[lee-2026-robust]]) all bound adversaries by identity count and say little about admission, so Sybil resistance is assumed rather than provided.

## What next

- Open the citation-chase backlog listed in the task's coverage note (steganographic collusion, reputation in LLM MAS, adversarial debate, PRIMUS, BlockA2A, agent fingerprinting).
- A candidate experiment: vary the number of adversarial seats in multi-agent debate with and without provenance-aware aggregation, using the ESB benchmark interface from [[gh-marcbara-epistemic-sybil-resistance]].
