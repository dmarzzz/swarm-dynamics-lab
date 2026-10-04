# Better cases for what copied reports actually say

**Added 32 authored development cases across eight source scenarios.** They test whether a report faithfully expresses its known source: SUPPORTED, CONTRADICTED, or NOT_ESTABLISHED. This is an explicit exploratory extension beyond the previous provenance-only contract; it is not a new native experiment. [Read all cases and rationales](CASEBOOK.md), [complete actor packets and gold labels](cases.json), [all diagnostic outputs](diagnostics.json), [prospective plan](PLAN.md).

## Why another revision?

The first set overfit six synonym templates. The second improved source attribution but could be solved entirely by traversing authenticated links. That is useful engineering, yet it leaves the central practical failure untested: a report can accurately cite an inspection while misrepresenting its finding. Ten copies of a misrepresentation remain one misrepresented source.

The new set holds source binding fixed and changes only the claim. Each source has a literal supported control, a supported reformulation, a contradiction, and an unestablished claim. The latter two are deliberately separate: lack of a later reading does not prove the later reading would be false. Authentication is assumed for these synthetic packets; no external truth is verified.

## Good and bad cases for this extension

| Good case | Corresponding bad case |
|---|---|
| Same entity and time, a negation changes the claim | Different entities, times and source quality change together |
| A copied report silently replaces 09:00 with 10:00; both readings are supplied | Ask the actor to infer an unrecorded transition time |
| An equivalent unit conversion versus a thousand-fold unit error | Treat superficial numeric similarity as correctness |
| “Exactly three of four” versus “all four,” with explicit source count | Score an unstated pump identity using the author's hidden knowledge |
| A schedule versus a completion report, with unknown completion status | Call “not recorded” a confirmed failure to complete |
| A quote versus a measurement, with explicit copy relation | Infer actual temperature or independence merely from a citation |
| A corrected entry versus its superseded value | Assume the corrected record certifies physical reality |
| Both supported and misleading high-overlap claims; controls and abstention remain | Select only spectacular errors or only baseline misses |

The eight families are polarity, time, entity, units, quantifiers, plan/completion, attribution and corrections. Example: “At 09:00, valve A was closed. At 10:00, valve A was open.” The claims “open at 10:00,” “not closed at 10:00,” “closed at 10:00,” and “open at 09:30” receive SUPPORTED, SUPPORTED, CONTRADICTED and NOT_ESTABLISHED respectively.

These are interpretable mechanisms rather than a representative survey of incident reports. Cases are authored by the same operator who specified their labels; no independent authoring or adjudication is claimed. The trust contract deliberately defines binary opposites and standard unit conversion, avoiding hidden domain assumptions. The authored order includes easy controls; it must be shuffled and identifiers relabelled if ever adapted to model inputs.

## What the offline diagnostics show

| Diagnostic | Correct relation /32 | False support | Missed supported claims |
|---|---:|---:|---:|
| Always NOT_ESTABLISHED | 8 | 0 | 16 |
| Exact normalized source-clause match | 16 | 0 | 8 |
| Token overlap >=0.65 | 16 | 7 | 6 |

The two lexical diagnostics have identical total accuracy but materially different false-support behavior. Seven times, overlap accepts a claim that the source contradicts or does not establish. This makes total accuracy alone inadequate. Full outputs retain every case, including the controls. No diagnostic can identify contradiction; their limited performance is expected from their declared algorithms.

**These are not strong semantic baselines and their misses do not demonstrate model headroom.** They diagnose traps in similarity-based admission. A capable compositional parser/rule system has not been implemented for this new contract. A structured gold oracle would have privileged information and would not be a fair comparator. Do not claim that a model is necessary until the stronger comparator and varied development cases are evaluated.

Eight automated checks pass: all IDs and 16/8/8 labels, eight groups of four with fixed sources, evidence-span presence, actor/gold separation, literal controls, complete output coverage, selected unknown-versus-false labels, and duplicate-report/source-order invariance. Ninefold report repetition is a software mutation of the same packets, not nine new observations. These checks verify structure and intended relationships; they do not independently prove semantic labels. Each source/claim/rationale is exposed in the casebook for inspection.

## Evaluation and progression

For a future model comparison, score three-class fidelity, false support, missed support and per-family confusion separately. Require a faithful source citation/evidence span, keeping answer labels and rationales out of inputs. Invalid/missing answers remain visible and receive no correct-resolution credit; do not hide them as valid NOT_ESTABLISHED responses. Preserve source identity and dependency checks in shared downstream code. A supported claim is not automatically independent, current, reliable, or safe to act on.

These 32 variants represent eight authored scenario units, not 32 independent worlds. No inferential confidence interval, safety guarantee, native capability or swarm benefit is claimed. The test labels and wording have been inspected, so none is an untouched holdout. A future split must separate sources, scenarios and linguistic construction families; repeat counts, paraphrases and order changes stay with their parent. Larger n from the same templates would not resolve the realism gap.

**HOLD native progression; requested offline case revision complete.** Next useful preparation is a frozen compositional baseline handling negation, entity/time binding, unit conversion, quantifier scope, modality, attribution and correction precedence, followed by varied independently authored or properly sourced development records. Do not hand-tune on a sealed evaluation set. Evidence of safe useful gain must precede any separately prepared native plan and concrete scope decision. This request did not authorize or launch a paid successor.

No new calls, machines, credentials or spending. Historical exposure remains 49 calls/$0.065856 reserved; known actual $0.00171696 plus $0.001344 bounded unknown. Original $1 API/$1 infrastructure authority is unchanged. Earlier case sets and negative Q1 results remain preserved, and the original swarm-efficacy confidence is unchanged.

Reproduce: `python3 build.py` and `python3 -m unittest discover -s . -p 'test_*.py'` from this directory. The casebook is the static comparison view; no temporal activity or agent reasoning is invented.
