# Source access and search ledger

Access date: 2026-10-03. Twenty new records were checked against the local catalogue by URL, DOI or arXiv identifier using `lab.py find` before creation. Deterministic identifiers and the repository duplicate validator provide another check. This is a targeted expansion, not a systematic or saturated survey. No bibliographic search-result count, saturation percentage or full-reading claim is inferred.

## Reading depth and evidence class

All sixteen new papers are conservatively recorded as **abstract**. Pescetelli and Edmondson were opened as actual paper PDFs and some opening text was also read; that does not constitute a full methods audit. The four technical posts are **skim**, based on introductions, selected implementation/results sections, figure descriptions where present, and conclusions or recommendations. No code was run. Preprints are cited as arXiv versions even when comments name a conference; unverified proceedings pages are not invented.

| New record | Opened source | Reading depth |
|---|---|---|
| [[wang-2025-beyond]] | [Primary paper](https://arxiv.org/abs/2505.12467) | abstract |
| [[yu-2026-multi]] | [Primary paper](https://arxiv.org/abs/2603.10062) | abstract |
| [[xiao-2026-when]] | [Primary paper](https://arxiv.org/abs/2608.01085) | abstract |
| [[wu-2026-scaling]] | [Primary paper](https://arxiv.org/abs/2604.03295) | abstract |
| [[hemmatian-2026-collective]] | [Primary paper](https://arxiv.org/abs/2607.05593) | abstract |
| [[de-pasquale-2022-modeling]] | [Primary paper](https://arxiv.org/abs/2204.08519) | abstract |
| [[edmondson-1999-psychological]] | [Primary paper](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Organizational_Learning_and_Change/Edmondson_1999_Psychological_safety.pdf) | abstract |
| [[pal-2026-context]] | [Primary paper](https://arxiv.org/abs/2607.10441) | abstract |
| [[gradel-2024-provenance]] | [Primary paper](https://arxiv.org/abs/2412.07986) | abstract |
| [[xu-2025-everything]] | [Primary paper](https://arxiv.org/abs/2512.05470) | abstract |
| [[gao-2026-distribution]] | [Primary paper](https://arxiv.org/abs/2605.19779) | abstract |
| [[pescetelli-2022-variational]] | [Primary paper](https://pdfs.semanticscholar.org/0624/153a8ea2348a9156100505b477b1607ac64b.pdf) | abstract |
| [[ma-2021-learning]] | [Primary paper](https://arxiv.org/abs/2109.05413) | abstract |
| [[jiang-2018-learning]] | [Primary paper](https://arxiv.org/abs/1805.07733) | abstract |
| [[fu-2025-absencebench]] | [Primary paper](https://arxiv.org/abs/2506.11440) | abstract |
| [[modarressi-2025-nolima]] | [Primary paper](https://arxiv.org/abs/2502.05167) | abstract |
| [[anthropic-2026-quantifying]] | [Primary post](https://www.anthropic.com/engineering/infrastructure-noise) | skim |
| [[anthropic-2025-effective]] | [Primary post](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | skim |
| [[langchain-2026-how]] | [Primary post](https://www.langchain.com/blog/how-we-built-agent-builders-memory-system) | skim |
| [[chroma-2025-context]] | [Primary post](https://www.trychroma.com/research/context-rot) | skim |

## Search routes used

| Route | Queries or trail | Disposition |
|---|---|---|
| Distributed evidence | Multi-agent collaboration, evidence integration and hidden-profile decisions | Added Wang and Pescetelli; kept effect-size and human-to-agent transfer limits. |
| Memory architecture | Multi-agent memory, consistency and repeated team tasks | Added Yu, Wu and Xu; position papers separated from experiments. |
| Collective failures | Evidence-threshold backdoors and quarantine | Added Xiao as a different threat model, not proof of the external-poisoning design. |
| Cross-field theory | Transactive memory, cooperative learning and psychological safety | Added De Pasquale and Edmondson; mathematical and observational evidence labeled. |
| Provenance trail | Green semirings to first-order provenance with negation | Reused Green; added Grädel and recorded overlap with its 2017 predecessor. |
| Practical memory | Anthropic context engineering and LangChain memory implementation | Added two first-party implementation posts; no independent replication implied. |
| Evaluation controls | Infrastructure noise, uncertainty and missing information | Added Anthropic infrastructure measurements, Gao and AbsenceBench. |
| Context and references | Chroma report and its reference list | Added Chroma and NoLiMa; the report’s links led to primary arXiv abstracts. |
| Routing predecessors | Selective communication and attentional cooperation | Added Ma and Jiang; adaptive routing itself is prior art. |
| Social discovery | `site:x.com multiagent memory paper`; Willison’s lethal-trifecta discussion | X announcement returned no readable text; reused existing social record and its opened primary blog instead of creating a duplicate or invented thread. |

## Existing records reused and limits

- [[green-2007-provenance]]: reopened the [authors’ paper](https://www.cs.ucdavis.edu/~green/papers/pods07.pdf), reading abstract and opening material. Provenance does not certify truth or independence.

- [[anthropic-2025-how]]: reopened the [first-party multi-agent engineering report](https://www.anthropic.com/engineering/multi-agent-research-system). Used as implementation context; no new controlled causal claim.

- [[simonwillison-2025-lethal]]: opened the [original blog](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/). Existing [[x-simonw-1934602159984984235]] supplies a social trail already in the catalogue; its current live X content and metrics were not freshly verified. No duplicate tweet entry or archived transcript was added.

Other linked older catalogue records, including the nearest predecessors already attached to atlas cards, are navigation anchors unless this ledger says otherwise. Their catalogue reading depth is not a claim about reading performed in this scan.

## Leads not promoted to records

- [DAIR.AI announcement](https://x.com/dair_ai/status/2055318564127809571): search discovery only; opening X returned no readable text. No thread contents, author claims or engagement metrics were catalogued.

- “Hidden Profile Decision Making in Multi-Agent LLM Groups”: a publishing-proof search hit could not be opened. Authorship, final publication status and methods remain unverified; it is not evidence for a novelty claim.

- Pescetelli’s PMC page presented an access challenge; the actual paper PDF was opened at the linked mirror instead. Edmondson’s publisher page failed, but the MIT-hosted paper loaded. Access failures were not interpreted as absence of prior work.


## Remaining verification before scientific claims

Read full methods for the closest task-specific predecessors, inspect source code and data, establish which versions were evaluated, and independently reproduce load-bearing results. In particular, check covariance assumptions for effective size, conformal assumptions under adaptive tasks, and whether existing transactional memory already tracks negative dependencies. This batch deliberately leaves those questions open.
