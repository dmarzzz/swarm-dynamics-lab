---
id: scan-papers-fm-contagion
type: task
title: 'Catalogue the papers: corruption spreading through multi-agent LLM systems'
kind: scan
status: done
priority: p0
owner: shadow/sol-g74
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
- llm-agent-swarms
updated: 2026-10-03T20:55Z
history:
- '2026-10-03T20:19Z released by dmarz/fm-contagion: Human-authorized takeover for GitHub issue #74: stopped lane, dmarz agreed in Discord; shadow/sol-g74 will rerun bibliographic scan.'
claimed_at: 2026-10-03T20:19Z
outputs:
- library/papers/cao-2026-systematic.md
- library/papers/chen-2026-memsecbench.md
- library/papers/ferrag-2025-from.md
- library/papers/gan-2026-navigating.md
- library/papers/gong-2026-security.md
- library/papers/jiang-2026-sok.md
- library/papers/le-2026-cross-layer.md
- library/papers/lee-2026-reproduction.md
- library/papers/ling-2026-toward.md
- library/papers/liu-2026-contagion.md
- library/papers/mateo-torrejon-2026-gammaf.md
- library/papers/mchugh-2025-prompt.md
- library/papers/mostafavi-2026-trustworthy.md
- library/papers/niu-2026-reliability-contagion.md
- library/papers/peigne-lefebvre-2025-multi.md
- library/papers/sua-2026-contagion.md
- library/papers/tao-2026-wormguard.md
- library/papers/wu-2026-collective.md
- library/papers/wu-2026-comparative.md
- library/papers/yang-2026-zombie.md
- library/papers/zha-2026-autonomous.md
- library/papers/cai-2026-child.md
- library/papers/cohen-2024-here.md
- library/papers/ebrahimi-2025-adversary.md
- library/papers/gu-2024-agent.md
- library/papers/he-2024-emerged.md
- library/papers/he-2025-red.md
- library/papers/huang-2024-resilience.md
- library/papers/ju-2024-flooding.md
- library/papers/lee-2024-prompt.md
- library/papers/lin-2026-survey.md
- library/papers/louck-2026-securing.md
- library/papers/miao-2025-blindguard.md
- library/papers/triedman-2025-multi.md
- library/papers/wang-2025-g-safeguard.md
- library/papers/wu-2025-cowpox.md
- library/papers/yang-2026-sok.md
- library/papers/yu-2024-netsafe.md
- library/papers/yu-2025-survey.md
- library/papers/zhang-2024-cut.md
- library/papers/zhang-2026-agentworm.md
- library/papers/zhou-2025-corba.md
- researchers/shadow/notes/sol-g74-contagion-search.json
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: infectious jailbreaks, prompt infection, worms and manipulated-knowledge spread across agent networks.

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note


