# shadow/sol-identity, 2026-10-04

Human-directed Wave 3 Project B. Claimed `wild-identity`, wrote a schema-informed descriptive plan before metric computation, and froze swarm-lab at pre-lane commit `4959a80b`. No hypotheses, interventions, model calls, paid calls, or external channel messages.

Parsed the complete 189,579-row SwarmTraces export on nyx-node, using one nice-10 process in `/root/swarm-run/identity`. Zero usable structured timestamps and no actor field mean a third identity lifetime/Gini/communication graph is not identifiable. Did not substitute parent links, code variables, runtime redactions or embedded dates for author/time metadata.

Wiki census: 14,591 revisions, 899 unlabeled, 3,102 named labels; git census: 2,897 commits, 950 unattributed, 161 ids. Ginis 0.602 and 0.640, respectively. Wiki median observed label span is 3.30 minutes versus git 44.73 minutes, but positive-span medians reverse the order (79.35 versus 65.47 minutes). Names are not authenticated agents.

Important measurement pitfall: wiki snapshots yield 11,053 directed non-self exact-name references, versus 1,602 in inserted/replaced edit-hunk lines. Reciprocal fractions 21.84% versus 2.37%. Retained sign-offs are often not the current editor's signature. Above-median-span wiki labels reference more often at identity level, but per-edit rates are essentially equal (15.75% versus 16.15%). No churn effect on coordination is established.

Initial parser failed closed because splitlines() excludes a trailing empty line counted by archive hunk offsets. Replaced it with split('\n'), added a regression fixture, and re-ran every record without clipping. All 3,102 wiki counts/first/last times agree with the supplied labels table. Ten fixture tests and 25 aggregate cross-checks pass, including an alternate Lorenz-area Gini computation.

Shipped derived aggregate CSV/JSON, reproducible stdlib CLI, an 1800px SVG figure, a one-page finding, and methods/novelty details. Only derived aggregates and code are public; raw dataset rows, private git exports, payloads and IPs stay out of git. Next: stable privacy-preserving run ids, timestamp provenance, alias links and actual read/coordination outcomes are prerequisites for a churn-effect analysis.
