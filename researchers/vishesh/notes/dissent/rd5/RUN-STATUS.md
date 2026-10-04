# Right Dissenter RD5 current execution status

**Blocked before native execution.** Reconciled 2026-10-04 at 15:24 UTC:24 frozen Q5 requests,0 started,0 valid responses,24 unstarted. Zero RD5 provider calls and zero model tokens/charges. H5 is not admitted. Qualification is unknown, not failed. [Dispatch post-mortem](reviews/Q5-A1-DISPATCH-POST.md), [structured review](reviews/Q5-A1-DISPATCH-QUALITY.json), [status figure](results/activation-a1/dispatch-closeout.png).

The first local relay expired at 09:14 UTC. A trusted read-only check at 15:19 found no RD5 worker, dispatch marker or result directory. Its expired allocation was explicitly released at 15:20. The earlier ready status was historical and must not be used for admission. No new host or relay is held.

## Approved scope and next action

Owner approval already covers Q5 and conditional H5 under the original cumulative cap. The direct-from-laptop exception remains unresolved; this review does not invent it or repeat a generic approval question. The authorized central queue still has no acknowledgement. **Obtain a confirmed central launch slot, then fresh dedicated allocation, current receipts and actual remote health; activate Q5-A2 once.** The private request has been corrected to block stale dispatch.

[Operational renewal](ACTIVATION-02.md) was published before the external-wrapper change. Five new activation/fault checks pass; all 61 scientific offline checks pass and both prepared packets validate unchanged. Old/new activations share a stage lock; prior markers/results block a renamed dispatch. The original A1 relay fence and all historical provider calls stay intact. No native response is retried or resampled.

Scientific source remains `27d63232559a2b6ccd9e317b1af5786b32c383bc`; the original [immutable amendment](https://github.com/dmarzzz/swarm-lab/blob/10e6b4d775c8409c1a9817ad633f0f6f84ae3c40/researchers/vishesh/notes/dissent/rd5/AMENDMENT-01.md) remains registered. Q5 allows 24 calls and needs 12/12 correct cards plus 24/24 valid complete responses. H5 allows 36 only after the real Q5 bundle audit and post-mortem. It compares 6 authored roots across 3 policies and 4 epochs:72 dependent decisions, with urgent delay reported separately.

## Cumulative accounting

428 historical provider calls remain: USD 0.016620450 settled plus USD 0.004032 unresolved = USD 0.020652450 committed. Maximum 60 RD5 calls; lifetime stop 488; 12 calls unallocated. Original USD 2 authority remains USD 1 API plus USD 1 infrastructure.

The conservative infrastructure estimate is USD 0.690783567, including historical wrong-account compute and the unused RD5 allocation through explicit release. Prior invoices remain unavailable; this is an estimate, not a settled bill. A renewed 90-minute allocation at the last verified rate would bring that envelope to USD 0.797928567, subject to fresh verification. [Full resource assumptions](results/activation-a1/resources.json).

The offline finalize hook and eleven-dimension scientific assessment close the expired activation. No native post-mortem or model-effect claim is fabricated. One admitted native cycle remains dependent on the exact external launch blocker above.
