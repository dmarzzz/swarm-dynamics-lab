# Prospective structured-output repair, 2026-10-04

Written before any calls in the new `-or-json` cohorts. The first paid route attempt (`952a618c`) received model answers but **all 20/20 were schema-invalid**: Sonnet included explanatory prose and sometimes a fenced JSON block despite the JSON-only instruction. No main comparison calls ran. All raw answer text, usage, costs and failed outcomes remain in the `-or` directories. This is an interface-contract failure; it is not evidence that Sonnet cannot recover clean facts. No JSON-block extraction or retrospective answer salvage will change those failed outcomes.

The new attempt uses the parent's `provider.SCHEMA` as native **strict structured output** via OpenRouter `response_format`. No model/prompt/estimator/comparison sample change. Qualification uses **fresh parent clean-screen roots 5140 (ring) and 5145 (community)** instead of 5139/5144, six shapes each. It must again pass 12/12 exact. The 48 comparison roots remain unchanged and have not received any model answer in this factory.

The new adapter is `structured.py`, added to the source pin set. Prior adapters/specs remain unchanged. The same **physical paid-ledger.jsonl** retains all prior spend, and enforces USD4 per new spec and **USD20 across every attempt in the entire factory**. No retries, no paid-cap expansion, no model switching. A capability/interface failure now stops the **entire queue**, instead of wasting the same interface failure on all five scientific specs. The initial queue's repeated failures are an implementation lesson, not hidden paperwork.

Native-schema output is a configuration change. Compared with Dmarz's parent: model Sonnet rather than Opus; temperature 0 instead of effort-low reasoning; native strict schema in both; same graph generation, public packets and scorer; reduced qualification. Confidence statements must retain these limits.

Exact launch after committing:

```sh
nice -n 10 python3 researchers/shadow/factory/structured.py queue --watch
```

Analysis-only command:

```sh
python3 researchers/shadow/factory/structured.py analyze --spec split-sonnet-linked-strong-or-json
```
