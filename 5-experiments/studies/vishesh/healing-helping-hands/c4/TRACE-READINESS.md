# C4 native trace readiness

This is a code/readiness review, not evidence from a new run. C4 has no native outputs. Source reviewed:94147dc7b0408912617725c76d39bbdffd14339b. C3's completed raw-call and deterministic replay audits remain the last observed evidence.

The fleet trace policy distinguishes experimental transcripts (run artifacts) from the operating assistant's Claude/Codex session transcripts. The latter require a separate privacy workflow and are not collected or published for this experiment. Dmarz's discussion-dose trace repair cf872ef6 preserves failed runs and compresses bounded uploads; its delivery repair must not be mistaken for new sampling. C4's archive should retain the complete native journal and hashes even if a public summary is smaller.

| Native evidence | C4 source behavior | Closeout obligation |
|---|---|---|
| Actual delivered model inputs | Durable start event stores exact payload, hash, report ID, model and variant | Reconstruct every request from the pinned contract; verify claim visibility and option-order-only manipulation |
| Valid model outputs | Completed event retains raw response, parsed label, usage and latency | Inspect correct, accepted-wrong, referred and disagreement examples; recompute all labels and costs |
| Model tools/actions | These classifiers have no model-selected external tools; their action is the returned label | Do not invent agent tool use or infer autonomous collaboration from the tile display |
| Routing actions | Deterministic scorer records referral and matched-referral per report | Reconstruct both from saved A/B/Jev labels; keep Jev collection cost separate from hypothetical deployment savings |
| Failures | Start/failed journals preserve exception class and duration; assignments retain failed/not-run status | Preserve missingness and ambiguous reserves; never turn a missing paired outcome into a null effect |
| Invalid response limitation | A response rejected inside validation in the original source could be reduced to a failure class rather than retained verbatim | Before any changed-source launch, repair raw task-response retention and test malformed-response cases; do not claim complete invalid-output observability from the present source |
| Publication | Full archive plus measured summary/PNG/replay | Check trace-to-score and score-to-visual consistency; retain compression/hash/readback receipts and all adverse outcomes |

The trace-readiness review therefore does not certify a fresh run or full malformed-response coverage. The repair described below is prospective and does not reconstruct missing historical responses. Any changed code must be newly pinned in the prospective registration and requalified; do not silently alter94147dc7 or fabricate historical responses.

Current dispatch boundary: the initial delegated request was rejected by automatic approval review. The portfolio owner subsequently fenced the central request through an approved action and published scoped direct-execution authority in the shared repository. That verified directive supersedes central-only waiting for C4; normal platform review and all allocation, source, runtime and spending checks remain mandatory. The historical admission closeout remains unchanged.

The prospective source now retains allowlisted task fields for rejected Qwen responses and invalid Jev replies. Jev rejections are stored separately from successful responses, retain the original reservation, and are recoverable by GET without another paid POST. Failed-call journals and the audit distinguish retained rejected outputs from failures with no response. Offline tests cover malformed JSON, unknown labels, GET-only recovery, and exclusion of unrelated fields. Raw non-JSON provider transport bodies are deliberately not retained: they cannot safely be treated as task responses. This limitation is reported rather than interpreted as model failure.
