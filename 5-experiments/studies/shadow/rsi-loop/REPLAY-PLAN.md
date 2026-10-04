# R0: trace-observability repair, frozen before evaluation

Status: offline engineering replay only. No paid calls. Not a scientific preregistration or independent review.

## Observation and change

Development source: the swarm-slop-audit session. Its typed metadata contains seven nonzero shell/process exit results, none marked `isError`. The same structural mismatch occurs in capture-memory development sessions. Raw text is neither needed nor exported. These are command return codes, not seven research defects: grep can legitimately return 1, and a failed negative-control command can be intended.

Baseline B0: a tool result is flagged when the wrapper's `isError` is true.
Candidate B1: preserve B0, and also flag an integer, non-boolean `details.exitCode != 0`. Do not infer failure from strings, missing codes, a running status, output prose or a negative research finding. Add a brief instruction to inspect typed exit status and classify its meaning before claiming command success.

## Fixed next replay run

Evaluate the complete saved transcripts with these four exact session labels, selected before inspecting their exit-status counts:

- swarm-writer-papers-p1
- swarm-writer-papers-p2
- swarm-survey-revise
- swarm-issue-74-contagion

Snapshot the inputs locally. Export only derived numeric metadata and opaque public aliases. No transcript text, arguments, response IDs, raw tool names, paths or errors leave the machine. Keep the label-to-file mapping local.

Primary engineering endpoint: sensitivity to explicit nonzero integer exit statuses. Denominator: all tool results with an explicit nonzero integer `details.exitCode`. Report numerator/denominator, not just a percentage. Secondary: false flags among explicit zero exit statuses without wrapper errors; wrapper-error events are outside that clean denominator. Report every selected lane even with zero eligible events. Missing status stays unknown and never becomes zero. Duplicated result observations are not independent command executions. Do not compute a statistical interval from this convenience sample.

Acceptance for the capture patch: every explicit nonzero status recognized, no new flags on clean zero statuses, wrapper error detection retained. This is deliberately a typed parsing contract, not an agent-quality score. It tests generalization of the parser across previously uninspected session files, not research competence or causal task improvement. We already inspected the development sources, and the developer owns this replay evaluator. Therefore scientific promotion is blocked regardless of the numbers.

## Artifacts and stopping

Commit this plan before running the four-lane evaluation. Preserve the first result, including an unfavorable or empty result. One baseline and one candidate replay only. No tuning on these lanes after evaluation. Unit tests may add synthetic edge cases separately and must not be counted as real episodes. Human/external reviewer approval and fresh research assignments are required for the prospective research experiment in DESIGN.md.
