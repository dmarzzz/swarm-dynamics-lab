# Agent protocol

This file is the operating manual for every AI agent working in this repository. Read all of it before your
first commit. If anything here conflicts with a general habit of yours, this file wins. If it conflicts with
a direct instruction from your human, your human wins, and you note the conflict in your log.

The layout is phase-ordered: the research lives in the numbered folders `1-library/` to `5-experiments/`, and
the coordination machinery (task board, researcher directives, inboxes, agent status files, intake pipeline)
lives under `lab/`. See [Layout](#layout).

If your clone or lane branch still has files at old paths (`library/`, `researchers/<you>/notes/`, `tasks/` and
so on), run `scripts/migrate_all.sh` once after pulling. It moves them, repairs links and paths, and runs the checks.

## What this repo is

Swarm Dynamics Lab is a research lab run by the swarm it studies. Three researchers each run their own AI
agents against this one repo to study how swarms of LLM agents get attacked, captured and repaired, and all
of those agents read and write here at the same time. The repo is the research record and the machinery that
produced it: the catalogue of prior work, the surveys built from it, hypotheses, experiments, results, and
the task board that coordinates who does what.

The work runs in phases, and the order is enforced:

1. **Scan.** Catalogue existing work: papers, blogs, X threads, code, datasets, talks. Goes in `1-library/`.
2. **Survey.** Turn the catalogue into a prior-art survey per topic or question. Goes in `2-surveys/`.
3. **Hypothesise.** Only after a survey passes the prior-art gate. Goes in `4-hypotheses/`.
4. **Experiment.** Only for a hypothesis another researcher has reviewed. Goes in `5-experiments/`.
5. **Analyse and ship.** Results, write-ups and synthesis. Goes in `5-experiments/<id>/` and `3-synthesis/`.

Phases overlap across topics: one topic can be in experiments while another is still being scanned. Within a
topic, the order holds. The tool `scripts/lab.py` and CI enforce it.

## Layout

The numbered folders follow the reading order of the research. The folder numbers are not the step numbers in
the list above: `3-synthesis/` holds cross-cutting documents and sits between surveys and hypotheses.

| Path | What it holds |
|---|---|
| `1-library/` | One entry per source: `papers/`, `blogs/`, `threads/`, `code/`, `datasets/`, `talks/`, plus `topics.yaml`, generated `INDEX.md` and `references.bib`. |
| `2-surveys/` | Prior-art surveys, one file per topic or question. Reviews of surveys, hypotheses and experiments are in `2-surveys/reviews/`. |
| `3-synthesis/` | Cross-cutting documents: landscape, people and labs, question atlas. |
| `4-hypotheses/` | Hypotheses that passed the prior-art gate. |
| `5-experiments/` | Registered experiments (`5-experiments/<id>/`), the evidence registry (`EVIDENCE.md`, `EVIDENCE-METADATA.md`, `evidence-metadata.json`), the shared toolkit (`5-experiments/toolkit/`), and each researcher's studies and working notes (`5-experiments/studies/<name>/`). |
| `artifacts/`, `artifacts.yaml`, `attestations/` | Finished deliverables and their provenance (see Deliverables). |
| `lab/` | Coordination: `lab/tasks/` (task board), `lab/researchers/<name>/` (directives `README.md`, `inbox.md`, `agents/` status files, `log/`), `lab/candidates/` and `lab/PIPELINE.md` (source intake), `lab/templates/`, generated `lab/STATUS.md`. |
| `scripts/`, `src/`, `dashboard/` | The `lab.py` tool and other scripts, shared source, and the dashboard. |
| `agentops/` | A scrubbed template of the fleet and infrastructure setup that ran the agents. |

A researcher's own area is two folders: `lab/researchers/<name>/` and `5-experiments/studies/<name>/`.

## Required setup workflow for new experiments

When a session starts work on a new experimental question, thesis, study or material revision, read
[the experiment setup runbook](5-experiments/toolkit/agent-experiments/EXPERIMENT-SETUP.md) before implementation.
Copy its [setup record](5-experiments/toolkit/agent-experiments/templates/experiment-setup.md) into the owned study
directory as `SETUP.md`, fix the copied links, and maintain evidence for each gate. Include the runbook,
setup record, current gate and exact next action in experiment handoffs so the next session resumes the
same process. This applies to exploratory setup as well as formal experiments; existing prior-art,
hypothesis and different-researcher review gates remain binding.

Write the plan before experimental implementation. Before each attempt, read the previous post-mortem,
complete the pre-run assessment, and satisfy public-plan registration, qualification, source/version,
budget and applicable machine/account checks. Missing or stale required evidence blocks launch.
Account for every assigned outcome, retain failed attempts, and complete the post-mortem and closeout.
The runbook is a required workflow, not a claim that all launchers enforce it automatically. Resource
ownership directives retain their stated scope; this requirement grants no new spending or deployment authority.

## Experiment operations

For Vishesh-owned studies, a request to do an experiment iteration invokes [the standing iteration process](5-experiments/toolkit/agent-experiments/ITERATION.md): review the latest results and native traces, address errors and quality gaps, interpret findings, prepare and test justified changes, push them, and execute the next useful stage when its scope is authorized and current admission passes. Finish its post-mortem and handoff. Already-approved unchanged scopes do not need another owner decision; material successors retain the existing update-approval rule. Report RUN, DECISION NEEDED, HOLD or FINISH / PARK with evidence and a concrete next action. This defines the workflow, not a new central launcher or blanket approval of future scopes. Other researchers' policies are unchanged.

Use `python3 scripts/experiment.py list` and `inspect <study-id>` to locate the current study,
setup record, post-mortem and supported operations. Follow
[the operations guide](5-experiments/toolkit/agent-experiments/OPERATIONS.md) before preparing an attempt.
The registry is navigation, not live admission evidence. Only explicitly implemented adapters
may dispatch through this interface; other studies retain their documented manual workflows.

Keep new designs, configuration iterations, fresh executions, interrupted attempts and saved-data
reports distinct. Preserve the original budget ledger and attempt lineage. Do not retry ambiguous
dispatches automatically, turn replayed responses into fresh samples, or copy the operating
assistant's conversation/memory into experimental-agent context. Reuse unchanged scientific evidence
only within its recorded scope; refresh operational receipts for each admitted attempt.

## Quick start

```bash
git clone https://github.com/dmarzzz/swarm-dynamics-lab && cd swarm-dynamics-lab
pip install pyyaml                                   # or use `uv run scripts/lab.py ...` everywhere below
python3 scripts/lab.py new agent --agent <researcher>/<agent-name>   # registers you; commit it
python3 scripts/lab.py check                         # must pass before every push
python3 scripts/lab.py sync --agent <id> --every 600 >> /tmp/swarm-lab-sync.log 2>&1 &   # push every 10 min
```

Your **agent id** is `<researcher>/<agent-name>`, for example `vishesh/claude-2` or `shadow/codex-1`. The
researcher part must be a folder in `lab/researchers/`. Pick an agent name that is unique among your human's
agents; check `lab/researchers/<you>/agents/` first. Use the same id for your whole session.

## The sync timer

Start this at the beginning of every session, in the background, and leave it running:

```bash
python3 scripts/lab.py sync --agent <id> --every 600 >> /tmp/swarm-lab-sync-<agent-name>.log 2>&1 &
```

Every 10 minutes it commits and pushes every changed file in your clone that passes `lab.py check`, after
re-checking the exact commit on a clean checkout. It also refreshes the claim on any task held by an agent of
your researcher whose status file says `state: working`, so a running timer is your heartbeat. It skips
files that still fail (half-written entries stay local until they are fixed), generated files, protected
files and other researchers' areas, and prints what it skipped. Your own area is both
`lab/researchers/<you>/` and `5-experiments/studies/<you>/`; the same two folders under another researcher's
name are theirs. Your work reaches the team within 10
minutes without anyone pushing broken files.

- Claude Code: launch it with the Bash tool's background option, or as above with `&`. Other harnesses: any
  background process works. If your harness cannot keep a background process alive, run
  `python3 scripts/lab.py sync --agent <id>` after every unit of work and at least every 10 minutes.
- Run one sync timer per clone. Ideally each agent has its own clone; if several agents share one, only one
  of them runs the timer, and it pushes everyone's passing files.
- Before you end a session, run `python3 scripts/lab.py sync --agent <id>` once more by hand and check the
  log for skipped files.
- Task claims still go through `lab.py claim`, which pushes immediately.

## The session loop

Repeat this loop until your human stops you or there is nothing left you can do.

1. **Sync.** `git pull --rebase --autostash`.
2. **Orient.** Read, in order: `lab/researchers/<you>/README.md` (your human's directives override the task
   board), `lab/researchers/<you>/inbox.md`, `lab/STATUS.md`, and the task you hold if any.
3. **Pick work.** Priority order: your human's directives; unprocessed items in your inbox; a task you
   already hold; open tasks with `for:` set to your researcher; open `p0`, then `p1`, then `p2` tasks whose
   `depends_on` are done. Prefer tasks that match your human's focus. For scan work, candidate batches published
   as GitHub issues labelled `batch` are pre-deduplicated sources ready to catalogue: see `lab/PIPELINE.md`.
4. **Claim.** `python3 scripts/lab.py claim <task-id> --agent <id>`. This pulls, edits the task, commits and
   pushes atomically. If it says someone else holds the task, pick another. Never edit claim fields by hand.
   Hold one task at a time.
5. **Work.** Follow the rules for the task kind below. The sync timer pushes your passing files every 10
   minutes; you can also run `lab.py sync --agent <id>` yourself after a batch.
6. **Heartbeat.** Keep `lab/researchers/<you>/agents/<agent-name>.md` current (`state`, `task`, `doing`,
   `updated`). While it says `state: working` and its `updated` is under 3 hours old, the sync timer refreshes your task
   claim. Without a timer, run
   `python3 scripts/lab.py touch <task-id> --agent <id>` at least once an hour. A claim with no heartbeat for
   3 hours is stale and anyone may take it over. Set `state: done` or `idle` when you stop.
7. **Finish.** Fill the task's Done-when items, then
   `python3 scripts/lab.py done <task-id> --agent <id> --output <paths>`. If you cannot finish, release it:
   `python3 scripts/lab.py release <task-id> --agent <id> --note "<where you got to>"`.
8. **Log.** Append a few lines to `lab/researchers/<you>/log/<YYYY-MM-DD>-<agent-name>.md`: what you did, what
   you found that surprised you, what you would do next.

When you discover work nobody has listed (a subtopic the scan missed, a review that is needed, a question for
another researcher), create a task: `python3 scripts/lab.py new task <id> --agent <id>`, fill it, commit it.

## Where you may write

Concurrency rule: write only to files you own, plus new files. This is what keeps many agents from
clobbering each other.

| Path | Who writes |
|---|---|
| `lab/researchers/<you>/**`, `5-experiments/studies/<you>/**` | You and your human. `README.md` directives in `lab/researchers/<you>/` are your human's; do not edit them. |
| `lab/researchers/<other>/**`, `5-experiments/studies/<other>/**` | Nobody but that researcher's agents. To reach them, add a line to their `inbox.md` under New, or open a task with `for: <them>`. |
| `1-library/<type>/<id>.md` | Anyone creates. The adder owns the entry. Others may append under a `## Notes from <agent-id>` heading at the end, and may add a topic slug to `topics:`; never edit the rest. |
| `1-library/topics.yaml` | Append a topic in its own small commit, only if no existing slug fits. |
| `2-surveys/<id>.md`, `4-hypotheses/<id>.md`, `5-experiments/<id>/` | The owner's agents only. |
| `2-surveys/reviews/<target>--<researcher>.md` | The reviewing agent, which must belong to a different researcher than the target's owner. |
| `lab/tasks/<id>.md` | Claim fields only through `lab.py`. The holder may fill Coverage note and Done-when progress. Anyone may create new tasks. |
| `3-synthesis/<file>.md` | The agent holding the synthesis task that names it. |
| `lab/STATUS.md`, `1-library/INDEX.md` | Nobody. CI regenerates them on every push. |
| `artifacts/`, `artifacts.yaml`, `artifacts.lock.json` | Only through `.flightdeck/fd.py add` (see Deliverables). Never by hand. |
| `data/` | Local inputs. Git-ignored; never committed. |
| `AGENTS.md`, `project.yaml`, `scripts/`, `lab/templates/`, `.github/`, `.flightdeck/` | Humans, or agents with explicit human instruction. |

## Git rules

- Commit messages start with your agent id in brackets and the area:
  `[vishesh/claude-2] library: add vicsek-1995-novel, couzin-2002-collective`.
- Before every push: `python3 scripts/lab.py check`. It must report 0 errors. CI runs the same check.
- Push with `git pull --rebase --autostash && git push`. On rejection, repeat. Never `--force`, never rewrite
  pushed history, never `git add -A` blindly (stage the paths you changed).
- If a rebase conflicts on a file you do not own, keep their version and redo your change on top.
- If two agents create the same library id, the second push conflicts. That is the dedup working: keep the
  existing entry and add your notes to it under `## Notes from <agent-id>`.
- **A red `main` is everyone's problem.** If the latest CI check on `main` fails, the agent whose commit broke
  it fixes it first. If it is still red 20 minutes later, any agent may make the smallest fix (finish or
  delete the broken entry) and say so in the commit message and in the owner's inbox.
- Push to `main` directly. No branches or pull requests during the hackathon unless your human asks.
- Large files (datasets, checkpoints, videos) do not go in git. Link them.

## Library entries

One file per source in `1-library/papers|blogs|threads|code|datasets|talks/`. Create with
`python3 scripts/lab.py new <paper|blog|thread|code|dataset|talk> <id> --agent <id>` and fill every TODO.

**Check before you add.** `python3 scripts/lab.py find "<arXiv id | DOI | owner/repo | title word>"`. The
check also rejects duplicates by URL, DOI, arXiv id and repo.

**Ids are deterministic** so duplicates collide. Lowercase, a-z 0-9 and hyphens:

| Type | Id pattern | Example |
|---|---|---|
| paper, talk | `<first-author-surname>-<year>-<first-significant-title-word>` | `vicsek-1995-novel` |
| blog | `<site-or-author>-<year>-<first-significant-title-word>` | `reynolds-1995-boids` |
| thread | `x-<handle>-<status-id>` | `x-someuser-1834567890123456789` |
| code | `gh-<owner>-<repo>` (or `<host>-<owner>-<repo>`) | `gh-projectmesa-mesa` |
| dataset | `data-<short-name>-<year>` | `data-starflag-2008` |

Strip accents (Sörensen becomes `sorensen`). Skip "a", "an", "the", "on", "of" when choosing the title word.
If the id is taken by a different source, append the second significant word.

**No phantom sources.** Every entry must be something you opened in this session. The `url` is the page you
actually loaded. Copy titles, authors, years and handles from the source itself, never from memory. If you
cannot reach a source, do not catalogue it: put it in your researcher's inbox with what you know. A
fabricated or misattributed citation is the worst error an agent can make here, worse than a missing one.

**read_depth is a claim about your work and must be true.** `abstract`: you read the abstract or README only.
`skim`: you read the intro, figures and conclusions. `full`: you read the whole thing including methods.
`ran`: you installed and ran the code or loaded the dataset. Downgrade if unsure.

**cite** (papers) is the full formatted reference: all authors (or the first ten and "et al."), year, title,
venue, volume, issue and pages, copied from the publisher or arXiv page. `1-library/references.bib` is generated
from the entries. After adding papers, run `python3 scripts/lab.py verify --agent <id>`: it checks every arXiv
id and DOI against arXiv and Crossref and flags titles that do not match. CI runs the same check on every
paper added or changed in each push: a red `verify` job means a citation did not resolve or its title does not
match. Fix the metadata from the real source, or delete the entry if the paper does not exist. Set `doi` or
`arxiv` whenever one exists; entries with only a URL cannot be verified.

**relevance** is 1 to 5 for this hackathon: 5 means we would build on it or must cite it, 1 means background.

**Summary in your own words**, at least 25 words, with the specific result and numbers where the source gives
them. Separate what the source measured from what it speculates.

**Topics** come from `1-library/topics.yaml`. Tag every topic that genuinely applies.

**Link generously.** Mention related entries as `[[id]]`. Link papers to their code (`code:` field) and code
to its papers (`papers:` field).

### Source-specific tactics

- **Papers.** Use the APIs, they are faster and do not rate-limit as hard as the websites:
  Semantic Scholar `https://api.semanticscholar.org/graph/v1/paper/search?query=...&fields=title,year,authors,externalIds,citationCount,abstract`,
  its `/paper/<id>/citations` and `/paper/<id>/references` endpoints for citation chasing,
  OpenAlex `https://api.openalex.org/works?search=...`, and arXiv `http://export.arxiv.org/api/query?search_query=...`.
  Read full text from arXiv HTML (`arxiv.org/html/<id>`) or the PDF.
- **Blogs.** Record what evidence the post rests on. Vendor posts and opinion pieces are fine to catalogue,
  labelled as such.
- **X threads.** X blocks most automated reading. Use a browser tool if you have one, then `site:x.com`
  web searches, then thread unrollers. If none work, put the URL in your researcher's inbox and ask them to
  paste the text. Always paste the full thread text into the entry: threads get deleted. Copy the handle from
  the page; never guess one.
- **Code.** Record stars, last commit and licence from the repo page. `ran` means you ran an example and
  wrote the exact commands and outcome in Run notes. Note anything that only runs on x86 or needs a GPU.
- **Datasets.** Record size, format, licence and how to get access. `ran` means you loaded it and put a short
  loader snippet in the entry.

## The prior-art gate

No agent proposes a hypothesis until a survey of the existing work on that question passes the gate. The
point is simple: an idea is only worth testing if we know it has not already been tested, and what the
closest attempts found. Hunches are welcome before that, in `5-experiments/studies/<you>/`, clearly labelled
as hunches. They do not go in `4-hypotheses/`.

A survey is `2-surveys/<id>.md` (`python3 scripts/lab.py new survey <id> --agent <id>`). It starts as
`status: in-progress`. It may be set to `status: complete` only when `python3 scripts/lab.py gate <id>`
reports nothing missing. CI rejects a complete survey that fails the gate. The mechanical floors (tunable in
`scripts/lab.py`, `GATE`):

- At least **20 distinct library entries cited** in the body as `[[id]]`, of which at least **10 papers**,
  **3 code repos** and **2 blogs, threads or talks**, and at least **3 from the last two years**.
- At least **5 cited papers read in full**.
- At least **3 seminal works** listed in `seminal:` and cited, with their **forward citations followed**.
- A structured **search log** of at least **8 rounds** in the frontmatter, covering: a scholarly index
  (Semantic Scholar, Google Scholar, OpenAlex, DBLP or PubMed), preprints (arXiv, bioRxiv or OpenReview),
  code (GitHub, Papers With Code or Hugging Face), social (X, Bluesky, HN, Reddit or LessWrong), the general
  web, and both backward and forward citation chasing.
- **Saturation:** the last 2 search rounds each found at most 15% new items (`new / results`). If your latest
  rounds still turn up new work, the search is not done. Keep going with different wording, neighbouring
  fields' vocabulary, and citation trails.
- All sections filled: Scope, Search log, Landscape, What is known, Open problems and disagreements,
  Code, data and tools, Gaps, Saturation. No TODO left.

The floors are mechanical. The judgement the floors cannot check is your responsibility:

- Search with the vocabulary of every community that might have studied the question. Physicists,
  biologists, roboticists, control theorists and ML researchers name the same phenomenon differently.
- Look for the work that would make the idea unnecessary: a negative result, a prior implementation, a
  benchmark that already answers it.
- Distinguish what a paper measured from what it claims. Note replication status where known.
- Prefer primary sources over reviews for any load-bearing claim.

**Review.** A complete survey becomes `reviewed` when an agent of a different researcher files
`2-surveys/reviews/<survey-id>--<their-researcher>.md` with `verdict: pass`
(`python3 scripts/lab.py new review <survey-id>--<researcher> --agent <id>`). The reviewer spot-checks five
cited sources against their entries, runs three searches of their own, and lists missed work. `revise` sends
it back. When you complete a survey, open a review task with `for:` set to another researcher.

## Hypotheses

`python3 scripts/lab.py new hypothesis <researcher>-<short-slug> --agent <id>`. The check enforces:

- `surveys:` lists one or more surveys, each **complete** (for `draft` and `proposed`) or **reviewed** (for
  `accepted` and beyond). The file cannot exist before that.
- `closest_prior:` lists at least 3 library ids, and `## Novelty` says for each what it did and how this
  differs. If the honest difference is small, say so: it may still be worth a replication.
- `## Prediction` gives the observable outcome if true and if false. `## Kill criteria` says what drops it.
- `accepted` needs a passing review of the hypothesis itself from another researcher.

Statuses: `draft`, `proposed` (ready for review), `accepted`, `testing`, `supported`, `refuted`, `parked`,
`rejected`.

## Experiments

`python3 scripts/lab.py new experiment <id> --agent <id>` creates `5-experiments/<id>/README.md`. Code goes in
`5-experiments/<id>/src/`, small outputs in `5-experiments/<id>/results/`. Requirements:

- The hypothesis is `accepted` or later.
- `## Protocol` and `## Metrics` are written and committed **before** the first real run. Changing them
  afterwards is allowed only with a dated note explaining why.
- Record seeds, versions, hardware and exact commands. Someone else's agent should be able to rerun it.
- Report every run, including failures. Separate measured results from interpretation.
- When results land, update the hypothesis status (`supported`, `refuted`) and log it.

### Experiment evidence metadata

Owner requirement, 2026-10-04: every experiment entry, including exploratory studies under `5-experiments/studies/`, must expose `evidence_confidence` and `sample_size_summary` using [the shared rubric](5-experiments/EVIDENCE-METADATA.md). State the claim, rationale, assessor/date and supporting evidence; distinguish independent sample units from agents/calls and planned counts from observed outcomes. Keep redesigned or model-specific cohorts separate. Update the editable registry and render the fields after analysis; do not modify frozen execution inputs to add reporting metadata. These scores do not replace qualification, uncertainty estimates or research gates.

### Required pre-run and post-run review

For every experiment attempt (including exploratory S0/S1 work), follow
[`5-experiments/toolkit/agent-experiments/RUN-REVIEW.md`](5-experiments/toolkit/agent-experiments/RUN-REVIEW.md).
Commit a pre-run planning/design assessment, then write a post-mortem covering results, experiment
quality, failures, causes and the next run. Read the previous post-mortem before launching again.
Continue diagnosing, repairing and rerunning material execution, design and qualification failures
within the authorized budget until acceptance checks pass; do not stop at publishing a failed pilot.
A failed qualification blocks escalation, not bounded repair diagnostics. Preserve each attempt and
never rerun merely to obtain a favorable scientific result. If access, budget or required input blocks
repair, record that blocker and the exact next step. Valid null or adverse findings are results, not bugs.
Use the linked pre-run and post-mortem templates; existing survey/hypothesis gates remain in force.

### Run visualization mapping

Owner preference recorded 2026-10-04 UTC: use frames to make run performance visible, and prefer
an embedded time-series animation/replay that shows how the run evolves. Before each run, define
its **Visualization mapping** in the pre-run assessment using
[the mapping template](5-experiments/toolkit/agent-experiments/templates/visualization-mapping.md).
Tailor the signals and visual encodings to the experiment (for example convergence, damage and
repair, or consensus); do not force every study into the same graphic. Resolve the mapping for each
run ID/arm/seed, version it with the source/configuration, and retain the time history needed for replay.
An unchanged experiment-level mapping may be referenced by version, with run-specific bindings.

The normal run deliverables include live frames or an appropriate live progress view, a final frame,
and a time-series animation/replay when temporal behavior is meaningful. A static or unsupported view
needs a stated reason and a supported fallback in the mapping. Check visual artifacts against recorded
metrics and report their availability in the post-mortem. Visualization must use measured events,
show missing/failed observations honestly, keep evaluator-only truth out of actor inputs, and never
expose secrets. Follow [RUN-VISUALIZATION.md](5-experiments/toolkit/agent-experiments/RUN-VISUALIZATION.md).
This is a required planning/reporting practice; existing workers do not acquire rendering support
merely because this instruction was added.

## Machine allocation for vishesh's experiments

Owner directive, 2026-10-04 UTC: before every new experiment launch, obtain a fresh, dedicated
machine allocation from Dmarz's machine list in the private fleet repo. This applies
to exploratory/model qualification as well as formal experiments, and to new versions launched as
separate experiments. A new checkout, container or process on another experiment's host does not
satisfy this requirement. Offline local unit tests do not need a fleet allocation.

- Refresh `fleet.yml` and active claims; select an available, authorized host from Dmarz's list and
  create an exclusive claim tied to the experiment before deploying, queueing or starting workers.
  Verify the claim is merged and still exclusive immediately before launch. Do not use `--shared`
  or reuse a host held by a different experiment, including another experiment of vishesh's.
- A fresh allocation may use an idle existing machine; an already-running unrelated machine is not
  spare capacity. The same experiment may keep its allocation across stages and replicate batches.
- If no eligible host is available, resolve a new machine through the private fleet's documented
  provisioning process before launching. Respect server ownership and the authorized infrastructure
  budget; do not run `task up` for somebody else's account or create an untracked host. New machines
  must be added to the fleet, have an expiry, be provisioned and be exclusively claimed before use.
- Record host name, claim ID/expiry, experiment ID, source commit and resource budget in the deployment
  record. Keep IPs, private inventory, credentials and billing tokens out of the public repository and
  transcripts. Preserve any existing shared API cap across machines; copying a per-host budget ledger
  does not create additional spending authorization.
- Extend the claim while jobs or artifact uploads remain active. Stop this experiment's workers,
  verify uploads, then release; the owner handles teardown of temporary machines through agentops.
  Do not interrupt or move existing runs merely to apply this new rule retroactively.

Owner correction, 2026-10-04 UTC: Immune Response needs its own dedicated machine within
Dmarz's existing DigitalOcean account/team and Swarm Lab provisioning setup. Do not borrow an
existing dmarz-named machine or provision through the user's personal/default DigitalOcean account.
The earlier interpretation that researcher ownership authorized a different billing account was wrong.
Before any create/apply, match the credential's actual account/team to an explicit approved identity
from the established Swarm Lab provisioner, verify the infrastructure state/project and exact resource
plan, and fail closed if identity or authorized access is unavailable. A fleet owner field, host name,
working credential or local default context is not account authorization. Record verification privately;
never publish account identifiers or secrets. Do not relaunch the mistaken deployment. The
unused claim on the originally claimed machine and the mistaken deployment remain historical records.

The detailed launch checklist is
[5-experiments/studies/vishesh/experiment-machine-workflow.md](5-experiments/studies/vishesh/experiment-machine-workflow.md).
This directive supersedes older instructions in vishesh's notes to use a shared test server or a
single multi-experiment machine. Other researchers retain their own allocation directives.

## Deliverables

This repo is a Flight Deck project (`project.yaml`). Working material (library entries, surveys, experiment
code and raw results) lives in the folders above. Finished deliverables that leave the team (a figure for the
submission, the final paper or deck, a demo film, a dataset we publish) are filed in `artifacts/` through the
Flight Deck tool, which records provenance:

```bash
python3 .flightdeck/fd.py add <file> --id <artifact-id> --type figure \
  --prompt "<what your human asked for, in their words>" \
  --ingredient 5-experiments/<id>/src/plot.py --ingredient 5-experiments/<id>/results/metrics.csv
python3 .flightdeck/fd.py check --strict .
```

- Give an `--ingredient` for every input and for the script that made the file.
- Files land as `artifacts/<id>/<id>-v<N>.<ext>` and are never overwritten; a new version supersedes the old.
- `project.yaml` `formats:` sets minimums (figures at least 1600 px wide, films h264/aac). Make the file meet
  them; never `--force`. If a request conflicts with a format, ask your human.
- Commit `artifacts.yaml` and `artifacts.lock.json` together with the files they name.
- Claude Code sessions in this repo run hooks from `.claude/settings.json` that block direct writes into
  `artifacts/`. Do not work around them.
- The template's general Flight Deck rule of committing only on a branch does not apply here: during the
  hackathon everyone pushes to `main` as described in Git rules.

## Communication between agents

- **To your human:** your log and agent status file. If you are blocked on a decision only they can make,
  set `state: blocked` in your agent file with the question in `doing`, and move on to other work.
- **To another researcher's agents:** a task with `for: <researcher>`, or a line in their `inbox.md`.
- **To everyone:** a task. Tasks are the only broadcast channel; do not create ad hoc shared files.
- Read `lab/STATUS.md` to see who is doing what before starting something big, so two agents do not duplicate a
  scan. If a similar task is claimed, coordinate through a task rather than starting a parallel one.

## Writing style for everything in this repo

- Plain, declarative prose. Specific numbers with their source. No hype, no emoji.
- Mark uncertainty exactly where it is: "measured in the paper", "inferred", "not checked".
- Cite with `[[library-id]]` next to the claim it supports.
- Never put personal information about anyone beyond what they publish themselves.

## Things that get an agent's work reverted

- A library entry for a source the agent did not open, or with invented details.
- A hypothesis written around the gate, for example in `5-experiments/studies/<you>/` but presented as a team proposal.
- Edits to another researcher's files, to generated files, or to claim fields by hand.
- Force pushes, history rewrites, or committing large binaries.
- Marking `read_depth: full` or `ran` without doing it.

## Single researcher review for Vishesh's experiments

Owner clarification, 2026-10-04 UTC: require one researcher review, not separate design and dossier sign-offs or approval from both Dmarz and Shadow. For How to win agents and influence swarms, Dmarz's published design feedback satisfies the researcher-review requirement by explicit owner direction. Retire the extra Q4 dossier-review gate. Resolve substantive feedback through the owning agent's implementation and validation; do not automatically request a second researcher review for routine repairs. Keep tests, bounded model qualification, public plans, budget and dedicated-account allocation checks. A completed design review must not be misrepresented as an independent code/arithmetic audit or formal hypothesis acceptance. This clarification supersedes duplicate review requirements in this owner's experiment plans.

## Swarm Lab Anthropic credential transfers

Owner directive, 2026-10-04 UTC: use the standing [Swarm Lab credential-transfer policy](5-experiments/toolkit/agent-experiments/SWARM-LAB-CREDENTIALS.md). Only Keychain service `swarm-lab-anthropic`, account `vishesh`, is authorized for this owner’s shared Anthropic experiments. Transfer only that API key through verified encrypted SSH stdin to currently registered, authorized and exclusively claimed Swarm Lab run machines for an admitted, budgeted run; no general/project-other Anthropic fallback, secret bundle or persistent installation. This owner instruction supplies transfer authorization within that scope without a new per-host one-off request. Other launch gates and platform approval enforcement remain in force. Record non-secret provenance and fail closed on ambiguity.

## Researcher review is optional for Vishesh-owned experiments

Owner directive, 2026-10-04 UTC: skip the researcher-review step for Vishesh-owned experiments, including Phantom Coast. No independent researcher, design, dossier or researcher sign-off is required to prepare, qualify or launch these experiments. This supersedes the earlier single-review requirement and conflicting researcher-approval launch gates in study plans and runbooks. The owning agent completes the pre-run assessment, resolves known substantive defects and records limitations; optional feedback must not become a blocking approval step.

Keep prospective plans and public registration, offline checks, bounded native qualification, honest analysis, original spending limits, secure credentials, current exclusive approved-account allocation, and source/runtime verification. Continue prior-art work and record research scope honestly, but do not reintroduce the skipped reviewer as a research-scope sign-off. A waived review is recorded as not required by owner direction, never as passed, independent validation or formal hypothesis acceptance. Preserve historical reviews and immutable plans. Other researchers' policies are unchanged. Update legacy launcher review gates before use rather than supplying a fabricated approval receipt.

## Default experiment spending authorization

Owner update, 2026-10-04 UTC: Vishesh-owned experiments have a **USD10 cumulative default**, or **USD50 cumulative for a promising experiment**. This replaces the former generic USD2 default. These are per-experiment ceilings, not an aggregate portfolio pool or per-run allowances. Do not request another budget approval for the applicable authorized tier.

Operational interpretation of “promising”: the owning session records a short evidence-linked assessment in the existing setup/next-run record explaining the useful unresolved question, what prior results/traces or offline validation support, and the credible next test whose outcome changes a decision. A valid negative result can support this assessment; positive effects, an arbitrary confidence score, visual appeal and sunk effort are not prerequisites or sufficient evidence. Record the assessor/date, evidence, selected tier and bounded next-stage envelope. This is the owning assessment, not a new independent-review or per-tier owner-sign-off gate. If the case for promising is not established, use the default or existing explicit study cap.

An explicit experiment-specific budget remains the baseline instead of being silently reduced or replaced by the default. The documented promising assessment can use this new standing authorization to raise a lower study ceiling to USD50; an already higher explicit authorization is preserved. Later explicit owner restrictions take precedence. Existing smaller **attempt/stage limits remain in force** until a prospective, appropriately authorized amendment; changing the study ceiling does not enlarge a running or frozen packet.

Both tiers cover all stages, qualification, attempts, retries, coordinator/model/tool charges and incremental infrastructure costs in the same study lineage. Carry actual spend and unresolved reservations forward. USD50 means USD50 total, not USD50 added to USD10. Before dispatch, append the selected authorization to the original ledger, reconcile exposure and reserve the exact next-stage maximum; never reset spend, discard unknown charges or create funds by renaming a continuation, opening a new chat, changing machines or starting a new ledger. Any increase beyond the applicable ceiling needs owner authorization.

This policy supplies budget authority only. It does not start experiments, authorize other researchers’ spending, expand scientific scope, or replace public-plan registration, qualification, source/runtime, credential and approved-account/exclusive-allocation checks. Necessary diagnostics retain their standing scoped authority; broader successors still need the applicable scope decision. Generic shared templates remain disabled until their study-specific budget, assessment where needed, ledger and admission evidence are filled. Existing launcher ceilings are not automatically raised by editing this guidance: reconcile and version the budget contract before the next admitted attempt, preserving historical receipts.


## Completion and owner-approved next iterations

Owner directive, 2026-10-04 UTC, for Vishesh-owned studies: finishing an attempt includes its post-mortem. Retain execution, qualification, scientific interpretation, reporting and cost status separately. The supported operations runner automatically writes an evidence-based operational post-mortem and next-session handoff; the owning session must complete the scientific assessment against [the run-quality rubric](5-experiments/toolkit/agent-experiments/RUN-QUALITY.md) before calling the overall attempt reviewed. A generated scaffold, process exit or hub status is insufficient. Failed, interrupted and valid negative attempts all receive a closeout.

The next session reads the latest native attempt records, post-mortem and handoff, checks them against the run-quality rubric, and evaluates suggested changes rather than adopting them blindly. Draft the prospective improvement plan before experimental implementation; complete offline repairs and checks so the owner reviews a concrete update. Specify independent sample units/counts and precision rationale, scenario construction/challenge/realism and holdouts, controls, data collection and missingness, scoring/analysis/stopping, acceptance checks, cumulative cost and machine needs.

Obtain the owner's approval of that updated next-run plan before allocating/provisioning resources or launching its attempts. Existing explicit approval can cover named attempts within its unchanged scope; do not request it twice. A changed scientific design, execution contract or resource envelope needs the corresponding renewed decision. This supersedes earlier permission to start new repair/diagnostic experiments merely because budget remains. Offline analysis, reversible code fixes and preparation continue without another approval. The separate researcher-review waiver remains in force.

After approval, verify or obtain the necessary dedicated approved-account allocation, retain the original spending ledger, publish/register the immutable condition-specific plan, refresh runtime/qualification evidence and launch only the approved scope. Reuse this experiment's still-valid allocation where permitted; no new allowance, machine or stage is created by a post-mortem. A valid negative result may end the study. Do not manufacture another run to obtain a favorable effect. Shared automatic dispatch coverage remains Theseus v2; other native entry points must include the offline finalize hook in their operator closeout until explicitly integrated. Existing historical workers are not silently rewritten.


## Direct execution for the current Vishesh study cycle

Owner direction, 2026-10-04 UTC: the prepared Vishesh-owned scopes may be provisioned, exclusively claimed and launched directly through the existing authorized access in Dmarz's verified DigitalOcean organization; waiting for central-orchestrator acknowledgment is not required for this cycle. Scope: Antsy v8 Q0, Poietic S0-02 bounded renewal, Right Dissenter RD5 Q5/conditional H5, Optimal Size Q-A7, Theseus A1, Immune A4, Influence D5 and Healing C4 qualification/conditional evaluation. This supersedes the central-only waiting condition for these scopes, not other researchers' dispatch policy.

The owning task fences its existing central queue request before direct launch to prevent duplicate dispatch, preserves the original attempt identity and all cumulative costs/reservations, and verifies current approved-account/state/resource plan, exclusive allocation, source/runtime, public registration and qualification. New machines remain inside the approved resource envelope and established provisioner; no personal/default account or independent state copy. A changed scientific design, broader stage or budget increase still requires its corresponding concrete decision. Keep operational identifiers and the owner-decision receipt private; publish only a concise paraphrase.

Post-mortems must inspect native experimental traces under RUN-REVIEW.md. Quorum and Phantom receive trace-grounded design/scenario revision and offline validation before any materially new run is proposed. Preserve valid negative results and distinguish absent evidence from agent failure.


## Improve insufficient test cases during iteration

Owner direction, 2026-10-04 UTC: when an iteration finds test cases insufficient or lacking, improve or try alternative cases as part of that iteration. Diagnose the weakness, prospectively design and implement feasible offline cases, validate labels and strong baselines, and push the concrete revision. Preserve old evidence and keep inspected development cases separate from held-out evaluation. Do not stop at noting a dataset gap when useful case work is possible; do not manufacture difficulty for a favorable result. Existing native-scope approval, admission and cumulative-budget rules remain unchanged. See the iteration process for the full workflow.

## Well-scoped experimental claims

Owner direction, 2026-10-04: define each claim prospectively and match its population, mechanism, comparator, sample unit and precision to the actual design. Distinguish execution, acquisition, continuity and comparative benefit. Apply [CLAIM-SCOPE.md](5-experiments/toolkit/agent-experiments/CLAIM-SCOPE.md); unsupported broad claims require better evidence, not stronger wording.


## Evaluate test-case quality during iteration

Owner direction, 2026-10-04 UTC: define and evaluate what makes the experiment’s cases good using the shared TEST-CASE-QUALITY.md rubric. Improve feasible gaps in task relevance, answerability, labels, isolation, controls, realistic challenge, strong baselines and holdouts before declaring cases ready. Publish evidence-linked acceptance checks and distinguish case readiness for a stated scope from native qualification and run admission. Preserve historical results and all spending/scope boundaries.

## OpenRouter migration for direct Anthropic failures

Owner direction, 2026-10-04 UTC: migrate Vishesh-owned experimental sessions blocked by HTTP429 on the direct Anthropic route to the existing authorized OpenRouter credential and route. This is explicit approval of that provider/credential change for already-approved bounded runs; do not request the same switch again or keep waiting for direct-Anthropic account recovery. Other researchers' credentials and policies are unchanged.

The owning task updates the real endpoint, authentication, request/response handling, model/provider routing and cost calculation, rather than substituting a key into the old client. Preserve the intended model when available; do not silently substitute a scientifically different model or allow provider/model fallback. Record the actual served model/provider and source hashes; qualify the changed route under the applicable existing stage and distinguish it from historical direct-route cohorts.

Use the established local OpenRouter consumer or bounded relay; consume the credential privately without printing or persistently copying it to experiment machines. Keep credential locations and access details in local private context. Publish the prospective routing amendment and verify current public-plan, offline checks, source/runtime, exclusive approved-account allocation and qualification evidence before dispatch. Direct-route recovery is no longer a prerequisite for these migrated scopes.

Carry forward every original ledger, settled cost, unresolved reservation and spending cap, including qualification and failed calls. The switch creates no additional allowance, generic probe, new scientific scope or automatic full rerun. Already-OpenRouter HTTP429 failures need their own diagnosis; do not mislabel them as direct-Anthropic failures. Existing negative results, failed attempts and stopped workers remain intact. If the intended route is unavailable or cannot fit the remaining authorized envelope, complete offline preparation and report the specific remaining decision.

## Standing authorization for necessary post-mortem diagnostics

Owner direction, 2026-10-04 UTC: for Vishesh-owned experiments, when a post-mortem identifies a necessary diagnostic, the owning agent prepares and runs it without requesting another owner approval. Diagnosing and resolving the gap is part of completing the iteration, not merely a recommendation to leave for the owner.

This covers bounded operational and scientific diagnostics needed to understand a failure, distinguish plausible causes, test a repair or establish readiness for the existing research question. Necessary changes to diagnostic prompts, evidence handling, measurement, scenarios or execution contracts do not by themselves create another approval gate. Record the evidence and alternatives, why saved-data analysis is insufficient, the smallest useful contrast, acceptance/stop criteria and a finite call/time/cost envelope before dispatch. Use the standing owner directive as the authority; do not invent a per-packet human sign-off.

Keep the original cumulative budget, settled costs and unresolved reservations. Publish/register the prospective condition-specific plan, complete offline checks and current runtime/credential/approved-account/exclusive-allocation admission, preserve all failed and negative results, and close every diagnostic with operational and scientific findings. Continue with further evidence-led diagnostics when necessary and affordable; stop when the question is resolved, further collection lacks decision value, or an actual admission/resource limit blocks progress. No blind retries, favorable-outcome rerolls, budget resets or fabricated receipts.

Ask only for genuinely new authority: increased spending, a different account or other unauthorized resource/data access, or a broader main experiment/new research question outside the diagnostic purpose. Standing diagnostic authority does not automatically launch the full successor study, schedule unattended work or waive platform enforcement. This supersedes earlier requirements for a separate owner decision on every changed diagnostic plan; other researchers' policies are unchanged.

## Standard diagnosis before experiment scaling

Owner direction, 2026-10-04: for Vishesh-owned experiments, apply [the shared diagnosis step](5-experiments/toolkit/agent-experiments/DIAGNOSIS.md) during iteration before choosing a repair or increasing scale. Connect native evidence to the practical bottleneck, qualify strong simple and coordinated baselines, improve realistic discriminating cases, and distinguish fixed-resource from added-capacity comparisons. Embed findings in the existing review/plan; implement and validate feasible offline improvements. Preserve useful negative results, original evidence and all scope/budget/admission rules. This is a shared workflow improvement, not a new reviewer gate, automatic paid run or claim that existing launchers enforce it. Other researchers retain their policies.
