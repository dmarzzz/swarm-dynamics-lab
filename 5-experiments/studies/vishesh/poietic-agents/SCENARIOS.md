# Public scenario and fixture contract v0.2

These hand-authored examples define the instrument before reserved fixtures are opened. They are not outcomes from agents.

All jobs carry a requested logical epoch, endpoint/entity requirements and source receipts. Inventory contains available and reserved quantities. Supplier terms contain supplier ID, unit price in integer cents, capacity and lead days. Deliveries contain expected/received quantities and due day. Replenishment chooses a supplier able to supply the requested quantity within max_lead, minimizing unit price and then alphabetical supplier ID; return `{supplier, total_cents}` or `{supplier:null,total_cents:0}`. Stock exceptions return sorted IDs with available minus reserved below threshold. Reconciliation returns the sum of positive expected-minus-received for shipments due by day. No identifier encodes a correct answer.

## A raw cache captures all reuse

Two jobs request inventory for sku-x at source version 1. Available=9, reserved=2. Threshold 8 returns `[sku-x]`; threshold 6 returns `[]`. Fetching the packet twice is unnecessary; A1 can deliver the same current bytes once to both agents. No special provider architecture is needed for this saving. Version 2 is a different key even if its values coincidentally match.

## Repeated derived work

Normalize and join sku-x's inventory (available=9, reserved=2) with supplier rows `(a, price=30, capacity=12, lead=2)` and `(b, price=20, capacity=4, lead=3)`. A reusable generic normalized/joined table can serve different downstream quantity or deadline queries. Quantity 5 / max_lead 4 chooses a at 150 cents; quantity 3 chooses b at 60 cents. The normalized join depends on source packets, not quantity. All arms have the same join/filter/arithmetic primitives. A1 may memoize that prefix too, using a program hash plus only referenced parameters; A2/A3 may install and share it. If coherent derived memoization captures the gain, that is a valid null for services.

## No useful reuse

Each of six jobs requests a distinct endpoint/entity/version key and a distinct transformation. Raw or derived sharing provides no hit; advertising, transferring and maintaining services can only add overhead within that batch. The low-overlap stress cell intentionally includes this case.

## Frozen finite pilot workload

The first executable fixture version uses six jobs with kinds cycling replenish, exceptions, reconcile. Each job requests one entity and its kind's endpoint. High reuse repeats two endpoint/entity pairs, producing 4 repeated required occurrences out of 6 (66.7%). Low reuse uses six distinct keys, producing 0/6. This **explicit v0.2 amendment replaces v0.1's approximate 80%/20% target**: six one-endpoint jobs cannot realize those percentages exactly. Log counts, not target labels. Additional multi-endpoint joins are hand-authored capability fixtures in this instrument; this pilot alone does not establish benefits on a broad multi-API join distribution. A later broader workload requires prospective redesign.

Version changes occur every two logical epochs, independently of requests. Schema-change roots nest records under body at epoch 5 and express prices in millicents; every arm gets the same public migration description. Models may compute answers themselves or use generic programs; the hidden reference solver is never a tool. Code never opens S1 or S2 fixtures during unit checks.

## Qualification case boundaries

Twelve cases per model contract each contain four dependent requests: required fetch; structured answer; refresh after source-version change; configuration action. The configuration action cycles through restoring an unloaded tool, registering a raw-data service, and installing a normalization procedure. After a correct action, the adapter actually fetches, serves to another identity, or executes the procedure. S0 explicitly requests those actions to test capability. S1's operating policy contains no instruction to specialize and no topology reward. Repeating a small set of operations is interface coverage, not 48 independent reasoning problems or proof of broad competence.
