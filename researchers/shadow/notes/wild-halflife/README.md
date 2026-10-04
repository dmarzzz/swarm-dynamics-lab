# Idea adoption timing: saved-data cross-swarm analysis

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by shadow/sol-halflife; source `48bc8a76` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — In these frozen corpora, conditional URL reuse delays and pooled adoption-rate slopes differ; a causal copying mechanism and semantic idea half-life are not identified. Basis: Two dependent observational corpora, unauthenticated identities, exact artifacts, unmatched time windows and unverified censoring assumptions. Origin-page/commit bootstrap intervals and same-author arithmetic checks do not establish exposure or causal influence. Initial review/preflight documentation gaps are explicitly retained.
- **sample_size_summary:** Observed: 2 dependent source corpora; 14,591 wiki revisions and 1,922 in-scope git commits, 3,102 labels and 163 git agent ids. Baseline has 12 artifact/identity summaries, 1,000 cluster resamples; no interventions or model calls.
<!-- experiment-evidence:end -->

Start with [FINDING.md](FINDING.md). Owner: shadow/sol-halflife. This is a human-directed exploratory observational instrument, not a controlled copying experiment or an accepted hypothesis. There are zero model/provider calls and zero spend.

## Reproduce

Python 3.12, NumPy and Matplotlib; [requirements.txt](requirements.txt). Source data are local external inputs and are not redistributed. Install dependencies into your own virtual environment, not a production runtime.

From the repository root, with the virtual environment's Python on PATH:

```sh
python researchers/shadow/notes/wild-halflife/test_halflife.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 python \
  researchers/shadow/notes/wild-halflife/halflife.py \
  --data /path/to/collusion-wiki --repo . --rev 66fa0aa6174003dbb4286ffc63d61dda791e903e \
  --out /tmp/halflife-reproduction --boot 1000
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 python \
  researchers/shadow/notes/wild-halflife/halflife.py \
  --data /path/to/collusion-wiki --repo . --rev 66fa0aa6174003dbb4286ffc63d61dda791e903e \
  --out /tmp/halflife-reproduction --boot 1000 --posthoc
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 python \
  researchers/shadow/notes/wild-halflife/supplement.py \
  --data /path/to/collusion-wiki --results /tmp/halflife-reproduction --boot 1000
python researchers/shadow/notes/wild-halflife/render.py --results /tmp/halflife-reproduction
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 python \
  researchers/shadow/notes/wild-halflife/verify_results.py \
  --data /path/to/collusion-wiki --repo . --results /tmp/halflife-reproduction
```

`--wiki` is retained as an alias of `--data`. `supplement.py` reuses the read-only AskSwarm JSONL reader from the adjacent `wild-askswarm/askswarm/` package, now on main. The primary analysis deliberately does not reuse AskSwarm snapshot text clustering: it measures **inserted** units only. Do not equate our unit denominators or git cutoff with AskSwarm's.

Current baseline aggregates were calculated under Python 3.12.3 / NumPy 2.4.3. Supplemental numeric outputs use the same versions; the final figure was rendered under NumPy 2.5.3 / Matplotlib 3.11.2 using an existing analysis virtual environment. Installing Matplotlib is necessary before plotting. Minor floating-point/bootstrap quantile differences across versions are possible. Top-example ties now sort lexically; this display-only stabilization does not change metrics.

## Evidence inventory

- [PLAN.md](PLAN.md): original definitions committed before outcomes at 2cb859a5; retained unchanged.
- [summary.json](results/summary.json): baseline, 12 corpus × identity × unit analyses, full frozen git SHA and source SHA256. All initial outputs retained in draft commit 48bc8a76. Later JSON repair changes undefined NaN scalars to null, not numerical findings.
- [posthoc.json](results/posthoc.json): first sensitivity, excludes the wiki English default and templates at any directory depth, identity A only. Not preregistered.
- [supplement.json](results/supplement.json): visible-pages uncertainty, whole-June-18 exclusion, schema key-count census. Post-hoc supplement with prospective execution assessment, not a new confirmatory cohort.
- [verification.json](results/verification.json): 12/12 reference checks of reach and conditional medians. Same author and shared loaders; not independent source/extractor validation or causal identification.
- [fig-adoption.png](results/fig-adoption.png): one 2,635 × 714-pixel figure, derived aggregates only. Static final-frame fallback for a frozen-data analysis, no live-model replay claimed.
- [SETUP.md](SETUP.md), [supplement-pre.md](reviews/supplement-pre.md), [supplement-post.md](reviews/supplement-post.md): admission and scientific-closeout limitations, including original missing review/preflight documentation.

