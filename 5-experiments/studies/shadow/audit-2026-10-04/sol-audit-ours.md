# Audit of the shadow/Sol lanes, Sat 14:00 EDT to Sun 11:20 EDT

Author: shadow/sol-audit-ours. Cutoff: 2026-10-04 15:20Z, repository `952a618c` (origin/main). Scope: everything
committed by git author `wakesync` since 2026-10-03 18:00Z, the two dashboards, the public report, the open RSI PR,
and the live worktrees under `~/projects/swarm-lab-wt/`. Method: `git log --author=wakesync`, file reads, HTTP checks
of a random sample of library sources, and a full Crossref/arXiv title check of every paper entry we added that
carries a DOI or arXiv id. No model calls. Judged against BRIEF-2026-10-03.md (deliverables: write-up, repo, real
results; suggested project types) and the time left (about 8.5 h to 00:00Z, 6.5 h to the 22:00Z model-call stop).

## 1. Volume, where it went

286 commits by wakesync in the window (of about 2,860 non-bot commits on main; dmarz's fleet about 1,000, vishesh's
about 860). By hour (UTC): 94 at 19h and 105 at 20h on Saturday, then 2 to 12 per hour overnight, 21 at 14h and
14 at 15h today. So about 70 percent of our commit volume landed in two Saturday hours of library writing.

Files touched (path prefix, counting name-only across those commits):

