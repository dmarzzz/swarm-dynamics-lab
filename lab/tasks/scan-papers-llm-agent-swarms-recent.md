---
id: scan-papers-llm-agent-swarms-recent
type: task
title: Catalogue LLM agent swarms papers from 2024 onward
kind: scan
status: done
priority: p0
owner: dmarz/llm-agent-swarms-recent
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- llm-agent-swarms
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T18:19Z
outputs:
- 1-library/papers
---

## Goal

The field moves fast and the seminal scan will skew old. Catalogue 2024 to 2026 work on LLM agent swarms, especially scaling the number of agents, coordination protocols, failure taxonomies, and agent-society simulations. Include strong preprints and workshop papers.

## Search plan

- arXiv listing searches sorted by date, OpenReview (ICLR, NeurIPS, ICML, CoRL), and forward citations of the seminal papers in the sibling scan task.
- Check the accepted-paper lists of the most recent relevant conferences and workshops.

## Done when

- At least 20 papers catalogued in library/papers/ with this topic, including every review article you found.
- At least 4 of them read in full (read_depth: full), chosen as the most relevant.
- Every paper that ships code has its repo catalogued in library/code/ and linked in `code:`.
- The coverage note below is filled and `python3 scripts/lab.py check` passes.

## Coverage note

Written by dmarz/llm-agent-swarms-recent on 2026-10-03. This scan ran in parallel with the seminal scan (dmarz/llm-agent-swarms), which catalogued much of the same 2024-2026 material in the same hour. Where that agent got to a paper first, I added no duplicate; where I had read the paper in full, I appended a `## Notes from dmarz/llm-agent-swarms-recent` section instead.

### Search rounds

"Relevant" means on-topic for LLM agent swarms (collective dynamics, scaling the number of agents, topology and coordination, failure modes, agent societies). "New" means not already in the library when the round ran.

| # | Where | Query or seed | Results screened | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex (title_and_abstract, year > 2023) | "multi-agent LLM" | 0 (daily budget used up, HTTP 429 all session) | 0 | 0 |
| 2 | arXiv listing, newest first | "multi-agent" LLM scaling agents | 60 | 6 | 6 |
| 3 | arXiv listing | "swarm intelligence" "large language model" | 22 | 9 | 9 |
| 4 | arXiv listing | LLM flocking OR "collective behavior" agents emergent | 40 | 3 | 3 |
| 5 | arXiv listing | "multi-agent" LLM "failure" taxonomy | 40 | 5 | 5 |
| 6 | arXiv listing | LLM agents "opinion dynamics" OR "social conventions" OR "consensus" population | 40 | 7 | 7 |
| 7 | arXiv listing | "scaling" "number of agents" LLM | 22 | 9 | 6 |
| 8 | arXiv listing | LLM agents "topology" communication graph multi-agent | 40 | 8 | 7 |
| 9 | arXiv listing | LLM agents society simulation "million agents" OR "thousands of agents" | 40 | 8 | 6 |
| 10 | Web search | emergent social conventions collective bias LLM populations Science Advances | 10 | 3 | 2 |
| 11 | Web search | "Towards a science of scaling agent systems" | 9 | 1 | 1 |
| 12 | Web search | LLM agents collective behavior Nature / PNAS / Nature Human Behaviour 2025 | 10 | 5 | 3 |
| 13 | Semantic Scholar, forward citations (by citation count) | De Marzo et al. arXiv:2409.02822 | 17 | 10 | 6 |
| 14 | Semantic Scholar, forward citations (by citation count) | Ashery et al. 10.1126/sciadv.adu9368 | 40 of 191 | 14 | 8 |
| 15 | Semantic Scholar, forward citations (by citation count) | Qian et al. MacNet arXiv:2406.07155 | 35 of 282 | 12 | 7 |
| 16 | Semantic Scholar, forward citations (most recent first) | Qian et al. MacNet arXiv:2406.07155 | 25 of 282 | 5 | 4 |
| 17 | Semantic Scholar, forward citations | Ruan et al. SwarmBench arXiv:2505.04364 | 4 | 2 | 1 |
| 18 | Semantic Scholar, backward references | Kim et al. arXiv:2512.08296 | 40 of 65 | 10 | 0 (all pre-2024 or already catalogued) |
| 19 | Semantic Scholar, forward citations (by citation count) | Kim et al. arXiv:2512.08296 | 30 of 139 | 8 | 5 |
| 20 | Semantic Scholar, forward citations | Flint et al. PNAS 10.1073/pnas.2531697123 | 19 | 8 | 4 |
| 21 | arXiv listing | "language model" agents "phase transition" collective | 3 | 2 | 1 |
| 22 | arXiv listing | "LLM" swarm "self-organization" OR "self-organizing" agents | 25 | 6 | 4 |
| 23 | Web search | "LLM agents" collective dynamics consensus Physical Review / Nature Communications / Royal Society 2026 | 10 | 9 | 3 |
| 24 | Web search | LLM agents swarm robotics flocking consensus journal 2025 2026 | 10 | 5 | 2 |

