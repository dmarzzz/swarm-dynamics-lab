# Review scope and evidence limits

Owner: dmarz/question-atlas. Date: 2026-10-03. Status: human-requested brainstorming before selection.

The human asked: “review everything and start creating a list of questions and related hypotheses and how we could test them,” generating many possibilities across the research areas for later human selection. We interpret this explicit direction as authorization for a broad preselection hunch bank. We preserve the formal survey and hypothesis gates: no files were added under `hypotheses/` or `experiments/`, and no status was promoted. This is not a substitute for a cross-researcher review.

## Update 2: new research since the first bank

The user asked to bring in the research added since the first version. The content comparison runs from the first atlas tree (`7333ef1`, identical atlas content to the original PR merge `ad723697`) through main `a860443d09c80fda1d87ddb9fc322811fb6801dd`. This captures **379 new catalogue records** (197 papers, 143 code repositories, 33 datasets, 3 blogs, 3 talks) and **56 edited records** (49 papers, 5 code repositories, 2 blogs), plus the new `agent-budgets` topic, B1–B5 budget hunches, the completed contagion scan, fork-merge setups report, revised LLM-swarm survey and now-merged simulator survey. The LLM and simulator batches landed during this refresh and were incorporated before candidate review. A final bounded refresh also includes seven Sybil records and Vishesh’s external-evidence/dissent design bundle. The latter is mapped to existing questions rather than treated as a completed survey or expanded into near-duplicate candidates. [The machine-readable inventory](research-delta-v2.json) records every changed library path. Inventory and relevance triage are not full-paper reading.

The [update guide](update-v2.md) maps the changes to candidate IDs. Targeted primary-source checks and exact reading limits are recorded in the lane notes. No inherited read depth is upgraded. All previous 143 IDs remain in place; new IDs are appended. Candidate-content fingerprints distinguish substantive revisions from unchanged cards, separately from refreshed source metadata. Older local selections and notes remain attached to their IDs; changed cards flag them for re-review rather than erasing them.

GitHub PRs and branch tips were checked again. No new open research PR was awaiting incorporation at the snapshot. Vishesh’s atlas/project-connections task was active with no finished output at this cutoff; its planned comments are not counted as evidence or independent approval here. `dashboard-v1` adds presentation and X-thread exploration, inspected as tooling rather than a new experimental finding. The simulator and factory-scan worktrees were inspected read-only. The simulator survey subsequently landed in main and is now a cited input; the factory-scan worktree showed only agent registration at inspection. A formerly listed factory worktree disappeared during the pass; no research was recovered or invented for it. Agentops main `f7953db` now contains the hub/reporting and public live-view plumbing formerly pending; this is operational context, not authorization or evidence of an experiment. No private operational details are copied into the public atlas.

Current gate checks still show: LLM-agent survey mechanically complete, with a new response to all review items and an open re-review task (the existing verdict remains revise); fork-merge incomplete on saturation; Sybil incomplete on search-log coverage and saturation; agent-budgets has an open survey task and no completed survey. The simulator survey meets mechanical floors but deliberately remains in-progress because its paper search is not saturated. The contagion scan task is now **done**, although GitHub issue #74 still appeared open. The old setups report has stale absence and independence claims; the security lane notes explain which statements were not carried forward.

The simulator survey records twelve teammate CPU smoke tests and execution caveats; this update ran none of them. Those measurements do not establish comparable speed across dissimilar workloads. API response replay can support deterministic execution replay without requiring deterministic fresh model generation. Universal absence claims about ownership, merge primitives or run manifests remain unverified and are not adopted as novelty claims.

## What the first “review” meant

This pass mapped the complete topic index and the available workstreams, read the syntheses, briefs and reviews, inspected selected source records and source anchors, and reconciled overlaps. It did **not** fully read every paper in the more-than-2,700-entry catalogue. Broad coverage is not saturated prior-art coverage for each question. Individual source read depths remain the catalogue authors' claims, with the open audit caveat.

The initial main snapshot was `248ca27` in `dmarzzz/swarm-lab`, with 2,725 catalogue entries, three surveys and no formal hypotheses or experiments. Repository metadata and GitHub state were checked during the session; the team continued adding material, so these are snapshot counts rather than live guarantees.

Before integration, main was refreshed through `73ccb3b`. The newly landed `tooling/agent-experiments/` README, integration and validation records, and Shadow's library QA audit were inspected. The toolkit is linked as reusable methods infrastructure; its scripted demonstrations are not experiments run by this pass. Candidate source metadata was regenerated after incorporating the catalogue QA changes. This refresh is not a claim to have deeply reviewed every newly arriving paper.

## Repositories and parallel work inspected

