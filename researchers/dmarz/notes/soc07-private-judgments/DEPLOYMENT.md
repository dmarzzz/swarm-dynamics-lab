# Deployment and accounting

Exploratory development study, built and operated by dmarz/soc07-private on dmarz's instruction. Reviewer: dmarz/fleet-monitor; cross-researcher review waived by dmarz ([launch/review-waiver.md](launch/review-waiver.md)). S2 is closed. This file is the deployment record; it is updated after each stage.

## Fleet and source

- Host: sim-dmarz-3, exclusive claim `dmarz-soc07-private` held by dmarz/soc07-private (claimed 2026-10-04 03:29 UTC, currently until 2026-10-04 14:37 UTC, status `planned` while no worker runs). Before the claim the host had no active claim, load 0.00 and no worker process. Older checkouts of other studies on its disk were left untouched.
- Dedicated paths on the host: one checkout, one virtual environment and one budget ledger directory for this study. Addresses, the hub address and credentials are not in this repository.
- Deployed revision: `61de92259f045fdd97255317a5f93dd0010119ad`; runtime fingerprint `afacff913d48c50a8fb5b00efd8775454cfbc62dba841a8f6be919ea7144d9fe` (all `src/*.py`, `design.json`, `execution.json`, `experiment.json`, `requirements.txt`). Review notes and results do not change it.
- Server: Python 3.12.3 on x86_64, 4 logical CPUs, Pillow 11.3.0, standard-library HTTP. 58 unit tests ran at this revision: 57 pass and 1 is skipped (the approval-pinning test, which needs the pre-run assessment committed after this revision).
- Hub experiment: `soc07-private-judgments` ([public page](https://swarm-live.pages.dev/#/x/soc07-private-judgments)). One finite worker per stage, at most 5 requests in flight, no automatic re-execution.
- Launch manifest m1: `claude-haiku-4-5-20251001`, no reasoning allowance, temperature 0.7, output caps 256 / 256 / 64 / 64 and 128 for qualification. Credentials by alias only, passed from encrypted storage over ssh standard input to the worker's environment by the private launcher.

## Attempts

| Attempt | Hub run | Revision | Outcome |
| --- | --- | --- | --- |
| local-s0-001 | none (builder's machine) | working tree before `b4e2cd5` | 69 of 69 checks; outputs not kept in the repository |
| s0-a1 | `soc07-private-judgments/ae76d67b` | `b4e2cd5…` | done; 69 of 69 checks; 1,500 scripted episodes; 0 model calls; 482 s |
| s0-a2 | `soc07-private-judgments/bafeae75` | `61de922…` | done; 69 of 69 checks; 1,500 scripted episodes; 0 model calls; 463 s |
| s1q-a1, s1r-a1, s1l-a1 | not started | | wait for the reviewer's go and `launch/s1-approval.json` |

## Budget

Enforced cap USD 40 for the study (USD 30 public-decision path, USD 10 auxiliary private finals), inside dmarz's USD 500 total. Hard call caps: S1-Q 12, S1-R 672, S1-L 4,080. **Spent so far: USD 0, 0 model calls, 0 tokens.** The persistent ledger file does not exist yet; it is created by the first paid stage.

## Visual delivery

Each run uploads a final 1800 x 1200 frame, a replay GIF over completed blocks and an initial frame; paid stages also refresh a progress image at most every 20 seconds. The public site serves images only. Summaries, analyses, manifests, compressed episode files and journals are team-private hub artifacts and stay on the host.

## Closeout

Open. The claim is released only after the last authorized stage has finished or been stopped, artifacts are verified and the worker has exited.
