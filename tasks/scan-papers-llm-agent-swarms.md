---
id: scan-papers-llm-agent-swarms
type: task
title: 'Catalogue the papers: llm agent swarms'
kind: scan
status: claimed
priority: p0
owner: dmarz/llm-agent-swarms
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- llm-agent-swarms
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T17:01Z
---

## Goal

Build the paper base for `llm-agent-swarms`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Park et al. 2023, Generative agents: interactive simulacra of human behavior (UIST)
- Du et al. 2023, Improving factuality and reasoning in language models through multiagent debate
- Li et al. 2023, CAMEL: communicative agents for mind exploration
- Wu et al. 2023, AutoGen; Hong et al. 2023, MetaGPT; Qian et al. 2023, ChatDev; Chen et al. 2023, AgentVerse
- Li et al. 2024, More agents is all you need
- Cemri et al. 2025, Why do multi-agent LLM systems fail?
- Large agent-society simulations: Project Sid (Altera, 2024), AgentSociety (2025)

## Search plan

- Start from the seeds. For each seminal paper, pull its references (backward) and the papers citing it (forward) from Semantic Scholar: https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>/citations?fields=title,year,externalIds,citationCount&limit=100
- Query arXiv (export.arxiv.org/api/query), Semantic Scholar search and OpenAlex (api.openalex.org/works?search=...) with at least 5 different phrasings of the topic, including the terms used by neighbouring fields.
- Look for review articles first: they give the map and their reference lists are dense seeds.
- Prioritise by relevance to the hackathon, then by citation count, then recency. Catalogue the review papers, the seminal papers, and the strongest recent work.

## Done when

- At least 25 papers catalogued in library/papers/ with this topic, including every review article you found.
- At least 5 of them read in full (read_depth: full), chosen as the most relevant.
- Every paper that ships code has its repo catalogued in library/code/ and linked in `code:`.
- The coverage note below is filled and `python3 scripts/lab.py check` passes.

## Coverage note

Scan by dmarz/llm-agent-swarms, 2026-10-03. A parallel agent (dmarz/llm-agent-swarms-recent) catalogued overlapping 2024-2026 work at the same time; duplicates were caught by `lab.py find` before every create.

**Tooling note.** The OpenAlex free daily budget for this machine's IP was exhausted at the start of the run (HTTP 429, "Insufficient budget", reset at midnight UTC), so OpenAlex could not be used for search, citation chasing or `cited_by_count`. Substitutes: arXiv listing search (arxiv.org/search), WebSearch, Crossref (`query.bibliographic` and `/works/<doi>`), DataCite for arXiv metadata, and the Semantic Scholar batch and `/citations` endpoints (single calls with backoff). The `citations:` field therefore holds Semantic Scholar counts dated 2026-10-03 rather than OpenAlex counts.

### Search rounds

"Results" counts the hits I screened. "Relevant" means LLM-agent-collective work. "New" counts relevant items not already seen in an earlier round or in the seed list.

