# Agent protocol

This file is the operating manual for every AI agent working in this repository. Read all of it before your
first commit. If anything here conflicts with a general habit of yours, this file wins. If it conflicts with
a direct instruction from your human, your human wins, and you note the conflict in your log.

## What this repo is

swarm-lab is a shared research workspace for a team working on swarm dynamics at a hackathon. Several humans
each run several agents, and all of those agents read and write here at the same time. The repo holds
everything: the catalogue of prior work, the surveys built from it, hypotheses, experiments, results, and
the task board that coordinates who does what.

The work runs in phases, and the order is enforced:

1. **Scan.** Catalogue existing work: papers, blogs, X threads, code, datasets, talks. Goes in `library/`.
2. **Survey.** Turn the catalogue into a prior-art survey per topic or question. Goes in `surveys/`.
3. **Hypothesise.** Only after a survey passes the prior-art gate. Goes in `hypotheses/`.
4. **Experiment.** Only for a hypothesis another researcher has reviewed. Goes in `experiments/`.
5. **Analyse and ship.** Results, write-ups and synthesis. Goes in `experiments/<id>/` and `synthesis/`.

Phases overlap across topics: one topic can be in experiments while another is still being scanned. Within a
topic, the order holds. The tool `scripts/lab.py` and CI enforce it.

## Quick start

```bash
git clone https://github.com/dmarzzz/swarm-lab && cd swarm-lab
pip install pyyaml                                   # or use `uv run scripts/lab.py ...` everywhere below
python3 scripts/lab.py new agent --agent <researcher>/<agent-name>   # registers you; commit it
python3 scripts/lab.py check                         # must pass before every push
```

Your **agent id** is `<researcher>/<agent-name>`, for example `vishesh/claude-2` or `shadow/codex-1`. The
researcher part must be a folder in `researchers/`. Pick an agent name that is unique among your human's
agents; check `researchers/<you>/agents/` first. Use the same id for your whole session.

## The session loop

Repeat this loop until your human stops you or there is nothing left you can do.

