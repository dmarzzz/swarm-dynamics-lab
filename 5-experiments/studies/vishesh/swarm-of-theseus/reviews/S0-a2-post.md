# Post-mortem: S0-a2

- Experiment / owner / stage / date: swarm-of-theseus / vishesh/codex-theseus / S0 / 2026-10-04 UTC.
- Source: 4c1272651eecf4d2ceef3dd6ebd4e473c08be066; pre-run S0-a2-pre.md; parent setup failure S0-a1.
- Disposition: repair-and-rerun. S1 blocked.

## What ran and what happened

12 planned → 12 started → 12 terminal → 8 complete trajectories plus 4 explicit failures → all 12 included in conservative scoring. 61/72 scheduled frames retained. All four observatory outcomes ended with sanitized PolicyError; no invisible retries. Actual 257 calls, 149,887 input tokens, 62,188 output tokens, estimated provider usage USD 0.460827; no missing usage. Conservative quota reservation USD 1.535697, not invoice spend.

Verbatim competence: seed bank 0.9375 accuracy / 0.9167 convention; repair dock 0.625 / 0; observatory 0 / 0 with all outcomes failed (not measured zero competence). Qualification failed. Founders also drifted: seed bank 0.875 accuracy / 0.1667 convention, repair dock 0.625 / 0. These are diagnostic outcomes under an inadequate response contract, not channel-transmission results.

## Visualization review

Latest/final 1600x900 PNGs and per-run HTML replays uploaded. All 61 scored frames remain in append-only events and history; missing observatory steps must remain gaps. Playback/metric audit accompanies downloaded results. No frames manufactured for failures. The public hub displays the plan and live metric progression; native custom HTML embedding is unsupported and the downloadable replay is the fallback.

## Experiment-quality assessment

Confirmed from synthetic traces: (1) convention sometimes contains the whole procedure instead of the receipt phrase; (2) notebooks exceed the hidden 600-character truncation boundary and contain case calculations; (3) some answer arrays contradict the calculations written later in the same output; (4) duplicated reports are sometimes counted as independent in observatory even with verbatim instructions. These show output-contract and capability issues. The notebook limit and convention field semantics should have been explicit in the prompt. Token-limit termination is a plausible cause of PolicyError in long observatory responses, but v1 did not preserve the sanitized reason, so this is not established for each failure.

The scorer's objective labels are independently auditable; model explanations do not override wrong actions. The adverse outcomes are preserved. No inheritance arm has been run, so useful culture survival remains unanswered. Process preflight succeeded for every launched condition, distinct from scientific qualification failure.

## Failure and repair ledger

| ID / kind | Evidence | Cause confidence | Repair | Acceptance | Status |
|---|---|---|---|---|---|
| CONTRACT-1 / field semantics | convention contains prose, memory exceeds 600 chars | verified ambiguity in prompt | define receipt-only field and memory bound explicitly | >=0.8 fresh verbatim convention in every scenario | pending S0-a3 |
| CONTRACT-2 / action computation | returned labels contradict later notebook calculations | verified trace inconsistency; causal attribution not proven | case-ID keyed evidence/result/label before notebook; no case histories in memory | >=0.85 fresh verbatim accuracy in every scenario | pending S0-a3 |
| EXEC-1 / provider error | four PolicyError outcomes | exact reason unrecorded | concise work contract, 1,024-token ceiling, sanitized error_reason | zero failed outcomes | pending S0-a3 |
| SETUP-1 / public fetch | every S0-a2 condition preflight passed before inference | verified successful rerun | retain fail-closed cache | passed receipts | closed |

## Next run

Read this assessment before S0-a3. Fresh seeds 104/105, same three scenarios, founders/verbatim controls, unchanged qualification thresholds. Version 2 response contract and precedence; no deterministic actor solver. Still three model actors. Shared dollar cap unchanged at USD 12; call reservation amended once to 1,728 under the existing shared authority, leaving 1,471 call slots and USD 10.464303 conservative quota after this attempt. S0-a3 maximum 288 calls. If it fails, diagnose further without opening S1 or claiming success; at most one further bounded qualification repair within remaining allowance. Do not rerun for a favorable culture contrast.
