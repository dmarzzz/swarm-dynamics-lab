# Factual API qualification results

Backend: laya. Source: `4f206268269d96c5fc8fe3426696345dd5af099a`.

Completed 168 arm outcomes across 6 task clusters. Numerical clean-task qualification pass: **False**.
Target coverage: {'C': 3, 'A': 2, 'NONE': 1}; missing labels: ['B']. This is not a balanced benchmark.

| Policy | Agents | Deadline | Correct/assigned | Constraint violations | Abstentions | False NONE | Invalid |
|---|---:|---:|---:|---:|---:|---:|---:|
| majority | 5 | 3 | 4/6 | 1 | 0 | 0 | 0 |
| majority | 5 | 6 | 4/6 | 1 | 0 | 0 | 0 |
| majority | 9 | 3 | 1/6 | 0 | 0 | 5 | 0 |
| majority | 9 | 6 | 1/6 | 0 | 0 | 5 | 0 |
| fixed | 5 | 3 | 4/6 | 2 | 0 | 0 | 0 |
| fixed | 5 | 6 | 4/6 | 2 | 0 | 0 | 0 |
| fixed | 9 | 3 | 4/6 | 1 | 1 | 0 | 0 |
| fixed | 9 | 6 | 4/6 | 1 | 0 | 0 | 0 |
| adaptive | 5 | 3 | 4/6 | 2 | 0 | 0 | 0 |
| adaptive | 5 | 6 | 4/6 | 2 | 0 | 0 | 0 |
| adaptive | 9 | 3 | 4/6 | 1 | 0 | 0 | 0 |
| adaptive | 9 | 6 | 4/6 | 1 | 0 | 0 | 0 |
| vote-at-deadline | 5 | 3 | 4/6 | 2 | 0 | 0 | 0 |
| vote-at-deadline | 5 | 6 | 3/6 | 2 | 0 | 0 | 0 |
| vote-at-deadline | 9 | 3 | 4/6 | 1 | 0 | 0 | 0 |
| vote-at-deadline | 9 | 6 | 3/6 | 2 | 0 | 0 | 0 |
| central-at-deadline | 5 | 3 | 3/6 | 2 | 0 | 0 | 0 |
| central-at-deadline | 5 | 6 | 3/6 | 2 | 0 | 0 | 0 |
| central-at-deadline | 9 | 3 | 3/6 | 2 | 0 | 0 | 0 |
| central-at-deadline | 9 | 6 | 3/6 | 2 | 0 | 0 | 0 |
| central-targeted | 5 | 3 | 0/6 | 5 | 0 | 0 | 0 |
| central-targeted | 5 | 6 | 0/6 | 5 | 0 | 0 | 0 |
| central-targeted | 9 | 3 | 0/6 | 5 | 0 | 0 | 0 |
| central-targeted | 9 | 6 | 0/6 | 5 | 0 | 0 | 0 |
| central-random | 5 | 3 | 1/6 | 4 | 0 | 0 | 0 |
| central-random | 5 | 6 | 1/6 | 4 | 0 | 0 | 0 |
| central-random | 9 | 3 | 1/6 | 4 | 0 | 0 | 0 |
| central-random | 9 | 6 | 1/6 | 4 | 0 | 0 | 0 |

Physical model calls: 828; estimated input tokens: 322404; episode wall seconds: 238.68.

No p-values or independent-agent sample counts. Full tapes are shared across stopping policies. Root availability is not causal evidence use. Verification has a terminal probe allowance; evidence deadlines are not wall-clock service guarantees.

Do not launch development after a failed clean-task screen. Publish failed decisions and improve or replace the decision layer on separate development fixtures. Jev via OpenRouter remains a separately qualified future backend.