| # | Where | Query / action | Results | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex | `search=large language model multi-agent survey`, `title.search` variants | 50 (before 429) | 2 | 1 |
| 2 | arXiv + DataCite | seed confirmation: 11 seed papers plus 4 known reviews checked by arXiv id | 15 | 15 | 15 (seeds) |
| 3 | arXiv listing | `multi-agent large language model survey` (date-sorted) | 50 | 4 | 2 |
| 4 | DataCite/arXiv | known-id confirmation round: 37 candidates from memory (debate, robotics, social simulation, conformity) | 37 | 37 | 37 |
| 5 | WebSearch | LLM agents swarm intelligence collective behavior emergent | 9 | 5 | 3 |
| 6 | WebSearch | LLM agents consensus / opinion dynamics / statistical mechanics | 9 | 8 | 6 |
| 7 | WebSearch | scaling number of LLM agents, science of scaling agent systems | 9 | 5 | 3 |
| 8 | WebSearch | LLM-driven robot swarm, decentralized flocking, drones | 9 | 7 | 2 |
| 9 | WebSearch | communication topology (G-Designer, AgentPrune, sparse debate) | 9 | 7 | 4 |
| 10 | WebSearch | infectious jailbreak / contagion among a million agents | 9 | 5 | 3 |
| 11 | WebSearch | herd behaviour, conformity, groupthink in multi-agent debate | 10 | 9 | 6 |
| 12 | WebSearch | social norms, cooperation, cultural evolution in LLM populations | 9 | 6 | 3 |
| 13 | Crossref | journal articles since 2023: "large language model agents collective behaviour", "LLM agents swarm intelligence", "generative agents emergent collective" | 75 | 4 | 3 |
| 14 | WebSearch | stigmergy, blackboard, shared memory, decentralized LLM coordination | 9 | 6 | 5 |
| 15 | WebSearch | information cascades, misinformation and error propagation in LLM MAS | 9 | 8 | 6 |
| 16 | WebSearch | LLMs and collective intelligence (Nature Human Behaviour) | 9 | 1 | 1 |
| 17 | Backward chase | full reference lists of [[riedl-2025-emergent]] and [[ashery-2024-emergent]] | ~150 | 15 | 6 |
| 18 | Forward chase (S2) | citations of [[de-marzo-2024-ai]] (17), [[ashery-2024-emergent]] (191, top 40 by count), [[ruan-2025-benchmarking]] (4) | 61 | 20 | 12 |
| 19 | Forward chase (S2) | citations of [[riedl-2025-emergent]] (25) and [[el-2026-physics]] (8), all 2025-2026, so this round also covers recency | 33 | 12 | 9 |
| 20 | WebSearch | LLM agents phase transition / Ising / Kuramoto synchronization | 10 | 6 | 3 |
| 21 | WebSearch | swarm robotics + LLMs (Dorigo, Strobel, LLM2Swarm) | 27 | 10 | 4 |
| 22 | WebSearch | naming game / voter model / Curie-Weiss with LLM populations | 9 | 7 | 1 |
| 23 | WebSearch | decentralized self-organising LLM swarms without an orchestrator | 9 | 6 | 2 |
| 24 | WebSearch | LLM agents + Vicsek / active matter / collective motion | 9 | 0 | 0 |
| 25 | WebSearch | LLM collective intelligence, group size, scaling, reviews 2025-2026 | 9 | 7 | 1 |

Saturation: round 24 found 0/9 new and round 25 found 1/9 (11%). The last two rounds are both under the 15% bar.

### Counts

- **54 new paper entries** created by this agent, all tagged `llm-agent-swarms`. `lab.py verify` reports 54/54 resolved, with 0 title problems.
- **6 matching entries already existed** (created by dmarz/llm-agent-swarms-recent) and already carried the topic: [[qian-2025-scaling]], [[flint-2026-group]], [[jimenez-romero-2025-multi-agent]], [[rahman-2025-llm-powered]], [[li-2024-challenges]], [[strobel-2024-llm2swarm]]. The library therefore holds 60+ `llm-agent-swarms` papers counting this agent's work and the overlap.
- **By kind (my 54):**
  - Reviews, surveys and perspectives (10): [[guo-2024-large]], [[xi-2023-rise]], [[wang-2023-survey]], [[tran-2025-multi]], [[gao-2023-large]], [[li-2025-large]], [[hammond-2025-multi]], [[burton-2024-how]], [[fan-2026-towards]], [[schroeder-2025-how]].
  - Seminal frameworks and protocols (13): [[park-2023-generative]], [[du-2023-improving]], [[li-2023-camel]], [[wu-2023-autogen]], [[hong-2023-metagpt]], [[qian-2023-chatdev]], [[chen-2023-agentverse]], [[liang-2023-encouraging]], [[zhuge-2023-mindstorms]], [[zhuge-2024-language]], [[wang-2024-mixture]], [[li-2024-more]], [[choi-2025-debate]].
  - Scaling and failure (6): [[kim-2025-towards]], [[yang-2026-understanding]], [[cemri-2025-why]], [[gu-2024-agent]], [[weng-2025-do]], [[cho-2025-herd]].
  - Statistical physics and collective dynamics of LLM populations (11): [[de-marzo-2024-ai]], [[ashery-2024-emergent]], [[riedl-2025-emergent]], [[el-2026-physics]], [[tanaka-2026-when]], [[de-nobili-2026-collective]], [[brockers-2025-disentangling]], [[zheng-2026-absorbing]], [[mehdizadeh-2026-exploring]], [[de-marzo-2023-emergence]], [[chuang-2023-simulating]].
  - Agent societies and simulations (7): [[al-2024-project]], [[piao-2025-agentsociety]], [[yang-2024-oasis]], [[piatti-2024-cooperate]], [[vallinder-2024-cultural]], [[de-marzo-2026-collective]], [[li-2025-swarmsys]].
  - Robotics and swarm-intelligence crossovers (7): [[ruan-2025-benchmarking]], [[li-2025-llm]], [[chen-2023-scalable]], [[mandi-2023-roco]], [[feng-2024-model]], [[zhang-2024-g-designer]], [[yang-2025-agentnet]].
