# Research notes and project guide

This collection documents candidate work on swarm evidence, communication, shared memory, and collective decisions. It includes sixteen project briefs, a twelve-reading synthesis, structured reading notes, an interactive dossier, and an external-influence explainer.

**Status:** working research and pre-survey hunches. No project here is an accepted hypothesis, no toy demonstration is an empirical result, and this documentation does not bypass the lab’s survey and review gates.

## Start here

| Reader’s task | Read | What to expect |
| --- | --- | --- |
| Choose a direction | [Project briefs](project-briefs/README.md) | All sixteen questions, design sketches, measures, controls, scope, and risks. |
| Understand the evidence | [Background readings](background-readings-2026-10-03.md) | Synthesis of twelve readings with disagreements, access limits, and version caveats. |
| Verify a particular claim | [Reading notes](readings/README.md) | Per-source methods, results, limitations, source URLs, and canonical library IDs. |
| Explore the biological framing | [Swarm ecology dossier](swarm-ecology-dossier.html) | Offline interactive overview and sixteen toy demonstrations. |
| Understand the current influence question | [Influence research brief](agent-swarm-influence-research.md) | External attacker, exposure and propagation assumptions, comparisons, and literature. |
| Explain the influence mechanism | [Animated influence guide](swarm-influence-guide.html) | Honest agents updating against false external evidence; all numerical outcomes are illustrative. |

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
