# Source access and claim boundaries

Fresh checks: 2026-10-03 UTC. This is targeted reading, not a new full survey, independent replication or source-quality certification. Existing catalogue depths belong to earlier readers; this pass does not upgrade them. Recommendations in the critiques are our design inferences, not findings of the cited papers. No quantitative agent effect size is adopted as a planning prior.

<a id="e1"></a>
## E1 — Debate versus independent aggregation

[[choi-2025-debate]] · [primary abstract, v2](https://arxiv.org/abs/2508.17536v2). Abstract and version metadata freshly read. The authors report that voting explains much of the gain in their tested debate setups, while targeted interventions can help. Their stochastic-process result has model assumptions; it does not prove that all discussion is useless. Here it motivates an equal-resource independent-work comparator.

<a id="e2"></a>
## E2 — Correlated model errors

[[kim-2025-correlated]] · [primary abstract](https://arxiv.org/abs/2506.07962). Abstract freshly read. The authors report substantial shared errors across the evaluated models, including models with different architectures or providers. This does not identify error dependence in our generated worlds, or calibrate a statistic based on citation overlap. Our recommendation is to measure dependence rather than assign independence from model labels.

<a id="e3"></a>
## E3 — Distributed information is not automatically integrated

[[zhang-2026-silo]] · [primary abstract, v2](https://arxiv.org/abs/2603.01045v2). Abstract freshly read. The benchmark reports failures of integration even when relevant information has been exchanged. It establishes a close benchmark precedent; it does not predict which of our routing, checklist or memory policies will work. We use it to distinguish acquisition, delivery, retention and reasoning failures.

<a id="e4"></a>
## E4 — Memory repair is established benchmark territory

[[chen-2026-memsecbench]] · [primary abstract](https://arxiv.org/abs/2607.27080). Abstract freshly read. The work evaluates persistence, downstream consequences and selective repair, using both deterministic checks and judge-based adjudication. We do not reuse its success percentages: the denominators, workloads and backend configurations differ. The claim that generic memory healing has never been studied is not defensible from this context.

<a id="e5"></a>
## E5 — Similar behavior need not establish influence

[[shalizi-2011-homophily]] · [primary abstract, v3](https://arxiv.org/abs/1004.4704v3). Abstract freshly read. The analysis identifies generic confounding among homophily, contagion and covariate effects in observational network studies. Transfer to our controlled agent setting is a design warning, not an automatic theorem: randomization and controlled common exposure can change identifiability.

<a id="e6"></a>
## E6 — Assignment, exposure and estimand must agree

[[aronow-2013-estimating]] · [primary abstract, v4](https://arxiv.org/abs/1305.6156v4). Abstract freshly read. The paper develops randomization-based inference using a specified assignment design and exposure mapping under interference. Its estimators are not automatically valid for every proposed swarm. Our recommendations about whole-world assignment, paired analysis and failure denominators require a protocol-specific analysis plan.

<a id="e7"></a>
## E7 — Transaction boundaries do not cover all semantic reuse

[[li-2026-memtx]] · [primary HTML](https://arxiv.org/html/2607.23929v1). Abstract, opening protocol description and the Section 5 “Scope blind spots” passage freshly inspected; not a full-paper or code audit. The authors report failures when transcription omits a provenance parent and when a stale action is retried in a fresh transaction. These are direct prior-work boundaries relevant to our missing-lineage and stale-return comparisons. They do not establish our proposed repair advantage or verify the paper's implementation.

<a id="e8"></a>
## E8 — Lineage guarantees have attribution preconditions

[[ouyang-2026-memlineage]] · [primary HTML](https://arxiv.org/html/2605.14421v1). Abstract, authority-repair proof-of-concept passage, and discussion of the theorem antecedent, no-strong-parent fallback and adaptive coverage freshly inspected. The stated propagation guarantee depends on critical attribution edges exceeding a threshold. The discussion describes a permissive fallback when no strong parent is found, possible stricter mitigations and limits of adaptive evaluation. The paper also includes recovery demonstrations; it should not be represented as prevention-only. These passages narrow the novelty opportunity but do not certify robustness of the released code.

<a id="e9"></a>
## E9 — Cellular repair is a model with a training objective

[[mordvintsev-2020-growing]] · [primary computational article](https://distill.pub/2020/growing-ca/). Model introduction and local differentiable update description freshly inspected; growth/repair context inherited from our [earlier source review](../biology-visual-review/sources.md#nca). Local learned update rules already support a concrete computational precedent. This is not evidence that language-agent recovery shares biological mechanisms, or that a maze checkpoint tolerates arbitrary hidden-state lesions. The latter remains a methods/checkpoint audit dependency.

<a id="e10"></a>
## E10 — Test whether the task requires the claimed capability

[[ellis-2022-smacv2]] · [primary abstract, v2](https://arxiv.org/abs/2212.07489v2). Abstract freshly read. A timestep-only policy achieves nontrivial results on parts of the original SMAC, motivating the revised benchmark. This is a specific MARL finding, not a measured flaw in our agent tasks. Metadata-only, blind and simple scripted policies are proposed diagnostic controls here. Behavioral constructs such as cooperation, causality and adaptation need their own operational validation.

<a id="e11"></a>
## E11 — Agreement guarantees are not guarantees of external truth

[[lamport-1982-byzantine]] · [primary paper](https://lamport.azurewebsites.net/pubs/byz.pdf). Abstract and opening problem definition freshly read. The paper considers agreement under arbitrary behavior by a bounded number of faulty participants and specified messaging assumptions. This is not an independent-errors assumption and does not establish truth when legitimate agents consume the same wrong external datum. Do not transfer a fault threshold to a free-text voting scheme without its full model.

<a id="e12"></a>
## E12 — Direct specification checks and engineering reasoning

This is not a literature source. It denotes the inspected repository specification or a reviewer-derived logical argument. The [previous Scheme C review](../atlas-review/design-review.md) and the current design still give `C* = 1 - 1/(1 + kappa*N_eff)` with commitment requiring `C <= C*`. For finite positive `kappa*N_eff`, a unanimous normalized distribution has `C = 1 > C*`. That is a counterexample to intended unanimous-commit reachability, not an empirical LLM result. Retry identity critiques similarly concern what the supplied fixture can establish; classical idempotency novelty has not received a new literature survey here.

## Evidence not newly verified

The existing biological precedents, twenty-source expansion, NCA reasoning references and 200-plus citations in the SEO bundle remain inherited context unless listed above. The team’s deployment and validation notes are reports by their authors, not runs performed in this review. We inspected discussion-dose task/evaluation and validation documentation, not private fleet traces or secrets. Its documentation reports scripted execution and zero real model calls at the reviewed snapshot; check the latest manifest before repeating that statement later.

No formal gate review is filed. The pending cross-researcher survey review remains separate. Before elevating a selected comparison, read the closest methods and code, inspect negative results, search forward/backward citations, and apply the repository’s review requirements.
