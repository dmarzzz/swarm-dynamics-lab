# How to run growth-pressure-200 (operator)

Nothing here is run by the builder. Paid stages need dmarz/fleet-monitor's go. Server names stay launch parameters; addresses, credentials and the hub address stay in the private fleet repository.

## Topology

- **Exactly 8 dmarz servers** (study.yaml `workers: 8`; the coordinator queues 8 worker sessions). The first named server runs the coordinator (`src/chain.py`: all economy states, the round clock, the only ledger, no model credential) and also one model worker; every other server runs one model worker (`src/worker.py serve`). All calls are spread over the 8 workers; each worker holds 1/8 of the token-rate governor's budget (85% of the key's limits) and at most 16 requests in flight (128 in total).
- One exclusive claim `claims/dmarz-growth-pressure-200.yml` listing exactly the 8 servers, `experiment: growth-pressure-200`, `until` at least 2 hours ahead.
- Fleet repository at or after agentops `e40ffce` (8-host coordinator-workers support, `--model`, `ledger: fresh`).

## Steps

```sh
H=<coordinator>,<s2>,<s3>,<s4>,<s5>,<s6>,<s7>,<s8>
python3 scripts/run-ready-chain.py growth-pressure-200 <launch commit> setup  --host $H --model gpt-6-sol
python3 scripts/run-ready-chain.py growth-pressure-200 <launch commit> chain  --host $H --model gpt-6-sol --stages S0,P0,Q0,X0,S1 --confirm-paid --source dmarz/<agent>
python3 scripts/run-ready-chain.py growth-pressure-200 <launch commit> status --host $H --model gpt-6-sol
python3 scripts/run-ready-chain.py growth-pressure-200 <launch commit> verify --host $H --model gpt-6-sol
```

`setup` runs the selftests (count in READY.yaml) and checks the source hash on every server. `chain` starts the coordinator, then the 8 workers with `SWARM_OPENAI_API_KEY` on ssh stdin. The chain runs S0 (scripted, about 15 s), P0, Q0, X0 (which decides N, the number of economy batches, from the measured mature-wave rate and cost), then S1 (N openings of 5 rounds, fork, 4N continuations of 20 rounds). A failed gate stops the chain. New requests stop at T0 + 52 minutes, where T0 is the start of P0; S1 then stops with `dispatch_deadline` and keeps its records. Exit codes of `src/chain.py`: 0 completed, 3 stopped at a gate or the deadline, 1 internal error.

## Expected time and cost

- Qualification: P0 1 call, Q0 95 calls (47 mechanics + 48 seeder decisions), X0 3,000 calls; a few minutes at the governor's rate (about 11 to 17 calls a second).
- S1: 17,000 calls per batch. At 11 to 17 calls a second, N = 1 takes about 17 to 26 minutes of calls plus round barriers; N = 2 is admitted only if the measured rate is at least 17.1 calls a second.
- Cost: hard cap USD 600 on settled cost plus open reservations. Expected about USD 0.010 to 0.016 a call: qualification about USD 30 to 50; N = 1 about USD 220; N = 2 about USD 440. X0 admits N only if `committed + 1.25 × 17,000 N × mature-wave mean cost ≤ 600`.

## After the chain

`verify` (re-simulates every S1 round from the saved answers), then `python3 analysis/analyze.py` on the S1 results directory, then the post-mortem `reviews/chain-001-post.md`; release the claim after uploads are verified.
