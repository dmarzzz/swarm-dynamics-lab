# Search scope and verification log

Actual research date: **2026-10-03**, confirmed by the session UTC clock (initial reading 20:01 UTC). Cutoff: material available and verified during this date. No claim of exhaustive coverage or of including every paper released that day.

## Scope and source hierarchy

Targeted narrative review of autonomous scientific research, agent evaluation, single/multi-agent coordination, simulation validity, reproducibility, statistical design and evaluation tooling. Start with foundational work (2018–2024), follow relevant 2025 work, and explicitly search 2026 and September 2026 updates. Include primary empirical, benchmark and methodological papers plus clearly labeled position papers. Official software documentation supports architecture descriptions. Exclude generic vendor roundups, unsourced performance claims and social-media interpretations from evidentiary synthesis.

The initial methods review used public literature and a synthetic collective-sensing teaching example. No private datasets were accessed. For this contribution, source records were reconciled against the existing shared library; reading-depth labels do not claim a new full-paper review.

## Search rounds (2026-10-03)

| Round | Queries / follow-up | What it resolved |
| --- | --- | --- |
| 1 | `AI scientist autonomous scientific discovery agent 2026 evaluation reproducibility arxiv`; `multi agent systems scaling principles 2026 agent evaluation reliability arxiv`; `LLM agents social simulation validation 2025 2026 research` | Broad map; numerous secondary results excluded |
| 2 | `site.arxiv.org "AI Scientist" "2025"`; `site.arxiv.org "Towards a Science" "Agent" reliability scaling`; `site.arxiv.org autonomous scientific discovery 2026 September agent`; direct 2609.04170 | Found primary records and latest reliability/scaling versions |
| 3 | Direct AI Scientist/v2, Co-Scientist, AI Agents That Matter and MAST records; selected HTML papers | Verified titles, versions and scope; detected Co-Scientist's 2026 update |
| 4 | `site.nature.com FunSearch mathematical discoveries language models 2023`; `site.nature.com autonomous laboratory synthesis inorganic materials 2023`; `site.arxiv.org September 2026 "scientific discovery" agents evaluation`; `site.arxiv.org 2026 "agent" "reproducibility" evaluation September` | SciAgentArena, SEE, EurekAgent and AgentActionBench; A-Lab correction |
| 5 | Generative Agents, tau-bench, SOTOPIA and ODD direct records; `site.jmlr.org empirical design reinforcement learning Henderson Agarwal statistical precipice` | Simulation architecture and statistical design anchors |
| 6 | Sample Size Justification, statistical precipice, LLM-as-a-judge searches; direct current judge records | Power/precision guidance and 2026 judge updates |
| 7 | Official Inspect, Mesa, PettingZoo, NetLogo, LangGraph and Melting Pot documentation | Verified framework capabilities, avoided assuming latest docs are stable releases |
| 8 | PaperBench/MLE-bench primary searches; Howard confidence sequences; social simulation validation search | Research execution benchmarks and sequential-inference basis |
| 9 | `site.nature.com "Author Correction" "accelerated synthesis" 2026`; `site.arxiv.org "Time to Close" "Validation" social simulations` | Correction text and ICML 2026 primary proceedings record |

Direct primary record checks established the revised scaling study uses 260 configurations/six benchmarks and reliability v3 uses 15 models. Older indexed abstracts differed. The bibliography uses current version-specific records for these papers. The A-Lab correction was read directly in the publisher PDF text; an intermittent publisher redirect prevented a stable full original-article fetch. Search snippets from reader comments were not treated as the journal's findings.

## Reading depth and limits

The bibliography identifies consultation depth per entry. Selected full-text material was retrieved for the swarm case study, reliability, scaling, MAST, ODD and FunSearch; this does not mean every supplement or proof was read. Most newer benchmark entries were screened from primary abstracts and metadata. Performance claims are deliberately qualitative except where essential to identify study scope or a correction. No quantitative meta-analysis, citation-network saturation claim, risk-of-bias score or complete exclusion count is asserted.

Publication status was verified where visible in primary records or proceedings; otherwise marked unverified rather than inferred from a familiar title. Newer preprints remain provisional. Indexing gaps, English-language emphasis, abstract screening, inaccessible supplements and evolving model services limit completeness. References are linked; no copyrighted full-text archive is redistributed. The examples and recommendations are an original synthesis, not borrowed author instructions.

For an update: repeat the date-bounded topic searches; check each arXiv version history and publisher correction page; add contradictory evidence; record changed recommendations; refresh framework pins and model availability before execution. Never silently replace a citation version in an already registered protocol.

## swarm-dynamics-lab contribution reconciliation

On 2026-10-03, primary arXiv abstract pages, Crossref records, the JMLR article page and the PMLR proceedings page were reopened for the 29-reference set. Three canonical records already existed and were reused; 26 new records were added with conservative `read_depth: abstract`. Automated `lab.py verify --agent vishesh/codex-methods` resolved 24 new records with zero metadata problems. JMLR and PMLR records have no arXiv/DOI field established here and were checked directly at their publication pages; the verifier explicitly warns that those two are URL-only. No fabricated identifiers were added to silence those warnings.

The existing scaling-agent record documents a journal version under a changed title; its audit notes remain authoritative, while the guide's empirical discussion identifies the particular arXiv version consulted. This methods reading guide is not submitted as a formal survey and makes no gate-passing or search-saturation claim.
