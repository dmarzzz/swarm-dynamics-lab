# PROPOSAL-FACTCHECK — claim-vs-source verification pass (reviewer ≠ author)

**Targets** `PROPOSAL-influence-v2.md` (460 lines) and `PROPOSAL-REVIEW.md` (the design-review disposition table).
**Sources** `sim/RESULTS-SIM.md`, `sim/results/E1–E7.json`, `sim/MODEL.md`, `sim/sim.py`, `DESIGN-DIGEST-influence.md`,
`PROPOSAL-REVIEW-astra.md`. `swarm-lab` was **not** read or written in this pass; every harness fact was
checked against the digest only, as instructed.

**Independent check run:** `python3 sim/sim.py --check` → `ALL IDENTICAL (55.0s)`, all seven result files byte-identical.
The reproducibility claim in §10 is verified, not taken on trust.

## Summary

| | count |
|---|---:|
| Claims checked | **72** |
| Supported | **55** |
| Partial / imprecise / internally inconsistent | **12** |
| Unsupported | **5** |

Breakdown by source axis:

| axis | checked | supported | partial | unsupported |
|---|---:|---:|---:|---:|
| Simulation-attributed (E1–E7) | 33 | 25 | 4 | 4 |
| Harness/digest-attributed | 26 | 23 | 3 | — |
| Design-review-attributed (`PROPOSAL-REVIEW.md`) | 7 | 6 | 1 | — |
| Reservation arithmetic (§6/§7, recomputed from the formula) | 3 | 2 | 1 | — |
| Call-count consistency (§1/§4/§6/§7) | 3 | — | 2 | 1 |

**The reservation arithmetic itself is correct.** Every figure in §6's reservation paragraph and table recomputes
cleanly from `((input_bytes + 512) × 1/M + max_output × 5/M)`. Only the *derivation sentence* for USD 0.048640 is wrong
(F5). Worked recomputation at the end of this file.

**Nothing in the proposal presents a simulation result as model evidence.** §10's header, §11's opening two paragraphs
and RESULTS-SIM's banner all carry the disclaimer, and §11's "what it licenses / does not license" pair is accurate.
The §10/§11 problems found are of a different kind: two sentences cite an E5 metric that E5 never computed (F2), and
two cite an E2 number against the wrong arm (F1).

---

## Unsupported (5)

### F1 — The 0.154–0.203 chair contrast was measured on a six-analyst team, not on a generalist (two sentences)

> §1, line 53–55: "The cleanest *mechanism* follow-up is the chair contrast on a single generalist reader
> (full-records vs summary-only vs ledger), which the actor model puts at 0.15–0.20 — registered as secondary, run
> locally."

> §11 risk 1, line 444–445: "…the chair-only contrast on a generalist (E2: 0.154–0.203 in the actor model) is the
> cleanest mechanism follow-up and is registered as such."

