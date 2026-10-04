# Deployment record: market-split-opus

2026-10-04; owner dmarz/market-split-opus. Server `sim-test-01` (existing 2 vCPU test server owned by dmarz), exclusive agentops claim `dmarz-market-split-opus`. One experiment, one worker. No server is created or destroyed by this study. Older checkouts of other studies on the server's disk are left untouched; this study lives under its own directory with its own checkout, virtual environment, ledger and worker log.

Launcher: `scripts/run-market-split-opus.py` in the private agentops repository. Runtime: Python 3.12.3 with PyYAML 6.0.3, numpy 2.0.2, matplotlib 3.9.4 and Pillow 11.3.0 from `requirements.txt`. The hub reporting configuration is already on the server. The model key and workspace id are read from the encrypted agentops store and passed over ssh stdin into the worker's process environment; they are not written to disk, a command line or a log. No credential, address or hub token appears in this repository.

Budget: at most 950 attempted calls and USD 60 for the whole study, enforced before each request by the study ledger. The ledger is created at the first paid stage and is never reset or copied. This study draws on dmarz's shared USD 500 allowance.

Process note: the agentops run-queue document says dmarz's runs are launched from orbital-one. This study is launched from halcyon on the instruction of the reviewer session dmarz/fleet-monitor, which relays dmarz. The conflict is recorded in [ISSUES.md](ISSUES.md) as O3.

Stage receipts are appended below after verification.
