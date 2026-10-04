# Pre-run assessment: follow-up F1, gpt-6-sol with reasoning_effort none (S0, P0, Q0, S1)

- Experiment / owner / chain: sybil-scarcity-xmodel / dmarz (built by dmarz/pipeline-scarcity-qwen) / follow-up configuration F1 of `gpt-6-sol`, batches `s0-001-solnone`, `p0-001-solnone`, `q0-001-solnone`, `s1-001-solnone`, hub experiment `sybil-scarcity-xmodel-solnone`, ledger `<stem>-solnone`, results `<results>/solnone`.
- Pre-registration: [preregistration.md, "Follow-up configuration F1"](../preregistration.md), committed in 2dc7a269 after the effort-low Q0 stop and before any F1 code.
- Previous attempts read: the gpt-6-sol effort-low chain (pin 1e56c70e, source hash f3ffc908) stopped at Q0: 48/48 valid, field accuracy 0.57 / 0.56 / 0.31 at 1 / 9 / 81 carriers, 148 of 264 present facts answered null and 1 wrong value, 24/24 withheld facts null (post-mortem [chain-002-post.md](chain-002-post.md)). The Qwen chain stopped at Q0 ([chain-001-post.md](chain-001-post.md)).
- Status: **ready**, for dmarz/fleet-monitor's same-researcher check and launch. Not launched by this assessment.
- Authority and review status: dmarz did not name this study; dmarz/fleet-monitor requested this follow-up (the same one the split study receives) under dmarz's instruction to keep experiments running and ship tonight. Cross-researcher review is waived by dmarz for these exploratory runs; the fleet monitor's check is a same-researcher check; the run is not independently reviewed.
- Question: does gpt-6-sol without reasoning answer the clean packets the parent's Opus 5.5 answered 48/48, and if so, does it collapse at one carrier on the attacked packets? A Q0 stop of F1 ends the gpt-6-sol route (pre-registered).
- Why effort none could differ (inferred, not tested): the effort-low misses were nulls on present, unanimous facts after a few hundred reasoning tokens at most; the split study's sol misses used more reasoning tokens than its exact packets. Without reasoning the model may follow the plurality of identical reports more directly. It may equally keep abstaining; either outcome is reported.

## Frozen execution plan

- Code commit: `fb7d14200af007d321eb3ea7532f99a153c7a87f`. Source hash: `51ffa0b009afd76bc989be5ffab4f9b6ef35d12fd020e10a4c9576f065a8868e`. `READY.yaml` carries this hash, `selftests: 96`, and names this review. Its `effort: low` is the launcher's required field, validated against the first ladder model's provider (openrouter, which does not accept `none`); the effort actually sent is `reasoning_effort: none` from the hashed design.yaml. The launch commit is the first commit on `main` containing this review with this hash.
- Changes from chain-002-pre: only the gpt-6-sol entry of design.yaml (`tag: solnone`, `reasoning_effort: none`, no per-model attempt override, so batches are `*-001-solnone`); the rehearsal stub emits no reasoning tokens at effort none; tests updated to the new names. Inputs, prompt, validation, thresholds, caps, margin, prices and analysis unchanged; the Qwen configuration digest is still the first commit's (test).
- Request: `model: gpt-6-sol`, `reasoning_effort: none`, `max_completion_tokens: 2000`, `response_format: {type: json_object}`, `messages`. No sampling parameters (allowed only at effort none but not used: same as the parent's request, which sent none). Any reasoning token is a failed call (`unexpected_reasoning_tokens`, not an integrity failure; S0/P0/Q0 strict, S1 tolerates 15).
- Calls: P0 1, Q0 48, S1 1,440 (1,489); 1,700 transport attempts; 2 in flight.
- Dollar cap USD 150, F1's own ledger. Measured at effort low: 0.319 tokens per byte, Q0 USD 2.27 for 48 calls (USD 0.047 per call, 172 output tokens per call). At effort none output falls to about 40 to 70 tokens; per call about 18,250 input tokens × USD 2.50 (cache-write upper bound) = USD 0.046 plus about USD 0.0006 output. Expected total: 1,489 × 0.047 = about USD 70. The S1 projection gate (1,440 × Q0 cost per call) would be about USD 67, well within the cap.
- Reservation (margin 2): (57,169 bytes × USD 2.50 + 2,000 × USD 10) / 10^6 × 2 = USD 0.326 per call; two in flight USD 0.65; with 15 unsettled failed calls USD 5.5 (under 4% of the cap).
- Input ceiling 50,000 tokens; measured largest projection at effort low 18,230 tokens.
- Time: at effort low P0 took 1.7 s. S1 at 2 in flight is 720 calls per worker; at 2 to 6 s per call 24 to 72 minutes, plus about 2.5 minutes of preparation. Stage limit 14,400 s.
- Gates and failure rule: as in [chain-002-pre.md](chain-002-pre.md): S0 byte-identity and plurality gate; P0 interface; ceiling projection before Q0 and S1; Q0 the parent's thresholds; S1 cost projection; billing or quota stop pauses then stops as `provider_billing_stopped`, resumable as `s1-001-solnone-r1`.
- Command: `python3 scripts/run-ready-chain.py sybil-scarcity-xmodel <launch commit> setup|chain|status|verify --host <server> --model gpt-6-sol`.
- Checks on the code commit (offline, Python 3.9.6):
  - `python3 src/selftest.py`: 96 OK three ways: environment unset; `STUDY_MODEL=gpt-6-sol STUDY_PROVIDER=openai`; `STUDY_MODEL=qwen/qwen3.7-flash STUDY_PROVIDER=openrouter`.
  - `STUDY_MODEL=gpt-6-sol python3 src/worker.py --stage S0`: 168/168 valid, 0 violations.
  - `STUDY_MODEL=gpt-6-sol python3 src/manifest.py --check`: current, unchanged (`cf501136…`).
  - `python3 src/rehearse.py --model gpt-6-sol`: 22/22 checks in 290 s; hub runs `s0-001-solnone`, `p0-001-solnone`, `q0-001-solnone`, `s1-001-solnone` done and verified; never-abstaining stub stops at Q0 with no S1 run; quota stop (`provider_billing_stopped`) then resume completes S1 inside the cap.
- Not tested: the live route at effort none on these packets (P0 is the first observation).

## Visualization mapping

Mapping v1 in [VISUALIZATION.md](../VISUALIZATION.md), unchanged; runs bind `sybil-scarcity-xmodel-solnone/<run id>`.
