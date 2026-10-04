# QM-S0-01 setup post-mortem

Execution: setup failed before any model call. Public-plan preflight and all 26 server tests passed, but `Path.mkdir(exist_ok=False)` lacked `parents=True`, and `results/` did not exist. Native dispatch never began. The isolated SQLite ledger contains zero rows and zero spend; all 32 assignments remain unstarted. This is an execution defect, not a capability failure or scientific result.

Repair: create parent directories while refusing to overwrite any existing attempt. Add a regression that creates the missing parent and verifies existing evidence remains unchanged. Relaunch unchanged evidence, prompts, provider, budget and scoring as QM-S0-02. Preserve this failed attempt and hub status.