1. **Sync.** `git pull --rebase --autostash`.
2. **Orient.** Read, in order: `researchers/<you>/README.md` (your human's directives override the task board),
   `researchers/<you>/inbox.md`, `STATUS.md`, and the task you hold if any.
3. **Pick work.** Priority order: your human's directives; unprocessed items in your inbox; a task you
   already hold; open tasks with `for:` set to your researcher; open `p0`, then `p1`, then `p2` tasks whose
   `depends_on` are done. Prefer tasks that match your human's focus.
4. **Claim.** `python3 scripts/lab.py claim <task-id> --agent <id>`. This pulls, edits the task, commits and
   pushes atomically. If it says someone else holds the task, pick another. Never edit claim fields by hand.
   Hold one task at a time.
5. **Work.** Follow the rules for the task kind below. Commit small and often (every few library entries).
6. **Heartbeat.** At least once an hour: `python3 scripts/lab.py touch <task-id> --agent <id>`, and update
   `researchers/<you>/agents/<agent-name>.md` (`state`, `task`, `doing`, `updated`). A claim with no heartbeat
   for 3 hours is stale and anyone may take it over.
7. **Finish.** Fill the task's Done-when items, then
   `python3 scripts/lab.py done <task-id> --agent <id> --output <paths>`. If you cannot finish, release it:
   `python3 scripts/lab.py release <task-id> --agent <id> --note "<where you got to>"`.
8. **Log.** Append a few lines to `researchers/<you>/log/<YYYY-MM-DD>-<agent-name>.md`: what you did, what you
   found that surprised you, what you would do next.

When you discover work nobody has listed (a subtopic the scan missed, a review that is needed, a question for
another researcher), create a task: `python3 scripts/lab.py new task <id> --agent <id>`, fill it, commit it.

## Where you may write

Concurrency rule: write only to files you own, plus new files. This is what keeps many agents from
clobbering each other.

| Path | Who writes |
|---|---|
| `researchers/<you>/**` | You and your human. `README.md` directives are your human's; do not edit them. |
| `researchers/<other>/**` | Nobody but that researcher's agents. To reach them, add a line to their `inbox.md` under New, or open a task with `for: <them>`. |
| `library/<type>/<id>.md` | Anyone creates. The adder owns the entry. Others may append under a `## Notes from <agent-id>` heading at the end, never edit the rest. |
| `library/topics.yaml` | Append a topic in its own small commit, only if no existing slug fits. |
| `surveys/<id>.md`, `hypotheses/<id>.md`, `experiments/<id>/` | The owner's agents only. |
| `reviews/<target>--<researcher>.md` | The reviewing agent, which must belong to a different researcher than the target's owner. |
| `tasks/<id>.md` | Claim fields only through `lab.py`. The holder may fill Coverage note and Done-when progress. Anyone may create new tasks. |
| `synthesis/<file>.md` | The agent holding the synthesis task that names it. |
| `STATUS.md`, `library/INDEX.md` | Nobody. CI regenerates them on every push. |
| `AGENTS.md`, `scripts/`, `templates/`, `.github/` | Humans, or agents with explicit human instruction. |

## Git rules

- Commit messages start with your agent id in brackets and the area:
  `[vishesh/claude-2] library: add vicsek-1995-novel, couzin-2002-collective`.
- Before every push: `python3 scripts/lab.py check`. It must report 0 errors. CI runs the same check.
- Push with `git pull --rebase --autostash && git push`. On rejection, repeat. Never `--force`, never rewrite
  pushed history, never `git add -A` blindly (stage the paths you changed).
- If a rebase conflicts on a file you do not own, keep their version and redo your change on top.
- If two agents create the same library id, the second push conflicts. That is the dedup working: keep the
  existing entry and add your notes to it under `## Notes from <agent-id>`.
- Push to `main` directly. No branches or pull requests during the hackathon unless your human asks.
- Large files (datasets, checkpoints, videos) do not go in git. Link them.

## Library entries

One file per source in `library/papers|blogs|threads|code|datasets|talks/`. Create with
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

**relevance** is 1 to 5 for this hackathon: 5 means we would build on it or must cite it, 1 means background.

**Summary in your own words**, at least 25 words, with the specific result and numbers where the source gives
them. Separate what the source measured from what it speculates.

**Topics** come from `library/topics.yaml`. Tag every topic that genuinely applies.

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
closest attempts found. Hunches are welcome before that, in `researchers/<you>/notes/`, clearly labelled as
hunches. They do not go in `hypotheses/`.

A survey is `surveys/<id>.md` (`python3 scripts/lab.py new survey <id> --agent <id>`). It starts as
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
`reviews/<survey-id>--<their-researcher>.md` with `verdict: pass`
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

`python3 scripts/lab.py new experiment <id> --agent <id>` creates `experiments/<id>/README.md`. Code goes in
`experiments/<id>/src/`, small outputs in `experiments/<id>/results/`. Requirements:

- The hypothesis is `accepted` or later.
- `## Protocol` and `## Metrics` are written and committed **before** the first real run. Changing them
  afterwards is allowed only with a dated note explaining why.
- Record seeds, versions, hardware and exact commands. Someone else's agent should be able to rerun it.
- Report every run, including failures. Separate measured results from interpretation.
- When results land, update the hypothesis status (`supported`, `refuted`) and log it.

## Communication between agents

- **To your human:** your log and agent status file. If you are blocked on a decision only they can make,
  set `state: blocked` in your agent file with the question in `doing`, and move on to other work.
- **To another researcher's agents:** a task with `for: <researcher>`, or a line in their `inbox.md`.
- **To everyone:** a task. Tasks are the only broadcast channel; do not create ad hoc shared files.
- Read `STATUS.md` to see who is doing what before starting something big, so two agents do not duplicate a
  scan. If a similar task is claimed, coordinate through a task rather than starting a parallel one.

## Writing style for everything in this repo

- Plain, declarative prose. Specific numbers with their source. No hype, no emoji.
- Mark uncertainty exactly where it is: "measured in the paper", "inferred", "not checked".
- Cite with `[[library-id]]` next to the claim it supports.
- Never put personal information about anyone beyond what they publish themselves.

## Things that get an agent's work reverted

- A library entry for a source the agent did not open, or with invented details.
- A hypothesis written around the gate, for example in `notes/` but presented as a team proposal.
- Edits to another researcher's files, to generated files, or to claim fields by hand.
- Force pushes, history rewrites, or committing large binaries.
- Marking `read_depth: full` or `ran` without doing it.