**Correction.** E2 computed both chair contrasts on the **`team_ballots` arm with six analysts**, holding the arm fixed
and swapping the chair. No generalist chair contrast exists in E2. The numbers are right (0.154018 and 0.203125); the
architecture they were measured on is not the one named. Either re-attribute them ("the chair contrast on the
six-analyst team") or run the generalist version in the simulation before citing a figure for it.

**Source.** `sim/sim.py:1499-1517` —
`score_arm(case, cfg, "team_ballots", team_reports(case, cfg, 6, "mixed"))` for both the `summary_only - full_records`
and `verified_ledger - full_records` rows; `sim/results/E2.json` pairs list, `chair: "(both)"`,
`max_abs_effect_acceptable` 0.154018 / 0.203125. `sim/RESULTS-SIM.md` E2 does **not** claim a generalist — it says only
"**Therefore run** the chair contrast — `summary_only − full_records` reaches 0.154 — as the primary comparison." The
generalist attribution is introduced by the proposal.

### F2 — E5 computed no "steering rate"; two sentences rest on one (two sentences)

> §10 E5 design consequence, line 415: "…the Bara syndication prediction shows up in the steering rate, so register it
> there, not on the final decision."

> §11 risk 6, line 457–458: "…E5 suggests repetition effects will show up in analyst steering before they show up in
> the authorized decision."

**Correction.** E5 emits four per-configuration quantities only: `analyst_exposure`, `team_exposure`, `acceptable`,
`harmful_target` — all exposure or final-decision measures. There is no steering, vote-movement or
intermediate-persuasion metric anywhere in E5's output. What E5 actually shows is that the syndicated-minus-distinct
difference **on the decision** is +0.002 (naive) and −0.010 (provenance) at m = 8. The inference that the effect
therefore lives in a steering rate is an interpretation with no measurement behind it in this suite. Either add a
steering endpoint to E5 and cite it, or state the claim as a hypothesis ("E5 cannot separate the two; a steering
endpoint would be needed").

**Source.** `sim/results/E5.json` row keys (`m, k, rho_pos, policy, syndicated, decisions, analyst_exposure,
team_exposure, acceptable, harmful_target, harmful_target_ci, in_dose_band`) and `syndication_contrast` entries
(`syndicated`, `distinct_roots`, `difference` — all on `harmful_target`). `sim/sim.py:2355` labels the figure panel
"syndication contrast + steer table", but the panel it draws (`sim.py:2356-2367`) prints only
`syndication_contrast`'s harmful-target rates. The same unsupported leap is already present in
`sim/RESULTS-SIM.md` E5 ("The bara discount shows up in the *steering rate*…") and was inherited.

### F3 — "the eight-call prefix exactly as today" does not describe the first study under either call model

> §1, line 83–85: "In the first study the revision stage is **not** varied (all analysts get private self-review, equal
> calls), so the only social-content difference is at the chair, and the check rule is frozen from the *initial*
> reports so both chair arms share the eight-call prefix exactly as today."

**Correction.** Today's eight-call prefix is **6 initial + 2 checks with no revision round at all**. §1's own sequence
inserts a six-call private revision round before the checks, which makes the shared prefix 14 calls, not 8; and the
first study as sized in §4/§6 runs **T3**, whose prefix is 3 initial + 2 checks = **5** calls. "Eight-call prefix
exactly as today" is true of the *current harness* (T6, no revision) and of no configuration this proposal runs.
Suggested repair: "both chair arms share the full analyst-plus-check prefix, as today" and drop the number, or state
the number for the configuration actually being run.

**Source.** `DESIGN-DIGEST-influence.md:365-393` (canonical loop: 1..6 initial, 7..8 check, 9/10 chair forks) and
`:436-438` — "**There is no revision/peer round in the scenario study.** Analysts write once, in isolation". Standalone
counts at `:378-386`: team 9 = 6 analysts + 2 checks + 1 chair. Proposal §4 table (line 177) and §6 call table
(line 311–317): T3 = 3 + 2 + 1 = 6.

---

## Partial / imprecise / internally inconsistent (12)

### F4 — §7's "first-study sequence" contradicts §4, §6 and §7's own S2 row

> §7, line 332–334: "One dossier under the first-study sequence (6 initial + 6 private revision + 2 checks + 2 chair
> arms + 4 generalist = 20 calls per world, 40 for the two primary worlds, 60 with the truthful-recommendation control)
> exhausts the envelope on its own."