Crossref, DataCite, Europe PMC, the arXiv abstract pages and single-work OpenAlex lookups were used for metadata, citation counts and full text, not for discovery.

Saturation: not reached. The last two rounds found 3/10 (30%) and 2/10 (20%) new relevant items, above the 15% gate. The 2026 literature on LLM populations seen as statistical-physics systems is growing weekly; arXiv listings for September 2026 alone added about 10 relevant preprints.

### Counts

- New library entries from this agent: 38 papers, all tagged `llm-agent-swarms`. Breakdown: 16 on collective dynamics and consensus (naming games, opinion dynamics, synchronisation regimes, spin-model framings), 7 on scaling the number of agents and its limits, 5 on topology and self-organisation, 6 on swarm intelligence and robotics with LLM agents, 4 on failure, contagion and adversarial influence, 3 surveys or reviews (Physics Reports, ACM Computing Surveys, agent protocols) plus 1 vision review (UAV swarms), and 2 methodological critiques ([[zhou-2025-pimmur]], [[barrie-2025-emergent]]). Some papers fall in more than one group.
- Venues: 6 journal articles (PNAS, npj Artificial Intelligence, Frontiers in AI, PNAS Nexus, ACM Computing Surveys, Physics Reports; the last two are surveys); 3 conference papers (ICLR 2025, ICLR 2026, NeurIPS 2024 workshop); the rest arXiv preprints, 2024-2026.
- Existing entries noted after an independent full read: [[de-marzo-2024-ai]], [[ashery-2024-emergent]], [[riedl-2025-emergent]], [[kim-2025-towards]], [[ruan-2025-benchmarking]]. All already carried `llm-agent-swarms`.
- Review articles found: [[mou-2026-individual]], [[jiang-2026-large]], [[yang-2025-survey]], [[emami-2026-llm-centric]] (mine), plus [[guo-2024-large]], [[tran-2025-multi]], [[gao-2023-large]], [[li-2025-large]], [[hammond-2025-multi]] and the position paper [[fan-2026-towards]] (catalogued by the sibling agent).
- `lab.py check --agent dmarz/llm-agent-swarms-recent`: 0 errors, 0 warnings. `lab.py verify --agent dmarz/llm-agent-swarms-recent`: 38 papers checked, 0 problems.

### Full reads (read_depth: full)

On entries I created: [[flint-2026-group]], [[qian-2025-scaling]], [[hirota-2026-collective]], [[de-nobili-2026-microscopic]], [[bertalanic-2026-ringelmann]], [[zomer-2026-unraveling]].
Also read in full, recorded as notes on the sibling agent's entries: [[de-marzo-2024-ai]], [[ashery-2024-emergent]] (journal version via Europe PMC), [[riedl-2025-emergent]], [[kim-2025-towards]] (main text and robustness sections), [[ruan-2025-benchmarking]] (including appendices).

### Notable gaps

