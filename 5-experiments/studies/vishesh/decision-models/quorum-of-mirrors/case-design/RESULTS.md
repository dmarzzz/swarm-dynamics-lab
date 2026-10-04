# Better cases: test evidence, not just vocabulary

**Completed 24 new development cases organized as 12 matched scenario pairs.** Nine automated checks pass, including label agreement, input-order and identifier invariance, missing/cyclic provenance refusal and duplicate-path handling. These are authored synthetic examples inspected by the owning operator, not independently authored/adjudicated, representative real records, untouched evaluation data, or native model trials. [Readable casebook](CASEBOOK.md), [complete packets and labels](cases.json), [all controller outputs](outcomes.json), [prospective plan](PLAN.md).

## What makes a good or bad case here?

| Dimension | Good case | Bad case |
|---|---|---|
| Identifiability | Actor-visible evidence establishes the origin, or the target explicitly requires abstention | Hidden author knowledge supplies an origin that the actor cannot recover |
| Mechanism | Same text from different acquisitions; different wording copied from one source | Only substituting dictionary synonyms and calling the task realistic |
| Trust boundary | Authenticated bindings are distinguished from an untrusted claimed receipt ID | Treating a plausible ID or matching text as proof |
| Paired controls | Change one evidence property and say whether the answer should change | Change wording, prior opinions, order and schema together and attribute the difference to one cause |
| Counting evidence | Resolve source identity separately from supplied dependence constraints | Assume every unique receipt is statistically independent |
| Realism | Plausible forwarding, duplicated templates, missing bindings and conflicting source records, with declared assumptions | Invent impossible puzzles or remove essential information solely to defeat lookup |
| Evaluation | Keep ordinary controls, ambiguity and failure cases; report each outcome | Select only baseline misses or model successes, or silently remove unanswerable cases |
| Generalization | Freeze controls and split future evaluation by scenario, acquisition and authoring template | Reuse inspected pairs as a holdout or count variants as independent worlds |

The old synonym-assisted set established fit to six wording templates. It did not establish actual provenance from semantic resemblance. A unique text match in a candidate list is not sufficient unless the task explicitly supplies a trusted, complete binding contract. The new cases repair that epistemic boundary; they do not retrospectively change old labels or outcomes.

## Six concrete challenge families

| Family (two scenario roots each) | Matched change | Expected behavior |
|---|---|---|
| Paraphrased copy | Remove the authenticated binding, leave words unchanged | Resolve with binding; DEFER without it |
| Identical independent observations | Remove the binding distinguishing two same-text acquisitions | Resolve the bound receipt; DEFER when indistinguishable |
| Misleading claimed reference | Remove trusted binding while keeping a wrong claimed ID | Follow trusted binding when present; never accept untrusted ID alone |
| Forwarded copy | Replace a direct link with a two-hop relay | Same acquisition and same evidence count |
| Dependence metadata | Change shared/unknown group to a supplied new group | Same source; change counting disposition. Unknown dependence is DEFER |
| Multiple origin paths | Change a convergent branch to terminate at a second acquisition | Multiple routes to one root resolve; distinct roots require DEFER |

Examples are loading-bay and reservoir observations, archive humidity and parcel weighing, freezer and bridge readings, ventilation and lift inspections, warehouse probes and clock monitors, pump and valve checks. Names are illustrative and do not supply domain validation. The actual packet makes no medical or operational decision.

For example, two archive-room sensors both record “Humidity was 45 percent at 10:00.” Text alone cannot say which sensor supplied a forwarded report. A trusted report-to-receipt binding makes it answerable. Deleting that one binding must change the answer to DEFER, not to the first or most similarly worded candidate.

A different pair inserts a forwarding hop into a ventilation report. The correct source must remain the same. That is a robustness control, not an additional independent observation. Mutating the report's factual statement also leaves its recorded origin unchanged: source identity does not certify content accuracy, and this suite does not score semantic entailment or factual admission.

## Offline results and fair-comparison limits

Across 24 cases, 16 have a unique origin and eight require source abstention. Fourteen permit NEW_GROUP under stipulated dependency metadata, one is KNOWN_GROUP and nine require counting DEFER (including one uniquely sourced receipt with unknown dependence). NEW_GROUP is a registry disposition, not empirical proof of independence.

| Controller | Correct origin /24 | Correct origin + counting /24 | Wrong source admissions | Unsafe new-group admissions |
|---|---:|---:|---:|---:|
| Frozen reference lookup | 6 | 6 | 4 | 4 |
| Frozen normalized text | 8 | 8 | 0 | 0 |
| Frozen lexical | 8 | 8 | 0 | 0 |
| Frozen synonym hybrid | 6 | 6 | 4 | 4 |
| Authenticated graph traversal | 24 | 24 | 0 | 0 |

**These rows are not an effectiveness contest under equal contracts.** The old controllers ignore origin edges and treat claimed references as authoritative; they were written for the old assumptions. Their failures demonstrate a contract mismatch and the risk of reusing them unchanged. They do not establish model headroom. The graph controller receives the relevant evidence, uses no gold labels or language dictionary, and is the appropriate strongest baseline for this task. Its 24/24 is software validation on authored cases, not a measured population success rate.

The graph resolver independently traverses all reachable branches, requires one in-event receipt, and refuses dangling paths, cycles, duplicate receipt IDs, roots with outgoing origins, and multiple roots. Hand-declared gold labels live outside actor packets. Mutation checks test order/opaque-ID invariance, text changes, duplicated edges, unknown dependence and deliberate invalid graphs. This same-operator construction and checking are not an independent code or label audit.

Reproduce from this directory:

```sh
python3 cases.py
python3 -m unittest discover -s . -p 'test_*.py'
```

## Assessment and next action

Question and usefulness improve: the tests now distinguish source identification from admission of evidence and refuse unknowable ancestry. Controls improve through matched variants and an exact graph baseline. Realism remains limited by synthetic authentication, small authored scenarios and supplied dependence metadata. Precision is coverage of six failure mechanisms across 12 authored roots, not 24 independent statistical trials. Data collection is complete for offline outputs; there are no model responses or missing native observations this cycle. Labels, packets, baseline hashes and all outcomes are published; the static casebook is appropriate because no temporal agent activity occurred.

**FINISH / PARK native dispatch; offline case revision complete.** These cases provide better regression and qualification material for a provenance-aware system. They do not justify a native semantic resolver: exact traversal solves the declared task. A useful further development branch would separate source binding from faithful extraction of claim, time, entity and negation in real or varied independently authored reports, with externally supportable labels and a strong parser baseline. That would be a new claim-fidelity question and must be prospectively designed, not smuggled into source-origin scoring. No new holdout or native adapter has been built, and no owner launch decision is requested on this package.

The prior conditional 8+24-call proposal is still not admitted. Its text-matching-to-origin premise needs the explicit trust distinction documented here before reuse. All old attempts, tests and negative results remain preserved. No machines, credentials, API calls or budget mutations: historical exposure remains 49 calls/$0.065856 reserved, $0.00171696 known actual plus $0.001344 bounded unknown, within the unchanged original $1 API/$1 infrastructure authority.
