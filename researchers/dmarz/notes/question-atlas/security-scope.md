# Security, identity, and detection candidate scope

**HUMAN-REQUESTED UNREVIEWED HUNCHES.** This file and `security.json` are a brainstorming collection for human selection. They are not accepted hypotheses, a completed survey, or permission to run experiments. The user explicitly requested broad questions, related hypotheses, and ways to test them before human review. Keeping these candidates under the researcher's notes follows the repository's hunch provision. Formal promotion still requires the appropriate survey and independent review.

The updated collection contains 53 candidates: 19 for `fork-merge-security`, 21 for `sybil-resistance`, and 13 for `swarm-detection`. Original IDs SEC-01–36 are preserved; this research update adds SEC-37–53. The original creation pass covered 36 candidates, and its read-depth notes below remain a historical record. Each has a falsifiable direction, test sketch, comparators, separate utility and failure measures, confounds, prerequisites, and two or three existing source records. No study was run, no new source records were added, and no source read-depth field was changed.

## What this pass inspected

Read the repository protocol and dmarz directives; inspected the current pre-experiment synthesis, fork-merge synthesis, Sybil/Flashbots synthesis, detection taxonomy, and the fork-merge and Sybil survey status, gaps, tools, and saturation sections. The large existing syntheses were read selectively, not audited line by line. Read summaries, methods/limitation excerpts, or source metadata from 57 cited library entries. Existing entry read-depth labels describe the original cataloguing agents' work; they do not mean this pass independently read all 57 underlying papers.

Reopened these primary anchors to check the candidate framing:

- [BadMerging](https://arxiv.org/html/2408.07362): abstract, introduction, and threat-model framing. It concerns weight-space merging and supports keeping that object distinct from returning text reports. No training procedure was reproduced.
- [MemTX](https://arxiv.org/html/2607.23929v1): protocol and typed-repair passages. The primary text explicitly limits repair to recorded provenance and distinguishes compensation bookkeeping from environment replay. Its action gate is not a guarantee that every action parameter derives from safe beliefs.
- [BuilderNet refunds](https://buildernet.org/docs/refunds): the published flat-tax and identity-constraint definitions. The page warns that the rule described is indicative and actual implementation includes modifications. SEC-14 transfers a published mechanism idea into a toy task setting; it does not claim to replicate current production behavior.
- [On Sybil-Proof Mechanisms](https://arxiv.org/html/2407.14485v5): abstract, introduction, and the boundaries of the stated single-parameter result. Its theorem does not automatically apply to every task allocator or every multi-good environment.
- [Beyond Interaction Patterns](https://arxiv.org/html/2502.17344): matched organic controls, test definition, evaluation, and limitations. This provides a concrete caution against inferring coordination from raw similarity without a relevant null comparison.
- [Simplistic Collection and Labeling Practices](https://arxiv.org/abs/2301.07015): primary abstract alongside the fuller repository record; no independent reanalysis of its datasets.
- [Identifying AI Web Scrapers Using Canary Tokens](https://arxiv.org/html/2605.13706): attribution setup and inference robustness passages, including false matches, missed emissions, and intermediary routing. These motivate separating content exposure from operator ownership.
- [Black-Box Forensics](https://arxiv.org/abs/2606.22698): primary abstract alongside the repository record. Same-prompt linking is not treated as verified same-operator identification.

These were targeted framing checks, not full reads of every method, exhaustive novelty searches, or closure of the existing survey gates.

## Boundaries carried into the candidates

- Classical Byzantine agreement permits arbitrary coordinated faults within its fault bound and message assumptions. It does not assume independent coin-flip failures, and agreement is not factual truth. An older sentence in the fork-merge synthesis remains overly broad; this collection follows the correction in the pre-experiment synthesis and the appended Lamport note.
- Returning a text report, changing persistent memory, changing permissions, and merging model weights are separate experimental objects. SEC-09 concerns small isolated classifiers only. None of the other candidates borrows its threshold or security guarantees.
- True dependency graphs, operator labels, and coalition ownership can be evaluator ground truth or explicitly privileged ceilings. They are never silently available to the evaluated policy. Access logs show retrieval, not necessarily causal semantic dependence.
- Rejection, abstention, isolation, and memory reset can appear safe by eliminating usefulness. Every intervention sketch includes legitimate task performance or another explicit cost of that behavior.
- Per-key or per-credential rate limits do not establish one-person-one-agent. Resource conservation, credential issuance, delegation, shared infrastructure, and multiple radios are distinct assumptions.
- Model attribution, prompt attribution, common ownership, coordinated behavior, and harmful intent are different targets. A shared model or a shared cloud service does not by itself establish any of the latter three.
- Synthetic prevalence scenarios test review-queue behavior; they do not estimate wild agent prevalence. Paired sessions and messages within one interacting episode are not independent replicates.
- All proposed adversarial conditions use synthetic data, controlled local systems, or authorized test setups. Canary sketches use fictional local facts. Market sketches use simulated value and payments. No live attacks, covert tracking, external messages, or production financial actions are proposed.

## Remaining caveats before selection

Several load-bearing neighboring records remain abstract-level, including shared-memory honeytoken theory, the personhood analysis, survey-assistance studies, and the bot realism study. Candidates citing them identify that limitation and ask for full-method checks before promotion. The formal mechanisms, privacy constructions, and attestation semantics also need specialized review if selected; a simulation using ideal primitives cannot validate real cryptographic security.

The novelty tags classify intended study type, not verified novelty. Replication and boundary tests are included deliberately. The broad older synthesis claims that no one has studied particular agent settings remain bounded by their search coverage and are not repeated as established absence claims here.

Some overlap with memory, quorum, regrowth, external influence, robotics, and measurement candidates in other lanes is intentional. Human review should merge duplicates by causal question rather than select two variants merely because they use different terminology. Particularly strong cross-links are SEC-03 (evidence versus identity), SEC-06–07 (repair and stale returners), SEC-08/13 (attention budgets), SEC-25/27 (what detection identifies), and SEC-30/34 (measurement under scarce or incomplete observations).

The exact review thresholds, sample sizes, cost ceilings, permitted hardware, and access arrangements remain to be specified after human selection. Hardware and human-participant sketches are explicitly marked as requiring those resources; they are not immediately runnable commitments.


## Research update after the original atlas

Snapshot basis: changes from `ad723697` through the newly merged research at `bf74eb0`, including the earlier `7866552` and `b9cd5eb` additions. Only this bank and its scope note were edited by this lane. The root agent owns git, task state, compilation, and the human review interface. All entries remain **HUMAN-REQUESTED UNREVIEWED HUNCHES**. This is an editorial and prior-art update, not independent cross-researcher approval.

### Exact candidate changes

Nine existing candidates were refined: **SEC-04, SEC-06, SEC-07, SEC-08, SEC-14, SEC-19, SEC-26, SEC-33, SEC-34**. No original ID was removed or renumbered.

- SEC-04 narrows typed-return enforcement to incomplete taint observations and includes temporal re-entry controls as existing prior.
- SEC-06 recognizes MemSecBench as direct lifecycle/selective-repair prior and separates all-episode from successfully-poisoned denominators.
- SEC-07 compares stale-child revalidation with conservative temporal re-entry gates rather than implying re-entry controls are new.
- SEC-08 distinguishes availability loss from wrong answers, adds CORBA prior, and aligns the hunch's comparator with per-identity fair queueing in its test.
- SEC-14 separates a payout cap over fixed submissions from general false-name-proof allocation and adds allocation-rule prior.
- SEC-19 includes SybilShield and trusted-seed vertex-cut admission, because multi-community false positives and admission-mechanism composition already have direct treatments.
- SEC-26 includes the collusion release's shared task sequences, private-view restriction, and judge-label caveat.
- SEC-33 adds the Ethereum discovery measurement and keeps shared infrastructure and key rotation as benign explanations.
- SEC-34 records that posts-only fraud data and keyword-selected Moltbook records cannot establish propagation edges or successful infection.

Seventeen new candidates were added: **SEC-37–53**. SEC-37–44 cover complementary task bundles, finite false-name counterexamples, job splitting/merging, costly collective choice, trust intermediaries, temporal bidding, verification selection, and power-index credit. SEC-45–52 distinguish error from policy-violation spread, shared-tool reservoirs, the full acquisition/return chain, quarantine release, cumulative harm versus recovery, live detector interventions, evaluator-preference convergence, and repeated reintegration. SEC-53 covers selective withholding in reputation-based routing. These are distinct causal or mechanism questions, not a multiplication of population-size or model-name settings.

### New input mapping

| Input inspected | Candidate impact | Scope of evidence |
|---|---|---|
| New false-name papers: Yokoo 2003; Todo 2009/2011; Iwasaki 2010; Moulin 2007; Wagman 2008; Bachrach 2008; Resnick 2009; Lin 2017/2018; Wang 2017 | SEC-14, SEC-37–42, SEC-44 | Several formal domains differ from agent procurement. Two-sided markets, quality verification, and many online mechanisms remain only abstract-level in the catalogue; no blanket theorem transfer. |
| Conitzer 2010 and SybilShield | SEC-19, SEC-43 | Trusted seeds, bounded real coalitions, and endorsement constraints are assumptions. An agent-created edge is not verified social trust. |
| Eisenbarth 2022 and Pecori 2016 | SEC-33, SEC-53 | Historical discovery-network measurements do not prove owner identity or intent; reputation-routing full methods still need access. |
| Shadow `scan-papers-fm-contagion` completion note and source addenda | SEC-08, SEC-45, SEC-47, SEC-49, SEC-51 | Separates availability, execution, persistence, relay, and projected epidemic quantities. Retries and denominators matter. |
| MemSecBench; Autonomous LLM Agent Worms; Zombie Agents | SEC-04, SEC-06–07, SEC-46–48, SEC-52 | Lifecycle repair and temporal re-entry already have close predecessors. Recorded provenance and conservative declassification remain explicit assumptions. |
| Reliability–Contagion; Cross-layer contagion; Reproduction Number | SEC-45–46, SEC-49 | Fixed-sender and fixed-edge exposure differ; false claims and policy violations are different propagated variables. Abstract-level theory is not calibrated deployment evidence. |
| GAMMAF; Contagion Networks | SEC-48, SEC-50–51 | Live isolation and evaluator-preference propagation already exist. Novelty is narrowed to their operational boundaries and matched budgets. |
| `src/fork-merge-setups/rigs.json`, cards A–F cluster summaries, `prose.html`, and generated artifact context | SEC-45, SEC-47, SEC-52 | Used as a rig and threat-model taxonomy, not a new empirical source or an independently audited result. |
| Agent-collusion, Agent-IPI, FraudBench, stego-collusion, AgentLogs, TRAIL, Moltbook-injection, Instrumental Choices cards | SEC-26, SEC-34 and selection caveats | Cards inspected only; no dataset downloaded or experiment executed. Dataset-wide readiness audit belongs to the other atlas lane. |
| AgentsNet and Kademlia simulator code entries and upstream READMEs | SEC-50, SEC-53 | Practical starting environments with additional required implementation. This lane ran neither. |

### Targeted primary openings in this update

Opened and inspected selected passages from [Yokoo's characterization](https://www.ijcai.org/Proceedings/03/Papers/107.pdf), [Todo's allocation-rule characterization](https://www.ifaamas.org/Proceedings/aamas09/pdf/01_Full%20Papers/04a_23_131_FP_0865.pdf), [Iwasaki's efficiency paper](https://users.cs.duke.edu/~conitzer/worstcasefnpAAMAS10.pdf), and [Conitzer's graph-composition paper](https://www.cs.cmu.edu/~conitzer/fnp_socialWINE10.pdf). This was a targeted framing check of abstracts, domain definitions, and selected theorem statements, not a full proof audit. The attempted Wagman costly-voting PDF opening failed; its record is used only as an explicitly pending full-method prerequisite.

Opened [Reliability–Contagion](https://arxiv.org/html/2607.21912), [Autonomous LLM Agent Worms](https://arxiv.org/html/2605.02812), [MemSecBench](https://arxiv.org/html/2607.27080), [Collective Loss of Control](https://arxiv.org/html/2609.18460), [Contagion Networks](https://arxiv.org/html/2606.20493), and [GAMMAF](https://arxiv.org/html/2604.24477). Selected methods, model assumptions, lifecycle definitions, and limitations were inspected where relevant. No full-reading claim or updated catalogue read-depth is made. Reopened the [Cowpox publisher page](https://proceedings.mlr.press/v267/wu25aq.html) for abstract and publication framing, using the attributed shadow full-read addendum for its prevention-versus-recovery caution.

Opened upstream [AgentsNet](https://github.com/floriangroetschla/AgentsNet) and [Kademlia simulator](https://github.com/datahop/kademlia-simulator) READMEs. AgentsNet's prior one-example execution belongs to the simulation catalogue lane and is not a security evaluation. Its synchronous rounds need explicit isolation hooks. The PeerSim project has no stated license in its record and abstracts transport; resolve reuse terms or independently implement the minimal model, and do not interpret simulated timing as measured network latency. Maelstrom and GossipSub-hardening entries were also inspected but not proposed as drop-in security solutions: the former lacks a Byzantine model, and the latter has licensing and old Testground dependencies.

### Corrections and limits that must survive compilation

The newly published fork-merge setups page still says the contagion lane never ran. That statement is superseded by the completed shadow rerun, which added 21 papers and 21 attributed source corrections. The page also repeats the incorrect blanket statement that every Byzantine threshold assumes independent faults. Classical agreement permits coordinated arbitrary faults within the stated bound. Several broad absence claims and homogeneous-agent descriptions in the cards are also older than the new papers or their audited appendices. This bank uses the artifact's taxonomy and concrete setup differences; it does not propagate those outdated universal claims. No source artifact was edited here.

The strongest new close-prior constraints are substantive: lifecycle selective repair, temporal re-entry gates, live graph-based isolation, and error/evaluator-preference contagion are already studied. Remaining candidate differences must concern incomplete observations, return/release criteria, denominators, matched information budgets, utility tradeoffs, or a clearly specified new setting.

Dataset caveats from this lane's card reads and the parallel dataset audit: Agent-collusion shares 50 task sequences across conditions and its private reflections are not an ordinary monitor view. Its judge labels have limited human checks. FraudBench releases posts, not a usable interaction graph. Moltbook-injection is keyword-selected and may contain human-controlled accounts; neither successful propagation nor a valid prevalence figure follows. Its quoted percentage and raw denominator are inconsistent, so this bank repeats neither percentage. Stego v3.2 itself warns of lexical separability and partially post-hoc labels, and v3.1 is invalid. Agent-IPI and Instrumental Choices have unspecified reuse terms; TRAIL has gating and redistribution conditions despite its license tag. AgentLogs is valuable activity evidence from one platform, not verified ownership or malicious-coordination labels.

Validation for the update checks JSON shape, unique stable IDs, candidate-to-source and brief-path resolution, and directional agreement between hypotheses, tests, and falsifiers. It does not certify scientific novelty, dataset correctness, completed survey gates, or readiness to launch the studies.