- `dmarzzz/swarm-lab`: topic vocabulary, current status, tasks, all current syntheses, the three surveys and the LLM survey's revise review; collaborator briefs, background digest, external-influence note and selected library entries across all topics. The lane scope records below specify source checks.
- GitHub: all returned remote branches and PR states in `swarm-lab` and `swarm-labs-agentops`, plus open research issues. Fork-merge, Sybil, swarm-detection, pipeline and collector branches had no unmerged branch commits at inspection. The prior preflight PR was squash merged, explaining its surviving non-ancestor branch history. `dashboard-v1` retained presentation and export work; its data contract and research-path implementation were read, without modifying that branch.
- `/Users/halcyon/swarm-lab-lanes` is a set of worktrees, not a third independent repository. Its `sim-envs` worktree contained substantial uncommitted research: `surveys/sim-environments.md`, candidate records and smoke-test scripts. The survey was read and its implementation-level lessons inform SIM-01–04. The draft was not copied, merged, certified or used as evidence of novelty. Pending source records are not silently treated as existing main citations.
- `swarm-labs-agentops`: README, GitHub PR/branch state, local change inventory and blueprint model. Its local hub/reporting work is in progress. No server, secret, access, infrastructure or generated-owner file was changed. The blueprint is not evidence of available experimental capacity or approved spending.

The simulator draft's absolute “none exists” claims, deterministic-LLM claim and cross-workload speed comparisons were treated as leads requiring narrower checking. Its teammate-run smoke tests are not new runs by this pass.

## Source and editorial work

The three research lanes reviewed complementary material:

- [Physical systems](physical-scope.md): motion, biological decisions, active matter, robots, synchronization and crowds; includes explicit source-access limits and NCA follow-up.
- [Datasets and simulators](datasets-scope.md): the update inventories all 33 new dataset records and states access, label, splitting, licensing and observed-versus-causal limits.
- [Agent societies](society-scope.md): all sixteen original briefs, the external-influence note, digest, LLM survey and its revise review; source framing checked against primary abstracts.
- [Security and detection](security-scope.md): fork/merge objects, identity mechanisms, attention, economic and physical Sybil defenses, operator/model attribution, coordination and detection validity.

The methods lane inspected catalogue summaries and limitations for MARL, optimization, criticality and causal-measurement references, plus simulator code records. Primary pages reopened for framing, at abstract/landing-page depth only:

- [Mean Field MARL](https://arxiv.org/abs/1802.05438), [QMIX](https://arxiv.org/abs/1803.11485), [Deep RL for Swarm Systems](https://jmlr.org/papers/v20/18-476.html).
- [Large-scale optimizer benchmarking](https://arxiv.org/abs/2402.09800), [center-bias audit](https://arxiv.org/abs/2301.01984), [PSO to CBO](https://arxiv.org/abs/2012.05613).
- [Information-theoretic emergence](https://arxiv.org/abs/2004.08220), [subsampling](https://arxiv.org/abs/2209.05548), [PIMMUR](https://arxiv.org/abs/2509.18052).

New predictions are our tentative inferences, not findings from those papers. Source relationships are written beside each candidate. The earlier [preflight synthesis](../../../../3-synthesis/pre-experiment-research.md) provides the provenance/recovery cautions; its CPB/MemLineage/MemTX comparisons are not repeated as new discoveries.

An editorial audit across lanes checked overlap, coverage and directional consistency. It identified and corrected several falsifiers that would have supported the hypothesis instead of contradicting it, and prompted additional NCA and external-influence coverage. Parallel assistants are all working for dmarz in this task; this audit does not count as another researcher's formal approval.

## What is deliberately still unresolved

- No candidate has an established novelty judgment or an approved experimental protocol.
- No full-read upgrade is claimed for inherited records. Primary-anchor checks do not clear the open read-depth audit.
- Feasibility classes describe possible first tests. Exact cost, hardware, licenses, annotation access, API budgets and sample sizes require verification after shortlisting.
- Security, attribution and external-influence sketches are bounded to synthetic or authorized environments. A simulation result would not establish real-world attacker or detector performance.
- A source can be real and correctly catalogued yet fail to support a broad interpretation. The LLM survey review is retained precisely because it documents this distinction.
- No code in this package runs a scientific experiment. The renderer validates and presents the candidate bank only. Human choices remain local until exported and intentionally shared.

## Reproducibility of the review material

The five lane JSON files are the editable source. `revision.json` records the frozen research snapshot and previous candidate fingerprints; `research-delta-v2.json` records the input changes. `python3 src/question-atlas/build.py` validates their fields and references and regenerates the consolidated JSON, Markdown bank and self-contained HTML review. The canvas is an optional local projection of the same bank. Its review notes and the HTML browser's notes are separate stores; JSON export allows human transfer without an external service.

The renderer checks unique IDs/questions, all topic areas, all original brief mappings and every source and brief path. Human editorial review is still required for semantic duplication and whether the comparison answers the question.

## Patchwork addition, 2026-10-04

The user explicitly requested adding the diamond-heist connections to the public research page and repo. [The Patchwork addendum](patchwork-addendum.md) records the five new unreviewed cards, source fingerprints, private/uncommitted source-access limits, and exact reading scope. The canonical bank is rebuilt from its editable lanes; the dashboard is generated from that same bank. This addition does not promote formal hypotheses or rerun the earlier experiments. Existing papers retain their original read-depth metadata.