- **By year (my 54, arXiv v1 year):** 2023: 16; 2024: 14; 2025: 16; 2026: 8. 24 of the 54 are from 2025-2026.

### Full reads (read_depth: full), 7

[[riedl-2025-emergent]], [[de-marzo-2024-ai]], [[ashery-2024-emergent]], [[ruan-2025-benchmarking]], [[kim-2025-towards]], [[cemri-2025-why]], [[el-2026-physics]].

Every other entry is honestly marked `abstract`. The biggest gain from more reading would be full reads of [[tanaka-2026-when]], [[de-nobili-2026-collective]], [[flint-2026-group]] and [[zheng-2026-absorbing]], which carry the physics-style scaling laws.

### Notable gaps

- **No LLM work at the scale of collective motion or active matter.** No paper puts LLM agents in a continuous-space Vicsek or Couzin setting and measures polarisation or phase transitions (round 24 came back empty). The closest are [[ruan-2025-benchmarking]] (grid flocking scored as shape matching), [[li-2024-challenges]], [[li-2025-llm]] and [[jimenez-romero-2025-multi-agent]]. This looks like a real gap and a hackathon opportunity.
- **Swarm sizes are small.** Task-solving MAS mostly use 2-16 agents. Large-N work exists only in social simulation ([[yang-2024-oasis]] at 10^6, [[piao-2025-agentsociety]] at 10^4, [[al-2024-project]] at 1000+), in [[qian-2025-scaling]] (1000+ agents on DAGs) and in [[de-marzo-2024-ai]] (N up to 1000).
- **Not catalogued because I could not open them:** the Science Robotics piece by Strobel, Dorigo and Fritz (2026), "How foundation models will revolutionize robot swarms" (doi 10.1126/scirobotics.adz1543; publisher page returned 403); and a TechRxiv review, "Emergent Intelligence in Multi-Agent and LLM" (2026).
- **Seen and screened but not catalogued** (candidates for the next pass): Ren et al. 2024, emergence of social norms (arXiv 2403.08251); Han et al. 2024, static networks cannot stabilise cooperation (2411.10294); Perez et al. 2024, LLM telephone game and cultural attractors (2407.04503); Lee and Tiwari 2024, prompt infection (2410.07283); Horiguchi et al. 2024, norms in natural language (2409.00993); Gupta et al. 2025, social learning and norms, AAMAS 2026 (2510.14401); Papachristou and Yuan, network formation among LLMs, PNAS Nexus 2025 (2402.10659); Bellina et al. 2026, conformity and social impact (2601.05384); De Nobili et al. 2026, microscopic naming-game dynamics (2608.02178); De Marzo et al. 2026, copying explains AI agents in the wild (2609.09150); Fukushima 2026, message capacity and truth-finding transitions (2609.19183); Maini et al., LLMs vs humans in group binary search, COLM 2026 (2604.02578); Zou et al. 2026, Waggle (2609.34136); Mitra 2025, Kuramoto model of multi-agent AI (2508.12314); hallucination cascades (2606.07937); misinformation in distributed fact recovery (2608.03421); CodeCRDT (2510.18893); emergent collective memory (2512.10166); LLM-Foraging (2605.01461); SwarmChat (2509.16920); Self-Organized Agents (2404.02183); Wisdom of the Silicon Crowd, Science Advances 2024 (2402.19379); CoELA (2307.02485); embodied LLM agents in organised teams (2403.12482); theory of mind for MAS, EMNLP 2023 (2310.10701); Multiagent finetuning (2501.05707); Rethinking the bounds of multi-agent discussion (2402.18272); "Should we be going MAD?" (2311.17371); ChatEval (2308.07201); collaboration mechanisms from a social-psychology view (2310.02124); and limits of agency in ABMs (2409.10568).
- **Venues not verified at the publisher.** Several published versions are named only from arXiv comments: ICML, NeurIPS, ICLR, EMNLP and TMLR. Semantic Scholar's venue claims (for example IJCAI for [[guo-2024-large]] and ICRA for [[mandi-2023-roco]]) are noted but not used in `cite`.

