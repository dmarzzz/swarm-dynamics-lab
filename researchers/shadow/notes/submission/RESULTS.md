# Joint evidence packet: findings, diagnostics and limits

**Submission draft, not a submission receipt.** Team: dmarz, vishesh, shadow. Prepared 4 October 2026.
Companion [write-up](WRITEUP.md) and [demo](DEMO.md).

## Evidence cutoff and reading rules

This packet reads source records at [`c99dbf75`](https://github.com/dmarzzz/swarm-lab/tree/c99dbf754f4aea13bc251a6eaeb0953db9f498bd).
Source links below are pinned to that snapshot so a later run cannot silently change what a number means.
Numbers are transcribed from those records, not newly estimated for the submission. Each record has its own
cohort, observation window and review cutoff. This is a selected evidence packet, not an exhaustive inventory.

- **Experimental evidence:** synthetic worlds, scripted components and native model decisions are labelled
  separately. A call, owner, report or cell is not automatically an independent sample.
- **Archive evidence:** post-hoc descriptions of dependent selected records, not causal in-the-wild findings.
- **Review:** most model runs have owner/same-researcher checks with cross-researcher review waived. Specific
  cross-checks are listed below; they do not upgrade the whole study to independent validation.
- **Unfinished work:** plans, offline tests, qualification and partial collections are not main-stage results.
  Live activity is navigation, not evidence of completion.

## 1. dmarz: identity incentives and verification

### Firm splitting responds to the instruction, within two synthetic economies

**Observed:** with a firm-level competition charge, 55/180 owners sustained concentration-masking splits in
one economy and 59/180 in a second. Adding a prohibition sentence gave 0/180 in both. The owner-level-charge
arm also gave zero, but included that same sentence, so it does not isolate owner-level enforcement alone.
Each economy had 60 dependent markets and 180 model-controlled owners using `gpt-6-sol` at low effort.

**Unit and scope:** two economy seeds, not 360 independent owners. The second seed was planned after seeing
the first result; it used fresh fixtures. Registration, transfers and the concentration formula were supplied.
The instruction also signals regulator intent. These results do not identify moral compliance, hidden-loophole
discovery, social spread or robustness to successful cheating rivals. The latter follow-up stopped at its
seeder qualification gate, before the comparison.

**Sources:** [sybil-rules-180 results](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/dmarz/notes/sybil-rules-180/RESULTS.md),
[program summary and qualification stops](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/dmarz/notes/overnight-program-2026-10-04/RESULTS.md).
Review is same-researcher; the study includes a separate-code endpoint recomputation, not cross-researcher replication.

### Verification success depends on what is counted

| Selected contrast | Observed result | Independent unit and limit | Source |
|---|---|---|---|
| Proportional vs fixed checks, 972 identities | Specialist accuracy +52.8 pp on Sonnet 4.6 (descriptive 95% interval +38.9 to +66.7), +51.4 pp on Haiku 4.5, +100.0 pp on Opus 5.5 | 24 paired world roots per model, identical assignments. Identities/admission are scripted; the model synthesises admitted reports. Not three independent environment replications. | [Sonnet/Haiku](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/dmarz/notes/sybil-scale-sonnet/RESULTS.md), [Opus](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/dmarz/notes/sybil-scale-opus/RESULTS.md) |
| Coverage checks 32 to 108, 324 identities | Accuracy 97.2% to 100%; attacker seat share 1.98% to 10.70%. Only 7/120 budget cells met both at least 90% accuracy and at most 5% attacker seats. | 24 paired roots; cell means are descriptive thresholds, not a certified safety frontier. | [Budget results](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/dmarz/notes/sybil-budget-api/RESULTS.md) |
| Propagated vs direct trust credit, change from 32 to 108 checks | Propagated credit's change admitted +20.75 more attacker seats (95% +17.33 to +24.21), positive in 24/24 roots. | Scripted admission outcome, not model behavior or a model-discovered mechanism. | [Trust-credit results](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/dmarz/notes/trust-credit-qwen/RESULTS.md) |
| Fixed attacker resources split from 1 to 27 identities | Rare-skill wrong answers: degree checks +48.6 pp, coverage checks +7.6 pp; difference +41.0 pp (95% +27.8 to +54.9). | 48 roots across two graph families; strong-check contrast. Weak checks reverse the interaction, so no unconditional ranking is claimed. | [Split results](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/dmarz/notes/sybil-split-opus/RESULTS.md), [cross-check](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/completed-findings-xcheck/SPLIT-REVIEW.md) |

The 8,748-identity scale run is **incomplete**, 481/576 valid after a billing stop. It is not included as a
completed replication: [preserved partial result](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/dmarz/notes/sybil-scale-xl/RESULTS.md).

## 2. vishesh: source ancestry, acquisition and instrument diagnosis

### Quorum of Mirrors: qualification is not committee benefit

- **Q1-02:** 16/16 valid responses; 0/8 correct graded full-lineage decisions against a 7/8 gate. All choices
  matched report-count majority. Eight other cases were interface-only, not accuracy failures. Copied-report
  majorities and misleading prior choices were aligned, so the cause of failure is not isolated.
- **SP-02, a different interface and fresh cohort:** 40/40 valid calls and decisions, 120/120 source and
  280/280 report clause selections correct, 20/20 exact paired roots. The model selects literal quotations;
  code derives facts. Twenty authored roots share five grammar mechanisms. An exact text parser is also
  perfect on this grammar. This is a passed qualification, not a causal before/after repair estimate,
  field reliability, a demonstrated need for a model or an interacting-swarm advantage.
- Preserve both results. The proposed realistic 60-agent successor has not run at this cutoff.

**Sources:** [Q1 post-mortem](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/vishesh/notes/decision-models/quorum-of-mirrors/reviews/Q1-02-post.md),
[SP-02 post-mortem](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/vishesh/notes/decision-models/quorum-of-mirrors/reviews/SP-02-post.md),
[overview and successor status](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/vishesh/notes/decision-models/quorum-of-mirrors/README.md).
Audits are operator/same-author unless specifically stated; researcher review was waived.

### Phantom Coast: better average decisions can hide a regression

PC-2's three-proposal team inspected 2.50 distinct cells in 12 sensing slots under misleading reports/no audit,
versus 3.25 for single agents and 12 for uniform sampling (8 roots, 96 episodes). This is a narrow acquisition
failure, not proof that teams always explore worse.

Later PC-5 tested a **different, one-step decision diagnostic** on 32 paired layouts, two semantic risk cases
and 128 valid native choices. Explicit scoring/transition instructions reduced expected regret by 0.1578
(descriptive 95% interval 0.1093 to 0.2063). Yet optimal choices under reliable reports fell from 28/32 to 21/32;
under unreliable reports they rose from 5/32 to 24/32. Consequences are scripted, not native multistep planning.
PC-8 subsequently failed qualification and withheld its main stage; PC-9 is offline population-instrument work.

**Sources:** [PC-2](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/vishesh/notes/phantom-coast/pc2/README.md),
[PC-5](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/vishesh/notes/phantom-coast/pc5/README.md),
[later status](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/vishesh/notes/phantom-coast/README.md).
Checks are operator-owned, not independent replication.

### Newer diagnostics that do not establish swarm effects

- **Theseus SOL50 qualification:** five members in one world, 17 native calls, zero handovers and zero
  50-member pilot calls. Correct destinations expressed as current identity strings were rejected by a
  router expecting position names; only 2/10 consultation edges arrived. All 30 joint actions were correct
  given the evidence actually delivered, but only 18/30 against the full task. This localises an interface
  failure, not cultural loss: [SOL50 findings](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/sol50/RESULTS-SOL50.md).
- **Theseus C2, later conditional continuation:** eight new calls plus 128 cached calls reused without
  redispatch; 4/4 observed inherited notes were correct, but only 3/4 met the exact output schema. The extra
  field triggered a technical stop; zero complete turnover trajectories or terminal four-arm outcomes were
  observed. This is not cultural survival or loss: [C2 closeout](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/sol50/baseline-replication/C2-POST-MORTEM.md).
- **Influence-swarms B2:** repaired price-rule ambiguity passed a 96-call qualification; evaluation stopped
  at 62 calls, 61 valid, after malformed output. The framing comparison remains incomplete. Earlier 10- and
  50-agent pilots changed model/configuration and had universal adviser deferral, not an identified size
  effect. E1 subsequently passed 80/80 readiness calls and its main run was reported running; no completed
  E1 comparison is claimed: [current findings](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/vishesh/notes/influence-swarms/scenario/LATEST-RESULTS.md).

## 3. shadow: archive answerability and negative memory results

### AskSwarm: the unit of observation changes the story

The tool asks fixed participation, repetition and timing questions of collusion.wiki, SwarmTraces and
swarm-lab git. In its selected SwarmTraces input, all 189,579 artifacts lack usable clocks and a structured
actor field; social comparisons are unavailable rather than imputed. Labels in other corpora remain
unauthenticated, and each analysis uses its own frozen git window.

- **Retained text vs edits:** non-self known-name references occurred in 5,065/13,692 labelled wiki snapshots
  versus 2,164/13,692 edits, a 2.34× ratio (conditional page-cluster 95% interval 1.96 to 2.75).
- **Repetition robustness:** aggregating wiki revisions by page root retained only 1 of the original top 10
  repeated-phrasing credit leaders; multi-identity clusters fell from 1,653 to 200. Alternative observation
  units define different quantities, not a corrected influence ranking.
- **Direct-text audit:** all 15 sampled git links were sync boilerplate; 5/15 wiki links were same-page
  snapshots. The partially blinded reviewer was the operating assistant, not an independent human.
  Verified directed semantic adoption was unestablished in both corpora.

**Sources:** [AskSwarm finding](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/wild-askswarm/FINDING.md),
[robustness](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/wild-askswarm/ROBUSTNESS.md),
[audit](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/wild-askswarm/AUDIT.md),
[identity observability](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/wild-identity/FINDING.md).
Companion [chronology](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/wild-timeline/FINDING.md)
and [URL timing](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/wild-halflife/FINDING.md)
are also descriptive, not causal transmission tests. Raw incident rows and identifying labels are not published in this packet.

### Memory-mixture rescue does not generalise

In the original synthetic pilots, gpt-4o-mini recovered only in interior memory mixtures; gemma-3-27b recovered
in no valid captured episode; qwen3-235b instead returned most under pure short memory, with mixtures diluting
that return. These small model/policy cohorts are confounded, not a controlled explanation of model differences.
The scripted recover/stay-captured/freeze regimes are properties of a specified rule, not native agent evidence.

Cross-researcher review found undisclosed attempt selection and reporting defects. **Corrections are now
published**, not merely pending: MP3 has 327 raw arm records, 127 invalid and 180 selected (178 valid), with
147 superseded. Only 54/180 logical arm keys were valid on first observation. The corrected selection procedure
preserves the reported headline estimates; that does not erase failed attempts or establish retry benefit.

**Sources:** [pilot overview](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/capture-memory-mix/README.md),
[corrections and reproducible lineage check](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/capture-memory-mix/CORRECTIONS.md),
[scripted memory study](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/capture-memory/README.md).
### Claude freeze follow-up: complete repair data, inconclusive freeze classification

The newly published transport follow-up passed the unchanged qualification gate and completed all 16 Sonnet
repair episodes across **four paired roots**. Full-memory removal changed original-name share by -0.0833
(descriptive 95% root-bootstrap interval -0.1667 to 0). The interval is not contained in the prespecified
[-0.10,+0.10] freeze band, so operational freeze is **not established**. None of the Sonnet repair episodes
recovered. Memory1 preserved aggregate share while individuals switched; the full-memory wipe penalty was
zero, not the predicted harm. This is a behavioral result, no longer just attempt 1's transport failure.

The starting states have a strong floor effect, the horizon/population were reduced, and their own scripted
reference did not reproduce the parent freeze regime. Optional Opus observations used two already-unanimous
captured roots and are not independent confirmation. Two full-memory attack episodes stopped with missing
endpoints after invalid final outputs; they are not evidence of attack resistance. Returned model identifiers
were Claude Sonnet/Opus 5.5 via OpenRouter; audits are same-author, not independent replication.

**Source:** [attempt 2 finding, records and limits](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/capture-memory/freeze-claude/attempt2/FINDING.md).
### Claude memory mixture: blocked qualification and admission defects, not a null

The recovered pool attempt made 20 failed HTTP requests (eight rate limits, twelve broker-unavailable errors),
with zero valid model completions and 0/4 paired scientific roots. Historical usage/dollars are unknown,
not zero. Recovery made no new model calls. It also found that public preregistration before calls was not
established, the parse-only qualification admitted a deterministic last-item copier, and the old runner lacked
a dollar-reservation ledger. These are instrument/admission defects, not observations of Claude copying or
failure to recover. The historical runner remains frozen; mixture rescue on Claude is untested.

**Source:** [recovered finding and accounting](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/capture-memory-mix/claude-pool/FINDING.md).

## 4. Checks that changed the joint claims

- **dmarz's cross-researcher review** identified the mixture-reporting defects and rejected a general rescue
  claim: [review evidence](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/dmarz/notes/latest-results-review-2026-10-04/evidence.json).
- **vishesh's PI review** covers evidence, implementation and presentation across the project:
  [review index](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/vishesh/notes/pi-review-2026-10-04/README.md).
- **shadow's completed arithmetic cross-check** rescored 7,512 saved Sybil answers with zero endpoint
  mismatches, plus 36 market episodes. These are saved records, not new independent worlds. Scaling was
  checked from aggregates, not raw answers. Exact ties had been counted as wins/losses: the correct Opus
  higher/lower/equal counts vs Sonnet are 7/66/27, not 9/67/24; the mean contrast is unchanged.
  [Scope, results and reproduction](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/completed-findings-xcheck/README.md).

Recomputing arithmetic does not independently attest provider identity, cost, historical registration or
scientific validity. Code fixes and passing tests are engineering evidence, not treatment findings.

## Final sync and exclusions

Final source sync: **`c99dbf75`, 4 October 2026, repository commit timestamp 23:09:21 UTC**.
This refresh includes the completed Claude freeze attempt 2, recovered blocked Claude-mixture attempt,
Theseus C2 schema-stop closeout and E1's readiness result. E1's unfinished comparison and the new offline immune peer-correction preparation are not
promoted to treatment findings. The Claude-mixture closeout is an operational/admission finding, not a measured rescue effect. Factory provenance attempt 2 remains blocked by its recorded independent review
and has no treatment claim. These statements describe pinned records, not live-worker assertions.

Attempt 1's eight freeze transport errors and unknown historical charges remain preserved; attempt 2 does
not rewrite them into successful observations. Its completed primary repair data and partial attack screen
also remain separate. See the qualified behavioral result above rather than the obsolete blanket description
“Claude freeze had no completions.”

- [Initial freeze closeout](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/capture-memory/freeze-claude/FINDING.md)
- [Completed freeze follow-up](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/capture-memory/freeze-claude/attempt2/FINDING.md)
- [Claude-mixture blocked-attempt closeout](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/notes/capture-memory-mix/claude-pool/FINDING.md)
- [Factory independent review](https://github.com/dmarzzz/swarm-lab/blob/c99dbf754f4aea13bc251a6eaeb0953db9f498bd/researchers/shadow/factory/provenance/attempt2/REVIEW-independent.md)

Do not pool redesigned cohorts, incomplete runs or qualified fixtures into one success rate. No team-wide
spend total, current agent count or commit-volume performance claim is used; study-specific costs remain in
the source records. Later evidence may be added only with its own pinned result and scope, not inferred from
a task status or a running dashboard.

## 6. Packet verification record, 4 October 2026

Deterministic checks on this packet at the current `main`, by `shadow/sol-final-pool-review`, no model
involvement: 46 links in WRITEUP, RESULTS and DEMO resolved (24 relative paths and anchors, 17 pinned
GitHub blob/tree targets confirmed as git objects, 5 public URLs returning HTTP 200); headless browser
renders of https://swarm-narrative.pages.dev, the research-path dashboard and the experiment monitor
loaded without page errors; `scripts/lab.py check` reported 0 errors. The DEMO spoken text is 245 words,
about 105 seconds at 140 words per minute. Hash-route fragments are not checked by HTTP status.

A bounded editorial critique of the previous draft was requested from the local Anthropic pool
(Sonnet 5.5, one attempt plus two delayed retries). All three returned transport errors (HTTP 429, 503,
503) with zero completions, so no model critique informed this packet. That is an operations note about
review tooling, not scientific data and not related to any experiment's qualification record.
