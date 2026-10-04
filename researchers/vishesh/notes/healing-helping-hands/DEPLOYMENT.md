# Deployment and reproduction

Exploratory work owned by vishesh/codex-regrowth-docs. Active allocation: sim-vishesh, exclusive claim `vishesh-healing-helping-hands`, merged via private fleet claim PR 41, expiry 2026-10-04 04:48:54 UTC. Four CPU cores, approximately 8 GiB RAM, existing authorized host; no new VM or account charges created. Private addresses and credentials are deliberately absent.

Pilot-01 and pilot-02 used the earlier local runtime. The new dedicated-allocation omission is recorded in pilot-02-post.md; no retroactive allocation is claimed. Diagnostic-03 onward use the exclusive fleet host. Ollama 0.30.5 and the fixed Qwen digest were verified there. Laya source/weights are pinned in agent-definitions.json; runtime Torch 2.14.1, Transformers 4.57.6, Laya 0.3.26, NumPy 2.5.3, Hugging Face Hub 0.36.2. CPU/runtime changes mean wall times across local and fleet attempts are not directly comparable.

## Reproduce deterministic dynamics

The public `src/corpus.py`, `src/reference.py` and `src/sim.py` use Python's standard library. Rebuild a corpus with the recorded seed and correct version (`corpus.make` for pilot-01/02; `reference.corpus` for pilot-03), load the saved extraction tape and run `sim.rollout(corpus, tape, policy, scenario)`. Compare all recorded `state_sha256` values, metrics and final memory/notices. Provider sampling need not reproduce exactly; saved tapes are the reproducible intervention inputs. Fixture gold never substitutes for a model tape except in the explicitly exact arm.

Run offline tests with `python -m unittest discover -s researchers/vishesh/notes/healing-helping-hands/tests -q` from the repository root. Twenty-two checks cover state dynamics, faults, terminal assignment accounting, route validation, ordered wire payloads and budget settlement. For a new inference attempt, first commit its plan/source, register that immutable README and verify the public page; `source_check` refuses mismatched tracked files. Do not rerun an old output directory or copy a failed attempt over its previous records.

## Local models

Set PYTHONPATH to the pinned Laya source and HF_HOME to the prepared model cache. Qwen is served by local Ollama on the allocated host, digest verified before inference; Laya uses its pinned weights and a bounded worker process. Exact commands and immutable versions are in the attempt manifests and pre-run assessments. The adapters used by the earlier pilots remain available through their recorded source commits; current source does not retroactively describe an old prompt.

## Jev credential relay and budget

`src/jev_relay.py` runs on the credential-owning computer and reads a mode-0600 OpenRouter key file directly. It binds loopback only, accepts a frozen synthetic request allowlist and forwards to the fixed official HTTPS endpoint. A private SSH reverse tunnel exposes it only on loopback of the allocated worker. The model and qualification run on that worker; no key is copied to it. Never print the key or use shell substitution to form a header.

The durable SQLite ledger includes earlier qualification costs. Pilot-03 reserves full-context worst-case cost, settles only validated completed responses to actual cost, and keeps failed/uncertain reservations. Cumulative cap $0.10; maximum 720 calls including the first qualification; no retries. Stop the relay and tunnel after the bounded attempt. The per-study ledger is not an account-wide allowance or permission for other experiments to spend it.

## Results and rendering

The hub retains full safe journals, fixture corpora, model tapes and measured history as private artifacts. Public Swarm Lab exposes image/GIF artifacts, metadata and metrics. `visualization/render.py --results <results-root> --attempt <attempt-id> --out <site-dir>` compiles the standalone replay and measured PNG/GIF exports (Matplotlib, NumPy and Pillow). Its inputs are saved data; it makes no inference calls. The supported public fallback is the GIF, not arbitrary uploaded HTML.

Standalone hosting was previously blocked by expired Cloudflare login; the local replay and verified public hub GIF do not depend on that login. No dedicated-host process or allocation may be left running after results are verified and uploads complete.