### Code repositories seen (for the code-scan task)

The hard rules for this run did not allow creating code entries, so these are listed here instead:

- https://github.com/riedlc/AI-GBS ([[riedl-2025-emergent]])
- https://github.com/giordano-demarzo/LLMs-Opinion-Dynamics ([[de-marzo-2024-ai]])
- https://github.com/Ariel-Flint-Ashery/AI-norms ([[ashery-2024-emergent]])
- https://github.com/x66ccff/swarmbench ([[ruan-2025-benchmarking]])
- https://github.com/ybkim95/agent-scaling ([[kim-2025-towards]])
- https://github.com/multi-agent-systems-failure-taxonomy/MAST, plus the dataset at https://huggingface.co/datasets/mcemri/MAST-Data ([[cemri-2025-why]])
- https://github.com/SafeRL-Lab/Agent-Scaling ([[yang-2026-understanding]])
- https://github.com/MoreAgentsIsAllYouNeed/AgentForest ([[li-2024-more]])
- https://github.com/OpenBMB/ChatDev ([[qian-2023-chatdev]], [[qian-2025-scaling]])
- https://github.com/OpenBMB/AgentVerse ([[chen-2023-agentverse]])
- https://github.com/geekan/MetaGPT ([[hong-2023-metagpt]])
- https://github.com/camel-ai/camel ([[li-2023-camel]])
- https://github.com/metauto-ai/gptswarm ([[zhuge-2024-language]])
- https://github.com/Skytliang/Multi-Agents-Debate ([[liang-2023-encouraging]])
- https://github.com/deeplearning-wisc/debate-or-vote ([[choi-2025-debate]])
- https://github.com/Zhiyuan-Weng/BenchForm ([[weng-2025-do]])
- https://github.com/crjimene/swarm_gpt ([[jimenez-romero-2025-multi-agent]])
- https://github.com/Pold87/LLM2Swarm ([[strobel-2024-llm2swarm]])
- https://github.com/openai/swarm (OpenAI Swarm framework, cited by [[de-marzo-2024-ai]] and [[rahman-2025-llm-powered]])
- Agent Smith project page: https://sail-sg.github.io/Agent-Smith/ ([[gu-2024-agent]])
- Paper lists: https://github.com/WooooDyy/LLM-Agent-Paper-List and https://github.com/Paitesanshi/LLM-Agent-Survey

### Done-when status

- **25+ papers including every review found:** met (54 new plus 6 pre-existing). The Science Robotics perspective and the TechRxiv review could not be opened.
- **5+ full reads:** met (7).
- **Code repos catalogued in library/code/ and linked in `code:`:** not done. This run's rules forbade creating code entries, so the repos are listed above for the code-scan task, and `code:` stays empty.
- **`lab.py check`:** 0 errors. The only 2 warnings come from another agent's notes.

### Suggested follow-up tasks

1. **Code scan for llm-agent-swarms.** Catalogue the repos above, prioritising swarmbench, LLMs-Opinion-Dynamics, AI-norms, AI-GBS and agent-scaling, then back-fill `code:` on these entries.
2. **Second paper pass on the screened-but-uncatalogued list** above. Focus on the 2026 statistical-physics cluster (De Nobili 2608.02178, Fukushima 2609.19183, Bellina 2601.05384, De Marzo 2609.09150) and on norms and cooperation (2403.08251, 2411.10294, 2510.14401).
3. **Full reads of the scaling-law papers** [[tanaka-2026-when]], [[de-nobili-2026-collective]] and [[zheng-2026-absorbing]], extracting exponents and critical parameters for the survey.
4. **Re-run citation counts through OpenAlex** after its daily budget resets, or with an API key, and replace the Semantic Scholar counts in `citations:`.
5. **Survey task "LLM swarms through a statistical-physics lens".** The library now has enough for the gate: order parameters, majority force, naming-game tipping points, Ising fits, synergy measures, scaling and coordination costs.
6. **Ask the human** to fetch the Science Robotics perspective (doi 10.1126/scirobotics.adz1543) through institutional access so it can be catalogued.

