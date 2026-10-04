# Heterogeneous swarms: established work and remaining questions

Research snapshot: 2026-10-04 UTC / October 3 Pacific. This is a source-grounded scoping review, not a completed systematic survey. [Source records](sources.json) give access depth and URLs. Nineteen papers, six repositories and four first-party posts/API/project pages were opened. Three fresh X posts and two inherited X records are discussed in [search notes](SEARCH-LOG.md). Most papers were screened at abstract level; selected methods passages were inspected for Self-MoA, C2-MAS and reward-design theory. No paper is newly certified as read in full, no code was run, and no experimental results are claimed.

## What heterogeneous means here

Keep six axes separate: **model family/weights**, **capability or tools**, **role**, **private evidence**, **decision interface**, and **speed/resource constraints**. A collection of differently prompted copies is role-diverse but model-homogeneous. Multiple identities sharing one model are not multiple independent weight instances. A Jev choice head attached to a Qwen worker is a composite agent unless it has its own state and decision loop. Haiku is a model family, not a pinned model; Qwen spans very different sizes. We interpret the user's “Quen” as Qwen. Jev and the local Regrowth pilot's Laya head must not be treated as interchangeable.

## What has already been researched

| Research area | Closest work and reported answer | Consequence for our research |
|---|---|---|
| Multi-model output fusion | MoA and LLM-Blender report gains from combining candidate outputs. [[wang-2024-mixture]] [[jiang-2023-llm]] | A mixed-model answer ensemble is established. Include a strong aggregator and repeated samples from one model. |
| Is diversity itself beneficial? | Self-MoA often beats mixed proposers; quality loss can outweigh diversity. [[li-2025-rethinking]] | “Different models are better” is not a defensible premise. |
| Selecting complementary teams | C2-MAS profiles quality, error decorrelation and predictive divergence; it already tests held-out distribution shift. [[teng-2026-which]] | A held-out split alone is not our novelty. HX-07 studies how communication changes complementarity after selection. |
| Cost-aware routing | RouteLLM routes queries; MasRouter chooses collaboration, roles and models. [[ong-2024-routellm]] [[yue-2025-masrouter]] | New routing implementations need a new mechanism or environment stressor, not a new name. |
| Within-role mixtures and topology | HieraMAS combines heterogeneous role-level mixtures and graph selection. [[yao-2026-hieramas]] | “One cell uses several models” is already an architecture. |
| Strong/weak capability mismatch | Guided Collaboration reports that strong-weak pairings can lose to weak-weak pairs and studies adaptive guidance. [[wang-2026-guided]] | A powerful supervisor may be hard for a small worker to use. Measure interface fidelity and actual progress. |
| Modular small-model tool use | Separate planner/caller/summarizer training is already demonstrated. [[shen-2024-small]] | Specialist pipelines are a baseline, not a fresh discovery. |
| Debate, confidence and escalation | ReConcile combines discussion and confidence weighting; Conformal Social Choice includes Haiku and Qwen and separates automation accuracy from reasoning improvement. [[chen-2023-reconcile]] [[wang-2026-debate]] | Generic mixed-model debate and abstention are crowded. Test partner-induced shift and feedback, with coverage as well as accuracy. |
| Communication can hurt | Collaboration Tax studies grounding failures; Diversity Collapse finds authority and dense interaction can suppress ideation diversity. [[sun-2026-collaboration]] [[chen-2026-diversity]] | Use independent/no-communication baselines. Diversity of ideas is distinct from correct decisions. |
| Biological/robotic division of labor | Reward-design theory identifies when specialized allocation pays; adaptive robot allocation responds to changing capabilities. [[amir-2025-when]] [[emam-2020-adaptive]] | HX-02 is a transfer test under noisy language-agent feedback, not an invention of specialization. |
| Minority defense | Cowpox already studies recovery driven by a small defensive population. [[wu-2025-cowpox]] | HX-03 must manipulate model-error covariance and common evidence separately. Minority placement alone is insufficient novelty. |
| Practical Jev integration | Jev/SLM workers and Jev per-action monitoring already have repositories. [[gh-svitatlco-jev-skill]] [[gh-shapor-jev-sentinel]] | Do not pitch “Jev supervises Qwen” as a novel result. |
| Missing actions | Zhong et al. directly study Jev's arithmetic rejection bottleneck and Boolean/threshold mitigations. [[zhong-2026-when]] | HX-04 was demoted. Any follow-up must include those baselines and genuinely different menu-generation conditions. |
| Fast/slow control | AI-RAN combines slow LLM placement and fast exact allocation. A control-code study attributes some hierarchy advantages to internal memory; its LLM backend results are mocks. [[li-2026-deadline]] [[gh-kuznetsovkarazin-causal-depth-limits]] | HX-01 needs memory-matched flat and exact-controller baselines. Delay-induced instability is known; semantic state validity is the narrower test. |
| Persistent economies | CoffeeBench supplies heterogeneous firm roles and long-horizon dependencies. [[sakana-2026-coffeebench]] | Role diversity and model diversity must be separated; bounded task worlds are cheaper first tests. |
| Capability advertising | A lemons-market framing and proposed screening/reputation layer already exist. [[mittal-2026-capability]] | HX-24 tests a remedy in a bounded system, not a new economic framing. |

## Jev evidence boundaries

The vendor describes typed probabilistic decisions over supplied state and questions. Type safety prevents a class of malformed outputs; it cannot establish correct interpretation, complete options, calibrated uncertainty under shift or resistance to adversarial content. [[typesafe-2026-introducing]] [[typesafe-2026-systemone]] The sentinel repository's categorical robustness language should be tested, not inherited as a fact. [[gh-shapor-jev-sentinel]]

AutoJev offers a Qwen-derived decision interface, training code and model card, with author-reported calibration results. Its exact curated training corpus is not bundled. It is a useful alternative implementation lead, not a free reproduction or an independent validation of Jev. [[gh-denis-pplx-autojev]]

Anthropic's research-system account motivates parallel workers but also emphasizes increased token use and limits on tightly coupled tasks. It does not isolate model heterogeneity as the cause of gains. [[anthropic-2025-how]]

## Read methods before promotion

For each shortlisted question, the unresolved claim is narrow and conditional. Full-methods comparison could still reveal it is already answered. Search saturation has **not** been reached: targeted searches late in this session found direct counterexamples to our initial novelty assumptions. New-source metadata validation checks titles/identifiers, not scientific correctness. Formal survey, cross-researcher review, hypothesis acceptance and public-plan registration remain separate gates.

The current workspace's Regrowth pilot already mixes Qwen identities with Laya heads. It has one-map and extra-compute limitations recorded in its results. HX-02/03/05 should reuse its lessons while separating evidence exposure, model identity, extra inference and damage exposure. The original pilot is not a Jev replication. Existing SOC-01/38, PX-01/03/04, EX-01, immune-response and Theseus work are mapped per question to prevent parallel reinvention.
