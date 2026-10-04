# Pre-run assessment: S0-a1

- Experiment / owner / stage: swarm-of-theseus / vishesh/codex-theseus / S0 exploratory competence screen.
- Parent attempt: first attempt; no preceding experimental post-mortem.
- Status: ready (launch remains mechanically gated on public registration, exact deployment, claim and tests).
- Decision: can this pinned model perform the three simple tasks and preserve a seeded convention when the procedure is directly available?
- Expected: verbatim control accuracy >=0.85 and convention >=0.8 in every scenario. Negative result: model or adapter fails; no S1. This does not yet test channel effects.

## Design and assessment

Closest evidence: Perez et al. transmission framework and Ashery et al. conventions, as discussed in README; no claim to completed prior-art review. Strongest comparator is the executable rule implemented separately in the scorer and an observation-only exact fixture policy. World is the unit; two paired seeds per scenario, six worlds, 12 world-arm outcomes. Three dependent members and six dependent steps per world are not extra replicates. Cases use new identifiers with recurring binary features; no broad generalization claim.

S0 uses seeds 100/101; development tests use 22/23; S1 200/201 is unopened. Labels and conventions explicitly counterbalance across adjacent seed pairs. Newcomers have empty private notes, only allowed channel text or explicit verbatim reference. Full turnover must occur in verbatim; founders retain IDs. Actor payloads exclude evaluator labels. Three solve calls per step and two onboarding calls per replacement are equal across arms; actual tokens differ and will be reported. Notes cap 600 characters; messages cap 300. Prior questions/answers generated in masked arms consume compute without conveying information. No tools, persistence outside notebook, or grader access.

Scorer uses distinct-root majority for observatory and XOR/mapping for the other tasks. Scripted positive controls score 1.0; naive duplicate-count baseline is wrong on every constructed observatory case. Wrong agreement scores zero; convention is separate. Exact-policy tests do not establish LLM competence. Meaningful effect threshold for later pilot is 0.10 accuracy points, descriptive only. Denominator for failures includes every assigned world-arm. Logical steps are not wall-clock evolution.

## Changes and unresolved issues

| Issue | Change | Expected effect | Acceptance | Owner |
|---|---|---|---|---|
| Prior shared budget cannot be copied | USD 12 / 1,152 calls reserved once from shared USD 45 authority | No double-spend across hosts | local cap <= reserved amount; unique allocation ID | codex-theseus |
| S1 originally oversized | Two worlds per scenario, 36 outcomes | Fits pilot allowance | No stronger precision claim | codex-theseus |
| Same binary features recur | Explicit limitation; disjoint IDs and split seeds | Honest generalization scope | No claim of unseen compositions | codex-theseus |

## Frozen execution plan

README, design.yaml, model-config.json, all src/tests and this review are committed before inference; manifest records exact commit and SHA256 values. Model `claude-haiku-4-5-20251001`, temperature 0, max 768 output tokens, 8,000 input bytes, 60-second request timeout. Three concurrent world-arm workers on sim-shadow; pinned prompts in study.py. S0 maximum 288 calls. Shared allocated cap USD 12 includes later S1; no added infrastructure spend. Cost estimates are reservations, not invoices. Stop on exhausted quota, expired claim, 2-hour runtime limit, or systemic defect. No semantic or transport retries.

Command: `python src/runner.py --stage S0 --attempt S0-a1 --out /srv/swarm/theseus-results/S0-a1` from deployed study. Credential alias: macOS Keychain service `swarm-lab-anthropic`, account `vishesh`; local launcher injects via SSH stdin/process environment without display or storage. Quota allocation `swarm-of-theseus-v1`; dedicated claim `vishesh-swarm-theseus` on sim-shadow, exclusive merged claim PR 32, four-hour expiry. Refresh immediately before launch. Exact expiry recorded in deployment receipt, never addresses.

Regression: 10 offline unit tests passed, covering positive/negative controls, turnover, masks, empty newcomer memory, mutation, counterbalance, disjoint identifiers, call counts, fail-closed public-plan validation, and failure denominators. Deployed tests and renderer smoke check required before inference. S1 is disabled until this S0 is reviewed; S2 unconditionally unavailable.

## Visualization mapping

Mapping v1: each `swarm-of-theseus/S0-a1-<scenario>-<arm>-<seed>` binds design/model/source and six logical frames. `accuracy` is correct collective answers /4; `convention` is exact receipt matches /3; `turnover` is nonfounder members /3. Separate labeled panels, 0–100% scale; no merged culture score. Roster IDs show all replacements. Rule-change marker is evaluator metadata, not injected as a hidden answer; only the explicitly authorized bulletin is actor-visible.

Upload latest PNG after each scored step (six/run), retain all frames in events.jsonl/history.json and every request/response. Final image 1600x900; standalone HTML replay with play/pause, cursor, world filter. Hub supports PNG contact sheets; custom HTML is downloadable there, so public GitHub artifact plus locally openable replay is fallback. No claim of native spatial-view support. Grey gaps mark missing frames. Maximum 72 S0 frames, no downsampling. Rendering is outside model budget. Renderer test must cover initial/final/missing state; post-run reviewer compares every frame against event scores and checks actual playback. Failed rendering is a reporting defect requiring repair, not evidence about culture.
