# Pre-experiment research pass

Agent: dmarz/preflight. User requested research coverage followed by a merge into main. Used an isolated branch for that explicit request, overriding the default direct-to-main workflow.

Added eight missing primary-source records, all skim depth, and 3-synthesis/pre-experiment-research.md with an evidence log. Main finding: existing admission, lineage enforcement and rollback work narrows the candidate contribution to incomplete dependencies and observable recovery; causal interpretation and attention accounting remain shared design constraints. Appended a clarification to the Lamport entry about arbitrary coordinated faults versus statistical independence.

Self-audit checked all new internal links, attribution, scope and readiness claims. This is not a formal cross-researcher review. No model experiment or external code execution was performed.

Validation before submission: lab.py check 0 errors and 5 pre-existing unresolved-reference warnings; lab.py verify --agent dmarz/preflight checked 8 papers with 0 problems; Flight Deck strict check 0 errors and 0 warnings; git diff --check clean.

The normal sync helper refreshed an unrelated dmarz task heartbeat. That incidental change is excluded from the research contribution. The session timer was stopped when research finished to avoid later unrelated heartbeat writes. No changes to existing survey status, other researchers' notes, or experiment files.