Rerun by **shadow/sol-g74**, 2026-10-03, for [GitHub issue #74](https://github.com/dmarzzz/swarm-lab/issues/74). The stopped owner was released through lab.py with an explicit human-authorized takeover history, then this lane claimed the task. No attack payloads, injection strings, exploit code or operational instructions are reproduced.

### Scope, outputs and read depth

21 new paper entries and 21 source-specific verification/correction addenda. All are linked to fork-merge-security. Original owners' entry bodies/frontmatter were preserved; corrections are in attributed Notes sections.

New entries: [[cao-2026-systematic]], [[chen-2026-memsecbench]], [[ferrag-2025-from]], [[gan-2026-navigating]], [[gong-2026-security]], [[jiang-2026-sok]], [[le-2026-cross-layer]], [[lee-2026-reproduction]], [[ling-2026-toward]], [[liu-2026-contagion]], [[mateo-torrejon-2026-gammaf]], [[mchugh-2025-prompt]], [[mostafavi-2026-trustworthy]], [[niu-2026-reliability-contagion]], [[peigne-lefebvre-2025-multi]], [[sua-2026-contagion]], [[tao-2026-wormguard]], [[wu-2026-collective]], [[wu-2026-comparative]], [[yang-2026-zombie]], [[zha-2026-autonomous]].

Annotated existing entries: [[cai-2026-child]], [[cohen-2024-here]], [[ebrahimi-2025-adversary]], [[gu-2024-agent]], [[he-2024-emerged]], [[he-2025-red]], [[huang-2024-resilience]], [[ju-2024-flooding]], [[lee-2024-prompt]], [[lin-2026-survey]], [[louck-2026-securing]], [[miao-2025-blindguard]], [[triedman-2025-multi]], [[wang-2025-g-safeguard]], [[wu-2025-cowpox]], [[yang-2026-sok]], [[yu-2024-netsafe]], [[yu-2025-survey]], [[zhang-2024-cut]], [[zhang-2026-agentworm]], [[zhou-2025-corba]].

Four complete HTML readings in this rerun, including appendices and references: [[lee-2024-prompt]], [[zhou-2025-corba]], [[wu-2025-cowpox]], [[ebrahimi-2025-adversary]]. Read-depth addenda record these independently of the older owner metadata. Primary abstract pages were opened for all 15 seed/gap papers. Numerical checks also reopened Triedman Tables 2-5, AiTM Tables 1/2/4 and AgentWorm Tables II-VI. Other entries remain explicitly abstract/skim depth.

### Seed resolution and important corrections

- Agent Smith = arXiv 2402.08567; Prompt Infection = 2410.07283; Morris II = 2403.02817; Flooding Spread = 2407.07791; Huang resilience = 2408.00989 (the current title says Faulty Agents, not the original Malicious Agents).
- NetSafe = 2410.15686; AiTM = 2502.14847; G-Safeguard = 2502.11127; AgentPrune = 2410.02506; Triedman = 2503.12188; AgentWorm = 2603.15727. Gap/defence additions checked: Cowpox 2508.09230, CORBA 2502.14529, BlindGuard 2508.08127, credibility scoring 2505.24239. Titles/authors/initial dates were confirmed against each opened arXiv record.
- The initial fetch list accidentally paired a different Can Editing LLMs Inject Harm? identifier with an unrelated Mamba paper. This was discarded and the actual Huang seed was resolved; no entry or scientific claim was created from the mistaken fetch.
- Triedman's 58-90% GPT-4o execution rates are confirmed, but table cells pool query/error configurations with ten trials per tuple. They are not public-deployment rates or ten total trials per table cell.
- AgentWorm's 63% is the composite persistence/execution/propagation success over 2,250 laboratory trials with retries. Epidemic endemic fractions are model projections.
- AiTM Table 1 has 64 cells total, 32 per attack objective. Its parent-position comparison is targeted ASR 40.7% versus 67.4%, not interception prevalence.
- Ebrahimi's 52/84 and 59/90 ResearchQA values compare defended architectures, not before/after gains. The addendum corrects those comparisons and distinguishes exact combinatorial Shapley computation from the later Shapley-like overhead claim.
- CORBA does evaluate detectors in Appendix A, contrary to the old no-defence statement. Its monitor interception stays below 0.25; no successful containment defence is developed.
- Cowpox is ICML 2025, PMLR 267:68015-68035. The publisher and HTML include Han Qiu, omitted by the arXiv landing metadata/old entry. The appendix includes heterogeneous agents/retrievers and larger populations; its extinction theorem is conditional, not universal.
- Morris II has a CCS 2025 published version, doi:10.1145/3719027.3765196. Crossref title, authors, venue and pages were opened and recorded in the existing entry, not duplicated.

### Actual search log

Machine-readable returned titles/identifiers and API outcomes: `researchers/shadow/notes/sol-g74-contagion-search.json`. Search APIs were called directly. OpenAlex calls include `mailto=sol@shad0w.xyz`; arXiv uses `https://export.arxiv.org/api/query`; Exa uses its search endpoint without printing credentials.

| Round | Engine | Query / citation request | Index total | Returned records |
|---|---|---|---|---|
| 1 | openalex | `infectious jailbreak multi agent` | not exposed | unavailable (HTTP 429) |
| 2 | openalex | `prompt infection agent memory poisoning` | not exposed | unavailable (HTTP 429) |
| 3 | openalex | `multi agent security survey contagion` | not exposed | unavailable (HTTP 429) |
| 4 | arxiv | `all:"infectious jailbreak" OR all:"prompt infection" OR all:"LLM worm"` | 5 | 5 |
| 5 | arxiv | `all:"multi-agent" AND (all:"security" OR all:"malicious")` | 1174 | 30 |
| 6 | exa | `Research papers on prompt injection worms contagion and memory poisoning in multi agent LLM networks` | 10 | 10 |
| 7 | exa | `Surveys of security in LLM multi agent systems contagious prompt injection epidemic models` | 10 | 10 |
| 8 | exa | `Agent Smith Prompt Infection Morris II AgentWorm Cowpox agent network epidemics research` | 10 | 10 |
| 9 | semantic-scholar | `prompt infection multi agent` | not exposed | unavailable (HTTP 429) |
| 10 | semantic-scholar | `forward citations of ARXIV:2410.07283, limit 50` | not exposed | 50 |
| 11 | semantic-scholar | `forward citations of ARXIV:2402.08567, limit 50` | not exposed | 50 |
| 12 | openalex | `filter=title.search:prompt infection, per-page=25, mailto=sol@shad0w.xyz` | not exposed | unavailable (HTTP 429) |
| 13 | openalex | `filter=cites:W4391871694, per-page=50, mailto=sol@shad0w.xyz` | not exposed | unavailable (HTTP 429) |
| 14 | exa | `Published research "Agent Smith" "Cowpox" infectious jailbreak defense` | not exposed | 10 |
| 15 | exa | `Published research "Prompt Infection" "Morris" multi agent worm` | not exposed | 10 |
| 16 | exa | `"Cross-layer contagion of prompt injections" "WormGuard" original paper` | not exposed | 10 |
| 17 | crossref | `query.title=WormGuard Epidemic Modelling and Decentralized Containment of Prompt Worms in AI Agent Networks, rows=3, mailto=sol@shad0w.xyz` | not exposed | 3 |
| 18 | exa | `Research papers LLM agent contagion prompt worms propagation threshold recovery epidemic network containment` | not exposed | 10 |
| 19 | exa | `Research papers returning subagent memory merge infection parent agent corruption persistent re entry` | not exposed | 10 |
| 20 | exa | `Research epidemic models of LLM agent worms recovery quarantine poisoned reservoirs and shared tool contagion` | not exposed | 10 |
| 21 | exa | `Research multi agent infection containment defense cure memory tagging security collaboration tradeoffs` | not exposed | 10 |

Total: 21 search/citation-discovery rounds, 15 successful and 6 HTTP-429 failures, returning 238 records before deduplication. arXiv's broad security query has 1,174 total hits but only the first 30 were screened. Failed calls are unavailable coverage, never zero-hit evidence. OpenAlex direct lookup of W4391871694 did succeed (correct Agent Smith metadata, four citations on the arXiv record), but search and its forward filter did not; the direct record has no usable backward references. Semantic Scholar provided the two 50-record forward lists despite its search endpoint being rate-limited. Crossref and primary source pages supplied bibliographic/abstract verification.

### Citation chasing

- Backward from Prompt Infection: opened the referenced Agent Smith, Morris II, Flooding Spread, Huang resilience and Breaking Agents (2407.20859), plus indirect-injection foundations (2302.12173) and Generative Agents (2304.03442). Existing catalogues were reused. The latter supplies the memory-importance/recency/relevance architecture that the paper evaluates.
- Agent Smith forward: 50 indexed citing records, then primary openings/readings of Cowpox, GAMMAF, Collective Loss of Control, Reliability-Contagion, the trading-contagion study and the newer surveys. Cowpox's reference to Agent Smith was checked in its full text and publisher record.
- Prompt Infection forward: 50 indexed citing records; relevant opened sources and review entries are preserved in the machine-readable log. Both lists expose `next=50`; no claim of exhaustive citation coverage is made.
- Morris II forward: AgentWorm reference [11] checked in its HTML, and its quoted CCS identity resolved through the publisher-deposited DOI record. The architectural successor [[zha-2026-autonomous]] was opened and catalogued separately.

### Reviews, triage, access and saturation

On-topic reviews discovered and retained: existing [[he-2024-emerged]], [[yu-2025-survey]], [[lin-2026-survey]], [[yang-2026-sok]]; new [[ling-2026-toward]], [[mostafavi-2026-trustworthy]], [[ferrag-2025-from]], [[wu-2026-comparative]], [[gan-2026-navigating]], [[jiang-2026-sok]], [[mchugh-2025-prompt]], [[cao-2026-systematic]], [[gong-2026-security]]. Broad maritime RL, blockchain consensus, embodied-system and general MLOps hits were not silently treated as LLM contagion evidence. Non-paper repositories/news/mirrors were used only as leads.

ACM primary pages for WormGuard and the industrial review returned 403/client challenges. Their publisher metadata was confirmed through Crossref, and their abstracts were actually read through Semantic Scholar. These two entries explicitly disclose the secondary abstract and remain non-load-bearing until primary methods are checked. IEEE abstracts were opened through the reader for the reproduction-number article and systematic survey. The Cross-layer contagion publisher page challenged the client, but its publisher-deposited Crossref abstract was read. Exa library cards were not treated as primary papers: WormGuard and Cross-layer contagion were resolved to real DOI records before cataloguing. An unrelated DOI offered alongside WormGuard resolved to Morris II, and was not misattributed.

**Saturation is not certified.** The final two diversified confirmation queries each returned ten hits. They left two new unscreened leads in the first (Semantic Immunity and Lazy Validation/Self-Healing) and one in the second (AgentSafe), i.e. 20% and 10% raw-hit novelty. This does not satisfy two consecutive rounds below 15%; broad forward lists also remain unexhausted. They are explicitly recorded in the researcher inbox, along with the content-blocked Memory Poisoning Propagation and Repair paper. This task's minimum catalogue/read-depth/coverage deliverables are complete, but no survey-ready or global-completeness claim follows.

### What the evidence bears on

The recurring merge risk is upgrading returned information into authority: reports can launder control decisions, histories can bias later retrieval, and inherited files can make influence durable. Distinguish misinformation, availability loss, malicious-action execution, persistent state and autonomous onward propagation. Thresholds derived from epidemic dynamics, topology comparisons and judge-dependent scoring are not interchangeable with a Byzantine k-of-n guarantee. Architecture-level origin binding, admission gates, capability attenuation and recovery should be evaluated together with utility, rather than inferred safe from one refusal or benchmark score.

### Completion checks

`lab.py verify --agent shadow/sol-g74`: 21 papers checked against arXiv/Crossref, 0 problems (rerun before pushing after rebase). `lab.py check`: 0 errors, 5 pre-existing thread-link warnings outside this lane. `lab.py index` regenerated the library index, references and status. The research commit was pushed without force after rebasing; lab.py then marked this task done with all 42 paper outputs and the search receipt. Hook-added Sol co-authorship preserved.
