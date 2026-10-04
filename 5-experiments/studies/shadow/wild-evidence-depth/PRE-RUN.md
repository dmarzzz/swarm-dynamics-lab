# A1 pre-run assessment, 2026-10-04

Decision: ready for **saved-data census only**, by shadow/sol-audit-gap. No model qualification, intervention or hypothesis acceptance is claimed.

- Prospective plan and ranking pushed at `b9eb6c8e`; immutable public plan https://raw.githubusercontent.com/dmarzzz/swarm-lab/b9eb6c8e/researchers/shadow/notes/wild-evidence-depth/PLAN.md fetched successfully (HTTP 200) at 15:06:03Z. Returned full content matches the intended v1 plan.
- Fifteen hand-authored analyzer tests pass: graph ancestry, direct/indirect distinction, all descendant categories, orphans, cycles/self-links, duplicate ids, null/empty text, exact text versus components, unknown kinds, bins, deterministic order, escaping and deep trees. Synthetic fixtures are not empirical evidence.
- Minor implementation clarification before the first corpus run: preserve an `other_descendants_only` category if nested payloads have no response/recovered descendants; this prevents forcing unanticipated graph structures into the three expected categories. No endpoint is dropped.
- Previous attempt/post-mortem: none. First full census of the already-saved public export.
- Resources: local single CPU, nice 10. No network in analyzer, no credentials read, zero model/API spend. Input and code hashed by analyzer; all rows retained in denominator. No dataset text is emitted.
- Visualization mapping: static primary coverage bar plus exclusive descendant categories. Direct and descendant metrics are visually separated. No animation because null timestamps cannot support temporal replay.
- Next command: `nice -n 10 python3 analyze.py --data /path/to/redacted.jsonl.gz --out results`.
- Acceptance: unique ids, valid kinds and acyclic graph; component sizes sum to full input; primary recomputation agrees exactly; figures use the recorded denominator. Follow with separate reference arithmetic and POST-MORTEM whether useful result or null.
