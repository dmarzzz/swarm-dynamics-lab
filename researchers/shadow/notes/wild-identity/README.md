# Wild identity: names, participation and reference provenance

Owner: `shadow/sol-identity`. Status: complete descriptive analysis, 2026-10-04. Not a hypothesis-gated experiment, intervention, model evaluation, or identification of a churn effect. No new model calls or paid calls.

Start with the one-page [FINDING.md](FINDING.md). The [plan](PLAN.md) was written after schema/sign-off inspection and before the full metric run. All conclusions are post-hoc and exploratory.

## Outputs

- [summary.json](results/summary.json): denominators, spans, Ginis, reference-graph metrics, sign-off diagnostics, missingness, input SHA256 hashes.
- [identity-observability.svg](results/identity-observability.svg): 1800 by 960 vector figure, lifetime CDF and Lorenz curves. SwarmTraces missingness is shown rather than imputed.
- [curves.csv](results/curves.csv): exact empirical step CDF and Lorenz coordinates.
- [identity-aggregates.csv](results/identity-aggregates.csv): per-observable-name counts, spans and reference-event counts; names replaced by deterministic SHA256 digests. These are derived aggregates, not raw events.
- [degree-histograms.csv](results/degree-histograms.csv): reference graph indegree/outdegree distributions, including isolated labels.
- [audit.json](results/audit.json): 25 passing aggregate checks, including independent Gini calculation by Lorenz trapezoids and wiki label-table checks.

## Rerun

Python 3.10+ and the standard library only. Dataset text is processed as inert strings; never execute it or visit payload endpoints. Supply externally downloaded files, which are deliberately not distributed here:

```text
DATA/
  collusion-wiki/revisions.jsonl.gz
  collusion-wiki/labels.jsonl.gz
  swarmtraces/redacted.jsonl.gz
```

Sources: [collusion.wiki report and explorer downloads](https://collusion.wiki/), [SwarmTraces report](https://swarmtraces.org/) and [redacted export](https://swarmtraces.org/data/final/redacted.jsonl.gz). License/republication permissions are not established; only derived aggregates, figures and code are committed. File hashes are in `summary.json`.

From the repository root:

```sh
python3 researchers/shadow/notes/wild-identity/test_analyze.py
nice -n 10 python3 researchers/shadow/notes/wild-identity/analyze.py \
  --data /path/to/DATA --repo /path/to/swarm-lab \
  --commit 4959a80b --out /tmp/wild-identity-results
python3 researchers/shadow/notes/wild-identity/audit.py \
  --data /path/to/DATA --results /tmp/wild-identity-results
```

The stored git census is frozen before this lane's own commits. Uses **committer** dates, not author dates, and counts each commit once across the reachable DAG. It excludes bot/merge/human/unprefixed messages from the agent population without pretending that those 950 commits were 950 agents. Agent recognition requires a message starting `[researcher/agent]`. Alias/case sensitivity is deliberate: wiki has 3,102 exact labels versus 3,095 casefolded names; no authenticated alias map exists.

To process on another machine without transferring a repository, export locally and keep the export private:

```sh
git log 4959a80b --format='%H%x1f%cI%x1f%B%x1e' > /tmp/wild-identity-git.private.txt
nice -n 10 python3 researchers/shadow/notes/wild-identity/analyze.py \
  --data /path/to/DATA --git-log /tmp/wild-identity-git.private.txt \
  --commit 4959a80b --out /tmp/wild-identity-results
```

The recorded run used one `nice 10` CPU process on nyx-node, outside all production paths. Available RAM exceeded 25 GB and load was below 1 at launch. Local tests/audit ran on shad0wbot. Data and private exports were transferred only to the sanctioned compute lane. No dataset text, credentials, IPs, raw git messages, or raw event rows are in these outputs.

## Metric definitions and caveats

**Observed span**, not survival: `max(time)-min(time)` for each nonblank exact label/id. Singletons are zero, but zero-span need not mean singleton: simultaneous events create one additional zero-span identity in each archive. The positive-span sensitivity therefore excludes 1,333 wiki labels and 22 git ids, not just the 1,332 and 21 singletons. Endpoints are censored by archive and commit cutoff; neither a Kaplan-Meier estimator nor a true identity-lifetime claim is justified. Normalized CDFs divide by each full archive's observation window, which does not make the sampling processes equivalent.

**Participation:** Gini uses every attributed event and exact named identity, including potentially human or reused labels. Top-10% share uses `ceil(n/10)` names. Names and repeated events are dependent; no artificial bootstrap of revisions is offered as uncertainty about unseen agents. The archive is the observed census, not a sample of an authenticated agent population.

**Graph:** literal case-sensitive known-label/id references with conservative token boundaries; directed editor -> mentioned name; remove self references; one count per target per event. Wikipedia-like retained snapshots preserve predecessors' prose and signatures. The conservative graph uses only `insert`/`replace` target line ranges in the archive's diff hunks. Whole replacement lines can still contain retained or copied tokens, so even that graph is **not** proof that the editor read or addressed the named agent. Removed text is not added. Cross-page copying is not distinguished from an original message. The method misses unnamed, indirect, encoded, differently cased, and punctuation-boundary references. The two graph edge sets measure different textual artifacts; their difference is not a causal estimate.

Hunk line offsets use `body.split('\n')`, including the empty trailing line. The initial run failed closed on a trailing-newline offset because `splitlines()` drops that line. This was our parser mistake, not a source defect. The fix is covered by a regression test, and no record was silently clipped or discarded. Final run accepts every revision and exactly reproduces all 3,102 nonblank source-label counts and first/last timestamps. Wiki timestamp grades: 14,482 `reqlog`, 103 `rclog`, six `write_date`; these are reconstructed public-record clocks, not process uptime.

**Sign-offs:** standalone dash-prefix names are compared with the known wiki label registry, separately in snapshots and hunk text. They are a deliberately narrow diagnostic, not a universal author extractor. For SwarmTraces, an explicit `Signed:`/`Sign-off:` probe returns zero records; 86 loose dash-prefix matches are merely candidates in code/file-list text, not 86 validated identities. `time_utc` is null throughout. Runtime-id placeholders (169 distinct placeholders across 16,012 rows) and parent links are not author ids or timestamps. An `agent_id` inside code can name a target whose records are being requested, not the code's author. We therefore decline to infer SwarmTraces identity Gini, lifetime or a communication graph.

## Novelty boundary

Checked the local library, especially [[de-marzo-2026-copying]], [[collusion-wiki-2026-discovery]], [[swarmtraces-2026-revealing]], [[gh-kmad-agent-swarm-forensics]] and [[gh-catgirl3d-agent-collusion-wiki-archive]]. Reopened the primary [arXiv abstract](https://arxiv.org/abs/2609.09150) and [SwarmTraces report](https://swarmtraces.org/) on 2026-10-04. The former already models wiki naming/page/text copying; the latter explicitly describes a redacted payload/recovery dataset. Earlier village work already discusses persuasion and cascades. We do not reproduce those discovery claims or report a new copying law. The useful addition is a same-code comparison against our own research swarm, a provenance audit showing why retained name references inflate a fresh-message graph, and a checked negative result on whether the SwarmTraces public export supports identity-level comparison.

## What would identify a coordination effect

Obtain a privacy-preserving, stable actor/run id, an event timestamp with provenance and uncertainty, event type, and lineage/alias links. Record which artifact and message each actor actually read. Compare read/coordination outcomes at matched event exposure, not simply longer-lived names versus shorter-lived names. Preserve old author attribution when later editors retain content. Without those fields, a third graph or a claim that churn improves/worsens coordination would overstate what these archives measure.
