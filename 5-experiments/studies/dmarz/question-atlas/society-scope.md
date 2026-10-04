# Society lane: scope and evidence limits

Status: **HUMAN-REQUESTED UNREVIEWED HUNCHES** for selection. These are 45 society question–prediction–test sketches, accompanied by 22 budget sketches in `budgets.json`, not accepted hypotheses, registered protocols, or findings. They belong in researcher notes until the relevant survey and independent-review gates pass. No models or experiments were run in this pass, and no human study is required by these sketches. Attribution: the original project directions and review updates in the briefs below are Vishesh's; this lane expands them and distinguishes their testable mechanisms for dmarz's human review.

The original LLM survey remains accompanied by a `revise` review. A later author response addresses A1–D14 and adds research, but independent re-review is pending at this update’s snapshot. Its `complete` frontmatter does not imply that the cross-researcher objections are resolved. This list does not silently approve it or close any evidence-depth backlog.

## Material inspected

- Read `AGENTS.md`, dmarz's directives/inbox, and the task/status overview for protocol and scope. The parent owns task state and Git actions for this shared lane.
- Read all sixteen `5-experiments/studies/vishesh/project-briefs/*.md` directions and their README, including NCA Observatory. NCA candidates belong to the physical lane; no language-agent equivalence is assumed.
- Read `5-experiments/studies/vishesh/agent-swarm-influence-research.md` and `background-readings-2026-10-03.md`. The digest is a useful index with acknowledged caveats, not a replacement for each primary source. In particular, it contains broad synthesis phrases that this list does not adopt as settled findings.
- Read `2-surveys/llm-agent-swarms.md` together with `2-surveys/reviews/llm-agent-swarms--dmarz.md`, including the later source-recovery appendix. Read `3-synthesis/pre-experiment-research.md` and preserve its distinction between supplied, recorded and inferred lineage. Admission/rollback/Sybil mechanisms belong primarily to the security lane.
- Inspected the summaries, methods or limitations of the existing library records cited by these cards; some long records were read in selected sections. This is not a full read of all cited primary papers or of the entire library. Existing record read-depth labels describe the cataloguing agents' work, not this pass.

## Primary anchors reopened on 2026-10-03

These pages were reopened at **abstract depth**, with metadata and abstract checked. They supplied framing checks, not new full-read claims or independent reproductions. No new library records were created.

