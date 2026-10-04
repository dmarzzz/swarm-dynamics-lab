# References and extensions for twenty priority research candidates

This contribution adds twenty canonical references (sixteen papers and four first-party technical posts), maps them to twenty atlas candidates, and develops fourteen source-grounded comparisons. It prioritizes an evidence-and-memory testbed spanning collective sensing, quorum, diversity, dissent, memory and recovery, with governance and budget extensions.

**Status:** editorial selection by vishesh/codex-methods on 2026-10-03. These are promising questions to investigate, not the team’s accepted top twenty hypotheses. No survey is completed by this scan, no formal hypothesis is registered and no experiment was run. The sources include older human-team and routing research as well as recent agent papers; transfer between those settings is explicitly uncertain.

Read the [fourteen experimental extensions](idea-bank.md), [source access and search ledger](source-ledger.md), [machine-readable priorities](priorities.json) and [machine-readable ideas](ideas.json). The [earlier atlas review](../atlas-review/README.md) covers all 214 candidates and maps all sixteen original briefs. The [immune-response design](../swarm-immune-response/experiment-design.md) remains the shared recovery protocol to refine rather than duplicate.

## Selection and sequencing

The first eight preserve the earlier review shortlist. The remaining twelve provide measurement, memory, dissent, governance and budget comparisons that can reuse its task worlds. Ordering reflects controllability, shared infrastructure and likely decision value, not measured superiority or a claim of novel prior art. Prioritize a falsifiable small comparison over an elaborate new framework.

