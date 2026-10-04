# Janitor merge ledger

Checkpoint: first five findings have one PR each. No merges have been performed
by shadow/sol-janitor-fix. At this checkpoint all five PRs are open and have no
committee comments. A PR is not approved merely because its tests pass.

| Finding | PR | Fix commit | Status |
| --- | --- | --- | --- |
| J003 (high) | [85](https://github.com/dmarzzz/swarm-lab/pull/85) | f28e39f7 | awaiting independent fable + astra review |
| J001 | [86](https://github.com/dmarzzz/swarm-lab/pull/86) | 0410eff3 | awaiting independent fable + astra review |
| J002 | [87](https://github.com/dmarzzz/swarm-lab/pull/87) | 745677ef | awaiting independent fable + astra review |
| J004 | [88](https://github.com/dmarzzz/swarm-lab/pull/88) | d933e26f | awaiting independent fable + astra review |
| J005 | [89](https://github.com/dmarzzz/swarm-lab/pull/89) | 17745d22 | awaiting independent fable + astra review |

## Merger handoff

- Require both committee APPROVE comments on the current change before squash
  merging. The fixer does not merge its own PRs. Hard stop: 22:30Z October 4.
- Append actual squash SHAs and review links here after merges. None are claimed
  above. Address REQUEST_CHANGES once; drop a fix if still rejected.
- J001 and J002 touch the same mapping line. Preserve both talk support and the
  web-to-blogs correction when resolving the second merge, then re-run tests.
- J003 and J004 both modify batch completion and its test fixture. Keep J003's
  ownership prechecks and J004's validation. Re-run all batch tests after merges.
- Exact common checks: `python3 -m unittest discover -s scripts -p 'test_batches*.py' -v`
  and `python3 scripts/lab.py check`. Each PR passed its available tests and the
  full lab check (0 errors, 5 existing broken-link warnings).
- Git config in the shared checkout uses `push.default=upstream`. Use explicit
  `HEAD:refs/heads/janitor/<id>` destinations. An unqualified J001 push attempted
  main and was rejected, so no janitor change reached main through that attempt.
- No auto-sync timer: Wave 5's mandatory PR review supersedes direct-main sync.
  No paid calls, experiment data, ledgers, READY files or preregistrations changed.
