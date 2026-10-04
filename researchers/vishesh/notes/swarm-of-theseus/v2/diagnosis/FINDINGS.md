# Theseus rule-application diagnosis

**The repaired model can state the right rule and still produce inconsistent decisions. The harness also has two diagnostic-design defects: learner instructions leak into the explicit-rule control, and qualification never tests stale ledger/canary evidence.** These findings narrow the problem considerably, but do not identify one causal model failure.

This is a retrospective audit of all saved S0 and S0-repair evidence: 48 calls, 288 decisions, 70 incorrect decisions. No additional model calls, spending, or experimental runs. Original outcomes and gates are unchanged. See [analysis scope](PLAN.md), [reproducible audit](audit.py), [machine-readable findings](audit.json), and [case annotations](ceiling-error-annotations.json).

## What is ruled out in these records

The independent audit agrees with all 288 scores. Every request joins to its durable call-start record; every result matches its call-finish record. All 48 responses ended normally and contain exactly six unique, valid commands. No case-ID mismatch, missing row, invalid console command, truncation or provider error explains the failures.

All 144 current rows in the repaired exact user text reproduce the structured observations field for field. All 12 repaired ceiling prompts contain the correct explicit rule and omit history, feedback and prior notebooks. Historical examples uniquely identify the original governing source in every audited class/history pair. Thus malformed table serialization, missing explicit rules and ambiguous founding examples do not explain these observed errors. This checks the saved client request, not the provider's internal tokenization or execution.

## The strongest behavioral evidence

| Repaired control | Correct / decisions | Wrong decisions |
|---|---:|---:|
| Explicit-rule incident | 22/24 | 2 |
| Explicit-rule release | 20/24 | 4 |
| Explicit-rule migration | 17/24 | 7 |
| All explicit-rule tasks | 59/72 | 13 |
| Historical learners, both checkpoints | 52/72 | 20 |

Manual inspection finds the correct class-to-source mapping in all 12 repaired ceiling notebooks. That does not prove a stable internal representation, but it rules out the claim that every error arose because the output could not articulate the mapping.

Seven of the 20 repeated-input groups in the ceiling outputs disagree internally: cases with the same class and the same governing signal/freshness receive different actions within one response. For incident, freshness is excluded from the equivalence key because it is irrelevant. The rest of each row can differ; this is a test of invariance to information the rule declares irrelevant, not literal duplicate prompts. These seven groups occur in seven separate calls. The learner outputs contain nine inconsistent groups out of twenty.

Three directly inspectable failure types:

1. **Wrong evidence asserted in the notebook.** For release world 302, changed checkpoint, B:0 has ledger `signal=YES, fresh=YES`. The command is hold and the notebook says ledger freshness is NO. For migration world 302, changed checkpoint, both B:1 and B:2 have ledger signal YES; the notebook calls both signals NO. These are observable false evidence statements; notebooks are not trusted explanations of internal reasoning.
2. **Correct evidence stated, wrong action emitted.** Release world 302, stable checkpoint, B:0 is explicitly described as ledger YES/YES in the notebook, yet both its notebook action and command say hold. Misreading the values alone cannot explain this particular output.
3. **Notebook correction fails to change the decision.** In that same release response, B:1 is emitted as ship. The notebook correctly says ledger NO/YES and explicitly corrects the action to hold, but the machine-readable decision remains ship. The current interface has two competing action representations and no final consistency reconciliation.

The case annotations classify all 13 repaired ceiling errors: seven explicit false evidence/condition statements, one correctly stated evidence with wrong action, one notebook/command disagreement, and four without a specific case-level notebook diagnosis. Categories describe the saved text; they are not validated causal categories.

Ten of the eleven release/migration ceiling mistakes are false holds, and one is a false ship. That is a strong descriptive asymmetry in this small sample, not evidence for a general safety bias. No fixed wrong-source, class-swap or adjacent-row-shift candidate reproduces all decisions. Migration's outputs match an always-probe candidate on 19/24 decisions versus 17/24 for the correct rule, but also match an all-sources-ready candidate on 19/24. This non-uniqueness is exactly why signature matching cannot identify the mechanism. Valid new-console commands also mean these records do not establish a command-syntax migration failure.

