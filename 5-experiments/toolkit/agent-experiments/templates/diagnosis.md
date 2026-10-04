# Diagnosis for [study / attempt]

Embed this worksheet in the existing post-mortem or next-run plan. Follow [DIAGNOSIS.md](../DIAGNOSIS.md); fix links when copying. This is evidence-guided judgment, not an approval receipt or new scoring system.

- Attempt/source/configuration; evidence and manual/automated trace coverage:
- Practical decision and unresolved need; what the previous result already answers:
- First observed divergence, or evidence for a ceiling/floor; affected outcome:
- Limiting stage: evidence acquisition / interpretation / coordination / execution / verification / unresolved. Is the work independent, coupled, serial or batchable?

| Explanation | Supporting and contradicting evidence | Confidence / missing evidence | Smallest discriminating check |
|---|---|---|---|
| Candidate cause | Paths and hashes where available | Observed / supported / plausible / unresolved | Offline first; specify falsifier |
| Strongest alternative | Paths and hashes where available | Same labels | Different predicted observation |

- Strongest relevant simple baseline; capability evidence and any defect repaired:
- Comparator information, tools, ownership/handoffs and conflict protocol; all coordinator/tool costs:
- Proposed case changes and why they reflect a real need; sufficient evidence or correct abstention, label validation, no leakage:
- Clean/adverse controls; answer-changing and answer-preserving variants where applicable:
- Independent task/incident units and count; dependencies; development exposure and untouched holdouts:
- If scaling: fixed-resource or added-capacity estimand; tool slots, aggregate compute, deadlines, actual tokens and total cost. Otherwise mark not applicable:
- Offline implementation/validation completed; unresolved gaps and explicit acceptance checks:
- Why saved evidence is insufficient for any proposed native collection; finite calls/time/cost, stopping and decisions by outcome:
- Disposition: RUN / DECISION NEEDED / HOLD / FINISH / PARK. Exact next action, authority, original cumulative exposure and responsible task:

A valid negative result can finish the study. Do not weaken baselines, lower acceptance thresholds or manufacture difficult cases to obtain a preferred effect.
