# C3 native launch and recovery

Status: code and prospective design published; not natively admitted or run. This document is an operator procedure, not evidence that prerequisites passed.

The worker and relay must be on the same dedicated host. No reverse SSH forward, laptop process or operator terminal is part of the inference path. Launch `supervise.py` from a detached systemd service on the admitted host, through the current fleet coordinator. The supervisor starts its own relay, verifies its PID in the health response, launches exactly one stage, monitors both child processes and terminates them on deadline or transport failure. It does not automatically advance stages or restart provider calls.

Before launching, securely transfer the unchanged original SQLite ledger under an exclusive writer lock and record a single authoritative writer. Disable the original local dispatch path throughout remote ownership. Verify every historical row after transfer: at least the retained 859 reservations, completed cost USD 0.015678054 and one unresolved USD 0.001344 exposure. Keep an immutable local backup, but never treat it as another spending authority. At closeout verify all historical entries unchanged, retain added rows, reconcile the ledger back, then release authority and retire the host. Do not create an empty ledger.

The admitted host needs a private `authority.json` with attempt C3, active_writer equal to its actual hostname and local_dispatch_disabled true; these fields must reflect observed transfer/lock evidence. The current stage admission uses worker.py's existing schema and a verified public plan receipt. A separate S1 admission follows audited S0, with the same qualified Python source hashes. The prospective S1 assessment may be a new documentation commit; admission source still points to the frozen instrument.

Only transfer the model credential through the approved encrypted process to a mode-0600 file inside a mode-0700 directory on `/dev/shm`. Never put the value in arguments, logs, Git or admission JSON. Relay deletes that file after reading. Supervisor removes it on exit if startup fails. Use the standard secure reporting SDK already provisioned on the worker. Verify the pinned Ollama image and Qwen digest from PLAN.md and the prior runtime receipt before model load.

Native stage command, with the paths resolved by the admitted operator:

```sh
python3 composite/supervise.py --stage S0 --credential /dev/shm/PRIVATE/key \
  --ledger PRIVATE/original.sqlite --authority PRIVATE/authority.json \
  --admission PRIVATE/S0-admission.json --out RESULTS/C3-S0
```

For S1 use `--stage S1 --parent RESULTS/C3-S0`, the separately admitted S1 receipt and a new RESULTS/C3-S1 directory. Run within a detached service with a 20-minute S0 / 65-minute S1 upper lifetime. The operator observes exits and audits manifests; zero exit alone is insufficient for scientific acceptance.

Verify operator disconnect does not terminate the service. The loopback health check runs at launch and before each new Qwen report/Jev request. Validated provider responses and settled usage commit atomically before delivery. A lost response can be recovered only through GET /result/<payload hash>, never a second provider POST. A missing cached response fails the stage and preserves the unresolved reservation. Schema/provider errors also stop. Record transport logs separately from research measurements.

Archive run manifests, assignment statuses, calls, transport receipts, raw outcomes, source/public-plan receipts, original-ledger reconciliation and visual traces before releasing the claim. Use the existing saved-data report compiler. No C3 registration/readback, allocation or native pass is currently claimed.
