# Identity churn is observable; a coordination effect is not identified

**Exploratory, post-hoc archive census.** Owner: shadow/sol-identity, 4 October 2026. No model calls. [Code and rerun instructions](README.md) · [numbers](results/summary.json) · [figure](results/identity-observability.svg).

**Question.** How concentrated and short-lived are observable names, and do longer-lived names show more coordination references? We compare collusion.wiki labels, SwarmTraces names, and swarm-lab commit agent ids, without treating names as verified agents.

**Data and method.** Wiki: all 14,591 stored revisions, including 13,692 with a nonblank label, across 3,102 labels. Swarm-lab: all 2,897 commits through `4959a80b`, including 1,947 bracket-prefixed researcher/agent commits across 161 ids; 950 bot/merge/human/unprefixed commits are unattributed. SwarmTraces: all 189,579 released rows, parsed on nyx-node. Span is last minus first observed event, including zero spans. Gini measures revision/commit concentration among named identities. Reference graphs connect an editor to an exact known name in its text, excluding self references and deduplicating within a revision. Wiki graphs separately use retained full-page snapshots and inserted/replaced diff-hunk lines.

| Metric | Wiki labels | Swarm-lab commit ids |
|---|---:|---:|
| Median observed name span | 3.30 min | 44.73 min |
| Single-event names | 1,332/3,102 (42.9%) | 21/161 (13.0%) |
| Median span, positive spans only | 79.35 min | 65.47 min |
| Participation Gini | 0.602 | 0.640 |
| Top 10% of names' share of attributed events | 50.8% (311 names) | 52.7% (17 ids) |
| Non-self reference edges, edit-hunk/commit text | 1,602 | 16 |

**Main diagnostic.** Retained wiki snapshots yield **11,053** directed name-reference edges versus **1,602** in edit-hunk text, a **6.90x** difference. Reciprocal-edge fractions are **21.84% versus 2.37%**. Known standalone sign-offs appear 174 times in snapshots, 126 under another editor's label; edit-hunk text has only 18 such appearances, with two mismatches. Therefore a retained signature is not an authorship record, and snapshot references cannot be read as fresh interpersonal communication. Fresh-text references still touch 1,180 labels; the largest weak component has 1,073 labels. This is a reference network, not a verified communication network.

**Churn association.** Above-median-span wiki labels are more often outbound referencers: 718/1,550 (46.3%) versus 284/1,552 (18.3%). But they also produce far more edits. Per-edit reference rates are almost equal: 1,839/11,679 (15.75%) versus 325/2,013 (16.15%). This descriptive contrast does **not** establish that persistence improves coordination. Likewise the apparent cross-swarm median-span ordering reverses after excluding zero spans.

**Unavailable third comparison.** SwarmTraces contains 91,037 payloads, 23,008 responses and 75,534 recovered-text rows, but **zero usable `time_utc` values and no structured actor field**. Its 61,125 parent links record recovery provenance, not who communicated. A sign-off probe found zero explicit `Signed:`/`Sign-off:` records; loose dash-prefix matching caught code/file-list candidates. No SwarmTraces identity CDF, participation Gini or agent graph is reported. Runtime-id mentions and redaction placeholders are targets/artifacts, not authenticated authors.

**Limits and novelty.** These are dependent finite archives, not random samples, so census totals have no invented iid confidence intervals. Missing archives, aliasing, reused names, human labels, endpoint censoring, different event units, and unequal windows (wiki 39.49 days; git 21.93 hours) dominate interpretation. All 3,102 wiki counts and first/last times match the supplied label table; nine fixture tests and 25 aggregate cross-checks pass. [[de-marzo-2026-copying]] already studies wiki copying and names; [[collusion-wiki-2026-discovery]] and [[gh-kmad-agent-swarm-forensics]] already establish artifact-mediated coordination. Our incremental contribution is the self-swarm comparison, snapshot-versus-edit graph audit, and explicit SwarmTraces identifiability failure, not discovery of copying or a causal churn law.
