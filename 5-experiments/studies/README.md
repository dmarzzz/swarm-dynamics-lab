# Studies

One folder per researcher. A study folder holds that researcher's exploratory studies and working notes:
plans, pre-run assessments, code, results, post-mortems and reviews for one question, or a single Markdown
file for a hunch or a note. Studies here have not all passed the hypothesis gate. The
[evidence registry](../EVIDENCE.md) records the confidence and sample size of each implemented study.

Only the owning researcher's agents write to a researcher's folder (see [AGENTS.md](../../AGENTS.md)).
The matching coordination folder (directives, inbox, agent status files, logs) is
`lab/researchers/<name>/`.

| Folder | Contents |
|---|---|
| [`dmarz/`](dmarz/) | 51 study folders and 10 loose notes. Includes the sybil series (`sybil-*`), the market-split series (`market-split*`), `discussion-dose/`, `compositional-safety/` and `question-atlas/`. |
| [`shadow/`](shadow/) | 17 study folders and 5 loose files. Includes the experiment factory ([`factory/`](shadow/factory/README.md)), `qa/`, `capture-memory/`, `landscape-map/` and the hackathon submission packet (`submission/`). |
| [`vishesh/`](vishesh/) | 49 study folders and 7 loose files. Start with its [README](vishesh/README.md), which indexes the project briefs, readings and studies. |

The shared methods, runbooks and templates these studies follow are in [`../toolkit/`](../toolkit/README.md).
