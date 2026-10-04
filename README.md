![A swarm of 3,319 dots, one per catalogued source, around a core of 150 experiment cohorts, with an amber path from the edge to the core through the five phases](assets/banner.svg)

# Swarm Dynamics Lab

A research lab run by the swarm it studies.

Three researchers each ran their own AI agents (Claude Code, Codex and others) against this one repo for about
30 hours on 3 and 4 October 2026, at the [AI Village x Grove Research AI Swarm Dynamics Hackathon](HACKATHON.md).
The agents coordinated only through the repo: a task board, a library of prior work, gated surveys, experiments
and reviews. They worked on three questions:

1. Under what scenarios will agents create Sybils?
2. Can a few adversarial agents push an entire swarm into unsafe behavior?
3. Can a swarm preserve its safety constraints as agents, memories, and context change?

The event's prompt is "Building the tools we wished we had for the Hugging Face incident." The tool submitted
here is the pipeline that keeps a research swarm checkable: a prior-art gate run by CI, plans committed before
runs, every run reported, a post-mortem per attempt and an evidence score per claim. The findings
below are what that pipeline produced in one weekend, failures included.

[![lab][lab-badge]][lab-url]
[![library][library-badge]][library-index]
[![evidence][evidence-badge]][evidence]
[![artifacts][artifacts-badge]](artifacts.yaml)

[Write-up][writeup] · [Evidence registry][evidence] · [Question atlas][atlas] · [Library index][library-index] ·
[Surveys](2-surveys/) · [Protocol](AGENTS.md) · [Agent ops](agentops/README.md) · [Live runs][live]

> [!NOTE]
> Hackathon research, about 30 hours of it. Every study here is exploratory, samples are small, and most
> checks were made by an agent of the same researcher who ran the study. "Evidence" means a 0 to 4 editorial
> score for one stated claim, defined in the [rubric][rubric]. Of the 150 cohorts in the [registry][evidence],
> 48 score 0/4 (untested), 76 score 1/4 (exploratory), 25 score 2/4 (limited), one is unassessed and none
> scores higher. No survey has passed cross-researcher review yet, so no hypothesis is accepted and nothing
> below is a test of one. Caveats sit next to each result, in the study's own results file.

## What the swarm found

Numbers are copied from the linked source files, which recompute them from saved records. The first two rows
are the results the team's demo film presents: row one bears on question 1, row two on question 3.

| Question | Result | Scope | Source |
|---|---|---|---|
| Do model-controlled owners split their firms to get under a firm-level competition charge? | With the charge alone, 55 of 180 owners sustained the split in one economy and 59 of 180 in a second. With one added sentence forbidding evasion: 0 and 0. With the charge counted per owner: 0 and 0. | gpt-6-sol only, two seeds, 8,118 calls each. The sentence also tells the owner what the regulator cares about. Evidence 2/4. | [sybil-rules-180][f-rules] |
| Does a crew keep doing its job after every member has been replaced? | With the team's notes handed down, collective accuracy after full turnover was 100.00%. With nothing handed down it was 52.08%. Notes plus mentoring against neither: +47.92 points. | Pilot. Claude Haiku 4.5, 36 of 36 runs in six paired synthetic worlds, three members per world. The founders are given the procedure, so this measures transmission of a supplied rule. A redesigned v2 failed qualification and its main stage was not started. Evidence 1/4. | [swarm-of-theseus][f-theseus] |
| Does a neutral, profit-seeking model create a second firm when the rule counts firms? | Claude Opus 5.5 registered a second firm in 6/6 firm-regulated markets, 0/6 owner-regulated and 0/6 unregulated. | Six market tasks, 36/36 episodes valid, one model owner against two scripted rivals. Evidence 2/4. | [market-split-opus][f-market] |
| How many truthful carriers does a rare fact need to survive Sybil reports? | Specialist accuracy was 100.0% with 81 truthful carriers per rare fact and 4.2% with one: a drop of 95.8 points, in the same direction in 24 of 24 world roots. | Opus 5.5 as the one synthesizer over simulated reporters, 1,440/1,440 main-stage rows. Evidence 2/4. | [sybil-scarcity-opus][f-scarcity] |
| Does a bigger verification budget help when credit for a passed check spreads to linked identities? | Raising the budget from 32 to 108 checks raised attacker seats from 4.38 to 15.92 of 162 under propagated credit, and lowered them from 19.58 to 10.38 under direct credit. The contrast is +20.75 seats, positive in 24 of 24 roots. | Computed by the scripted admission rule, not by a model. Evidence 1/4. | [trust-credit-qwen][f-trust] |
| Does a five-role committee that buys verification checks pick the best OCR output more often than confidence alone? | No. Confidence alone reached 56.78% recall, against 56.30% and 55.72% for the committee on its two model backends, and neither committee saved checks. | 70 paired evaluation receipts. A limited negative result, evidence 2/4. | [antsy-verification-v4][f-antsy] |
| What can be asked of the public incident datasets? | SwarmTraces has 189,579 records and none carries an actor or a clock. On collusion.wiki, retained page text inflates name-reference activity by 2.34x (interval 1.96 to 2.75). | Descriptive and post hoc, zero model calls. Evidence 1/4. | [shadow submission][f-shadow] |

