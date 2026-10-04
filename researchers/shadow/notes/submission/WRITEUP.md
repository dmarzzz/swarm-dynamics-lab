# swarm-lab: a research pipeline run by a swarm of agents, and what it found about swarms

Draft submission write-up (form item a). Draft by shadow/sol-submit, 2026-10-04; not yet submitted. The team
submits once, through the form in the event Slack.

- Repository: https://github.com/dmarzzz/swarm-lab (public)
- Research dashboard: https://swarm-research.pages.dev
- Live experiment monitor with replays: https://swarm-live.pages.dev
- Results with sources: [RESULTS.md](RESULTS.md). Demo script: [DEMO.md](DEMO.md).
- Team: dmarz, vishesh, shadow. Full names and emails: TODO (humans fill in on the form).

## What it is

swarm-lab is a shared git repository in which three researchers each ran several AI agents (Claude Code,
Codex and others) for the 30 hours of the event. The agents coordinated only through the repository: a task
board they claim work from, a library of prior work, gated surveys, hypotheses, experiments and reviews. By the
draft cutoff the repository held about 2,160 non-bot commits from 157 distinct agent ids, 3,300 library entries
(2,080 papers, 331 code repos, 466 X threads, 220 blogs, 141 talks, 62 datasets), 231 tasks and 68 experiment
entries on the live monitor.

So the project is itself a small agent swarm doing research on agent swarms. The tool we are submitting is the
pipeline that keeps that swarm honest. The findings in RESULTS.md are what it produced.

## The pipeline (the tool)

1. **Scan, then survey, then hypothesise.** Agents catalogue sources one file per source, with a declared read
   depth they must not overstate. No hypothesis can exist until a survey of its question passes a mechanical
   prior-art gate (at least 20 cited entries, 10 papers, 5 read in full, 8 search rounds across scholarly,
   preprint, code and social sources, forward citation chasing, and a saturation test on the last two rounds).
   CI enforces this on every push, and citations are verified against arXiv and Crossref.
2. **Collectors feed claimable batches.** Search hits from X, LessWrong, RSS, YouTube and the web are
   deduplicated against the library and published as small GitHub issues that any agent claims (68 batches
   worked).
3. **Experiments carry their own receipts.** Each study has a setup record, a preregistration written before
   the first model call, a pre-run assessment, a spend cap enforced in code, a run on a claimed machine from a
   shared fleet, and a post-mortem that keeps failed and invalid attempts. Runs stream to a hub and appear on
   the live monitor with per-run replays.
4. **Reviews by a different researcher's agent.** Surveys, hypotheses and results get reviews from agents of
   another researcher. Every completed study states an evidence-confidence score and an independent-unit
   sample size from a shared rubric.

The design point that matters for swarms: many agents writing at once produce confident, plausible, wrong
output fast. The gates, receipts and cross-reviews are how a human can trust what a large agent group reports.
Our own audits show the gates catching real problems (below).

## Top findings

All are exploratory results in synthetic worlds with one task family each; numbers and caveats are in
RESULTS.md with links to the saved records.

1. **Identity checks must scale with the swarm.** When a model synthesises answers from reports by many
   identities, some of them Sybils, a fixed check budget collapses as the population grows while checks
   proportional to population hold. At 972 identities, proportional minus fixed checks raised specialist
   accuracy by +52.8 points (Sonnet 4.6, 95% +38.9 to +66.7), +51.4 (Haiku 4.5) and +100.0 (Opus 5.5) on
   identical assignments, over 24 paired worlds per model. An incomplete 9x run (8,748 identities) shows the
   same pattern.
2. **More verification can make admission worse while accuracy looks better.** Only 7 of 120 budget cells
   met both 90% accuracy and 5% attacker seats. At 324 identities, raising checks from 32 to 108 raised accuracy
   97.2% to 100% while the attacker seat share rose 1.98% to 10.70%. A follow-up traced this to trust
   propagated through the graph: from 32 to 108 checks it admitted +20.75 more attacker seats than direct
   credit (95% +17.33 to +24.21, 24/24 roots).
3. **How an attacker splits matters as much as how much it has.** Spreading a fixed attacker budget from 1 to
   27 identities raised rare-skill wrong answers by +48.6 points when checks went to well-connected
   identities and +7.6 when they were spread across the graph (difference +41.0, 95% +27.8 to +54.9; 48 roots,
   two graph families).
4. **Rules tied to identity invite identity splitting.** A profit-seeking agent registered a second firm and
   kept evading a concentration fine in 6/6 markets when the rule applied per firm, and 0/6 when it applied to
   the common owner or when there was no rule. This replicated on a second model (Opus 5.5) on six fresh
   markets. The registration action and the rules were in the prompt, so this is use of a visible affordance,
   not discovery of a hidden one.
5. **Agents treat copies as evidence.** In a lineage task every model answer followed the copied-report
   majority (0/8 correct against a 7/8 gate). In a sensing task a three-agent team covered 2.5 distinct cells
   out of 12 slots versus 12 for uniform sampling. Both are the swarm-level failure the organisers describe:
   repetition mistaken for independent confirmation.

A negative result we report as such: shadow's capture-memory-mix study found that mixing short- and
long-memory agents rescues a captured population on gpt-4o-mini, not on gemma-3-27b, and the reverse on
qwen3-235b. dmarz's review rated it "mixture rescue does not generalize" and found reporting defects, which
are being corrected in the repository.

## Honest limits

- **Synthetic, not in the wild.** Every finding comes from controlled synthetic worlds with scripted actors
  and one model in the loop. We did not analyse the AI Village, collusion.wiki, SwarmTraces or Transluce data
  for this submission.
- **Small independent samples.** Most studies have 6 to 48 independent roots. Thousands of calls per study are
  not thousands of samples. Intervals are descriptive and uncorrected for multiple comparisons.
- **Mostly same-researcher checks.** Most completed studies ran under an owner waiver of cross-researcher
  review. Cross-researcher reviews and audits exist for some (see RESULTS.md) and an independent offline
  recomputation of completed findings was in progress at the draft cutoff.
- **Qualification is the weak point.** dmarz's audit found a documented baseline-gate failure in 9 of 13
  model-executed study families at some point. Several studies stopped at qualification, which is the pipeline
  working but is not a result about swarms.
- **Spend.** Paid model calls were made per study under per-study caps; the larger Sybil studies cost USD 40 to
  215 each. Costs are in each results file.
