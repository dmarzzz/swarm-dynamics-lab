# Idea half-life: analysis plan, 2026-10-04

Status: exploratory observational analysis, human-directed (Shadow, hackathon Wave 3, project A of
BRIEF-2026-10-03). Plan written after schema inspection and a unit-definition probe (counts of
repeated lines, no adoption timing computed), before any adoption curve, rate or half-life was
computed. Agent: shadow/sol-halflife. No model calls, no paid APIs. Task: [wild-halflife](../../../../tasks/wild-halflife.md).
Not a gated hypothesis test; no claim here enters `hypotheses/`.

## Question

When a text unit (a URL, a line) first appears in a swarm, how fast do *other identities* start
writing it, and does the rate of new adopters grow with the number of identities that already
wrote it? Compare collusion.wiki (ephemeral OpenAI eval agents, about one hour each, no memory)
with this repository's own commit history (persistent research agents with a shared protocol).

Prior work this extends rather than repeats: de Marzo, Alboré, Garcia, arXiv 2609.09150
([de-marzo-2026-copying](../../../../library/papers/de-marzo-2026-copying.md)) show that wiki agents
choose pages, names and wording roughly in proportion to their visible share. They do not report
adoption timing, half-lives, or a second swarm. kmad's forensics
([gh-kmad-agent-swarm-forensics](../../../../library/code/gh-kmad-agent-swarm-forensics.md)) reports
one protocol's 3 introducers / 41 inheritors. Our addition: time-domain adoption curves, an
exposure-dependence slope, and the same instrument applied to a second, very different swarm.

## Data

- collusion.wiki `revisions.jsonl.gz` (14,591 revisions, 2026-05-24 to 2026-07-02), local path
  passed with `--data`. Inserted text = lines inside `insert`/`replace` hunks of each revision
  (page creations are all-insert). Unchanged retained text is never counted as adoption.
  Identity A = nonempty `label` (claimed handle); identity B = `ip16` (/16 block, coarse, many
  agents can share one; a label can span blocks). Empty labels are excluded from identity A
  analyses and counted. Clock = `time`.
- swarm-lab git history, non-merge commits on origin/main frozen at
  66fa0aa6 (2026-10-04). Added lines (`+`) per commit, excluding generated files
  (STATUS.md, library/INDEX.md, library/references.bib), `templates/**`, commits whose subject
  starts `[bot]` or whose author is the CI bot, and commits with no bracketed agent id (counted).
  Identity A = bracketed agent id (`researcher/agent`); identity B = researcher. Clock = author time.

## Units (fixed now)

- Primary: URL units. Regex `https?://` up to whitespace or `]|"'<>)`, trailing `.,;:` stripped,
  lowercased entirely (percent-encoding case varies across copies).
- Secondary: line units. NFKC, lowercase, whitespace collapsed, leading markup `*-#=>|` and
  surrounding spaces stripped; keep if >= 25 characters. Excluded: the wiki's default new-page
  text ("beschreibe hier die neue seite.") and, for git, any line present in any version of
  `templates/**`. Line units in git include YAML frontmatter lines; reported as-is with that caveat.
- Sensitivity: URL host units (technique/source level).

A unit's *adopters* are distinct identities that insert it; the first dated insertion defines the
origin (ties: all identities at the earliest time count as originators, j starts at their count).
Repeat insertions by an identity already counted are ignored.

## Measures (fixed now)

1. Reach: fraction of units ever written by >= 2, >= 5 identities. Units with >= 2 adopters only
   are "adopted".
2. Time to second identity, Kaplan-Meier with right censoring at the end of each corpus, on
   two clocks: wall time and activity time (count of in-scope revisions / commits elapsed swarm-wide).
   Reported: KM curve, KM fraction adopted at 1 h / 1 day / end, and the conditional median
   among adopted units ("half-life" in the brief's sense, explicitly conditional).
3. Within-unit half-life: for units reaching >= 5 identities, time from origin until half of the
   eventual adopters have arrived (t50); median over units on both clocks.
4. Exposure dependence (headline): for each unit, the waiting time from the j-th to the (j+1)-th
   distinct identity, j = 1, 2, ..., censored at corpus end. Pooled adoption rate per bin
   r(j) = adoptions / unit-time at risk, bins j = 1, 2, 3-4, 5-9, 10-19, 20+. Slope beta of
   log r(j) on log j (bin midpoints, weighted by events). beta near 1 = arrival rate
   proportional to prior adopters (aggregate frequency-dependent copying); near 0 = constant rate.
   Also within-unit version restricted to units reaching >= 5 identities (j = 1..4 only) to remove
   selection on eventual popularity. Activity clock is primary (removes the swarm's changing
   overall tempo); wall clock reported alongside.
   Wiki only, secondary exposure: number of distinct pages whose latest revision at time t contains
   the unit (visible copies), ignoring deletions; same rate-by-bin analysis.
5. Same measures with identity B.

## Uncertainty

Units are not independent: one revision or commit can introduce many units, and pages/projects
cluster. 95% intervals by cluster bootstrap, 1,000 resamples, seed 20261004, clusters = origin
page (wiki) or origin commit (git). These intervals describe resampling of these corpora only; no
claim generalizes to other swarms. No significance tests.

## Known limits, stated before results

- Text identity is not idea identity: paraphrased ideas are missed, and boilerplate or scripts
  inflate adoption. Same-second multi-label bursts on the wiki look like many adopters and may be
  one operator; identity B partly checks this.
- Labels are claimed handles, not verified agents. Git agent ids are self-reported in subjects.
- The two corpora differ in size, duration (6 weeks vs about 1.5 days) and genre; the activity
  clock helps but does not equalize them. Comparison is descriptive.
- Git author times can be reordered by rebases; ties are kept, not broken by row order.

## Outputs

`halflife.py` (takes `--wiki` and `--repo` paths), `test_halflife.py` (synthetic fixtures:
censoring, ties, repeat writers, rate-by-bin arithmetic), `results/summary.json` (aggregates only,
input hashes), `results/fig-adoption.png`, `FINDING.md`. No raw dataset rows committed; at most
short quoted examples of the most-adopted units.
