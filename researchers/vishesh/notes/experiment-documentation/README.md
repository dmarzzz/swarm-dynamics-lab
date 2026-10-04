# Public experiment documentation contract

Owner request, 2026-10-04 UTC: every run on Swarm Lab must explain what it is testing in a short reader-facing TLDR and link its experimental design. This applies to engineering checks and exploratory pilots as well as confirmatory work. It follows the [Regrowth registration failure](../regrowth-200/REGISTRATION-FAILURE.md).

## Before every launch

1. Publish the plan with `## TLDR`, `## Question and prediction`, `## Setup`, `## Protocol` and `## Metrics`. Make a directional prediction only if it was actually specified before seeing results. Label retrospective plans explicitly.
2. The TLDR answers: what question, what changes, compared with what, what counts as success, and what cannot be concluded. Four to six plain-language sentences are enough.
3. Register `url` pointing to the exact committed README, and `description` starting with `TLDR:` so it appears near the experiment title. Use a commit SHA for reproducibility. Preserve the model/backend, stage and condition in run parameters.
4. Run `public_plan.py` before queueing or loading a model. It verifies the public registration and the required README sections, then writes a receipt with the plan hash, immutable URL, question, timestamp and registered TLDR. Failure stops the launch. A network outage is a failed preflight, not permission to omit documentation.
5. Add a per-run TLDR to the start message: “This run tests [condition] against [comparator], measuring [endpoint]; [stage/limitation].” Explain qualification as a competence check, not an intervention result. Link both the receipt and plan in the run artifacts. If a version changes, preserve each earlier run's original plan and annotate it rather than silently relabeling it.
6. After start, verify the rendered experiment and run pages. After completion, retain failed or invalid runs and distinguish execution status, process compliance and scientific outcome.

## Reusable preflight

```sh
python3 public_plan.py --experiment regrowth-200 \
  --run-tldr 'This pilot compares local Qwen, composite Qwen/Laya and exact routing with and without damage; it measures valid/shortest paths and recovery on one fixed map.' \
  --receipt /tmp/new-regrowth-plan-receipt.json
```

The receipt does not itself prove preregistration; its timestamp must precede the recorded launch. Existing runners must call the helper or an equivalent preflight before their next run. The current repair adds the gate to the local Regrowth runner and records this standing requirement; it does not claim every team's runner already enforces it.

## Current registrations

`registrations.json` contains the six reviewed experiment summaries and their document paths. These summaries are public design descriptions, not private traces or the previously blocked full evidence archive. The current page already displays `description` and reads plan sections from the registered GitHub URL, so this repair needs no front-end redeployment.
