# Native Q1-01 post-mortem

Nine terminal slots retained; two valid and acceptable, seven invalid. Sixteen API calls; reported USD 0.04256; no missing usage/reporting errors. Citation-array repair worked. The next failure was an API/validator mismatch: generic schema generation allowed numeric fields to be null, including confidence, while study validation required finite numeric confidence. A security analyst returned DEFER with null confidence, terminating the shared team prefix. Null is not a valid estimate under the frozen contract; these downstream invalid slots are not model purchasing mistakes.

Repair only the schema: require numeric confidence for initial/final reports; cost remains nullable when unknown. Add a regression test matching enum citations and confidence type to validation. Retain all failed records. Use fresh buyer profile 6 for the next qualification, not the failed values. Budget remains the same unreplenished USD 1.40 subquota; no scientific escalation yet.
