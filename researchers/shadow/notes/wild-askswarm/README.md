# AskSwarm

An offline Python package for asking the same descriptive questions of any
`agent_id, time, text[, thread]` table. Three bundled adapters cover collusion.wiki
revision snapshots, SwarmTraces redacted artifacts, and swarm-lab's own git/task activity.

**Important coverage finding from schema inspection:** this SwarmTraces release contains
no actor column and its top-level `time_utc` values are all null. The adapter intentionally
does not invent identities from `parent_id` or extract claimed dates/names from attack text.
Its lexical reuse report is available; temporal adoption and identity metrics are not.
The same questions do not imply equally answerable questions.

## Install and run

Python 3.10+, NumPy (tested Python 3.12.3, NumPy 2.4.3). No model calls, keys, web access,
or source data downloads. Run from this directory, or add it to `PYTHONPATH`.

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 -m askswarm analyze --source wiki --data /path/to/collusion-wiki --out results/wiki --name collusion.wiki
python3 -m askswarm analyze --source swarmtraces --data /path/to/swarmtraces --out results/swarmtraces --name SwarmTraces
python3 -m askswarm analyze --source git --data /path/to/swarm-lab --ref 4959a80b2e48050066630c5d22ea5d1fa1b0beb2 --out results/git --name swarm-lab
python3 -m askswarm compare results/wiki/metrics.json results/swarmtraces/metrics.json results/git/metrics.json --out results/comparison.html
```

Each analysis writes derived `metrics.json` and a self-contained `report.html`. Open the HTML
locally. No raw source text is exported. Source SHA256/file size or frozen git commit, Python
and NumPy versions, and clustering parameters are recorded. Never commit source dataset rows.

Generic tables: `--source table --data events.csv` or `events.jsonl`, gzip supported.
Required keys: `agent_id`, `time`, `text`; optional `thread`, `event_id`, `kind`.
Time is Unix seconds or timezone-qualified ISO-8601. Missing/invalid/naive clocks become null.
Missing actors stay null. Table input must explicitly carry required columns, even if null.
Use stable unique `event_id` for reproducibility when records have tied timestamps.

## Importable API for other lanes

```python
import sys
sys.path.insert(0, 'researchers/shadow/notes/wild-askswarm')
from askswarm import Event, wiki, swarmtraces, git_log, task_events, analyze, gini

# All adapters yield Event dataclasses without eagerly loading the corpus.
for event in wiki('/local/data/collusion-wiki'):
    # agent_id: str|None; time: float|None (Unix UTC seconds); text: str;
    # thread: str|None; event_id: str; kind: str; metadata: dict
    pass

# Optional network-block proxy. Do not call an IP block an agent.
block_rows = wiki('/local/data/collusion-wiki', identity_field='ip16')
report = analyze(block_rows, name='wiki /16 proxy', threshold=.7, window=100)
commits = git_log('/path/to/repo', ref='4959a80b2e48050066630c5d22ea5d1fa1b0beb2')
claims_and_done = task_events('/path/to/repo', ref='HEAD')
```

Other lanes may import this package; its owner is shadow/sol-askswarm. Do not edit shared code
from another lane. Write your own analysis under your lane directory.

## Metric definitions

- **Lexical clusters:** NFKC/lowercase word trigrams, deterministic 64-permutation MinHash,
  16 LSH bands of 4, exact Jaccard verification against fixed representatives at threshold .7.
  LSH proposes candidates and can miss matches (probability about .988 at J=.7 under ideal
  independent permutations). Only representatives are indexed, so no transitive chaining.
  Trigrams are hashed to 32 bits (rare collisions possible). Long texts sample at most 512
  evenly spaced trigrams. Exact normalized duplicates always match. Under six words only
  exact duplicates cluster. This is lexical reuse, not semantic idea discovery.
- **First movers:** earliest observed dated identities in a cluster, retaining ties. Unknown
  clocks do not win. These are not inventors. Global identity count includes undated actors;
  temporal metrics include only dated actors. Unknown-identity texts can cluster but not adopt.
- **Adopters/time to k:** unique identities, first identity included, elapsed seconds from first
  dated identity. Not reaching k is null and counted as censored. The hourly/rank adoption
  table is a derived curve of first identity appearances, not repeated records.
- **Influence proxy:** at a new identity's first dated appearance in a cluster, give total
  credit 1 split across distinct prior identities seen in that cluster within 100 globally
  dated-record steps. Strictly earlier clocks only. Timestamp ties share the first step index
  of that timestamp, so row-id tiebreaks cannot manufacture credit. No eligible prior actor
  means no credit. Report raw credit and credit per participation record, not a causal ranking.
- **Participation Gini:** finite-population Gini over nonmissing observed identity counts,
  including one-record identities and excluding missing actors. No finite-sample correction.
- **Identity span:** last minus first observed clock, in seconds. Singletons have zero span.
  This is not lifetime or survival; both ends are observation-window censored.
- **Dissent/revert:** separate unvalidated English marker regexes. Fractions use all input
  records, including unknown actors/clocks. A quoted claim can trigger a marker; absence is
  not agreement. Never use this as a classifier without source-specific validation.
- **Task events:** `task: claim|done|release|touch` subjects with explicit researcher/agent
  prefixes, a subset of non-merge git commits. Not added again to participation counts.
  Bulk/nonstandard task edits are not inferred. Bot commits remain in record counts but
  not identity counts; unprefixed and legacy single-component IDs are missing, not merged.

## Limits and research status

Human-directed exploratory build, not a gated hypothesis test. See [PLAN.md](PLAN.md).
Full snapshots retain earlier authors' words; labels may be shared or spoofed. SwarmTraces
contains representations of payloads/responses, not comparable agent actions. Git commit
subjects contain administrative templates, not the research itself. Thresholds and observation
windows differ in meaning between corpora; do not rank swarms by these metrics as if matched.
Full observed-corpus descriptive numbers have no IID confidence interval. Underlying population,
selection, clustering and identity uncertainty are not captured by a naive row bootstrap.

No new claim of wiki copying relative to arXiv 2609.09150 or village persuasion/cascade work.
The tool and explicit cross-corpus answerability map are the contribution.