### Audit (dmarz/llm-agent-swarms-audit)

Audit on 2026-10-03. **Verified:** `lab.py verify` gave 54/54 clean. I pulled OpenAlex single-work records for all 54 entries and compared titles, first authors and author counts. There were no mismatches apart from version differences: [[de-marzo-2024-ai]] and [[schroeder-2025-how]] use the arXiv title with the journal DOI. OpenAlex's arXiv-DOI record for [[wu-2023-autogen]] is merged with an unrelated work. I spot-checked 11 entries against the paper text: all 7 full reads ([[riedl-2025-emergent]], [[de-marzo-2024-ai]], [[ashery-2024-emergent]], [[ruan-2025-benchmarking]], [[kim-2025-towards]], [[cemri-2025-why]], [[el-2026-physics]]) plus [[schroeder-2025-how]], [[zheng-2026-absorbing]], [[tanaka-2026-when]] and [[de-nobili-2026-collective]]. I also checked 10 venue claims against arXiv comments (TMLR, NeurIPS, ICLR, ICML, EMNLP). Every number and venue checked out, and no read_depth needed downgrading. **Fixed:** I rewrote `citations:` on all 54 entries to OpenAlex counts with W-ids and kept the Semantic Scholar count alongside. Single-work lookups worked even after the list endpoints hit the daily budget again. OpenAlex badly undercounts arXiv-only records, so read the Semantic Scholar numbers for preprints. I added audit notes to the 11 spot-checked entries. **Deleted:** none. **Added (11; a 12th, GenSwarm, collided with [[ji-2026-genswarm]] created minutes earlier by dmarz/swarm-robotics, so I deleted my copy and merged its content there as notes):** [[chen-2023-multi]] (full read), [[li-2025-systematic]], [[bellina-2026-conformity]], [[han-2026-conformity]], [[mi-2025-mf-llm]], [[schoenegger-2024-wisdom]], [[han-2024-static]] (skim), and [[williams-2023-epidemic]], [[ghaffarzadegan-2023-generative]], [[ren-2024-emergence]], [[perez-2024-cultural]] (abstract). **Audit search rounds:** (a) Semantic Scholar forward citations of [[park-2023-generative]]: all 5,817, filtered by collective-dynamics keywords to 390 and sorted by year. (b) The same for [[du-2023-improving]]: 2,371 filtered to 243. Together these gave about 150 distinct relevant titles, 12 of them new. (c) WebSearch on generative agent-based modelling and epidemics, from the ABM and system-dynamics vocabulary: 9 results, 4 new. (d) WebSearch for 2025-2026 reviews: 9 results, 2 new. (e-g) Crossref `query.bibliographic` for "wisdom of the crowd LLM", "LLM agents opinion dynamics network" and "language model robot swarm consensus": 75 results, 3 new. **Found but not added:** ReConcile (2309.13007); LLM Voting (2402.01766); Heterogeneous Swarms (2502.04510); SwarmAgentic (2506.15672); Wisdom of Partisan Crowds (2311.09665); Collective Innovation in Groups of LLMs (2407.05377); Hidden Strength of Disagreement (2502.16565); Error cascades, "From Spark to Fire" (2603.04474); Byzantine-robust decentralized coordination (2507.14928); Polarization under echo chambers (2402.12212); AgentScope very-large-scale simulation (2407.17789); MegaAgent (2408.09955); S-Agents (2402.04578); Spontaneous emergence of agent individuality (2411.03252); Group conformity in MAS (2506.01332); Social learning and norms (2510.14401); "LLM Social Simulations Are a Promising Research Method" (2504.02234); Generative AI collective behavior needs an interactionist paradigm (2601.10567); the validation critique of LLM ABMs in Artificial Intelligence Review (doi 10.1007/s10462-025-11412-6); S3 social-network simulation (2307.14984); and the telephone-game paper (2407.04503). **Still thin:** 47 of the 54 original entries remain abstract-only. There is still no LLM swarm with continuous-space collective-motion order parameters measured against N; [[ji-2026-genswarm]] is the closest route. Validation and critique papers (PIMMUR, the AI Review critique, the Moltbook-illusion paper 2602.07432) are under-represented relative to positive results. Code entries are still missing for every repo listed above.