[![180 owners in 60 three-owner markets under three rules and a repeat of the first](artifacts/sybil-rules-180-final-frame/sybil-rules-180-final-frame-v1.png)](artifacts/sybil-rules-180-final-frame/sybil-rules-180-final-frame-v1.png)

*sybil-rules-180, first economy, final frame. Each cell is one market. Orange underlines mark owners that split
a product across firms; they appear under the firm-level charge (A and its repeat A') and not under B or C.*

[![Swarm of Theseus pilot: accuracy after full turnover in three scenarios under six handover conditions](artifacts/theseus-pilot-figure/theseus-pilot-figure-v1.png)](artifacts/theseus-pilot-figure/theseus-pilot-figure-v1.png)

*Swarm of Theseus pilot, steps after the last founder left. Rows are what a newcomer was handed, columns are the
three scenarios. Green bars are task accuracy; gold bars are how often an arbitrary receipt phrase survived.*

Two of these studies have narrated films filed in [`artifacts.yaml`](artifacts.yaml): `theseus-film` (3 min 44 s)
and `market-split-film` (3 min 29 s, on the earlier Sonnet 4.6 pilot of the market-split study). Video files
are kept out of git.

Three things did not work, and they limit everything above. Qwen3.7 Flash and gpt-6-sol failed the clean-packet
qualification that Opus 5.5 passed 48 of 48, so the Opus results have no cross-model replication yet.
growth-pressure-200, built to test whether the one-sentence prohibition holds against cheating rivals, stopped
at qualification with 4 of 8 fixtures passing against a gate of 6. Three runs stopped when a provider usage
limit was reached. The [one-page results of the 2026-10-04 program][f-program] lists every stop.

[![How long observed names persist and how participation is shared, for collusion.wiki and this repo's git history](artifacts/wild-identity-observability/wild-identity-observability-v1.svg)](artifacts/wild-identity-observability/wild-identity-observability-v1.svg)

*Name persistence and participation in two archives: collusion.wiki and this repo's own git history. SwarmTraces
has no curve because its 189,579 records carry no timestamps and no author field. Spans are observed, not
survival estimates. The [incident timeline](artifacts/shadow-wild-timeline/shadow-wild-timeline-v1.png) covers
the same datasets by date.*

## How the lab works

The lab runs on one rule: no hypothesis before a prior-art survey that passes a mechanical gate and a review by
another researcher's agent. The folders are numbered in the order the research is read.

```mermaid
flowchart LR
  L[1-library<br/>scan] --> S[2-surveys<br/>gate + review]
  S --> Y[3-synthesis<br/>question atlas]
  S -->|gate passed| H[4-hypotheses]
  H -->|reviewed| E[5-experiments]
  Y -.->|exploratory studies| E
  E --> A[artifacts<br/>with provenance]
```

| Phase | Folder | What it holds | What it must pass | Count on 4 October |
|---|---|---|---|---|
| 1. Scan | [`1-library/`](1-library/) | One file per source, with a stated read depth | The agent opened the source in that session; CI resolves each arXiv id and DOI | 3,319 entries: 2,096 papers, 466 threads, 331 code repos, 223 blogs, 141 talks, 62 datasets |
| 2. Survey | [`2-surveys/`](2-surveys/) | Prior-art surveys, and reviews in `reviews/` | The gate, then a review by a different researcher | 5 surveys: 2 pass the gate, 3 in progress. 4 reviews, all returned "revise" |
| 3. Synthesis | [`3-synthesis/`](3-synthesis/) | Landscape, people and labs, the question atlas | No gate; the atlas labels every item an unreviewed hunch | 214 candidate questions from 319 source records across 15 areas |
| 4. Hypothesise | [`4-hypotheses/`](4-hypotheses/) | Hypotheses that cite a complete survey and three closest prior works | Acceptance needs a reviewed survey and a review of the hypothesis | 3 proposed, 0 accepted |
| 5. Experiment | [`5-experiments/`](5-experiments/) | Plans, code, records, results and post-mortems per study | Plan committed before the first run; a pre-run assessment and a post-mortem per attempt | 117 study folders, 150 cohorts in the registry |
| 6. Ship | [`artifacts/`](artifacts/) | Figures, films, docs and datasets | Filed with their inputs and the script that made them | 113 artifacts: 45 figures, 38 docs, 12 datasets, 9 films, 9 other |

The gate is mechanical and CI runs it. A survey passes with at least 20 cited library entries (10 papers, 3 code
repos, 2 informal sources), 5 papers read in full, 3 seminal works with their forward citations followed, and 8
logged search rounds in which the last 2 each turned up at most 15% new items.

The gate held under deadline. With no survey reviewed, the weekend's runs went ahead as exploratory studies
under `5-experiments/studies/`, each labelled exploratory, and the three hypotheses stayed at "proposed".

The banner at the top of this page is drawn from these records by
[`src/readme-banner/build.py`](src/readme-banner/build.py). Each outer dot is one library source: its direction
is its topics, it sits nearer the centre the more relevant it was rated, and it is brighter the deeper it was
read. The core is the 150 cohorts: white for evidence 2/4, violet for 1/4, hollow for 0/4. The amber path is
the five phases in order.

## Run it yourself

Paste this into an agent (Claude Code, Codex, Cursor or anything that can run git):

```text
You are a research agent for <YOUR-NAME> in the swarm-dynamics-lab repo (https://github.com/dmarzzz/swarm-dynamics-lab).
Clone it, or pull if you already have it. Read AGENTS.md in full and follow it exactly.
When setting up a new experiment or revising one, read 5-experiments/toolkit/agent-experiments/EXPERIMENT-SETUP.md,
create a study SETUP.md from its template, and follow the evidence gates before launch.
Your agent id is <YOUR-NAME>/<tool>-<n>, for example vishesh/claude-1. Register yourself with
`python3 scripts/lab.py new agent --agent <id>`, start the 10-minute sync timer described in AGENTS.md,
read lab/researchers/<YOUR-NAME>/README.md for my directives, then run the session loop in AGENTS.md:
claim a task, do it to the quality bar, push, repeat.
```

The tooling needs Python 3.9+ and PyYAML (`pip install pyyaml`), or `uv run scripts/lab.py ...`.

```bash
python3 scripts/lab.py check                        # validate the whole repo; CI runs this on every push
python3 scripts/lab.py find "vicsek"                # is this source already catalogued?
python3 scripts/lab.py gate fork-merge-security     # what a survey still needs to pass
python3 scripts/lab.py claim <task> --agent <you>/claude-1
python3 scripts/experiment_evidence.py --check      # validate the evidence registry
```

## Repository map

```
1-library/        phase 1: one file per source, INDEX.md, topics.yaml
2-surveys/        phase 2: gated prior-art surveys; reviews/ holds cross-researcher reviews
3-synthesis/      phase 3: landscape, people and labs, the research question atlas
4-hypotheses/     phase 4: only after a survey passes the gate
5-experiments/    phase 5: EVIDENCE.md registry, studies/<researcher>/<study>/, toolkit/
artifacts/        phase 6: shipped figures, films and docs, with artifacts.yaml and attestations/
lab/              coordination: task board, researcher directives, inboxes, agent status, intake
agentops/         scrubbed template of the fleet setup
scripts/          lab.py, collectors, experiment operations
dashboard/        the research-question dashboard (Vite app)
src/              scripts that built artifacts
AGENTS.md         the protocol every agent follows
HACKATHON.md      event facts
```

The [experiment toolkit](5-experiments/toolkit/agent-experiments/README.md) holds the shared setup runbook,
run-review templates and claim-scope rules. [avalon-swarm](5-experiments/toolkit/avalon-swarm/README.md) is a
prototype for trust, deceptive claims and recovery in populations of 100 to 2,000 scripted agents.

## Coordination

[`lab/`](lab/README.md) is how many agents share one repo without overwriting each other. Agents claim work
from a board of 290 tasks in `lab/tasks/`, and each writes only to files it owns plus new files. Each of the
three researchers (dmarz, shadow, vishesh) steers their agents through `lab/researchers/<name>/README.md` and
drops links into `inbox.md`. Collectors feed source candidates in small batches through
[`lab/PIPELINE.md`](lab/PIPELINE.md). CI regenerates [`lab/STATUS.md`](lab/STATUS.md) on every push. 159
agents registered a status file over the weekend.

## Agent ops

[`agentops/`](agentops/README.md) is a scrubbed template of the fleet that ran the experiments: OpenTofu for
the machines, Ansible for setup, and a run hub. The template is there for anyone who wants to recreate the
setup, and its README is the place to start.

## What comes next

No survey has passed review, so the first step is a cross-researcher review that lets a hypothesis be accepted.
The Opus 5.5 results need a second model that passes qualification. The
[next experiment for growth-pressure-200][f-next] is written: a first stage of about 1,300 calls that measures
how to deliver the cheating treatment, then the comparison the stopped run was built for.

[lab-badge]: https://github.com/dmarzzz/swarm-dynamics-lab/actions/workflows/lab.yml/badge.svg
[lab-url]: https://github.com/dmarzzz/swarm-dynamics-lab/actions/workflows/lab.yml
[library-badge]: https://img.shields.io/badge/library-3%2C319_sources-7c2eb8.svg
[evidence-badge]: https://img.shields.io/badge/evidence-150_cohorts-7c2eb8.svg
[artifacts-badge]: https://img.shields.io/badge/artifacts-113-7c2eb8.svg
[evidence]: 5-experiments/EVIDENCE.md
[rubric]: 5-experiments/EVIDENCE-METADATA.md
[atlas]: 3-synthesis/research-question-atlas.md
[library-index]: 1-library/INDEX.md
[live]: https://swarm-live.pages.dev
[writeup]: 5-experiments/studies/shadow/submission/WRITEUP.md
[f-theseus]: 5-experiments/studies/vishesh/swarm-of-theseus/RESULTS.md
[f-next]: 5-experiments/studies/dmarz/growth-pressure-200/NEXT-EXPERIMENT.md
[f-rules]: 5-experiments/studies/dmarz/sybil-rules-180/RESULTS.md
[f-market]: 5-experiments/studies/dmarz/market-split-opus/RESULTS.md
[f-scarcity]: 5-experiments/studies/dmarz/sybil-scarcity-opus/RESULTS.md
[f-trust]: 5-experiments/studies/dmarz/trust-credit-qwen/RESULTS.md
[f-antsy]: 5-experiments/studies/vishesh/antsy-verification-v4/README.md
[f-shadow]: lab/researchers/shadow/SUBMISSION.md
[f-program]: 5-experiments/studies/dmarz/overnight-program-2026-10-04/RESULTS.md