- No OpenAlex search rounds: the shared daily OpenAlex budget was exhausted (HTTP 429 with "dailyRemainingUsd 0"). Citation counts use single-work OpenAlex lookups. These under-count arXiv-only papers badly, so Semantic Scholar counts are given alongside them.
- OpenReview and the accepted-paper lists for ICLR 2026, NeurIPS 2025 and ICML 2025 were not checked directly. Venue claims that only Semantic Scholar supports are marked "not verified" in the entries ([[zhang-2025-which]], [[huang-2024-resilience]]).
- Not saturated. Some September 2026 preprints were seen but not catalogued: "Width, Memory, and Delay" (arXiv:2608.00028), "Emergent Culture in Minimal LLM Systems" (2606.30668), "Absorbing State Phase Transitions in Multi-Agent Search" (catalogued by the sibling agent as [[zheng-2026-absorbing]]), "Copying explains the collective behavior of AI agents in the wild" (2609.09150), "Message capacity ..." (catalogued as [[fukushima-2026-message]]), "Generative AI collective behavior needs an interactionist paradigm" (2601.10567), "Gender Dynamics and Homophily in a Social Network of LLM Agents" (Phil. Trans. A, 10.1098/rsta.2025.0205), "Conformity and Social Impact on AI Agents" (2601.05384), "LLM-Foraging" (2605.01461).
- Most 2026 preprints are catalogued at abstract level only. Several make strong quantitative claims that a full read should check: [[ricco-2026-consensus]], [[fukushima-2026-message]], [[wu-2026-predicting]], [[zou-2026-waggle]], [[celiktemel-2026-group]].
- No library/code or library/datasets entries were created (left for the code scan). The released datasets Eraclitus-4.7M ([[ricco-2026-consensus]]), Who&When ([[zhang-2025-which]]) and the SwarmBench logs are not yet catalogued.
- Robot-swarm uses of LLMs (LLM-Flock, LLM-Foraging, the multi-robot survey) overlap with the swarm-robotics scans and are covered only partly here.
- No X, blog or talk sources (papers only, per the brief).

### Code repositories seen (for the code scan)

- https://github.com/giordano-demarzo/LLMs-Opinion-Dynamics ([[de-marzo-2024-ai]])
- https://github.com/Ariel-Flint-Ashery/AI-norms ([[ashery-2024-emergent]]; data at Zenodo 10.5281/zenodo.14937173)
- https://github.com/x66ccff/swarmbench ([[ruan-2025-benchmarking]])
- https://github.com/OpenBMB/ChatDev/tree/macnet ([[qian-2025-scaling]])
- https://github.com/ybkim95/agent-scaling ([[kim-2025-towards]]; seen in search results, not opened)
- https://github.com/riedlc/AI-GBS ([[riedl-2025-emergent]])
- https://github.com/crjimene/swarm_gpt ([[jimenez-romero-2025-multi-agent]])
- https://github.com/Pold87/LLM2Swarm ([[strobel-2024-llm2swarm]])
- https://github.com/CUHK-ARISE/MAS-Resilience ([[huang-2024-resilience]])
- https://github.com/mingyin1/Agents_Failure_Attribution ([[zhang-2025-which]])
- https://github.com/CoMuNeLab/LLM-Agents ([[zomer-2026-unraveling]]; announced as released on acceptance, not checked)
- https://github.com/FudanDISC/SocialAgent ([[mou-2026-individual]] paper list)
- https://github.com/tsinghua-fib-lab/LLM-Agent-Based-Modeling-and-Simulation ([[gao-2023-large]] paper list)
- https://github.com/MoreAgentsIsAllYouNeed/AgentForest ([[li-2024-more]])
- https://github.com/metauto-ai/gptswarm ([[zhuge-2024-language]])
- https://github.com/Zhiyuan-Weng/BenchForm ([[weng-2025-do]])
- https://github.com/SafeRL-Lab/Agent-Scaling ([[yang-2026-understanding]])

### Suggested follow-up tasks

I did not create these, because this run was limited to library entries and this task file.
1. `scan-code-llm-agent-swarms`: catalogue the repositories above, starting with swarmbench, LLMs-Opinion-Dynamics, AI-norms and AI-GBS. Run SwarmBench and the De Marzo opinion-dynamics code with a small local model.
2. `scan-datasets-llm-agent-swarms`: catalogue Eraclitus-4.7M, Who&When, the SwarmBench logs and the AI-norms Zenodo data.
3. `fullread-llm-swarm-physics-2026`: read in full [[ricco-2026-consensus]], [[fukushima-2026-message]], [[tanaka-2026-when]], [[wu-2026-predicting]] and [[celiktemel-2026-group]], and catalogue the uncatalogued preprints listed under gaps.
4. `scan-openreview-llm-mas`: go through the OpenReview listings for ICLR 2026, NeurIPS 2025 and ICML 2025 (and the ICLR 2027 submissions once public) with the queries above.
5. The survey `survey-llm-agent-swarms` can begin. The strongest seeds for its seminal and forward-citation chains are [[de-marzo-2024-ai]], [[ashery-2024-emergent]] and [[qian-2025-scaling]]. The most direct hackathon candidates, all cheap and with a quantitative prediction to test, are the Hirota ring and rewiring protocol ([[hirota-2026-collective]]), the temperature-controlled naming game ([[de-nobili-2026-microscopic]]) and the Ringelmann N_eff pilot ([[bertalanic-2026-ringelmann]]).

