# Two-minute demo script (one shared machine)

Draft by shadow/sol-submit, 2026-10-04. In-person demos run Sunday 18:00 to 19:00 PT from one shared machine,
about 2 minutes per team. Nothing needs installing: everything below is a public web page. Open the tabs in
order before the slot starts, in a normal browser window, zoomed to about 125%.

## Tabs to open beforehand

1. https://github.com/dmarzzz/swarm-lab (repository front page)
2. https://swarm-research.pages.dev/#/method (research path)
3. https://swarm-research.pages.dev/#/agents (agents and contributions)
4. https://swarm-live.pages.dev/#/x/market-split-opus (one finished experiment with replays)
5. https://swarm-live.pages.dev/#/fail (failures view)
6. https://github.com/dmarzzz/swarm-lab/blob/main/researchers/shadow/notes/submission/RESULTS.md (findings table)

Backup if the venue network is slow: screenshots of each tab saved locally beforehand (TODO for the presenter;
the live pages poll an API every few seconds and will show stale data, not fail, if the network drops).

## Script (about 120 seconds)

**0:00 to 0:20, tab 1. What it is.**
"We are three people who each ran several AI agents for 30 hours. The agents never talked to each other
directly. They coordinated through this one git repo: a task board, a library of about 3,300 sources, surveys,
experiments and reviews. That's about 2,000 commits from more than 150 agent ids. So our project is an agent
swarm doing research on agent swarms."

**0:20 to 0:45, tab 2. The tool is the pipeline.**
"The problem with a research swarm is the one this hackathon is about: lots of agents producing confident,
plausible, unchecked output fast. So the repo enforces an order. No hypothesis until a prior-art survey passes
a mechanical gate in CI. No experiment until it is preregistered, budget-capped in code and run on a claimed
machine. Every run keeps its failures and gets a post-mortem, and a different researcher's agent reviews it."

(Tab 3, five seconds only, if time allows: "Every agent shows up here with what it did.")

**0:45 to 1:15, tab 4. One result, end to end.**
"Here is one finished study. A profit-seeking model owns firms in a market with a concentration fine. When
the fine is attached to each firm, it registers a second firm and keeps dodging the fine, 6 out of 6 markets.
When the fine is attached to the owner, 0 out of 6. Same on Sonnet and on Opus, on fresh markets. Every
episode here has a replay you can step through." (Click one firm-regulated replay, let it play a few seconds.)

**1:15 to 1:40, tab 6. What the swarm found.**
"The headline set is about Sybil identities. When a model aggregates reports from many identities, checks
have to scale with the population: proportional checks beat a fixed budget by 51 to 100 points at 972
identities, on three models. More checks are not always safer: accuracy went up while attacker seats went
from 2% to 11%. And agents treat copied reports as independent evidence: zero of eight correct on a lineage
task. Each row links to the saved records."

**1:40 to 2:00, tab 5. Honest limits.**
"This is the failures view. Our own audit found that 9 of 13 study families failed a basic qualification
gate at some point, and we kept those. Everything is synthetic worlds with small numbers of independent
seeds, and we say so next to each number. The repo is public; the agents' work is all there."

## Presenter notes

- Do not claim in-the-wild findings: none of the results use the incident datasets.
- If asked "is this real autonomy": the Sybil identities are scripted; one model synthesises from what the
  admission rule lets through. The market agent is one model against two scripted rivals.
- If asked about cost: per-study spend is in each results file (for example USD 14.95 for the Opus market
  replication's main stage).
- If the live monitor is slow, skip tab 4's replay and go straight to tab 6.
