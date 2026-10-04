# Research notes and project guide

This collection documents candidate work on swarm evidence, communication, shared memory, and collective decisions. It includes sixteen project briefs, a twelve-reading synthesis, structured reading notes, an interactive dossier, and an external-influence explainer.

**Status:** working research and pre-survey hunches. No project here is an accepted hypothesis, no toy demonstration is an empirical result, and this documentation does not bypass the lab’s survey and review gates.

## Start here

[Telephone: where evidence changes in an agent swarm](telephone/README.md) — new exploratory design page, focused background research, prospective three-hop comparison, annotation specification and setup record. [AI Village dataset resource](../../../library/datasets/data-ai-village-2026.md) and [study data guide](telephone/DATA.md). No Telephone outcomes or launch claimed.

[Run completion and improvement cycle](../../../tooling/agent-experiments/RUN-REVIEW.md): automatic operational post-mortem, scientific quality assessment, concrete next-run plan, owner approval, then allocation and launch. [Quality rubric](../../../tooling/agent-experiments/RUN-QUALITY.md).

[PI review decision guide](pi-review-guide-2026-10-04/README.md): dark visual overview of all ten projects, explicit green/yellow/red judgments, concise limitations and three next-step options per project. Full scientific assessments remain available in the same page.

[Experiment operations](../../../tooling/agent-experiments/OPERATIONS.md): one registry and command interface for finding study state, preparing iterations and operating supported adapters. Start with `python3 scripts/experiment.py list`; adapter coverage and current admission remain separate.

[Experiment confidence and sample sizes](../../../experiments/EVIDENCE.md): dated evidence scores and independent sample-size summaries for each study and distinct cohort, with [scoring rules](../../../experiments/EVIDENCE-METADATA.md).

[Principal-investigator project review](pi-review-2026-10-04/README.md): 57 evidence/implementation findings, individual scientific assessments of all ten named projects, 110 scenario/condition assessments, sixteen proposal reviews and agent lifecycle guidance. Dated evidence cutoffs and source availability are explicit. This is an internal PI-style critique, not a formal independent gate review.

[Dmarz review reconciliation and incorporated changes](pi-review-response-dmarz-2026-10-04/README.md): item-by-item dispositions, later evidence, direct study-document amendments and shared methods improvements. The original PI review remains a dated snapshot.

| Reader’s task | Read | What to expect |
| --- | --- | --- |
| Launch an experiment on its own machine | [Dedicated-machine workflow](experiment-machine-workflow.md) | Select from Dmarz's fleet, claim exclusively, verify the deployment and shared budget, and release after artifact upload. |
| Design a run visualization | [Run visualization workflow](../../../tooling/agent-experiments/RUN-VISUALIZATION.md) | Per-run signal-to-view mapping, live frames, dynamic time-series replay, event markers and validation. |
| Inspect immune-response evidence and replay | [Immune-response v3 review and results](immune-response-v3/README.md) | Native failure diagnosis, agent contract, five-scenario robustness suite, time-series replay, and remaining native qualification gate. |
| Choose a direction | [Project briefs](project-briefs/README.md) | All sixteen questions, design sketches, measures, controls, scope, and risks. |
| Connect our briefs to the team question atlas | [Atlas review and project connections](atlas-review/README.md) | Review of all 214 candidates, 40 exploratory extensions, a 16-brief crosswalk, design findings, primary-source checks and importable review JSON. |
| Expand the priority research questions | [Priority references and new comparisons](priority-research-expansion/README.md) | Twenty new sources, twenty selected candidates, fourteen additional comparisons and a full sixteen-brief coverage map. |
| Define an agent swarm | [Agent swarms background brief](agent-swarms-background.md) | Working definition, distinctions from orchestration and subagents, applications and evidence limits. |
| Understand the evidence | [Background readings](background-readings-2026-10-03.md) | Synthesis of twelve readings with disagreements, access limits, and version caveats. |
| Verify a particular claim | [Reading notes](readings/README.md) | Per-source methods, results, limitations, source URLs, and canonical library IDs. |
| Explore the biological framing | [Swarm ecology dossier](swarm-ecology-dossier.html) | Offline interactive overview and sixteen toy demonstrations. |
| Understand the current influence question | [Influence research brief](agent-swarm-influence-research.md) | External attacker, exposure and propagation assumptions, comparisons, and literature. |
| Explain the influence mechanism | [Animated influence guide](swarm-influence-guide.html) | Honest agents updating against false external evidence; all numerical outcomes are illustrative. |
| Read the external-injection experimental design | [SEO-poisoning bundle](seo-poisoning/README.md) | Hunch-level experimental design for an outside content injector steering provider/MCP selection, whether evidence-backed dissent helps, five supporting notes, and eight open questions for dmarz and shadow. |
| Explore containment and recovery | [Swarm immune response](swarm-immune-response/README.md) | Exploratory design separating source isolation, private-memory repair and shared-store repair, with recurrence and correct-minority controls, existing-toolkit integration and primary-source boundaries. |
| Browse research connections | [Dashboard research-area guide](../../../dashboard/RESEARCH-AREAS.md) | Eight cross-cutting focus areas, all sixteen project briefs, contributed designs and explicit formal-hypothesis tagging. |

