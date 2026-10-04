# Antsy execution repair v1

**Prepared offline; no new native call or allocation. D1 requires owner approval.**

The [prospective plan](PLAN.md) was published at `17e2c440` before implementation. The [Q0 post-mortem](../reviews/Q0-attempt-1-post.md) diagnosed the concrete gap: EasyOCR's third call timed out without a phase timeline or retained timeout streams. This implementation addresses observability and containment; it does not claim to make OCR faster.

- [telemetry.py](telemetry.py): allowlisted append-only fsynced child events, strict sequence/numeric validation and explicit incomplete-tail handling.
- [worker.py](worker.py): original EasyOCR configuration and frozen parser, with imports, reader construction, combined OCR, extraction and output phases. No finer detection-versus-recognition attribution is claimed.
- [capture.py](capture.py): one no-retry child process group; private direct-to-file streams, timeout cleanup, durable start/terminal journal, input hashes and sanitized status/hash metadata. No model credentials or general environment fallback. A valid slow call remains latency-ineligible.
- [fault_child.py](fault_child.py) and [tests](test_repair.py): fake local processes, not OCR or research observations.
- [validation.json](validation.json): exact tested source hashes and test results.

The wrapper is a development component, **not an admitted experiment launcher**. It does not allocate a host, register a plan, enforce a six-call study ledger or dispatch D1. Those gates remain required before native integration. Native output streams and raw OCR stay private; `result.json` includes only fixed categories, numeric events and artifact hashes. Never publish the private directory.

Run the software tests from the repository root:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/antsy-targeted-v8/execution-repair-v1 -p 'test_*.py' -v
```

No warm-up, altered model, resize or additional receipt is hidden in the tests. All original `src/` and `results/Q0-attempt-1/` files remain unchanged by this repair. [SETUP.md](../SETUP.md) remains the single authoritative study setup record.

## Concrete proposal awaiting approval

D1-latency-attempt-1: three reused receipts (two576×864, one960×1706), at most two cold EasyOCR repetitions each, fixed60,61,62,60,61,62 order, maximum6calls.45s remains the eligibility threshold; a proposed90s diagnostic ceiling can identify slow completion without qualifying it. Stop on the first slow completion, failure or trace defect. No warm reader, hosted call, new billable infrastructure or automatic qualification. The owner reviews this changed contract before launch.

Limits: phase fsync adds small unmeasured overhead; native instrumentation overhead and CPU latency have not been measured. Raw streams may contain untrusted engine output and are not public diagnostics. The current supervisor requests process-group cleanup and records direct-child reaping; it does not independently attest the whole host is idle. Before allocation release, the operator must still inspect native workers/children and verify artifact readback. The fixture confirms that a same-group descendant stops writing after timeout; it is not a general sandbox for a deliberately escaping child. OCR and model load remain untested here.
