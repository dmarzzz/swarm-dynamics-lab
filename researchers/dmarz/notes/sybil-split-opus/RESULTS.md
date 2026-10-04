# Results: identity splitting with fixed attacker resources (Opus 5.5)

Completed 2026-10-04. Exploratory chain 001 at source hash `95889bea…` (launch commit `75d51695`, code `0b8a444a`), operator dmarz/orchestrator-2, ready request agentops #252. All four stages ran once: S0 1,853/1,853 scripted rows, P0 1/1, Q0 60/60, S1 2,688/2,688. No row failed, was retried or went unstarted. Total model cost USD 45.38592 over 2,749 calls. Same-researcher check only; the run is not independently reviewed. Sanitized records are in [records/](records/); the post-run review is [reviews/chain-001-post.md](reviews/chain-001-post.md).

## Primary contrast

Informative checks (attacker passes a check 10% of the time), 12 checks, model answers, paired by root, mean of the two graph-family means:

| Rare-skill wrong answers | k = 1 | k = 3 | k = 9 | k = 27 | 27 minus 1 |
|---|---:|---:|---:|---:|---:|
| `degree`, 12 checks | 7.6% | 17.4% | 43.8% | 56.2% | +48.6 (+35.4 to +61.1) |
| `coverage`, 12 checks | 0.0% | 0.0% | 4.2% | 7.6% | +7.6 (+2.8 to +13.2) |
| `random`, 12 checks | 0.7% | 0.0% | 0.0% | 3.5% | +2.8 (−0.7 to +6.9) |

**Primary (degree change minus coverage change): +41.0 percentage points** (descriptive 95% bootstrap interval +27.8 to +54.9; 48 of 48 roots complete). By family: ring +50.0 (+31.9 to +68.1), community +31.9 (+11.1 to +52.8). The predicted direction was positive with a 10-point useful size; the scripted plurality calibration on engineering roots had given +0.41, and the model gives the same value on fresh roots. With every outcome present, the all-assigned bounds equal the estimate.

Splitting the same 27 rows, 27 edges and 27 verification attempts across more identities made the attacker far more harmful when admission spent its checks on well-connected identities (`degree`), and barely more harmful when it spread checks across the graph (`coverage`) or chose them at random.

## Secondary outputs (prespecified, descriptive, no multiplicity correction)

- Primary at 4 checks: +50.7 (+38.2 to +63.2).
- Primary scored on rare-skill accuracy instead of wrong answers: −20.8 (−31.9 to −9.7). Splitting lowers accuracy more under `degree` than under `coverage`, so the harm is not only a shift from abstention to wrong answers.
- Same packets answered by deterministic plurality: +44.4 (+31.9 to +56.9); by identity-level plurality: +42.4 (+29.2 to +55.6). The model and the scripted rules agree on the primary.
- The primary with `random` in place of `coverage` (degree change minus random change, 1 to 27 identities): +45.8 (+32.6 to +58.3). Random change minus coverage change: −4.9 (−11.1 to +0.7).
- **Unreliable checks** (attacker passes 90%): the primary reverses, −52.8 (−70.2 to −34.0); ring −19.4, community −86.1. With unreliable checks a single attacker hub (k = 1) passes and dominates `degree` and `coverage` packets; splitting reduces that. Under `coverage` at 12 checks wrong answers rise from 0.0% (k = 1) to 34.0% (k = 27), under `degree` they fall from 74.3% to 55.6%. This was a prespecified stress condition; the engineering calibration had predicted a negative value (−0.16).
- No verification: wrong answers 48.6%, 40.3%, 56.9%, 41.0% at k = 1, 3, 9, 27 (attacker row share falls from 33.8% to 8.4% as identities split and fewer are seated).
- Model minus plurality on rare-skill wrong answers, mean over 56 pooled cells: −30.6 points (range −90.3 to +8.3). Opus abstains where plurality would pick a fabricated value, mostly in packets where the attacker's rows are the only rare-skill evidence.
- Repeated packets: 767 packets appear more than once across cells (1,554 calls); 727 of those groups received identical answers.

Full per-cell table: [records/s1-cells.csv](records/s1-cells.csv) (family × check strength × policy × budget × k: model wrong/abstain/accuracy, plurality wrong, attacker row and seat share, specialist retention, cost).

## Interpretation and limits

Supported (exploratory, this synthetic task and configuration): with a fixed attacker budget and informative checks, splitting across more identities raises harmful synthesized answers much more under degree-ranked admission checks than under coverage or random checks, for an Opus 5.5 synthesizer, in both graph families. Not supported: any claim about published Sybil defenses (none implemented), other population sizes, fabrication types or attachment rules, or other models. Attacker-internal links are free and vary with k, so k changes both the partition of resources and the attacker's internal structure (without those links the scripted primary is about zero; see SETUP.md). Under unreliable checks the sign reverses; neither policy is safe there. Roots are development-sized (24 per family).
