# lab: coordination

This folder is the machinery that ran the swarm of research agents. Three researchers each ran several
agents against this repository at the same time, and everything those agents needed to divide the work and
stay out of each other's way is here. The research itself is in the numbered folders at the repository root
(`1-library/` to `5-experiments/`).

The rules for all of it are in [AGENTS.md](../AGENTS.md). The servers the agents ran on are described in
`agentops/` at the repository root.

## What is here

| Path | What it is |
|---|---|
| [`tasks/`](tasks/) | The task board. One Markdown file per task, with frontmatter for kind, priority, status, owner and dependencies. |
| [`researchers/<name>/`](researchers/) | One folder per researcher: `README.md` (the human's directives to their agents), `inbox.md` (links and notes for the agents to process), `agents/` (one status file per agent), `log/` (session logs). |
| [`candidates/`](candidates/) | Source intake: deduplicated batches of candidate sources waiting to be catalogued into `1-library/`. |
| [`PIPELINE.md`](PIPELINE.md) | How intake works: collectors, batching, and the GitHub issues that agents claim. |
| [`templates/`](templates/) | The templates `scripts/lab.py new ...` fills for library entries, surveys, hypotheses, experiments, reviews, tasks, agents and researchers. |
| [`STATUS.md`](STATUS.md) | Generated dashboard of library counts, tasks, surveys, hypotheses, experiments and agents. CI regenerates it on every push. Do not edit it. |

## The task board and claiming

A task is a file in `tasks/`. Anyone may create one with `python3 scripts/lab.py new task <id> --agent <id>`.
Tasks are the only broadcast channel between agents.

An agent takes a task with `python3 scripts/lab.py claim <task-id> --agent <researcher>/<agent-name>`. The
command pulls, writes the claim fields, commits and pushes in one step, so two agents cannot both hold the
same task: the second push fails and that agent picks another task. Claim fields are never edited by hand.
An agent holds one task at a time.

A claim needs a heartbeat. The sync timer (`lab.py sync --every 600`) refreshes the claim while the agent's
status file says `state: working`. A claim with no heartbeat for 3 hours is stale and any agent may take it
over. An agent finishes with `lab.py done <task-id> --output <paths>` or hands the task back with
`lab.py release <task-id> --note "..."`.

## Researcher folders

- `README.md`: the human's directives. Agents read it at the start of every session, and it overrides the
  task board. Agents do not edit the directives.
- `inbox.md`: where the human, or another researcher's agent, leaves links and requests. Agents process it
  top to bottom.
- `agents/<agent-name>.md`: one status file per agent with `state`, `task`, `doing` and `updated`. It is
  the agent's heartbeat and the source for the agent table in `STATUS.md`.
- `log/<date>-<agent-name>.md`: what the agent did in a session, what surprised it, and what it would do
  next.

A researcher's studies and working notes are in `5-experiments/studies/<name>/`. Only that researcher's
agents write to either folder.

## Source intake

Finding sources is split from cataloguing them. Collectors (`scripts/collect.py`) pull candidate sources
from X, blogs, feeds and seed lists. The batcher drops anything already in the library, groups the rest by
source and topic, and writes small batches to `candidates/`. `scripts/batches.py publish` opens one GitHub
issue per batch. An agent claims an issue, writes a library entry for each item, and closes the issue.
[PIPELINE.md](PIPELINE.md) has the commands and the 90-minute stale rule for batch claims.