## Confirmed design defects

### The ceiling is still told to behave like a learner

`runner.qualification` supplies the same `instructions(scenario, 'rolling')` to both arms. In every repaired ceiling request the system text says:

> Each service class has ONE unknown governing source.

It then tells the actor to learn the source from accepted examples or inherited records and says current answers are withheld. The user message supplies an authoritative current rule, and the clean ceiling contains no historical examples at all. The missing distinction makes the control less clean than its name implies. It is a verified instruction mismatch, not a proven cause: the model still writes the correct mapping in all 12 ceiling notebooks.

**Repair:** use a separate explicit-rule executor instruction with no acquisition, inheritance, environmental-change or withheld-rule language. Keep learner instructions separate. Compare the old and corrected instruction on matched fresh worlds before attributing any benefit to it.

### Qualification freshness coverage is incomplete and coupled to ID

The generator uses `(step + index + source_index) % 5 != 0`. Both tested checkpoints are multiples of five; indices are 0, 1, 2. Therefore only probe at index 0 is stale. Across all 288 current decisions, ledger freshness is always true and canary freshness is always true; probe is stale 96 times. Both class rows ending in index 0 always have stale probe evidence. The fixed checkpoint spacing reproduces the same freshness mask.

The model sometimes attributes this probe staleness to a governing ledger/canary source. That is compatible with cross-column contamination, but the record cannot establish causation. The coverage omission is certain: the supposedly general conjunction ceiling does not actually test every source's stale/positive condition.

**Repair:** balance signal/freshness combinations for each governing source, separately for each class. Independently balance irrelevant sources. Use opaque case IDs unrelated to the bit mask and randomize row order independently. Require a coverage table to pass before dispatch. Those changes belong to a new instrument version, not a retrospective adjustment of the failed gate.

### The changed learner checkpoint is not evidence of failed adaptation

For release/incident, the world changes at step 5. That request has the old labeled history and feedback from step 0, with no labeled observation of the new mapping. It cannot uniquely infer which new mapping now applies from unlabeled current cases alone. Consequently, changed learner accuracy should remain descriptive; the existing gate correctly uses only stable learner accuracy. A later adaptation study must specify when new evidence first makes the change identifiable and measure after that point. Migration holds the mapping fixed, so this particular limitation does not apply to it.

## Concrete next diagnostic

The old culture pilot remains blocked. The next model test should isolate execution rather than add more turnover:

- First fix instruction-mode consistency and validate balanced input coverage offline.
- Freeze a small paired diagnostic crossing **one case versus six cases** with **decisions only versus decisions plus notebook**, using the same fresh worlds and explicit rules. Prespecify whether comparisons match cases, calls or tokens; these budgets are not interchangeable.
- Include the old instruction as a matched diagnostic comparator if attributing an improvement to that fix. Do not bundle an instruction change with formatting changes and then name a cause.
- Measure exact action accuracy, false holds/ships, invariance across equivalent relevant inputs and notebook/command disagreement. Report by independent world; do not treat each row as an independent replicate.
- Use a separate structured evidence-selection probe only if distinguishing source selection from Boolean application is still necessary. Do not silently replace agent decisions with an oracle. A deterministic executor is a different architecture and a useful later comparator.

No claim that any of these changes improves model performance is made here. The practical diagnosis is now narrower: **observable rule-to-row/action inconsistency, including false evidence statements and unresolved output corrections, in an instrument whose ceiling prompt and input coverage also need repair.** It is not yet a cultural-memory failure, and scaling crew count would not resolve it.

## Reproduce

Run `audit.py SAVED_RESULTS_ROOT audit.json` with the original S0 and S0-repair folders from the two published evidence packages. It reads evidence only, asserts the joins/score/table checks and writes all error cases, descriptive signature matches, equivalent-input groups, freshness coverage and SHA256 hashes of all 48 input events. Manual annotations identify exact cases and quote the recorded notebook. This is a same-author audit, not independent scientific review.