## Current ten-study update

[Focused research refresh and launch blockers](pi-research-refresh-2026-10-04/README.md) records the next decision for each active study, four new primary sources and two community failure reports. It supersedes older generic approval-wait descriptions where explicitly noted; it is not live machine admission.

## How the artifacts relate

The **library** contains canonical source records. **Reading notes** document how a source was accessed and interpreted. The **digest** compares findings across sources. **Project briefs** turn those observations into possible questions and design sketches. The **HTML files** explain and illustrate; they do not supply experimental evidence.

The project briefs now include the dossier’s previously HTML-only experiment designs, metrics, controls, minimum outputs, optional extensions, and presentation narratives. Original planning ranges are retained as estimates rather than measured costs. October 3 review notes identify questions to settle before promotion.

Markdown is the current research handoff. The dossier retains its October 2 visual snapshot and now carries an October 3 update notice. If the visual recommendation and a newer reading conflict, use the newer documented evidence and revise the recommendation; do not silently treat both as current.

## Current research position

- **Collective Sensing:** check Silo-Bench and Proxifield before claiming novelty. Compare matched evidence and compute, not only network shapes. [[zhang-2026-silo]] [[tambwekar-2026-proxifield]]
- **Quorum:** test provenance and common upstream sources, not just counts of distinct documents. A provenance oracle must be identified as such.
- **Telephone:** claim-level evidence fidelity is a candidate contribution. Confidence calibration itself is already studied; do not claim its absence from the field.
- **External influence:** the attacker controls outside content, not swarm membership. Separate document exposure, claim acceptance, peer propagation, and final decision quality. Profiling must beat a generic intervention to demonstrate incremental value.

These are editorial assessments and unresolved questions, not team rankings or demonstrated results.

## Open the interactive files

GitHub shows HTML as source. Download or clone the repository and open either HTML file in a browser. Each is self-contained and works offline; research links require connectivity. Keep the sibling Markdown files alongside the HTML so the relative links remain useful.

For a local preview, from this directory run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit `http://127.0.0.1:8000/swarm-ecology-dossier.html` or `http://127.0.0.1:8000/swarm-influence-guide.html`. Stop the server with Ctrl-C. The toy demos are hand-authored rules; playback does not call language models.

## Documentation and evidence conventions

- Link to canonical records using `[[library-id]]` and use ordinary relative links for navigation.
- Label published measurements as reported by their source. Independent replication requires an actual run record.
- Preserve model, task, budget, version, table, and uncertainty beside numerical claims.
- Record multiple loaded URLs as YAML lists, never repeated keys. See [reading schema](readings/_SCHEMA.md).
- Separate actual ground truth from agent-visible observations and estimates.
- Record unresolved discrepancies instead of selecting whichever number supports a preferred story.
- Update the digest and project brief when a new reading changes the recommendation. HTML summaries should point to that update.

## Before an experiment is proposed

Identify the closest implementation and what remains unanswered. Resolve data access, model availability, costs, ground truth, and a simple baseline. State a result that would narrow or reject the hunch. Promote it only through the repository’s [research protocol](../../../AGENTS.md), with a qualifying survey and the required review. The separate inbox review request remains outstanding unless completed through that protocol.

## October 3 documentation changes

Expanded all sixteen briefs; added the external-influence animation and revised its threat model; repaired reading-note URL lists; corrected the omitted GPT-4 evaluation and documented the Debate-or-Vote table inconsistency; qualified broad claims about calibration, debate, and fitted scaling laws. These corrections are targeted checks, not certification of every claim in the collection.

- [Biological precedent and visualization review](biology-visual-review/README.md): 301 assessed records, all 16 briefs, source boundaries, eight priorities and an offline searchable view.

- [Hackathon task scenarios](hackathon-scenarios/README.md): one to three ranked tasks for every atlas candidate and related proposal, nineteen bounded task kits, scoring contracts and a three-scenario LLM shortlist.

- [Experimental question expansion](experimental-expansion/README.md): 24 EX comparisons, count reconciliation and the dashboard contribution-bank contract.

- [Skeptical research context and review](skeptical-review/README.md): three reusable context notes, forty specific critiques across all sixteen briefs, primary-source boundaries and decisions to narrow, merge or revise.

- [Heterogeneous Jev / Haiku / Qwen swarms](heterogeneous-swarms/README.md): 30 source-grounded exploratory comparisons, prior-work exclusions, owner-rubric ratings, editorial reviews and five prospective designs.

- [Dmarz market-methods transfer review](dmarz-methods-transfer-2026-10-04/README.md): checked results, transfer cautions and integrated prospective notes for eleven study families.

- [Combined PI next-step decisions](pi-next-decisions-2026-10-04/README.md): dispositions for every owned study, current evidence, accepted/rejected review inputs and explicit stop/park choices.

- [Active ten-study cycle: findings, prepared runs and remaining gates](pi-cycle-2026-10-04/README.md).

- [AI Village dataset and replay proposal](ai-village-replay-2026-10-04/README.md): authenticated metadata access, transfer options for eleven study directions, and a prospective memory/handoff pilot; no model run.
