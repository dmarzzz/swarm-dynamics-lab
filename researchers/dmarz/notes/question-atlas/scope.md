# Review scope and evidence limits

Owner: dmarz/question-atlas. Date: 2026-10-03. Status: human-requested brainstorming before selection.

The human asked: “review everything and start creating a list of questions and related hypotheses and how we could test them,” generating many possibilities across the research areas for later human selection. We interpret this explicit direction as authorization for a broad preselection hunch bank. We preserve the formal survey and hypothesis gates: no files were added under `hypotheses/` or `experiments/`, and no status was promoted. This is not a substitute for a cross-researcher review.

## What “review” means here

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
- [Agent societies](society-scope.md): all sixteen original briefs, the external-influence note, digest, LLM survey and its revise review; source framing checked against primary abstracts.
- [Security and detection](security-scope.md): fork/merge objects, identity mechanisms, attention, economic and physical Sybil defenses, operator/model attribution, coordination and detection validity.

The methods lane inspected catalogue summaries and limitations for MARL, optimization, criticality and causal-measurement references, plus simulator code records. Primary pages reopened for framing, at abstract/landing-page depth only:

- [Mean Field MARL](https://arxiv.org/abs/1802.05438), [QMIX](https://arxiv.org/abs/1803.11485), [Deep RL for Swarm Systems](https://jmlr.org/papers/v20/18-476.html).
- [Large-scale optimizer benchmarking](https://arxiv.org/abs/2402.09800), [center-bias audit](https://arxiv.org/abs/2301.01984), [PSO to CBO](https://arxiv.org/abs/2012.05613).
- [Information-theoretic emergence](https://arxiv.org/abs/2004.08220), [subsampling](https://arxiv.org/abs/2209.05548), [PIMMUR](https://arxiv.org/abs/2509.18052).

New predictions are our tentative inferences, not findings from those papers. Source relationships are written beside each candidate. The earlier [preflight synthesis](../../../../synthesis/pre-experiment-research.md) provides the provenance/recovery cautions; its CPB/MemLineage/MemTX comparisons are not repeated as new discoveries.

An editorial audit across lanes checked overlap, coverage and directional consistency. It identified and corrected several falsifiers that would have supported the hypothesis instead of contradicting it, and prompted additional NCA and external-influence coverage. Parallel assistants are all working for dmarz in this task; this audit does not count as another researcher's formal approval.

## What is deliberately still unresolved

- No candidate has an established novelty judgment or an approved experimental protocol.
- No full-read upgrade is claimed for inherited records. Primary-anchor checks do not clear the open read-depth audit.
- Feasibility classes describe possible first tests. Exact cost, hardware, licenses, annotation access, API budgets and sample sizes require verification after shortlisting.
- Security, attribution and external-influence sketches are bounded to synthetic or authorized environments. A simulation result would not establish real-world attacker or detector performance.
- A source can be real and correctly catalogued yet fail to support a broad interpretation. The LLM survey review is retained precisely because it documents this distinction.
- No code in this package runs a scientific experiment. The renderer validates and presents the candidate bank only. Human choices remain local until exported and intentionally shared.

## Reproducibility of the review material

The four lane JSON files are the editable source. `python3 src/question-atlas/build.py` validates their fields and references and regenerates the consolidated JSON, Markdown bank and self-contained HTML review. The canvas is an optional local projection of the same bank. Its review notes and the HTML browser's notes are separate stores; JSON export allows human transfer without an external service.

The renderer checks unique IDs/questions, all topic areas, all original brief mappings and every source and brief path. Human editorial review is still required for semantic duplication and whether the comparison answers the question.