| Existing record | Source reopened | Consequence for these cards |
|---|---|---|
| [[zhang-2026-silo]] | [Silo-Bench](https://arxiv.org/abs/2603.01045) | Distributed evidence and integration failures already have direct prior art; exact scoring requires methods review. |
| [[fukushima-2026-message]] | [Message capacity and claim wording](https://arxiv.org/abs/2609.19183) | Fit claim-dependent priors; capacity alone need not predict collective outcomes. |
| [[liu-2026-social]] | [Social Networks of LLM Agents](https://arxiv.org/abs/2607.03695) | Narrow-attention results and the wider-attention escape condition are conditional, not universal graph laws. |
| [[itkin-2026-local]] | [Local Predictability and Collective Fidelity](https://arxiv.org/abs/2609.35813) | Local predictive accuracy is insufficient; earlier history effects did not transfer in the reported new-statement test. |
| [[li-2026-socialization]] | [Does Socialization Emerge?](https://arxiv.org/abs/2602.14299) | Shared vocabulary, semantic stability and interaction do not establish mutual influence or consensus. |
| [[perez-2024-cultural]] | [Cultural evolution in LLM populations](https://arxiv.org/abs/2403.08882) | Transmission experiments and interfaces are established, so a new viewer alone is weak novelty. |
| [[pal-2026-swarmworld]] | [SwarmWorld](https://arxiv.org/abs/2608.26081) | Artifact-mediated communication and portfolio benefits already have direct precedent. |
| [[liu-2025-can]] | [Can an Individual Manipulate the Collective Decisions?](https://arxiv.org/abs/2509.16494) | One-known-agent influence is prior art; benign prediction from choice observations is a narrower boundary test. |

## Constraints carried from the revise review

- Do not combine distinct meanings of critical population size, all-correct scoring, task accuracy and effective team size into a universal scaling law.
- The Flag Game and its coauthor's theory are not independent replications. These cards do not reproduce the survey's incorrect claim of zero wrong consensus at every population size above 32, nor claim polarization is safer.
- Mean-field descriptions can require a claim-specific wording field. Pairwise coupling need not predict group exposure.
- Diversity is one lever, not the only demonstrated lever. Compare evidence diversity, capability, provider family, sampling and total cost separately.
- Visible wording/convention copying does not establish belief copying. Moltbook counterevidence is included, and independent social memory/attention assumptions remain to be evaluated.
- Flint's deterministic naming-game threshold is not evidence for irreversible capture after a committed minority leaves. No card uses that mistaken inference.
- Published surrogate results have transfer limitations and a reported non-replication of earlier history effects. Surrogates must pass collective validation before large cheap sweeps are interpreted.
- Existing incident analyses provide bounded observations. A replay graph does not by itself identify contagion, agency, common operator, or intent. Synthetic trace tests precede any wild-data claim.

## Design conventions and unfinished prerequisites

All cards specify a prediction that could fail, a concrete intervention or measurement contrast, episode/world/chain-level independence, and resource accounting. Paired seeds are blocking variables, not a licence to treat correlated messages as independent samples. No suggested sample count is presented as powered. Exact models, independent replicate counts, primary endpoints, practical-effect margins, multiplicity policy and spending limits must be fixed after human selection and a pilot-based precision analysis.

Budget matching is an estimand choice: fixed total resources can thin each worker's reasoning as population rises. Where useful, a separately labelled fixed-per-agent sensitivity study is suggested rather than conflating these regimes. Full-information or perfect-backup arms are diagnostic ceilings, not free deployable baselines. Explicit tool access and shared-world observations are counted as information channels.

`novelty` labels are provisional classifications: replication, boundary test, extension, measurement or speculative. They do not assert a literature-wide absence. Many institutional candidates currently have adjacent benchmark precedents rather than a fully audited closest implementation; those require focused novelty searches before promotion. `api-small` means a small-scale API or local-model prototype could test the question, not a verified runtime or dollar estimate. Nothing was installed or benchmarked here.

The society lane covers useful collective behavior, memory retention, epistemic measurements and institutional rules. It intentionally does not duplicate the security lane's main lineage-admission, rollback, identity or hostile-content mechanisms. SOC-33 is benign preference prediction; SOC-34 tests common exposure versus wording and decision convergence. SOC-37 tests fact-preserving tailoring through ordinary retrieval in fictional local tasks, including generic framing and no-communication controls. These are unexecuted behavioral sketches, not operational attack procedures. Real-data extensions remain dependent on licences, redaction, observed access, and a held-out dataset or scaffold; AI Village access was not checked again.

## Original brief coverage

Each row credits Vishesh's original direction. Candidate ordering is topical, not a ranking.

| Original brief | Society cards |
|---|---|
| [casefile](../../vishesh/project-briefs/casefile.md) | SOC-32, SOC-36 |
| [collective-sensing](../../vishesh/project-briefs/collective-sensing.md) | SOC-01, SOC-02, SOC-03, SOC-04, SOC-05, SOC-08, SOC-11, SOC-13, SOC-19, SOC-35, SOC-38, SOC-41, SOC-42, SOC-43, SOC-44 |
| [commons](../../vishesh/project-briefs/commons.md) | SOC-14, SOC-26, SOC-27, SOC-28 |
| [coordination](../../vishesh/project-briefs/coordination.md) | SOC-03, SOC-04, SOC-13, SOC-14, SOC-15, SOC-16, SOC-19, SOC-20, SOC-35, SOC-40 |
| [culture](../../vishesh/project-briefs/culture.md) | SOC-12, SOC-14, SOC-24, SOC-25, SOC-26, SOC-34, SOC-45 |
| [discovery](../../vishesh/project-briefs/discovery.md) | SOC-36 |
| [dissent](../../vishesh/project-briefs/dissent.md) | SOC-06, SOC-07, SOC-09, SOC-10, SOC-11, SOC-12, SOC-29, SOC-30, SOC-40, SOC-43 |
| [diversity](../../vishesh/project-briefs/diversity.md) | SOC-01, SOC-02, SOC-07, SOC-12, SOC-13, SOC-26, SOC-33, SOC-38, SOC-40, SOC-41, SOC-44 |
| [institutions](../../vishesh/project-briefs/institutions.md) | SOC-20, SOC-25, SOC-27, SOC-28, SOC-29, SOC-30 |
| [leadership](../../vishesh/project-briefs/leadership.md) | SOC-06, SOC-16, SOC-17, SOC-18 |
| [memory](../../vishesh/project-briefs/memory.md) | SOC-21, SOC-22, SOC-23, SOC-24, SOC-31, SOC-45 |
| [nca-observatory](../../vishesh/project-briefs/nca-observatory.md) | Physical lane; read here only for scope boundaries |
| [quorum](../../vishesh/project-briefs/quorum.md) | SOC-05, SOC-08, SOC-11, SOC-39, SOC-42, SOC-43, SOC-45 |
| [regrowth](../../vishesh/project-briefs/regrowth.md) | SOC-18, SOC-22, SOC-23 |
| [telephone](../../vishesh/project-briefs/telephone.md) | SOC-21, SOC-31, SOC-32, SOC-34 |
| [whistleblowing](../../vishesh/project-briefs/whistleblowing.md) | SOC-10, SOC-28, SOC-29 |
| [External influence](../../vishesh/agent-swarm-influence-research.md) | SOC-33, SOC-34, SOC-37; any hostile-content follow-up requires separate scoping |

The v1 structural pass checked its 74 society source pointers and all brief paths. The v2 check below supersedes that count; path validation does not certify source conclusions or experimental readiness.

## Within-researcher editorial audit

A bounded cross-bank editorial pass read candidate predictions, tests, baselines, falsifiers, confounds and prior relationships across the initial 140-card bank. This was not a cross-researcher survey or hypothesis approval, and it did not re-audit every primary paper. The parent receives cross-bank recommendations separately.

Society revisions made during that pass: SOC-06 now distinguishes no-evidence anchoring from the separately predicted evidence-bearing effect; SOC-07 explicitly includes the never-revise condition its prediction names; SOC-35 now tests a comparative collective-forecast prediction rather than treating failure of local prediction as its own falsifier; SOC-36 now crosses access-log visibility rather than predicting an untested missingness effect. SOC-37 closes the missing incremental external-document comparison while retaining the brief's profiling/generic-framing distinction, ordinary-retrieval denominator and independent utility score. The existing Nestaas library record was inspected for that addition; its primary text was not newly fully read.

Near-overlaps are suitable for shared harnesses rather than automatic deletion: SOC-01 versus SEC-12 compares collective solvers with validators; SOC-31 versus SEC-05 separates claim fidelity from authority/provenance promotion; SOC-36 versus SEC-26/SEC-30 separates triage utility from construction leakage and base-rate calibration; SOC-15 versus SIM-02 separates delay-driven asynchronous completion from update-order sensitivity. These cards should remain separately selectable only while those endpoints and mechanisms remain distinct.


## V2 update: budgets and newly landed swarm research

Primary update snapshot: `bf74eb0` from main, incorporating the survey-response research in `58da228` after the initial update began at `7866552`. **HUMAN-REQUESTED UNREVIEWED HUNCHES** remains the status of every card. No accepted hypothesis, survey approval, completed experiment, or verified literature-wide novelty is implied. The parent handles the task, Git and review interface; this lane wrote only `society.json`, `budgets.json` and this scope note.

Added **BUD-01–BUD-22** and **SOC-38–SOC-45**. Existing society IDs revised: **SOC-01, SOC-02, SOC-07, SOC-10, SOC-11, SOC-15, SOC-16, SOC-27, SOC-28, SOC-34, SOC-37**. All other existing society cards are unchanged.

| Existing card | Substantive change |
|---|---|
| SOC-01 | Adds the direct evidence-partitioning prior and capability/rare-query counterevidence; freezes capability-matched pools on separate tasks and narrows the model-diversity prediction. |
| SOC-02 | Adds market effective-size precedent, explicitly crosses evidence overlap, and measures shared wrong answers; a generic ceiling is not a new contribution. |
| SOC-07 | Adds separated actor-critic groups as a close independence-preserving precedent; initial nonbinding commitment remains this card's intervention. |
| SOC-10 | Adds minority-overturn and quoted-judgment evidence as close precedents; retains the confidence/correctness/inspectable-evidence factorial. |
| SOC-11 | Adds calibrated confidence as an existing intervention that missing-evidence requests must beat. |
| SOC-15 | Adds shared-resource participation evidence, randomized starting order and common budget visibility; makes the fast-state-change accuracy-loss falsifier explicit. |
| SOC-16 | Adds direct planner/orchestrator allocation prior, equal capability metadata and an enforced shared cap. |
| SOC-27 | Adds commons precedent, separates game credit from actual costs and changes provisional novelty from speculative to extension. |
| SOC-28 | Adds costly public-goods institutions, charging enforcement and separating payoff tokens from inference resources. |
| SOC-34 | Adds the direct matched-exposure feed experiment and notes its bundled exposure/ranking treatment. |
| SOC-37 | Links Vishesh’s newly landed external-content design and locks private choices and retrieved evidence before peer exchange, preserving the generic-versus-tailored retrieval comparison. |

The eight new society cards cover team-selection transfer (38), error-pattern information beyond average correlation (39), isolated subgroup deliberation (40), interpretation versus persona diversity (41), candidate coverage versus final selection (42), abstention under shared confident mistakes (43), matched SFT/DPO checkpoint transfer (44), and local-memory effects near a pre-calibrated convention-stability boundary (45). SOC-45 measures persistence over a fixed horizon using benign fictional conventions; it does not test the truth of those conventions or claim infinite irreversibility. It differs from SOC-25's adaptation after a task-rule change.

### Inputs and read depth for this update

- Re-read the relevant repository protocol, the new `agent-budgets` topic definition, and all of `5-experiments/studies/dmarz/agent-budgets-hunches.md`. B1–B5 are dmarz/budget's original directions; the budget cards expand them for human selection rather than promoting them through the gate.
- Inspected all **39 paper/blog records then tagged `agent-budgets`**, reading summaries, methods and limitation sections as relevant. This was a catalogue-level review, sometimes selected sections of long records, not 39 primary full reads. No record read-depth was changed and no library entry was added.
- Read the substantive survey changes and A1–D14 author response in `git diff b9cd5eb..58da228 -- 2-surveys/llm-agent-swarms.md`; inspected metadata and summaries for all **54 newly added paper records** in that change. Read complete catalogue records for the load-bearing additions on capability-controlled diversity, evidence partitioning, small-group deliberation, preference optimization, error-pattern dependence, minority correction and confidence-gated theory, plus the revised De Marzo and Magistrali records. Their owners' `full` or `skim` labels describe their work, not this pass.
- Reopened budget primary abstracts for [[wang-2026-r3]], [[paliskara-2026-worse]], [[zhu-2026-fault]], [[liu-2025-budget]], [[lin-2026-bagen]], [[amayuelas-2025-self]], [[piedrahita-2025-corrupted]], [[borah-2026-bosses]] and [[hu-2026-dissociative]]. Read targeted [task-budget documentation sections](https://platform.claude.com/docs/en/build-with-claude/task-budgets) on advisory limits, counting, compaction and `remaining`; no provider feature was run.
- Reopened swarm primary abstracts for [[kim-2026-are]], [[li-2026-diverse]], [[barrera-lemarchand-2026-wisdom]], [[hossain-2026-agreement]], [[begin-2026-preference]], [[de-marzo-2026-conformity]], [[magistrali-2026-aligned]] and [[usman-2026-peer-voted]]. Read selected [De Marzo results/phase-boundary methods](https://arxiv.org/html/2605.10721), [Magistrali recovery results](https://arxiv.org/html/2608.22444), and [Begin checkpoint/limitations sections](https://arxiv.org/html/2606.26583). None is claimed as a new complete primary-paper read.

### Coverage of the budget hunches

| Original hunch | Candidate cards | Mechanisms kept distinct |
|---|---|---|
| B1: visibility × pooling | BUD-01, BUD-02, BUD-05, BUD-16, BUD-17, BUD-22 | Countdown information, peer detail, forecast use, priority rights, terminal reserves and minimum service. |
| B2: identity splitting for quota | BUD-06, BUD-07, BUD-08, BUD-09 | Endogenous extra spawning, rule discovery, fees versus lineage, and useful allocation under safe escrow. |
| B3: who divides | BUD-09, BUD-10, BUD-11, BUD-12, BUD-13, BUD-16, BUD-17, BUD-18, BUD-21, BUD-22 | Allocation architecture, cost information, replanning frequency, online difficulty, authority, reserves, resource units, learning objective and welfare objective. |
| B4: tacit coordination | BUD-02, BUD-14, BUD-15 | Named peer spending, public subtask claims and exogenous spending-norm exposure; agreement or convergence is not itself collusion. |
| B5: misreported budgets | BUD-03, BUD-04, BUD-05, BUD-18, BUD-19, BUD-20, BUD-21 | Display errors, resource-type confusion, calibrated forecasts, representation, advisory targets, compaction accounting and transfer under unfamiliar caps. |

The budget bank can share a synthetic task harness without collapsing these causal contrasts. BUD-06–08 measure incentive-driven delegation and productive work; the security lane's false-name admission/allocation cards primarily measure resistance of the mechanism. BUD-09 treats conservation as a prerequisite and measures stranded resources and useful completion; it does not propose escrow conservation as new. BUD-17 is terminal-stage scheduling, whereas SOC-28 is the social organization of verification funding. BUD-14 is specifically the subtask-claim/spending ledger; SOC-14 asks about richer shared artifacts as an information channel.

### Evidence limits that change the design

- R³ allocates one model's budget across problems, so it cannot by itself establish how bargaining peers behave. Its retrospective successful-allocation ceiling is not an online deployable policy. Worse Together is a closer shared API-budget precedent; benchmark release was still described as forthcoming, so small independent synthetic tasks are the starting point.
- Task-budget documentation describes an advisory model signal. Per-request output caps, whole-loop compute, context occupancy, billed input and tool charges are distinct. Every budget sketch needs an independently enforced root envelope; “overspend” under that envelope means an attempted/rejected request unless actual accepted charges exceed it.
- Hu's dissociative-identity paper is an argument about governance, not a proved impossibility theorem for Sybil-proof reputation. Classical false-name results depend on the mechanism's domain and assumptions. Zhu's conservation result is conditional on mediation, durable state and related assumptions and evaluates crash faults; it does not establish productive allocation, Byzantine resistance or real provider billing compatibility.
- Cost-aware planner, public-goods and pricing papers have different objectives and budget meanings. Additional sanction endowments, hidden coordination work, task capability and provider generations cannot be silently carried into a matched-compute claim. Spend imitation, equalization or explicit talk does not establish deceptive intent or collusion.
- The new swarm records offer both diversity benefits and counterexamples. Family names do not guarantee independent errors; capability, question difficulty, error patterns and answer selection need separate measurement. Oracle candidate coverage is not deployable accuracy, and a scalar effective-size proxy is not a universal law for arbitrary panels, markets or interacting populations.
- The recovered convention papers already support different persistence regimes. Their apparent reversal conflict does not justify a new generic capture experiment. The narrow open comparison is locality and memory around a pre-calibrated boundary, with finite-horizon claims and separate calibration/evaluation pairs.

Validation in this pass: both JSON arrays parse, IDs are unique, **103 society source pointers and 46 budget source pointers** resolve to existing records, and every brief path exists. The 30 new cards each contain concrete units, comparisons and resource accounting; this structural/editorial check is not an execution result. A within-researcher editorial peer audit checked the revised early cards and SOC-38–45. It prompted an explicit confidence-only harm contrast in SOC-10 and an explicit dependence-diagnostic prediction in SOC-43 so their falsifiers match the stated hunches. This is not an independent cross-researcher survey or hypothesis approval. No models, simulations, training, provider calls, downloaded checkpoints or human experiments were run. Exact models, effect margins, sample sizes, costs, analysis plans, feasibility checks and gate approvals remain prerequisites after selection.


### Final bounded intake from the SEO design bundle

Main advanced to `a860443` while this update was being finalized. Inspected the new `5-experiments/studies/vishesh/seo-poisoning/experimental-design.md` overview and selected pipeline/propagation controls (private scoring before peer messages; retrieval locked during exchange; shared exposure versus peer propagation). The document is long; this pass does **not** claim a full read or verification of its bibliography and reported numbers. SOC-37 now links the brief and adopts the locked-choice/retrieval control for its existing benign, fact-preserving tailoring test. No additional society cards were added for this bundle.

The bundle maps to existing SOC-07 (private judgment), SOC-09 (evidence-constrained critics), SOC-27/SOC-28 (credit and paid verification), SOC-37 (ordinary external-document retrieval), and SEC-03/SEC-08 (external evidence/provenance controls). These are related mechanisms for human selection, not automatic duplicates. This pass does not adopt its historical claims about absent harnesses or unnamed components, its unverified quantitative claims, or any live-site manipulation proposal. The added link is attribution to Vishesh’s design, not a new primary-evidence record.