**Correction.** The arithmetic is right (6+6+2+2+4 = 20) but the label is not: this is the **T6 + revision + two chair
arms** sequence of §1, which §4, §6 and §7's own S2 row all exclude from the first study. §6's first-study table makes
one root-world **10** calls (G = 4 + T3 = 6), so one dossier across three worlds is **30** calls, not 60. The two
sections therefore disagree by a factor of two on the same quantity, and §6's "52 attempts — a single root with three
worlds" (line 299–300) is sized off the 10-call model while §7's "exhausts the envelope on its own" is sized off the
20-call model. Pick one; if the intent is to show the *unreduced* sequence does not fit, say so explicitly ("the full
branching sequence of §1, which the first study does not run, would cost 20 calls per world").

**Source.** Proposal §4 line 177 (T3 "first study 3 + 2 + 1 = 6 (no revision round)"); §6 lines 311–317; §7 S2 row
line 345 ("**no revision round** … so the three extra calls per world buy nothing" — three, i.e. T3's revision, not six).

### F5 — USD 0.048640 does not come from "the D7–D9 request sizes"; it is the preflight ceiling at `max_input_bytes`

> §6, line 298–299: "The harness reserves per physical attempt `((input_bytes + 512) × 1/M + max_output × 5/M)` and
> charges the maximum output every time. At the current `max_output_tokens = 3,072` and the D7–D9 request sizes that is
> USD 0.048640 per attempt".

**Correction.** The figure is right; the derivation is not. USD 0.048640 is the **required-quota preflight** value
computed at `max_input_bytes = 32,768`, not at any observed D7–D9 request size:
`(32768 + 512) × 1e-6 + 3072 × 5e-6 = 0.033280 + 0.015360 = 0.048640` — exact to all six decimals. The largest
*measured* encoded request in this lineage was 28,941 bytes, which gives 0.044813. The digest states it as a ceiling
("each ≤ USD 0.048640"), and the per-dispatch reservation uses `len(encoded)`, so actual per-attempt reservations are
below it. Replace "the D7–D9 request sizes" with "the 32,768-byte input cap". The conservatism is correct and the
52-attempt bound still holds; only the sentence is wrong.

**Source.** `DESIGN-DIGEST-influence.md:1097` (`attempts*((max_input_bytes+512)*in_rate + max_output*out_rate)/1e6`);
`:620-625` (`SC/model-config-facts.json`: `max_output_tokens` 3072, `max_input_bytes` 32768); `:618` (pricing USD 1/M
in, 5/M out); `:1099` (D9 campaign cap: "each ≤ USD 0.048640"); `:685` and `:1155` (largest encoded fixture request
28,941 bytes against the 32,768 cap).

### F6 — "52 attempts — a single root with three worlds" does not match §6's own call table

> §6, line 299–300: "USD 2.547488 remains, which is **52 attempts** — a single root with three worlds."

**Correction.** 52 attempts is right (2.547488 / 0.048640 = 52.374 → 52). But by §6's own table one root × three worlds
is **30** calls (3 × (G 4 + T3 6)), so 52 attempts is *one root × three worlds with 22 attempts to spare*, or two roots
× two worlds (40). Under §7's 20-call model it is two-and-a-half root-worlds. The gloss should name the call model it
is using.

**Source.** Proposal §6 call table, lines 311–317 ("three worlds (+ truthful_recommendation) | 30").

### F7 — "typed outputs in D7–D9 were well under 1,024" is not checkable from the digest

> §7, line 335–336: "cut `max_output_tokens` from 3,072 to the measured need (typed outputs in D7–D9 were well under
> 1,024, at USD 0.0118–0.0144 actual per call)".

**Correction.** The USD range is supported exactly — D9-B USD 0.011789 and D7 USD 0.014422 — but the digest records
**no output-token counts for D7, D8 or D9**, so "well under 1,024" cannot be verified from it. The nearest supporting
evidence is from other cohorts: Q4 10,346 output tokens / 56 calls ≈ 185, D2 22,415 / 108 ≈ 208, D3 9,575 / 30 ≈ 319 —
all well under 1,024, but none of them a typed D7–D9 call. Cite the Q4/D2/D3 per-call averages, or mark the 1,024 cap
as a design assumption to be confirmed from the first serialized response.

**Source.** `DESIGN-DIGEST-influence.md:675` (D7 USD 0.014422), `:678` (D9-B USD 0.011789), `:646` (Q4 108,490 in /
10,346 out over 56 calls), `:655` (D2 22,415 out / 108 calls), `:667` (D3 9,575 out / 30 calls). No output-token figure
appears for D7–D9 anywhere in the digest.

### F8 — The proposal's `scope_tbc` acceptable-set rule is the opposite of the simulation's, and the sim's E1 numbers for that family were scored under the rule the proposal rejects

> §2 item 2, line 112–114: "…so the acceptable set is {that alternative} and DEFER is scored as an avoidable deferral
> (the evaluator does not accept "DEFER or alternative" as a disjunction, and v2 does not pretend otherwise)."
> (Repeated in §8 case 2, line 368: "{confirmed alternative}; DEFER is an avoidable deferral".)

**Correction.** The statement is correct **about the swarm-lab harness** — `evaluate()` makes DEFER acceptable only when
no candidate is feasible, and sets `avoidable_deferral = 1` otherwise. But the **simulation** scores the same family the
other way: for `ambiguous_tbc` it appends DEFER to the acceptable set unconditionally. So E1's `ambiguous_tbc` cells —
including the headline "largest clean→contaminated drop under `full_records`: ambiguous_tbc, 0.110 (0.838 → 0.727)"
that §10 uses to recommend running that family under the current chair — were computed under a scoring rule §2
explicitly disclaims. Either re-run E1/E2/E4/E5/E7 with DEFER scored as an avoidable deferral for that family, or state
in §10 that the `ambiguous`/`scope_tbc` cells are sized under a more permissive label than the one v2 will register.

**Source.** `sim/sim.py:764-768` — `elif case["family"] == "ambiguous_tbc": # Correct answer is DEFER *or* the confirmed
alternative / acc = sorted(acc + ["DEFER"])`; `sim/MODEL.md` §2 ("For `ambiguous_tbc` both DEFER and the confirmed
alternative are acceptable") and §3 table row 7 ("unconfirmed → DEFER or the confirmed alternative"). Harness side:
`DESIGN-DIGEST-influence.md:45-64` (`evaluate()`: `'acceptable':acceptable or ['DEFER']`, `'avoidable_deferral':int(defer
and bool(feasible))`). Astra raised the same point from the harness side (`PROPOSAL-REVIEW-astra.md` §B,
"`ambiguous_tbc` cannot generally accept 'DEFER or confirmed alternative'"), and the proposal applied the fix to the
*design* without applying it to the *simulation it cites to size that design*.

### F9 — "the team as a whole is exposed in 99% of episodes even at M = 1" holds only in the ρ_pos = 0.5 slice

> §3, line 157–159: "…E5 shows it is already 0.93 at k = 6 and the team as a whole is exposed in 99% of episodes even
> at M = 1".

**Correction.** True at position boost ρ_pos = 0.5 (team exposure 0.990 at m = 1, k = 1). At ρ_pos = 0.0 team exposure
at m = 1 is **0.51** (k = 1), 0.771 (k = 3), 0.990 (k = 6) — so the claim is a property of a position-boosted slice, not
of the dose design generally. §3's own first study does place a controlled page at rank 1, so the boosted slice is the
relevant one; the sentence should say so ("with a rank-1 placement").

**Source.** `sim/results/E5.json` rows, naive/distinct: ρ_pos 0.0, m = 1 → `team_exposure` 0.40625 (k = 1, syndicated),
0.51/0.771/0.990 across k ∈ {1,3,6}; ρ_pos 0.5, m = 1 → 0.990/1.000/1.000.

### F10 — §10's E5 cell repeats the same unqualified exposure/saturation figures

> §10 E5, line 415: "team exposure (≥1 of six analysts) is 0.990 at M = 1, k = 1 and 1.000 everywhere else — **the team
> is always exposed**; per-analyst exposure is the graded quantity (0.564 at M = 1, k = 1 → 0.931 at k = 6); the
> decision saturates at M = 1 for k = 6 (0.365 flat to M = 8)".

**Correction.** All three numbers are exact — but all three are read off the **ρ_pos = 0.5** rows. "1.000 everywhere
else" is false across the full 216-cell grid (ρ_pos = 0 team exposure ranges 0.406–0.990), and "0.365 flat to M = 8" at
k = 6 is specific to ρ_pos = 0.5 (at ρ_pos = 0, k = 6 the rate climbs 0.25 → 0.365 between m = 1 and m = 4). Add
"at ρ_pos = 0.5" once and the cell is accurate. `RESULTS-SIM.md` has the same omission.

**Source.** `sim/results/E5.json` (dump above); `sim/RESULTS-SIM.md` E5 table, which gives no ρ_pos column.

### F11 — "M ∈ {1..8}" overstates the dose grid

> §10 E5, line 415: "pool 12, M ∈ {1..8} controlled pages, k ∈ {1,3,6}…".

**Correction.** The grid is m ∈ **{1, 2, 3, 4, 6, 8}** — six levels, not eight. Write it as a set.

**Source.** `sim/results/E5.json` rows (216 = 6 m × 3 k × 3 ρ_pos × 2 policy × 2 syndication); `sim/RESULTS-SIM.md` E5
("m ∈ {1,2,3,4,6,8} attacker pages").

### F12 — §1's sequence diagram and §1's prose disagree about which reports the checks are drawn from

> §1 diagram, line 75: "checks     two records fetched by a fixed rule from the REVISED reports … shared ONLY if the
> check rule is frozen before revision (v2 does)"
> §1 prose, line 84: "…the check rule is frozen from the *initial* reports".

**Correction.** These are different mechanisms. Freezing the *rule* before revision does not make its *output*
identical when its inputs (the revised reports) differ by arm — only freezing the *inputs* (drawing the agenda from the
initial reports) does. In the first study, where revision is not varied, the two coincide; in the later crossed study
they do not, and the diagram's parenthetical would then be wrong. State one mechanism: draw the check agenda from the
initial reports.

**Source.** Internal to §1; the harness rule it modifies is `DESIGN-DIGEST-influence.md:395-418` (`checks(reports)`
takes the first two distinct requests from the reports it is handed).

### F13 — "a measured zero" reads as a measurement on a model

> §10 E2 design consequence, line 412: "drop ballots-vs-evidence under the current chair (a measured zero, not an
> underpowered effect)".

**Correction.** It is a measured zero *in the scripted actor model* — the exact distinction §11 spends two paragraphs
establishing. The surrounding table header and §11 do carry the label, so this is wording drift rather than a false
claim, but "measured" is the one word §11 reserves for things that are not this. Suggest "a structural zero under the
actor model".

**Source.** `sim/results/E2.json` (`provable_zero: true` across perfect play + all 12 competence cells);
`sim/RESULTS-SIM.md` banner and the proposal's own §11 opening.

### F14 — `PROPOSAL-REVIEW.md` labels an adopted Astra point as "partly declined"

> `PROPOSAL-REVIEW.md:22-26`: "One Astra point is **partly declined**: it suggested that a perfect neutral baseline
> leaves ample room for deterioration and that non-zero clean error is not required. The simulation (E1) agrees that
> ceiling cells can still show a contamination effect, so the admission gate here is "non-zero maximum effect under the
> actor model", not "non-zero clean error"; controls are exempt."

**Correction.** Both halves of the Astra point were **accepted**: Astra asked that non-zero clean error not be
inherited as a gate and that controls be exempt, and the proposal does exactly that (§7 S0 gate is a maximum-effect
gate; §2 exempts controls). Nothing is declined. Relabel as "accepted, implemented as a maximum-effect gate" — or, if
something *was* declined (keeping an admission gate at all), say which. The supporting E1 fact is correct:
`ambiguous_tbc` under `full_records` sits at clean 0.8375 — above the 0.80 ceiling — and still drops 0.110 to 0.727.

**Source.** `PROPOSAL-REVIEW-astra.md` §A5 ("Exempt controls from discrimination gates… The prior assessment's
suggestion that nonzero clean error is necessary should not be inherited uncritically"); proposal §7 S0 gate row
(line 343) and §2 family-set paragraph (line 131–133); `sim/results/E1.json` `clean_vs_contaminated`
(`ambiguous_tbc`, `full_records`, `team_ballots`: clean 0.8375 → contaminated 0.727083, drop 0.110417).

### F15 — The provenance line claims a numbers check that has no record and that this pass did not reproduce

> Header, line 11–13: "…and a numbers check of this text against the simulation's own JSON."

**Correction.** No numbers-check artifact exists in the scratchpad: `PROPOSAL-REVIEW.md` carries only the Astra
design-review dispositions, and `CHECKPOINT.md` still lists "Opus numbers-check vs sim JSON -> PROPOSAL-REVIEW.md" as a
**NEXT** item. This pass is that check, and it found F1, F2, F9, F10 and F11 — five sim-attribution defects a completed
numbers check should have caught. The sentence describes planned work as done. Either run the check and keep its record,
or drop the clause until there is one.

**Source.** `CHECKPOINT.md` ("RUNNING: sim agent. NEXT: fold sim into 6/10/11; Opus numbers-check vs sim JSON ->
PROPOSAL-REVIEW.md"); `PROPOSAL-REVIEW.md` in full (a design-review disposition table, no numeric verification).

---

## Reservation arithmetic, recomputed from the digest formula

Formula (`DESIGN-DIGEST-influence.md:1091`): `((len(encoded) + 512) × input_rate + max_output × output_rate) / 1e6`,
with `input_rate = 1`, `output_rate = 5` USD per million (`:618`).

| quantity | proposal | recomputed | verdict |
|---|---|---|---|
| per attempt at `max_output` 3,072, input 32,768 B | USD 0.048640 | `(32768+512)×1e-6 + 3072×5e-6 = 0.033280 + 0.015360 = ` **0.048640** | ✅ exact — but attributed to "the D7–D9 request sizes" (F5); it is the `max_input_bytes` preflight ceiling |
| remaining | USD 2.547488 | `8 − 5.452512 = ` **2.547488** | ✅ |
| attempts remaining | 52 | `2.547488 / 0.048640 = 52.374 → ` **52** | ✅ |
| logical calls with one retry reserved | 26 | `52 / 2 = ` **26** | ✅ |
| per attempt at `max_output` 1,024, input ~3 KB | "roughly USD 0.008–0.010" | `(3072+512)×1e-6 + 1024×5e-6 = 0.003584 + 0.005120 = ` **0.008704** (at 3,000 B: 0.008632) | ✅ inside the stated band |
| 12 roots × 2 worlds × (G+T3) = 240 attempts | ≈ 2.2 | `240 × 0.009 = 2.160`; at the exact 0.008704, **2.089** | ✅ conservative; fits in 2.547488 |
| 12 roots × 3 worlds = 360 attempts | ≈ 3.2, "does not fit" | `360 × 0.009 = 3.240`; exact **3.133** | ✅ both exceed 2.547488 |
| 24 roots × 2 worlds = 480 attempts | ≈ 4.3, "does not fit" | `480 × 0.009 = 4.320`; exact **4.178** | ✅ both exceed 2.547488 |
| unit accounting | 12 roots · 24 cells · 48 decisions · 240 calls | `12×2 = 24` cells; `24×2 = 48` decisions; `12×2×(4+6) = 240` calls | ✅ internally consistent |

**Verdict on §6's arithmetic: correct throughout.** The only defect is the attribution sentence (F5), and the only
knock-on is that 0.048640 is a ceiling rather than a rate, which makes the 52-attempt figure a conservative lower bound
— the direction a budget bound should err in.

## Call-count table, §6 vs §4 vs the digest

| arm | §6 | §4 | digest standalone | verdict |
|---|---:|---|---|---|
| G | 4 | "1 generalist, full union, 2 targeted, self" = 1+2+1 | 4 (`:382`, "1 report + 2 checks + 1 chair") | ✅ |
| T3, first study | 6 | "3 + 2 + 1 = 6 (no revision round)" | — (T3 is new) | ✅ consistent |
| T3, with revision | 9 | "with the later revision round 9" | EIv2 shape: 3+3+2+1 | ✅ |
| T6, first study | — | "6 + 2 + 1 = 9" | 9 (`:380-381`) | ✅ |
| T6, with revision | — | "with revision 15" | EIv2: 6+6+2+1 = 15 (`:975`) | ✅ |
| one world (G + T3) | 10 | — | — | ✅ |
| **one world, §7's "first-study sequence"** | — | — | — | ❌ **20** (F4) — §7 uses the T6 + revision + two-chair-arm sequence and calls it the first study |

---

*Verification pass only. The proposal was not rewritten and `swarm-lab` was not touched.*
