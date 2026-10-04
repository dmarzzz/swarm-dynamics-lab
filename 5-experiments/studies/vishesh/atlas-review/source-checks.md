# Primary source checks and evidence limits

Access date: **2026-10-03**. These are checks performed for this review, distinct from existing library metadata. Abstract access confirms scope and an author's reported claim; it does not validate a result, audit its methods, or constitute replication. No source is newly marked `full` or `ran` by this contribution.

## Fresh checks

| Canonical source or official documentation | Material inspected this session | What it supports here | Limit |
| --- | --- | --- | --- |
| [[choi-2025-debate]] · [primary abstract](https://arxiv.org/abs/2508.17536) | Abstract and version metadata | Separate debate from voting and independent-computation baselines. | No universal claim that debate cannot help; formal results depend on the paper's model. Prior reading notes' table discrepancy was not re-audited. |
| [[cemri-2025-why]] · [primary abstract](https://arxiv.org/abs/2503.13657) | Abstract and version metadata | Existing failure taxonomy and annotated trace work are nearest context for casefiles and discovery. | Does not validate our proposed ranking or establish real-world failure prevalence. |
| [[zhang-2026-silo]] · [primary abstract](https://arxiv.org/abs/2603.01045) | Abstract | Distributed evidence/coordination benchmarking already exists. | No claim that our routing comparisons are novel without full methods review. |
| [[tambwekar-2026-proxifield]] · [primary abstract](https://arxiv.org/abs/2609.20889) | Abstract | Semantic routing is existing prior for collective sensing and coordination. | Reported domains do not prove universal scaling or causal value of each routing component. |
| [[kim-2025-correlated]] · [primary abstract](https://arxiv.org/abs/2506.07962) | Abstract | Correlated model errors undermine treating models as automatically independent. | Does not calibrate the bundle's citation concentration statistic. |
| [[shalizi-2011-homophily]] · [primary abstract](https://arxiv.org/abs/1004.4704) | Abstract | Shared causes and influence are difficult to separate from observational similarity. | Human-network assumptions are not automatically the agent task model; randomized controls here are reviewer design inferences. |
| [[aronow-2013-estimating]] · [primary abstract](https://arxiv.org/abs/1305.6156) | Abstract | Interference requires specifying assignment and exposure, rather than treating outcomes as independent by default. | This review does not derive a valid estimator or power calculation for the final unbuilt experiment. |
| [[nestaas-2024-adversarial]] · [primary abstract](https://arxiv.org/abs/2406.18382) | Abstract | External manipulation of LLM-based search is prior for the retrieval surface. | Not evidence of peer amplification or of attacks succeeding against a live swarm. |
| [[blanchard-2017-byzantine]] · [primary abstract](https://arxiv.org/abs/1703.02757) | Abstract | Robust aggregation was developed for a specified distributed-learning setting. | No theorem transferred to text judgments. |
| [[el-mhamdi-2018-hidden]] · [primary PDF](https://arxiv.org/pdf/1802.07927) | Abstract; targeted model passage in Section 2 and algorithm precondition in Section 4 | Bulyan needs `n >= 4f+3` gradients; its statistical/fault setting differs from shared external misinformation. | Targeted methods check, not full-paper reading or implementation verification. |
| [[li-2026-memtx]] · [primary HTML](https://arxiv.org/html/2607.23929v1) | Abstract and opening scope | Staged belief commitment and cascading repair are existing work. | Reported guarantees and experiments were not independently verified; incomplete-lineage novelty still needs detailed comparison. |
| [[ouyang-2026-memlineage]] · [primary HTML](https://arxiv.org/html/2605.14421v1) | Abstract and stated scope | Provenance and derivation-aware action enforcement are existing work with explicit lineage conditions. | This check does not verify soundness, source code or robustness of inferred lineage. |
| [[leibo-2021-scalable]] · [primary abstract](https://arxiv.org/abs/2107.06857) | Abstract | Social interaction and generalization evaluation have established benchmark context. | Does not demonstrate the proposed LLM funding or institutional mechanisms. |
| [[perez-2024-cultural]] · [primary abstract](https://arxiv.org/abs/2403.08882) | Abstract | LLM cultural-transmission simulation is existing prior. | No inference that arbitrary persisted conventions are useful or independent of model priors. |
| [[mordvintsev-2020-growing]] · [primary article](https://distill.pub/2020/growing-ca/) | Article opened and growth/repair framing inspected | NCA growth and repair are established concepts. | Not a fresh full reading or checkpoint execution. |
| [[etcheverry-2026-reasoning]] · [primary abstract](https://arxiv.org/abs/2609.36126) | Abstract | NCA reasoning, stochastic updates and damage recovery are already claimed by recent prior work. | Exact hidden-state lesion and schedule coverage still needs methods/code inspection. |
| [[pal-2026-swarmworld]] · [primary abstract](https://arxiv.org/abs/2608.26081) | Abstract | Artifact-mediated agent societies are relevant context. | Does not establish our redundancy, portfolio or commons effects. |
| [[ellis-2022-smacv2]] · [primary abstract](https://arxiv.org/abs/2212.07489) | Abstract | Original SMAC admits surprisingly strong policies conditioning only on timestep; blind-policy validation is prior. | No SMAC or SIM-03 experiment was run by this reviewer. |
| [TypeSafe Choice](https://docs.typesafe.ai/primitives/choice) | Interface description and request/response examples | A concrete Jev-backed option-selection interface exists. | Vendor documentation; no provider call, latency, price or robustness verification. |
| [TypeSafe Confidence](https://docs.typesafe.ai/confidence) | Choice confidence formula and examples | Confidence is a deterministic transform of the returned probabilities and option count. | It is not a separate calibration test against task truth. |

## Inherited context

All other sources attached to candidate cards or extensions are **catalogued comparison anchors**, not newly verified claims. In particular, the rollback/checkpoint survey [[elnozahy-2002-survey]], swarm-trace tooling records, detailed physical-swarm mechanisms and individual fork/merge source batches need targeted primary review before they carry a novelty or quantitative claim. We preserve canonical IDs rather than duplicating bibliographic records or silently upgrading reading depths.

The new SEO-poisoning bundle uses numbered citations with its own verification labels. Those labels belong to that bundle's authors. This review inspected design-critical passages and selected primary sources, not all of its 200-plus numbered references. The simulator survey's run notes likewise describe work by other agents, not runs by vishesh/codex-methods.

## Remaining source work before promotion

For a selected direction, inspect the closest implementation and full methods; search its backward and forward citations; check negative results and alternative terminology; then complete the repository's survey gate. The most consequential unresolved comparisons are imperfect lineage versus MemTX/MemLineage, evidence-access controls versus Silo/Proxifield, and NCA lesion/schedule coverage versus the latest reasoning paper. The 40 extensions are candidates for that work, not evidence that the gap is unoccupied.
