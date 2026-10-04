# Right Dissenter follow up design

Status: **proposed, unimplemented, zero new experimental calls**. Areas: dissent and decision models. This is the planning successor to [RD4](../rd4/REPORT.md), not a new completed cohort or an accepted formal hypothesis.

The observed one-point accuracy gap comes from a missed recovery admission. The more general problem is that unresolved evidence can consume the check needed for a later change. We propose separating eligibility, interpretation and budget allocation, then testing when saving a check helps and when it delays a useful early decision.

- [Failure decomposition](FAILURE-ANALYSIS.md) explains every noncorrect checking-arm outcome.
- [Improvement contracts](IMPROVEMENTS.md) give priorities, acceptance checks and unresolved risks.
- [Prospective design](PLAN.md) specifies the three-policy contrast, scenarios and a proposed 60-call envelope within the 72 calls remaining.
- [Research questions](RESEARCH-QUESTIONS.md) develops the right to reopen, candidate mechanisms and falsifiers.
- [Setup record](SETUP.md) distinguishes completed planning from pending implementation and run admission.

Historical records remain unchanged. The next implementation step is the observation/interpretation/authorization ledger and its offline transition tests. No machine is held and no native stage is queued.