### Audit (dmarz/llm-agent-swarms-recent-audit)

Audited on 2026-10-03. `lab.py verify` gave 0 BAD lines on the 38 entries, and there were no phantoms. Spot-checked 17 entries against their sources. These included all six `read_depth: full` entries ([[flint-2026-group]], [[qian-2025-scaling]], [[hirota-2026-collective]], [[de-nobili-2026-microscopic]], [[bertalanic-2026-ringelmann]], [[zomer-2026-unraveling]]), checked against the arXiv HTML or the publisher's full text. Every number checked matched, so all six keep `full`. The other entries checked were [[jiang-2026-large]], [[jimenez-romero-2025-multi-agent]], [[mou-2026-individual]], [[papachristou-2025-network]], [[tastan-2026-stochastic]], [[strobel-2024-llm2swarm]], [[ys-2026-everyone]], [[ricco-2026-consensus]] and [[wu-2026-how]] (Crossref or arXiv records), plus [[huang-2024-resilience]] and [[zhang-2025-which]].
Fixed: [[huang-2024-resilience]] and [[zhang-2025-which]] now have their confirmed ICML 2025 venue and PMLR 267 pages (they had been marked "not verified"). The [[mou-2026-individual]] cite is cut to ten authors plus et al. A note on [[kim-2025-towards]] records its journal version, Nature Machine Intelligence 8(7):1157-1172 (10.1038/s42256-026-01268-y, retitled "Capable language models can outgrow the benefits of collaboration"), which reports revised numbers.
Searches added by the audit: (A1) Semantic Scholar forward citations of Ashery et al. (Sci. Adv.), newest first, 70 of 191 screened; (A2) Semantic Scholar forward citations of MacNet, newest first, 70 of 282 screened; (A3) web search using stigmergy and pheromone vocabulary; (A4) web search using sociophysics terms (echo chambers, polarization, opinion dynamics); (A5) web search using econophysics terms (minority game, El Farol, public goods); (A6) web search for 2025-2026 reviews of collective intelligence. OpenAlex was still returning HTTP 429.
Added 12 entries: [[de-marzo-2026-copying]], [[okawa-2026-emergence]], [[yang-2026-when]] and [[flint-2026-indirect]] (skim depth), and [[takata-2025-emergent]], [[pal-2026-swarmworld]], [[rodriguez-2026-emergent]], [[wang-2025-decoding]], [[kuznetsov-2026-width]], [[ezaki-2026-warned]], [[mori-2026-three]] and [[mieczkowski-2026-language]] (abstract depth).
Found but not added: "Multi-agent discussion gains less when dissent is withheld" (2609.38324), "AI Agents are Vulnerable to Radicalization" (2609.38296), "Local Predictability and Collective Fidelity in LLM-Agent Societies" (2609.35813), "Collective cooperation without individual fidelity in LLM agents" (2606.30454), "Emergence of Preferential Attachment and Glass-Ceiling Effects in Autonomous Networks of LLMs" (2607.01148), "AI agents reshape consensus formation in human groups" (2609.02122), "Most LLM Conformity Needs No Speaker" (2607.05545), "Do We Need Complex Topology Control? Distinct-Peer Random Routing..." (2609.27150), "Rethinking Multi-Agent Collaboration: When More Is Less" (2609.19759), "When Do Multi-Agent Systems Help? An Information Bottleneck Perspective" (2607.16133), "AgentFugue" (2605.24486), "Collective Cognition in Hybrid Groups: A Network Science Synthesis" (2607.05593, a book-chapter review), "Opinion Polarization in LLM-Based Social Networks" (2606.18795), "Large Language Model Driven Agents for Simulating Echo Chamber Formation" (2502.18138), "Superminds Test" (2604.22452).
Still thin: most 2026 entries are read at abstract depth only, including 8 of the 12 the audit added. Both reviews of collective intelligence ([[mieczkowski-2026-language]] and the hybrid-groups chapter) are recent and lightly read. OpenAlex citation counts are still missing for arXiv-only items. Stigmergic and environment-mediated LLM swarms, and resource-competition games (El Farol, minority game, congestion), have only just been covered and deserve their own round. The forward-citation lists of Ashery et al. and MacNet still show about 5 new relevant items per 70 screened, so the search is not saturated.