## Interpretation and definitions

Identity A: nonempty wiki label / bracketed git `researcher/agent` id. Identity B: wiki /16 block / git researcher. Blank labels are excluded only from A. These are proxies, not authenticated agents; B is not a pure merge of A, and three git researchers cannot reach five-identity endpoints.

URL units lowercase the entire URL and strip selected delimiters. This can merge case-sensitive paths; query variants remain separate. Normalized lines have at least 25 characters. Host units are exact URL authority strings, not semantic topics. Repeated insertions by an already-counted identity are ignored. All earliest-time ties count as originators, and tie units have zero time to second identity.

Activity clock is the number of in-scope records strictly before an event, with censoring at corpus record count. All original wiki revisions, including unlabeled ones, advance the clock. Git uses author time, not causal/topological commit order. Late units receive shorter observation windows. KM assumes noninformative censoring, which task lifecycles do not guarantee.

Pooled adoption rate is events divided by unit-time spent at each prior-identity count. The beta fit uses fixed bin midpoints 1, 2, 3.5, 7, 14.5, 30, with the last being a proxy for an open bin. It is neither a fitted per-view probability nor a causal reinforcement coefficient. Popular artifacts and tasks can differ in exposure and baseline arrival rate. Restricting to eventual ≥5-identity units does not remove selection; the original plan's phrase is corrected in the report, not rewritten.

“Conditional median to second identity” includes only units that were observed adopted. “t50” is time to half of final observed reach for units with at least five identities. Neither estimates semantic decay or an unconditional population adoption half-life. There is no basis to infer a half-life from visibility-bin pooled rates without an additional hazard model.

Visible copies count pages whose latest observed revision contains a URL. Revision removals update that state; moderator deletion events and actual read/view logs are not used. Secondary arrivals are attributed to state immediately before the timestamp; co-timed originators are omitted. The exact raw snapshot remains frozen for bootstrap, so intervals do not encompass exposure-reconstruction uncertainty.

The nearest source paper filters to task-engaged handles and reconstructs page/feed candidate exposure. Our broader all-revision census does neither. Excluding the June 18 UTC day is only a coarse post-hoc sensitivity: it also drops legitimate activity that day, while retaining other non-task activity. No mechanism or direct paper replication claim is made.

## Closest prior art checked

Opened the [arXiv HTML](https://arxiv.org/html/2609.09150) abstract/introduction and early results on 2026-10-04 and read the existing library entry [[de-marzo-2026-copying]]. It already establishes the relevant wiki-copying question and specifically flags the non-task June 18 poster burst. Read [[gh-kmad-agent-swarm-forensics]], which records protocol inheritance and its secondary-analysis limits. The novelty claim is narrow: cross-corpus adoption timing and definition-sensitive rates, not discovery of copying.

## Completion and publication

The task is `tasks/wild-halflife.md`. Hub publication is verified `done`, run `wild-halflife/retrospective-66fa0aa6-v1`; [receipt](results/hub-receipt.json). This is retrospective display of derived outputs only, not historical plan registration or scientific gate approval. The evidence assessment is owner-authored and explicitly exploratory.

The final figure is also [Flight Deck artifact wild-halflife-adoption v1](../../../../artifacts/wild-halflife-adoption/wild-halflife-adoption-v1.png), with generated manifest, lock entry and attestation. `file_figure.py` preserves only this new tool-generated provenance and restores unrelated automatic rehash changes; no peer artifact facts are changed. Whole-repo strict Flight Deck validation reports pre-existing absent film versions and the worktree-name/project-id mismatch; our PNG format and hash checks pass. See post-mortem for the exact boundaries.
