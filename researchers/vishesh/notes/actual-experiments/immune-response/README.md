# Immune response: private versus shared restoration

Executable Stage A of the [developed recovery design](../../swarm-immune-response/experiment-design.md). The research decision is whether restoring a shared store after an incident improves useful completion beyond restoring private agent memory, and whether recovery survives a stale artifact returning.

The fixed protocol is [preregistration.md](preregistration.md), assignments are [design.yaml](design.yaml), and the instrument is [immune.py](../src/immune.py). Seven specialists and one coordinator maintain twelve versioned facts for eight fictional services. Each of 24 rounds requests a six-service plan plus four compatibility values; an independent deterministic checker scores the plan and mock action request.

N does nothing; Q00 contains the source; Q10 adds private restoration; Q01 adds shared restoration; Q11 does both. CLEAN is a matched uncontaminated reference. All contaminated branches share the actual round-six checkpoint. The repair controller is explicitly an oracle receiving affected-state labels; acting agents never receive those labels.

Rounds 1–3 acquire evidence; 4–6 contain a bounded incident; intervention occurs before 7; a stale descendant returns at 13; a genuine compatibility-version update arrives at 18; scoring ends at 24. Source capability stays revoked in Q arms. The source is not silently replaced, and lost turns are counted.

The primary candidate is Q11–Q10 useful completion over the 18 assigned recovery requests. Also report recurrence, mock forbidden requests, retained initial facts, correct-specialist retention, benign-update acceptance and recovery censoring. Every branch keeps its own private/shared stores and queues. This is a bounded repair mechanism test; it does not validate autonomous detection, selective repair, safe real deployments or general self-healing.