| area | file-touches | what it is |
|---|---:|---|
| `library/{papers,talks,blogs,threads,datasets,code}` | 755 | 563 new entries added by us (248 papers, 138 talks, 91 blogs, 59 threads, 20 datasets, 7 code) |
| `researchers/shadow/notes/capture-memory-mix` | 200 | 3-model pilot, results, call logs, hub sync |
| `dashboard/`, `candidates/`, `scripts/` | ~150 | swarm-research.pages.dev build, collector pipeline (PR #1) |
| `researchers/shadow/factory` | 50 | experiment factory, 5 specs, 5 result dirs (lane 16, in progress) |
| `researchers/shadow/notes/capture-memory` | 40 | scripted S0/S1 (PR #83) |
| `researchers/shadow/notes/{rsi-loop, wild-askswarm, completed-findings-xcheck, submission, landscape-map}` | 41 | see sections below |
| `surveys/`, `synthesis/`, `tasks/` | ~40 | fork-merge-security survey closed, landscape map, task claims |

Only three wakesync commits touched `researchers/dmarz` or `researchers/vishesh`, all of them `inbox.md` receipts
(review request `2d0b7855`, review verdict `93a58d71`). No teammate experiment, ledger or READY file was edited.
`python3 scripts/lab.py check` on `952a618c`: 0 errors, 5 warnings (dangling `[[...]]` links in thread entries, none
ours).

## 2. Library entries: quality on a sample, and a full id check

**Random sample of 20 entries we added** (seeded `shuf`, list in the appendix). All 20 front-matter URLs resolve:
5 YouTube talks confirmed by oEmbed title + channel (Puzzo/ICTP-SAIFR, Berkeley blockchain lecture, three Couzin
talks), 3 DOIs confirmed on Crossref with matching title/venue/year (Suyama 2005 AAMAS journal, Lesniewski-Laas 2008
SocialNets, Hoffmann 2026 CCR), 1 arXiv id confirmed (2608.00285), 7 blog/dataset URLs return 200 with the expected
page, 4 X posts confirmed via fxtwitter with the right author handle and the archived first sentence matching the
entry's quoted text. The thread entries archive verbatim text and state their fetch method and its limit (for
example "self-reply search hit 429, later author replies not included"), which is the right level of honesty.

**Full check of every paper entry we added with a DOI or arXiv id**: 230 entries (150 DOI, 98 arXiv, some both). 230
of 230 resolve and the resolved title matches the entry title (SequenceMatcher ratio > 0.6 on normalised titles,
most near 1.0). Two arXiv ids (2609.22512, 2605.29800) were not returned by the export API but resolve on
arxiv.org/abs with matching titles. **Zero hallucinated DOIs or arXiv ids found.** Script: `/tmp/doicheck.py` on
shad0wbot, output `/tmp/doicheck.json` (not committed; it is an audit artefact, re-runnable in 5 min).

Front-matter over the 560 entries still on main: read_depth full 190, abstract 197, skim 168, ran 5; relevance 5:83,
4:151, 3:178, 2:125, 1:23. Body length median 246 words, minimum 115. No entry without a URL.

Verdict: the library work is real and clean. Its value to the *submission* is indirect: it fed the survey gates
(llm-agent-swarms, fork-merge-security) and the landscape map, and the research dashboard shows it well. Judges are
told in BRIEF section 1 that deliverables are tool + real results; a 3,300-entry library is context, not a result.
Roughly 200 of the 286 commits (Saturday 19h to 21h) went here. That was the right call for the Saturday gate
structure the team chose, but it is the single largest block of effort with the lowest direct submission weight.
Do not add more entries today except where a wild-* FINDING needs a citation.

## 3. Item by item: value for the submission

Status key: **ship** = on main, usable in the packet now; **half** = exists, needs a specific finish; **bg** =
background value only.

| item | status | evidence | assessment |
|---|---|---|---|
| capture-memory-mix (3-model pilot, USD 3.93) | ship, with corrections pending | `researchers/shadow/notes/capture-memory-mix/README.md` headline at 08:05Z (`e10201d2`); dmarz review verdict "does not generalize" | Our one real-model result. Honest negative with a plausible moderator (long-list read noisy/sharp/recency). dmarz's four reporting defects are real: 327 raw / 127 invalid / 180 selected without disclosure, redo vs no-retry text conflict, round 50 vs 30 caption, hub fraction > 1. The cm2 worktree has 24 modified files and two new scripts (`src/lineage.py`, `src/resummarize.py`) but **nothing pushed since 14:43Z** and no `CORRECTIONS.md` exists yet. The RSI PR already computed the lineage reconciliation (327/127/180/147 superseded/178 selected valid, only 54/180 valid on first attempt); cm2 should reuse that number rather than recompute. |
| completed-findings-xcheck | ship | `completed-findings-xcheck/README.md`, 5 reviews, `recompute.py`, zero model calls | High value, low cost. 7,512 saved answers rescored with independent code, zero endpoint mismatches, one real tie-counting defect found in `reporting/compare_models.py` (Opus 7/66/27 not 9/67/24). This is the kind of cross-researcher check judges can verify in one command. Already cited in RESULTS.md and the report. |
| submission packet (WRITEUP, DEMO, RESULTS, HACKATHON.md) | ship, stale | `d0a9b9a8` 14:03Z | Well written, numbers all linked to `b8d90f52`. Two problems: (a) RESULTS row 8 says corrections "are being corrected" and the WRITEUP limits say "we did not analyse the AI Village, collusion.wiki, SwarmTraces or Transluce data", both of which will be false by 21:00Z if Wave 3 lands; (b) the DEMO leads with the pipeline and a dmarz market-split replay, not with a wild-data tool, which sol-audit-gap correctly flags as mis-aimed against the organisers' suggested project types. Needs the planned 20:00Z refresh plus a lead swap. |
| RSI PR #84 (shadow/rsi) | ship as branch demo | 41 files, +17,795 lines, 566 envelopes, replay 75/195 vs 195/195 vs rejected 75/195, 32 tests | Coherent and honest about being same-author reporting-contract maintenance. For the hackathon it is a side quest: the brief's categories do not include agent self-improvement tooling. Its real payoff today is the lineage reconciliation it did for capture-memory-mix. Keep as "post-hackathon" in the packet; do not spend more lane time on it. |
| landscape map (sol-atlas) | ship | `synthesis/landscape.md` 4,761 words, `landscape-map/counts.md`, task closed `cc8cbb70` | Good synthesis, 16 topics, 28 transfers, corpus counts generated by script. Supports the write-up's "what we read" paragraph. No further work needed. |
| fork-merge-security survey (sol-fm) | ship | `surveys/fork-merge-security.md` 8,440 words, status complete, task done `2080bf26` | Gate closed. 83 wiki-links. Background value for the repo; zero direct submission weight today. |
| agent-budgets survey (sol-budget) | half | worktree `budget` has untracked `surveys/agent-budgets.md` + 2 library entries, nothing pushed since 14:28Z | Either push what exists by 17:00Z or drop. Not on the critical path. |
| AskSwarm (sol-askswarm) | half, promising | `wild-askswarm/` v0.1, 3 adapters, 17 tests, pushed 15:03Z; worktree has 13 dirty files (results in progress) | This is the item that most matches the brief verbatim ("pre-written questions you always want to ask about a multi-agent group"). README already states the SwarmTraces limits correctly (no actor column, all clocks null). The headline (same questions, three swarms, side by side, one of them our own repo) is the demo hook. No `results/` or comparison HTML on main yet. |
| wild-halflife, wild-identity, wild-timeline | half | PLAN.md only on main (15:03Z, 14:59Z); timeline has task claim only | Preregistrations exist, which is correct procedure; findings are 0 of 3 so far. These three plus AskSwarm are the only things that can fix the packet's biggest gap. |
| wild-evidence-depth (sol-audit-gap) | half | PLAN.md + SETUP.md 15:03Z | Zero-dollar census on SwarmTraces parent graph. Good pick, cheap, unowned. |
| factory (sol-factory) | half | 5 specs + 5 result dirs, `952a618c` "retain 20 pool 429s; preregister capped paid route attempts" | Built fast and already running Sonnet split sensitivities, but the last commit says the pool returned 429s 20 times and it is now preregistering a paid route. Pool availability is the risk. Results dirs exist; no FINDING.md yet. |
| dashboards | ship | swarm-research.pages.dev (200, title "swarm lab · research"), dashboard-v1.swarm-lab-c3n.pages.dev (200, 354 B shell, JS-rendered) | swarm-research is the canonical one, CI-rebuilt. Fine for the demo as a 5-second tab. |
| public report | ship | swarm-report-shadow.pages.dev, 24 KB, 5 sections, no key strings, no identity details | Honest problems section is good. Lane status table reads from the repo at a pinned commit; needs the 19:00Z and 23:00Z refreshes it promised. |
| collector pipeline + Discord setup (Sat) | bg | PR #1, 68 batches, `candidates/` | Enabled the library push. Done, no more work. |
| review of discussion benchmark v3 (sol-rev) | ship | `review-discussion-benchmark-v3.md`, pass-with-fixes, two blocking defects | Real cross-researcher review that changed a paid run. Cite it. |
| hypotheses PR #82 | bg | 3 proposals, status proposed | Superseded by capture-memory and capture-memory-mix. |

## 4. What was busywork

- About 150 to 200 commits of Saturday library writing beyond the gate thresholds. Clean work, verified above, but
  the marginal entry after the gate passes has near-zero submission value. The dmarz review of the llm-agent-swarms
  survey still shows a `revise` verdict despite 54 more entries (`58da2284`), which suggests the bottleneck was
  argument quality, not entry count.
- Dashboard polish passes (sol-dash-u, sol-dash-d, sol-dash-g, sol-dash-x: ~20 commits) after the first deploy.
  The dashboard is a 5-second demo tab.
- RSI protocol/spec work beyond the lineage reconciliation. Good engineering, wrong weekend.
- Per-lane `researchers/shadow/agents/sol-*.md` registration files and `sync: N file(s)` commits (about 30 commits).
  Repo convention requires them, but they inflate the commit count that the WRITEUP then quotes as a feature.

## 5. What is half-done and blocks the packet

1. **No wild-data finding on main.** Four lanes have plans, none has numbers. This is the one gap the brief and
   sol-audit-gap both call out, and the WRITEUP currently concedes it in its limits section.
2. **capture-memory-mix corrections not pushed.** cm2 has local work since 14:43Z and no CORRECTIONS.md. The RESULTS
   row 8 and the public report both promise corrections "in progress". A Claude replication was also promised (lane 1,
   part b); nothing on main shows a preregistration amendment for it.
3. **Submission packet is pinned to `b8d90f52`** and leads with the pipeline. It needs the lead swapped to AskSwarm +
   one wild result, with the Sybil work and xcheck as the "real results" section, once (1) exists.
4. **Factory depends on the pool**; 20 429s already. If the pool stays rate-limited, the factory's Sonnet specs will
   either stall or move to OpenRouter under its USD 20 cap. Either way, one finished spec with a FINDING.md beats five
   half-run ones.

## 6. Top five actions (owner, payoff before 00:00Z)

1. **us / sol-askswarm**: push `results/` for wiki + SwarmTraces + swarm-lab git and the 3-way `comparison.html` to
   main by 18:00Z, even with only the metrics that the data supports (lexical reuse for SwarmTraces, full set for wiki
   and git). Payoff: the demo's first 30 seconds become a tool the judges asked for, run on the data they pointed at.
2. **us / sol-halflife or sol-identity (whichever has numbers first)**: one FINDING.md with a figure and a CI by 20:00Z;
   the other lane stops at a short appendix if it is not there by 20:30Z. Payoff: converts "we did not analyse the
   incident data" into one checkable cross-swarm number.
3. **us / sol-cm2**: push CORRECTIONS.md now using the RSI PR's lineage numbers (327/127/180/178), fix the four
   captions, re-sync hub; skip the Claude replication unless the pool is free by 17:00Z. Payoff: closes the only
   open defect dmarz logged against us before the submission refresh.
4. **us / sol-submit at 20:00Z**: re-pin RESULTS to the latest main, swap the DEMO lead to AskSwarm tab + wild
   FINDING, keep market-split replay as the second beat, fix the limits paragraph. Payoff: packet matches what we
   actually have.
5. **dmarz / vishesh (no edit by us)**: pick the two strongest completed, xcheck-verified Sybil findings and freeze
   their numbers for the form; the xcheck README gives the exact figures. Payoff: strongest experimental evidence
   stated once, with an independent recomputation beside it.

Not recommended for the remaining hours: more library entries, more dashboard polish, RSI PR iteration, a sixth
survey.

## Appendix: sampled library entries (all 20 verified)

talks/puzzo-2025-short, blogs/quanta-2018-simple, talks/blockchain-at-berkeley-2020-distributed,
threads/x-curatedapes-2106058342317641992, papers/suyama-2005-strategy, blogs/mowatt-gok-2026-alternative,
threads/x-deanwball-2106111729566417345, talks/couzin-2017-ecology, talks/couzin-2024-cognitive,
threads/x-heisblesse-2106002189600620864, papers/vega-barbas-2026-sixteen, blogs/pangram-2026-feed,
papers/lesniewski-laas-2008-sybil-proof, papers/hoffmann-2026-robots, talks/couzin-2018-principles,
threads/x-nicolenotdunn-2102431225885704567, blogs/bradshaw-2026-swarm, blogs/reynolds-1995-boids,
blogs/schroederdewitt-2024-secret, datasets/data-aisilab-moltbook-2026.
