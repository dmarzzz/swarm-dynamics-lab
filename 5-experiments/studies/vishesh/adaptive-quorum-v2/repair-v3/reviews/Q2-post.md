# Q2 post-mortem

Narrow qualification passed. All 22 assigned cases completed: 16/16 core (A/B/C/NONE each 4/4), 6/6 changed boundary probes, zero schema/encoding failures. 66 physical calls, 198 logical predicates, no model acceptances needed blocking in these fresh cases. [Counts](../results/Q2/summary.json). The Q1 one-day-retention failure is retained; an offline adversarial regression verifies the new guard blocks it even when all model predicates wrongly say YES. Q2 alone therefore does not demonstrate the guard's causal benefit in a new failing model case.

The guard depends on typed observations and can be fooled by false sources. Stronger open-ended extraction and general API selection remain unqualified. No paid inference, retries or holdout access. Actual checkpoint/source/dependencies are in the manifest. All attempts and receipts remain retained.

Decision: advance only to the frozen engineering stress matrix, with misleading evidence included and a symbolic-policy comparison. Success there means reliable execution and useful measurement of this synthetic mechanism, not broad scientific confirmation. Static competence matrix is the declared visual mapping; the temporal replay passed an initial visual inspection on an offline recorded scenario, and a regression confirms future commitments remain hidden.