| Rank | Candidate and title | Original briefs | New canonical references | Why prioritize it |
|---|---|---|---|---|
| 1 | [SOC-01](https://swarm-research.pages.dev/#/questions?q=SOC-01) — Separate information diversity from model diversity | [collective-sensing](../project-briefs/collective-sensing.md), [diversity](../project-briefs/diversity.md) | [[pescetelli-2022-variational]], [[wang-2025-beyond]] | Separates evidence access from model labels on a shared task generator; begin with fixed fact unions. |
| 2 | [SOC-04](https://swarm-research.pages.dev/#/questions?q=SOC-04) — Ablate why semantic routing works | [collective-sensing](../project-briefs/collective-sensing.md), [coordination](../project-briefs/coordination.md), [leadership](../project-briefs/leadership.md) | [[ma-2021-learning]], [[jiang-2018-learning]], [[de-pasquale-2022-modeling]] | Routing has established predecessors; isolate decision relevance and charge the router rather than claim a new communication principle. |
| 3 | [SOC-08](https://swarm-research.pages.dev/#/questions?q=SOC-08) — Stop on evidence sufficiency instead of verbal agreement | [quorum](../project-briefs/quorum.md), [collective-sensing](../project-briefs/collective-sensing.md) | [[fu-2025-absencebench]], [[wang-2025-beyond]] | A deterministic evidence manifest can distinguish premature stopping from reasoning failure without supplying the answer. |
| 4 | [SOC-09](https://swarm-research.pages.dev/#/questions?q=SOC-09) — Evidence-seeking critics versus generic opposition | [dissent](../project-briefs/dissent.md), [discovery](../project-briefs/discovery.md) | [[pescetelli-2022-variational]], [[wang-2025-beyond]] | Critic value is directly testable against another solver; keep evidence acquisition and extra computation equal. |
| 5 | [SOC-23](https://swarm-research.pages.dev/#/questions?q=SOC-23) — Recover function after genuine knowledge loss | [regrowth](../project-briefs/regrowth.md), [memory](../project-briefs/memory.md) | [[modarressi-2025-nolima]], [[fu-2025-absencebench]], [[yu-2026-multi]] | Recovery should distinguish lost facts, lost indexes and inaccessible facts before using an ecological analogy. |
| 6 | [SOC-31](https://swarm-research.pages.dev/#/questions?q=SOC-31) — Find where uncertainty disappears in retelling | [telephone](../project-briefs/telephone.md), [culture](../project-briefs/culture.md) | [[anthropic-2025-effective]], [[chroma-2025-context]] | Claim scope and uncertainty can be scored per hop; separate compression error from already-false evidence. |
| 7 | [SEC-03](https://swarm-research.pages.dev/#/questions?q=SEC-03) — Count evidence domains rather than returning copies | [quorum](../project-briefs/quorum.md), [collective-sensing](../project-briefs/collective-sensing.md), [diversity](../project-briefs/diversity.md) | [[pescetelli-2022-variational]], [[pal-2026-context]] | A synthetic provenance oracle supplies a useful ceiling; observed ancestry remains the deployable comparison. |
| 8 | [SEC-06](https://swarm-research.pages.dev/#/questions?q=SEC-06) — Repair when the dependency graph is wrong | [regrowth](../project-briefs/regrowth.md), [memory](../project-briefs/memory.md), [casefile](../project-briefs/casefile.md) | [[gradel-2024-provenance]], [[yu-2026-multi]], [[langchain-2026-how]] | Highest-value immune-response extension: challenge repair with incomplete and negative dependencies while measuring retained valid knowledge. |
| 9 | [SOC-02](https://swarm-research.pages.dev/#/questions?q=SOC-02) — Measure effective team size on distributed evidence | [collective-sensing](../project-briefs/collective-sensing.md), [diversity](../project-briefs/diversity.md) | [[wu-2026-scaling]], [[pescetelli-2022-variational]] | Estimate covariance over independent task worlds; a single effective-size scalar can hide heterogeneous evidence and attrition. |
| 10 | [SOC-21](https://swarm-research.pages.dev/#/questions?q=SOC-21) — Compress memory by information value | [memory](../project-briefs/memory.md), [culture](../project-briefs/culture.md) | [[pal-2026-context]], [[anthropic-2025-effective]], [[chroma-2025-context]] | Memory selection provides reusable infrastructure; compare recurrence, rarity and eventual decision value under equal storage. |
| 11 | [SOC-22](https://swarm-research.pages.dev/#/questions?q=SOC-22) — Spend redundancy on rare knowledge | [memory](../project-briefs/memory.md), [regrowth](../project-briefs/regrowth.md) | [[pal-2026-context]], [[wu-2026-scaling]], [[yu-2026-multi]] | Copy counts are insufficient if caches and observations share a failure domain; measure marginal recovery per stored token. |
| 12 | [SEC-07](https://swarm-research.pages.dev/#/questions?q=SEC-07) — Stale children can undo a correction | [memory](../project-briefs/memory.md), [regrowth](../project-briefs/regrowth.md), [culture](../project-briefs/culture.md) | [[yu-2026-multi]], [[xu-2025-everything]] | Correction epochs and stale-read traces are inspectable before a model run; freeze merge semantics. |
| 13 | [SEC-48](https://swarm-research.pages.dev/#/questions?q=SEC-48) — When can an isolated child safely return? | [regrowth](../project-briefs/regrowth.md), [institutions](../project-briefs/institutions.md) | [[xiao-2026-when]], [[yu-2026-multi]] | Re-entry warrants held-out continuation tests and false-quarantine controls; a clean snapshot is weak evidence. |
| 14 | [SOC-10](https://swarm-research.pages.dev/#/questions?q=SOC-10) — Test dissent quality rather than dissent quantity | [dissent](../project-briefs/dissent.md), [diversity](../project-briefs/diversity.md) | [[pescetelli-2022-variational]], [[edmondson-1999-psychological]] | Distinct from rewarding disagreement: separate correctness, confidence, evidence quality and rarity. |
| 15 | [SOC-07](https://swarm-research.pages.dev/#/questions?q=SOC-07) — Protect private judgments before public discussion | [dissent](../project-briefs/dissent.md), [diversity](../project-briefs/diversity.md) | [[pescetelli-2022-variational]], [[wang-2025-beyond]] | Private judgments can preserve information or create anchoring; count both beneficial and harmful revisions. |
| 16 | [SOC-32](https://swarm-research.pages.dev/#/questions?q=SOC-32) — Stress-test a casefile when logs are missing | [casefile](../project-briefs/casefile.md), [coordination](../project-briefs/coordination.md) | [[fu-2025-absencebench]], [[anthropic-2026-quantifying]] | Incomplete logs need known deletion mechanisms and explicit unknown states; infrastructure faults must remain visible. |
| 17 | [SOC-29](https://swarm-research.pages.dev/#/questions?q=SOC-29) — Make a report lead to a verifiable response | [whistleblowing](../project-briefs/whistleblowing.md), [institutions](../project-briefs/institutions.md) | [[edmondson-1999-psychological]], [[hemmatian-2026-collective]] | Reporting matters only if it changes verified correction; keep detection, reporting and remediation denominators separate. |
| 18 | [SOC-30](https://swarm-research.pages.dev/#/questions?q=SOC-30) — Appeal false rejections without overwhelming review | [institutions](../project-briefs/institutions.md), [whistleblowing](../project-briefs/whistleblowing.md), [dissent](../project-briefs/dissent.md) | [[edmondson-1999-psychological]], [[langchain-2026-how]] | Appeals consume scarce review capacity; test noisy reviewers and a binding finalization rule before open-ended dialogue. |
| 19 | [SOC-38](https://swarm-research.pages.dev/#/questions?q=SOC-38) — Select complementary teams on a separate task set | [diversity](../project-briefs/diversity.md), [discovery](../project-briefs/discovery.md) | [[gao-2026-distribution]], [[wu-2026-scaling]] | Team selection can overfit a calibration set; hold out whole task families and account for profiling cost. |
| 20 | [BUD-17](https://swarm-research.pages.dev/#/questions?q=BUD-17) — Keep enough budget to finish and verify | [commons](../project-briefs/commons.md), [coordination](../project-briefs/coordination.md), [discovery](../project-briefs/discovery.md) | [[anthropic-2026-quantifying]], [[wu-2026-scaling]] | Final verification competes with exploration; distinguish issued resource caps from actual execution headroom. |

## What the added evidence changes

The hidden-profile study is a concrete predecessor to correlation-aware minority support, with limited collective performance gains. It makes preservation of a rare opinion and improvement of a final answer separate outcomes. [[pescetelli-2022-variational]] Our PX-08 comparison tests that distinction; it does not claim to originate the intervention.

AbsenceBench and NoLiMa supply useful controls for omissions and retrieval without lexical shortcuts. [[fu-2025-absencebench]] [[modarressi-2025-nolima]] Our inference is that successful recovery should be decomposed into restored facts, repaired indexes and justified completeness claims.

Memory architecture and logical provenance add two different repair questions: whether a correction is visible and which conclusions it invalidates. [[yu-2026-multi]] [[gradel-2024-provenance]] PX-02 and PX-03 isolate these mechanisms. Neither source establishes that a language-agent immune response works.

## Coverage of all sixteen original briefs

| Brief | Treatment in this expansion |
|---|---|
| [collective-sensing](../project-briefs/collective-sensing.md) | Core: SOC-01/02/04/08, SEC-03; PX-01/06/07/14. |
| [quorum](../project-briefs/quorum.md) | Core: SOC-08, SEC-03; PX-01/06. |
| [diversity](../project-briefs/diversity.md) | Core: SOC-01/02/07/10/38; PX-07/08/13. |
| [dissent](../project-briefs/dissent.md) | Core: SOC-07/09/10/30; PX-08. |
| [memory](../project-briefs/memory.md) | Core: SOC-21/22/23, SEC-06/07; PX-01/02/03/05/09/14. |
| [regrowth](../project-briefs/regrowth.md) | Core recovery: SOC-23, SEC-06/07/48; PX-02/03/04/05/14. |
| [telephone](../project-briefs/telephone.md) | Near-term measurement: SOC-31; PX-05/09. |
| [casefile](../project-briefs/casefile.md) | Near-term measurement: SOC-32; PX-02/06/11. |
| [coordination](../project-briefs/coordination.md) | Routing and accounting: SOC-04/32, BUD-17; PX-03/10/12. |
| [leadership](../project-briefs/leadership.md) | Secondary: routing roles in SOC-04 and PX-10. No new general leader-selection claim. |
| [whistleblowing](../project-briefs/whistleblowing.md) | Governance extension: SOC-29/30; PX-08/11. |
| [institutions](../project-briefs/institutions.md) | Governance extension: SOC-30, SEC-48; PX-04/09/11. |
| [culture](../project-briefs/culture.md) | Memory-rule transfer: SOC-21/31, SEC-07; PX-09. Human cultural mechanisms are not assumed. |
| [commons](../project-briefs/commons.md) | Budget extension: BUD-17; PX-12/13. No claim to address all public-goods mechanisms. |
| [discovery](../project-briefs/discovery.md) | Critic and selection methods: SOC-09/38, BUD-17; PX-10/12/13. Discovery success still needs independent confirmation. |
| [nca-observatory](../project-briefs/nca-observatory.md) | Parked for this batch: no new NCA-specific source audit. Existing brief and atlas mapping remain; shared recovery vocabulary does not establish a biological or cellular equivalence. |

## Most useful next work

Start with PX-02 (negative dependencies), PX-06 (completeness contracts), PX-01 (novelty versus ancestry), and PX-05 (facts versus retrieval keys): each has a deterministic ground-truth fixture and can change the harness design before spending on model runs. Then review PX-07/08 with the effective-team-size and dissent literature. PX-04 expands the immune-response evaluation only after its threat model is fixed. This is an editorial implementation order, not authorization to run experiments.

For promotion, read the closest papers in full, inspect released tasks and code, search forward and backward citations, and satisfy the lab’s survey and cross-researcher review gates. Abstract-level entries are screening material. Metadata verification establishes source identity, not correctness, novelty, reproducibility or peer review.
