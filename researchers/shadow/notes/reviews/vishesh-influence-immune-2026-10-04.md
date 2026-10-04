# Review: Vishesh status items 2 (Influence Swarms) and 4 (Immune Response)

Reviewer: `shadow/sol-vishesh-review`, 2026-10-04 ~23:40Z. Read-only saved-data review against `origin/main` at `1944c3fe` (Vishesh's latest commit, 23:25Z). Zero model calls, zero spend. Nothing under `researchers/vishesh/` was edited. Status text reviewed: Vishesh's four-priority message posted 22:19Z.

Summary: every number in the status for these two studies is correct against the files it was written from, but the status is already stale against main in both studies. Influence has moved from "B1 running qualification" to B1 FAILED, B2 qualification PASSED, E1 main COMPLETE (1,907 calls) with a null result, and two unlaunched successor plans (R2, R40). Immune has moved from "192-call study unfunded" to that study FUNDED, RUN and CLOSED (verification v1, $2.25), with a peer-correction stage prepared behind admission.

## 1. Verification table

Paths relative to `researchers/vishesh/notes/`. "Recomputed" = recalculated here from the public JSON/JSONL on main, not from the post-mortem prose.

### Influence Swarms (status item 2)

| Status claim | Verdict | Evidence |
|---|---|---|
| 10-agent and 50-agent pilots selected the correct supplier | OK | `influence-swarms/scenario/HISTORY-SCALE-AND-B1-PREPARATION.md` L19. Recomputed from `scenario/reviews/native-SP-SOL-01/protocol.jsonl` and `native-SC-LUNA-01/combined-protocol.jsonl`: chair = Cobalt in clean and omission, both rosters. Nuance: the Sol omission *auditor* chose Aster and both Luna auditors DEFERred; only the chair was correct 4/4. |
| "every adviser deferred" | OK | Recomputed: Sol 32/32 opinion rows DEFER (8 agents x 2 rounds x 2 conditions); Luna 192/192 DEFER (48 x 2 x 2). Matches HISTORY L19 "8/8 Sol; 48/48 Luna in each condition". |
| Did not meaningfully test peer influence; one synthetic world; model differences | OK | HISTORY L19, L27. `native-SP-SOL-01/summary.json` `independent_worlds: 1`, `team_size: 10`; SC-LUNA `team_size: 50`, GPT-6 Sol vs GPT-6 Luna. |
| "B1 is reported running its qualification stage, with evaluation conditional on passing" | STALE | B1-D0-02 completed 240/240 calls and **FAILED** qualification: `scenario/reviews/B1-D0-02-post.md` L1-L13 (neutral_peer/private/simple all `gap`, 1/6 acceptable finals per arm, 30 deferrals traced to an ambiguous cheapest-supplier benchmark). B1-E0 withdrawn, `scenario/b1/README.md` L37. Then B2-D0-01 (96 calls) **passed** qualification (`reviews/B2-D0-01-post.md` L5), B2-E0-01 stopped at 64 reservations on a 2,579-trailing-space length failure (`reviews/B2-E0-01-post.md` L5-L9), F0 diagnostic 12 calls, and **E1 main completed** (`reviews/E1-E0-01-post.md`, commit e149f1d6 23:18Z). |
| 30 authored dossiers, six development and 24 evaluation | OK | Recomputed from `scenario/b1/case-manifest.json`: case_count 30, development_roots 6, evaluation_roots 24, construction_families 6; `b1/dossiers.json` split counter {evaluation: 24, development: 6}. |
| "fresh repeats and stronger controls" | OK | `b1/README.md` L16 two fresh executions per cell; simple full-evidence comparator arm. |
| "No completed B1 scientific result is available yet" | STALE / now wrong | B1-D0-02 is a completed (negative) result. E1, the B2 instrument's main, is complete: 1,904 valid of 1,907 calls, 285/288 decisions, USD 1.094742225 (`reviews/native-E1-E0-01/summary.json` recomputed: calls 1907, valid 1904, unstarted 13, retries 0, usage_missing 0). Interaction bounds [0, 0.0625] (`native-E1-E0-01/assessment.json` overall_bounds). Simple analyst 96/96 acceptable; peer 90/96, private 93/96 (`semantic-summary.json`). Five unsafe purchases all in `b2-cost-2` (E1 post L22). |
| Evidence link | DEFECT | Points to `/private/tmp/swarm-pi-review-publish/...`, a local path. Should be `researchers/vishesh/notes/influence-swarms/scenario/LATEST-RESULTS.md` on main. |
| Not in status, on main since 23:23-23:25Z | NEW | `scenario/r2/PLAN.md` (14-call paired root, matched truthful vs single-false-clause) and `scenario/r40/PLAN.md` (40-member hierarchy vs 4-member team vs generalist, 756 qualification + 2,988 main = 3,744 calls, neutral panel deferred). Neither funded or launched. |

### Immune Response (status item 4)

| Status claim | Verdict | Evidence |
|---|---|---|
| C1 compared action-first vs justification-first across four incident cases | OK but STALE as "latest" | `immune-response-v3/controller-study/c1/reviews/c1-post.md` L7-L20. Superseded by verification v1 (below) committed 22:40Z, and README lead rewritten 23:16Z (`immune-response-v3/README.md` L12-L21). |
| Both repaired genuine failures; both intervened on a healthy service on stale evidence | OK | c1-post L7, L30. |
| Justification-first eliminated one action/explanation contradiction, no overall improvement | OK | c1-post L16-L17: rejected deployments 1 vs 0, contradictions 1 vs 0; gates identical. |
| All 32 calls completed | OK | c1-post L22; `c1-reconciliation.json` requests_reconciled 32, actual_usd 0.329025. |
| 3/4 service gates, 2/4 combined gates, both arms | OK | Recomputed from `c1-reconciliation.json` cells: action_first outcome 3/4, both 2/4, rejected 1, useful restarts 1, healthy ticks 8; justification_first 3/4, 2/4, 0, 1, 8. |
| Simple rule controller solved the cases offline | OK | c1-post L40 (4 C1 roots + 12 constructed future-panel cases). |
| Four cases, no repeats | OK | `c1-reconciliation.json` fresh_repetitions_per_arm_world 1, paired_world_roots 4, independent_authorship false. |
| C1 closed and failed qualification | OK | c1-post L7 "Neither arm qualified", L22 baseline GAP. |
| Next study: six paired roots, fresh repeats, guarded vs unguarded, offline validation | OK as of 21:43Z, STALE now | It ran. `verification-study/reviews/v1-post.md` L9: 48 episodes, 192 requests, no failures. Run 1004-221035-647292, 22:10-22:26Z. |
| "192-call native experiment remains unfunded and unlaunched" | WRONG on main since 22:40Z (commit 44bc2522) | Funded as PI-FUND-20261004-09 (v1-post L70). Actual cost USD 2.253050 (`v1-cost-closeout.json` known_actual_usd). Recomputed from `v1-reconciliation.json` arm_branch: confirmed-fault unguarded unnecessary_executed 4/12, guarded 0/12, guard_denials 4/12; post_action_verified 8/12 both; post_state_gate 11/12 vs 12/12; served opportunities 32/36 vs 36/36. All match v1-post table. |
| Not in status | NEW | `peer-correction/README.md` (23:14Z): 48-call qualification + conditional 184-call comparison, max USD 12.84, "funded bounded scope; live admission pending, no native attempt yet". evidence_confidence 0/4. |

Headline numbers Vishesh should swap into any resubmission: Influence = E1 1,907 calls / 285 of 288 decisions / analyst 96/96 vs peer 90/96 / bounds [0, 0.0625]. Immune = v1 192 calls / 48 episodes / 12 of 12 repairs both arms / 4 unnecessary proposals both arms, 4 executed unguarded vs 0 guarded / 8 of 12 verified both arms / USD 2.25.

## 2. Offline re-runs (this host, Python 3.12, no network, no keys)

| Script | Result |
|---|---|
| `influence-swarms/tests` (unittest discover) | 15 tests OK |
| `influence-swarms/scenario/b1`: `test_b1 test_runtime` | 23 OK (45.7s) |
| `scenario/b2`: `test_b1 test_runtime test_parallel_runtime` | 28 OK (84.6s) |
| `scenario/e1`: `test_acquisition` | 6 OK (74.1s) |
| `scenario/f0`: `test_diagnostic` | 7 OK |
| `immune-response-v3/tests`: `test_analysis test_immune` (run from inside `tests/`) | 13 OK. The README L54 command `unittest discover -s .../tests` from repo root fails with "Start directory is not importable" (no `__init__.py`); doc defect, not a code defect. |
| `controller-study`: `test_controller` | 9 run, **2 errors**, both `ModuleNotFoundError: matplotlib` in `render.py`. Environment, not logic; c1-post L46 reports all 9 passing remotely with matplotlib 3.11.2. Not reproduced here. |
| `controller-study/c1`: `test_c1` | 7 OK |
| `verification-study`: `test_instrument test_verification_cases` | 18 OK |
| `peer-correction`: `test_instrument test_native` | 21 OK; printed "maximum peer request bytes 7020", matching README L17. |
| `c1/validate_saved.py`, `verification-study/reviews/analyze_saved.py` | Not runnable: require the private `episodes.jsonl`/`transport.jsonl` archive, which is not on main by design (v1-post L66). Public JSON recomputations above stand in. |
| `scripts/lab.py check` | 0 errors, 5 warnings (pre-existing library link warnings). |

Total: 147 offline tests executed, 145 pass, 2 environment errors.

## 3. Battletest: strongest objections and whether the post-mortems concede them

**O1. Adviser abstention made the social arm uninformative, and E1 may not have fixed that.** Conceded in full for the pilots (HISTORY L19, L27: "universal adviser abstention make the current social mechanism uninformative; adding agents does not repair it"). B2-D0 fixed the deferrals by rewording the price benchmark, and Vishesh correctly labels that an instrument repair, not a model improvement (LATEST-RESULTS L19). But the open hole is sharper: `B2-D0-01-post.md` L9 reports 32 initial-to-revision adviser pairs, **all retaining their first-ranked supplier**. If that holds in E1, the peer arm and private arm are the same process with different latency, and the [0, 0.0625] null is guaranteed by construction, not discovered. E1's public `semantic-summary.json` does not report an adviser stance-change rate. **Not conceded; not measured.** This is the single most important number to extract before funding R2/R40.

**O2. "Trusted stale evidence" is a prompt-design issue, not a swarm finding.** Partly conceded. c1-post L20: the comparison "tests an output-order instruction/schema package, not hidden reasoning". v1-post L35 makes the finding more interesting than a missing instruction: in all 8 misses the model's own diagnosis field correctly says "probe stale, liveness unknown", then the action explanation treats the old failure as live evidence anyway. So the information is present and stated; the inconsistency is between fields. Still, no arm tested an explicit "when your own action made the probe stale, inspect before acting again" instruction, so "a one-line prompt removes it" is untested. And v1 is a single agent plus a guard: **the immune line currently has zero multi-agent native evidence**. Vishesh concedes this ("not natural-peer swarm evidence", c1-post L42; v1-post L80).

**O3. The rule controller solves everything offline, so the LLM result is a negative result about LLM agents vs. 20 lines of code.** Conceded (c1-post L40, v1-post table column 3 and L62; R40 PLAN "if the larger system adds no quality or resistance, its extra cost is not justified"). The same applies to Influence: the single analyst scored 96/96 while both multi-agent workflows scored worse at higher cost. Both studies are honest negative results for the swarm. That is fine for a submission if framed as such; the status currently frames them as "promising directions", which undersells the actual finding (swarm structure added cost and errors on these cases).

**O4. Four cases, no repeats (C1), and six roots in three families (v1) cannot support reliability claims.** Conceded (c1-post L20; v1-post L9, L56). v1 adds 2 fresh repeats and the repeat data makes the point for the skeptic: 4 of 24 root/branch/arm repeat pairs disagree on qualification, worker-expanded fails 4/4 across arms and repeats. Also v1-post L62: all catalog compatibility flags are true in the packet, so "diagnosis" is effectively a liveness/freshness test only.

**O5. Authored cases, templated variants, same-author assessment.** Conceded everywhere (E1 post L16 "24 variants nested in six families"; L33 "same-author and not an independent arithmetic audit"). The one thing our side can contribute cheaply is an independent recomputation, which this review partially is (section 1), and which `completed-findings-xcheck/recompute.py` did for Dmarz's studies.

**O6. Status evidence links are local filesystem paths** (`/private/tmp/...`, `/Users/ultron/...`). A reader cannot follow them. Replace with repo-relative paths or GitHub permalinks at commit `1944c3fe`.

## 4. Concrete next steps reusing our tooling

**N1. Adviser stance-change audit on E1 before any R2/R40 funding (zero model calls).** Reuse the saved-data independent-rescoring pattern from `researchers/shadow/notes/completed-findings-xcheck/recompute.py` against the E1 local replay (Vishesh holds the raw records; the script only needs `agent, round, ranked_supplier, cited_sources` per reply, which can be exported as aggregates without publishing prose). Output per case: (a) fraction of advisers whose ranked supplier changed between initial and revision, (b) of those, fraction that moved toward a peer who held a different position, (c) fraction whose final citations include a source they did not hold initially. Decision rule: if (a) is zero or near zero on cases where peers genuinely disagreed, R40's 3,744-call plan is testing a channel that transmits nothing and should be redesigned around forced disagreement first. This directly closes O1 and costs nothing.

**N2. Not-a-copier qualification gate for the R40 ring, borrowed from freeze-claude attempt2.** `researchers/shadow/notes/capture-memory/freeze-claude/attempt2/` (`check_attempt2.py`, `qualification.json`, FINDING L30-L34) ran a 12-decision sparse gate: 4 unanimous controls must be correct, and on conflicting histories at least one choice must differ from the last list item, rejecting universal last-item copying before the paid stage. R40's revision step shows each specialist its own report plus two ring neighbors. Before 756 qualification calls, run the same gate shape on the adviser revision prompt: 8 conflicting-neighbor contexts where the most recent neighbor is wrong and the other is right (and the reverse), 4 unanimous controls. About 12 calls, under USD 0.10 on the Luna route. If revisions just copy the most recent neighbor, the 40-member ring is a recency-propagation machine and the study measures topology, not influence. Reuse is direct: same gate logic, same pass criterion, same `qualification.json` receipt format.

**N3. Lexical contamination tracing with AskSwarm on adviser reports and peer-correction notes.** `researchers/shadow/notes/wild-askswarm/askswarm/` runs on any `agent_id, time, text[, thread]` table offline. For Influence: table = (adviser id, round, rationale text) with the advocacy page as a seeded source document; the lexical-reuse report measures how much promotional phrasing enters advisory rationales in advocacy vs neutral conditions, independent of whether the final choice changed. That gives the "did the pitch get in" measure Vishesh's endpoint (final acceptable action) cannot see; E1 post L20 already shows 187 reports with wrong intermediate fields despite correct finals. For Immune peer-correction: table = (member id, tick, note text and action explanation); measure whether a wrong peer note's wording reappears in the recipient's explanation, separating "read and rejected" from "absorbed". Both are descriptive, both are zero spend, and AskSwarm's own README already states its limits (lexical proxies, no semantic adoption claim), which matches Vishesh's reporting discipline.

**N4 (small, defuses O2). Add a third arm to the next immune run: unguarded agent plus one explicit freshness instruction.** 24 episodes, about 96 calls, roughly USD 1.15 at v1 rates. If the 8 of 12 verification misses disappear, the stale-evidence finding is a prompt finding and should be reported as one. If they persist while the diagnosis field keeps saying "stale", the field-inconsistency finding stands as an agent property. Either answer is useful; right now the claim is undetermined.

## Repo and process notes for Vishesh

- Replace the local evidence paths in the status with repo paths (O6).
- `immune-response-v3/README.md` L54 discover command fails from repo root; add `__init__.py` to `tests/` or document running from inside the directory.
- The status should lead with E1 and verification v1 numbers; both are complete, reconciled and stronger than the pilots/C1 they currently cite.
- Peer-correction (`peer-correction/README.md`) is the first immune design with actual peers. If only one more immune stage can be funded tonight, that one is the one that finally tests the word "swarm".
