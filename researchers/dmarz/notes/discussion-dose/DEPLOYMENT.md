# Fleet deployment and operations

Use the private swarm-labs-agentops repository for inventory, SSH configuration, claims and credentials. Do not copy any fleet address or hub credential into this public repository.

Deployment target: **sim-test-01**, an existing small simulation machine. Claim: **dmarz-discussion-dose**, shared, limited to environment deployment and bounded engineering smoke. Worker identity: **dmarz/discussion-dose**. No new infrastructure or open ports are required.

The private repository's `scripts/deploy-discussion-dose.sh` checks the active claim, fetches an exact committed public revision into a dedicated `/srv/swarm/discussion-dose-lab` checkout, verifies the offline tests, registers the exploratory study, queues S0 using the scripted backend, and runs one bounded worker. It uses existing `swarm_report`; it does not install orchestration frameworks or change system services.

```sh
# In swarm-labs-agentops, after committing/pushing the public plan and source:
python3 scripts/agentops.py claims
scripts/deploy-discussion-dose.sh <full-public-git-commit>
```

The study appears in the [live experiment list](https://swarm-live.pages.dev) with an exploratory title and plan URL. Until formal acceptance, the authoritative protocol is in researcher notes. The hub registry is an operational record and does not bypass the formal `experiments/` gate.

The bounded worker exits when its one batch finishes. Results and the event journal stay in the dedicated checkout and are uploaded as hub artifacts. Report both partial and complete outputs. Release the claim after deployment verification; another worker must obtain a new claim before using the server. Do not destroy this shared existing machine.

## Deferred model execution

The user asked to defer paid calls. The deployed script selects `scripted` explicitly. It neither reads model keys nor launches a paid endpoint. For a future approved pilot, inject `SWARM_MODEL_BASE_URL` and `SWARM_MODEL_API_KEY` through the approved private secret mechanism; do not add an `.env` file to this public directory.

Set nonsecret `SWARM_MODEL_CONFIG` to a JSON object containing exact `model`, `max_calls`, `max_output_tokens`, `max_input_bytes`, `timeout`, `max_cost_usd`, `input_usd_per_million`, and `output_usd_per_million`. Confirm endpoint compatibility and prices first. The adapter defaults to a zero dollar cap and refuses calls without a positive configured cap. Use one worker to keep that cap meaningful; it is per worker, not a distributed account-wide limit.

The shipped HTTP adapter's mock-server test is not real-provider qualification. No paid model was selected, and no cost or throughput estimate is claimed. Do not enqueue S1 until live S0 has qualified clean-task performance under a documented protocol amendment.

## Artifact transport

The hub's current reverse proxy limits each upload to 2 MB. `src/artifacts.py` compresses trace files and splits any larger compressed payload into parts of at most 1,000,000 bytes. `artifact-index.json` records ordered parts, encodings, sizes and SHA-256 hashes. Rejoin parts in order, verify the payload hash, decompress if needed, and verify the raw hash. `analyze.py` can read an intact `.jsonl.gz` directly. `recover_upload.py RUN_ID` repairs existing artifact uploads without reexecuting episodes or changing a failed run's terminal status. Raw local outputs remain unchanged.
