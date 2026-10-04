# PC-2 operator and reviewer handoff

The native implementation is implemented and offline-validated. No live PC-2 attempt is admitted or qualified. Use the [authoritative setup record](SETUP.md); do not treat this document, the common operations registry or a prepared packet as authorization. This study retains its manual adapter: `scripts/experiment.py run phantom-coast` is not its launcher.

## What is available

`src/run.py` is the single native entry point. It prepares metadata without opening reserved worlds and launches only with a current, evidence-linked private admission receipt. Researcher review is not a required receipt. `engine.py` writes assignments and started records before dispatch, records all failures, applies round barriers and reconciles unstarted endpoints. `wire.py` pins the TypeSafe route, typed inspection choices and maps. `ledger.py` carries the previous $0.162723246 into the existing $4 API cap and limits the successor to 1,816 calls. The remaining $1 of the original $5 is the infrastructure envelope, not an API top-up.

Native Q0 uses 24 calls on four roots. S1 uses at most 1,792 calls on eight independent roots, 96 dependent episodes. A request ceiling does not guarantee completion within the dollars: every call reserves its worst-case cost and the worker stops when it cannot reserve. No retry, fallback, second qualification attempt, copied-budget allowance or automatic pilot advancement is enabled.

The scientific plan was published before implementation. RUNNER-PRE.md was committed and published before native adapter work. API shape was rechecked against the [official Decisions reference](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request). Supporting 36 target alternatives on the actual pinned route still requires Q0; a schema reference is not paid qualification.

## Offline commands

From the repository root, with Python and Pillow installed:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/phantom-coast/pc2/tests -v
mkdir -p data/phantom-coast-pc2
python3 researchers/vishesh/notes/phantom-coast/pc2/src/run.py prepare --stage Q0 --output data/phantom-coast-pc2/q0-packet.json
python3 researchers/vishesh/notes/phantom-coast/pc2/src/run.py prepare --stage S1 --output data/phantom-coast-pc2/s1-packet.json
```

Keep packets and private operational evidence outside tracked public files. Preparation freezes assignment IDs and effective instrument hashes; it neither constructs reserved worlds nor contacts a provider. Tests construct only development roots. Scripted unit fixtures are not experimental outcomes.

## Owner-directed review policy

Researcher review is optional under the [prospective owner amendment](reviews/REVIEW-POLICY-AMENDMENT.md). No reviewer receipt or identity is required by the native launcher. The owning agent remains responsible for resolving known defects and recording the pre-assessment; this is not independent validation. Historical plans and reviews remain unchanged and are superseded only on this process requirement.

The `research_scope` receipt records the operator's intended exploratory experiment and authorized budget scope. It does not require another researcher or formal hypothesis acceptance. Continue documenting prior-art and inference limits without relabeling an unreviewed hunch as accepted research.

## Operational admission

1. Freeze and push the validated source; copy the unchanged effective instrument into an exclusive approved Mars fleet allocation. Refresh inventory and actual workload, merge the allocation claim, check expiry and verify deployed source/dependencies. Reuse an idle authorized host when possible. If none is available, creating a machine requires the verified Dmarz provisioning identity and original state; a candidate local token alone is insufficient. Do not hold a machine while launch is blocked.
2. Fence the completed PC-1 worker and verify its unchanged ledger has 540 settled calls, $0.162723246 total and no unresolved reservations. Record its SHA-256. Initialize exactly one PC-2 ledger through `Ledger(path, predecessor_sha256)`; keep PC-1 unchanged. On the same authority, Q0 and S1 share this successor ledger. Do not recreate it after a failure or move to a second competing copy.
3. Register `phantom-coast-pc2` with the immutable PLAN.md URL and the plan TLDR. Inspect the actual public page and save a rendered-page verification record. Register each stage's specific TLDR below. The launch path performs a fresh network preflight and binds URL plus exact plan bytes; a missing or stale registration blocks.
4. Complete the Q0 pre-assessment and private admission JSON using [admission-template.json](admission-template.json). Each evidence reference has an existing local `path` and `sha256`. Preserve private paths, account identifiers, host addresses and receipts outside public outputs. Snapshot source, current ledger hash, Python/Pillow/reporting runtime, credential availability, merged allocation, accounting authority and deadline. The aggregate check timestamp must be under five minutes old, with at least 65 minutes of claim and budget deadline remaining. Capture runtime package versions and reporting-helper hash in the bound runtime receipt; these are operator-verified dependencies, not checked automatically against a lockfile.
5. Supply only the approved OpenRouter credential on the allocated host using the existing secure workflow; never print it or place it in arguments. The launcher takes a permission-checked file path, has no environment fallback, and refuses redirects. This is not an Anthropic run. Remove the temporary credential at closeout. Before dispatch the hub must explicitly acknowledge run start. The private admission JSON is never uploaded.
6. Launch Q0 on that host. Analyze the saved qualification result, complete its post-assessment, and obtain a new current S1 admission receipt only if it passes. S1 recomputes Q0 from hash-bound saved records/worlds and requires matching instrument hashes. Different source/config semantics require fresh qualification under a separately amended repair plan; the launcher cannot silently repeat Q0.

```sh
python3 researchers/vishesh/notes/phantom-coast/pc2/src/run.py run --config PRIVATE_ADMISSION_JSON --out NEW_ATTEMPT_DIRECTORY --credential-file PRIVATE_CREDENTIAL_PATH
```

The template deliberately contains false/null gates. Do not change them merely to get past a check. Scope, account, rendered-page and exclusivity fields attest to the linked evidence; their truth must be checked by the operator. The live wrapper does not create infrastructure or conduct a review itself.

Q0 run TLDR: Test whether the pinned decision model can map complete direct evidence and select the unique cell missing a current measurement. Four roots across two families, three maps and three target checks per root; require all 24 valid, map upper error <=10% overall/20% per terrain stratum and >=11/12 correct targets. This qualifies interface use and mapping, not adaptive exploration.

S1 run TLDR: Compare misleading versus benign initial reports under team, single and uniform acquisition, with or without a source audit replacing slot six. Eight roots, twelve sensing slots per episode; measure paired whole-map error bounds, report-region visits and coverage at fixed sensing cost. A small synthetic exploratory comparison; shared observations and unequal inference compute limit interpretation.

## Interruption, reporting and closeout

Do not resume by deleting an attempt directory, reservation or stage claim. A crash after a reservation is unresolved exposure, even if the provider response was never saved. Fence the original worker, preserve ledger and records, and reconcile before proposing another attempt. Reports can be rebuilt from saved events without paying again. Failed start acknowledgment creates no model calls but retains its attempt identity for an explicit operator reconciliation.

S1 outputs include all actor requests and typed responses in records.json; actual targets, proposals, failures, fixed orders, audit choices and endpoint maps in episodes.json; per-world/family contrasts and per-policy usage in summary.json; every logical slot in replay-manifest.json, replay.gif and a 1600-pixel PNG. Images separate evaluator truth from acquired evidence. JSON retains native endpoint maps and hashes; an interactive PC-2 endpoint inspector is optional future presentation work, not implemented here. Upload acknowledgments are checked; verify remote artifact hashes at closeout before releasing the claim. Reporting success remains separate from qualification/scientific success.

No new spend or machine claim occurred during readiness work. The operator can complete registration, allocation and deployment under the existing owner authorization. The user does not need to provide another API key or another $5 authorization.
