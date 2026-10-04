# swarm-lab

A shared research workspace for a hackathon team working on swarm dynamics. Each researcher runs their own
AI agents, and all of them coordinate through this repo: a catalogue of prior work, surveys built from it,
hypotheses, experiments, and a task board that agents claim work from.

The rule that shapes everything: **no hypotheses before a proper prior-art survey.** Every hypothesis has to
cite a survey that passed a mechanical quality gate (enough sources across papers, code and informal
writing, full reads, citation chasing, and a search that has stopped turning up new work) and, before
experiments start, a review by another researcher's agent. CI enforces it.

## For your agent

Paste this into your agent (Claude Code, Codex, Cursor or anything that can run git):

```text
You are a research agent for <YOUR-NAME> in the swarm-lab repo (https://github.com/dmarzzz/swarm-lab).
Clone it, or pull if you already have it. Read AGENTS.md in full and follow it exactly.
When setting up a new experiment or revising one, read tooling/agent-experiments/EXPERIMENT-SETUP.md,
create a study SETUP.md from its template, and follow the evidence gates before launch.
Your agent id is <YOUR-NAME>/<tool>-<n>, for example vishesh/claude-1. Register yourself with
`python3 scripts/lab.py new agent --agent <id>`, start the 10-minute sync timer described in AGENTS.md,
read researchers/<YOUR-NAME>/README.md for my directives, then run the session loop in AGENTS.md: claim a task, do it to the quality bar, push, repeat.
```

[AGENTS.md](AGENTS.md) is the whole protocol. Claude Code also picks it up through `CLAUDE.md`.

## For humans

- **Steer your agents** in `researchers/<you>/README.md` under "Directives for my agents". They read it at
  the start of every loop and it overrides the task board.
- **Drop links** into `researchers/<you>/inbox.md`. Your agents catalogue them. This is also how X threads
  get in when agents cannot read X.
- **Watch progress** in [STATUS.md](STATUS.md): library counts by topic, the task board, which agents are
  doing what, and where each survey stands against the gate.
- **Add a researcher:** `python3 scripts/lab.py add-researcher <name>`, commit, and add them as a
  collaborator on GitHub.
- **Add work:** `python3 scripts/lab.py new task <id> --agent <you>/human`, fill it in, push.
- **Source candidates:** collectors (X, Apify, link extraction) feed small claimable batches as GitHub issues labelled
  `batch`; any agent claims one and catalogues it. See [PIPELINE.md](PIPELINE.md).

## Layout

```
AGENTS.md            the protocol every agent follows
HACKATHON.md         dates, theme, judging criteria, constraints
STATUS.md            generated dashboard (do not edit)
library/             one file per source: papers, blogs, threads, code, datasets, talks
  INDEX.md           generated catalogue
  topics.yaml        the topic vocabulary
surveys/             prior-art surveys, one per topic or question (the gate)
reviews/             cross-researcher reviews of surveys, hypotheses and experiments
hypotheses/          only after a survey passes the gate
experiments/<id>/    protocol, code, results, analysis
synthesis/           cross-cutting maps: landscape, people and labs, metrics, open problems
tasks/               the task board, one file per task, claimed through scripts/lab.py
candidates/          batched source candidates (jsonl) and the SEEN ledger; one GitHub issue per batch, see PIPELINE.md
researchers/<name>/  each person's area: directives, inbox, agent status files, logs, notes
templates/           what `lab.py new` copies from
scripts/lab.py       check, gate, claim, done, new, find, index
artifacts/           finished deliverables, filed with provenance through .flightdeck/fd.py add
data/                local inputs, git-ignored
project.yaml         Flight Deck project metadata
```

## Phases

1. **Scan**: catalogue existing work into `library/`. The initial tasks are mostly this.
2. **Survey**: one survey per topic, through the gate, reviewed by another researcher.
3. **Hypothesise**: grounded in reviewed surveys, with the three closest prior works named.
4. **Experiment**: protocol and metrics fixed before the first run.
5. **Analyse and ship**: results, write-ups, the research program that comes next.

## Tooling

Python 3.9+ and PyYAML (`pip install pyyaml`), or `uv run scripts/lab.py ...` which installs it on the fly.

```bash
python3 scripts/lab.py check                 # validate the repo; CI runs this on every push
python3 scripts/lab.py find "vicsek"         # is this source already catalogued?
python3 scripts/lab.py gate <survey-id>      # what a survey still needs
python3 scripts/lab.py claim <task> --agent dmarz/claude-1
```

On every push to `main`, CI runs the check and rebuilds `STATUS.md` and `library/INDEX.md`.

The repo is also a Flight Deck project (`project.yaml`, `artifacts.yaml`, tooling in `.flightdeck/`). Finished
deliverables go into `artifacts/` through `python3 .flightdeck/fd.py add`, and
`python3 .flightdeck/fd.py check --strict .` validates them. The Flight Deck checker needs PyYAML too.

## Shared experiment methods

The [agent experiment toolkit](tooling/agent-experiments/README.md) provides reusable protocols, agent and
context manifests, schemas, statistical guidance and an offline teaching harness for whichever project
passes the lab's research gates. See its [integration guide](tooling/agent-experiments/INTEGRATION.md) for
how to adopt it without changing the survey, review or experiment workflow.

Start every new experiment with the [setup runbook](tooling/agent-experiments/EXPERIMENT-SETUP.md) and
[setup record](tooling/agent-experiments/templates/experiment-setup.md). Carry the current gate and next
action into session handoffs; the runbook supplements the existing research gates.
