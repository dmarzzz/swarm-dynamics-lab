# D1-A1 post-mortem

All nine assigned calls completed with valid responses. The three exact S1 bug-reproduction inputs were valid this time; all six fresh clean controls returned the expected actions. Nine calls used 6,964 input tokens, $0.000292488 and 4.37 seconds. No retries, substitutions or missing cases. The original three S1 errors were **not reproduced** and their specific rejection predicates remain unknown. No D1 response changes a S1 score or releases its uncertain charge reservation.

The diagnostic now records fixed validation error codes and allowlisted numeric/shape metadata. Strict validation was unchanged. Fifty-three offline checks pass, including frozen reproduction payloads, fresh-control truth isolation and an arbitrary-string canary proving the numeric diagnostic cannot copy provider strings into artifacts. This closes the observability defect for future errors; it does not claim retrospective diagnosis of missing data.

Public plan and source/host/allocation preflight passed before dispatch on sim-shadow. All seven D1 artifacts were read back and matched their worker SHA-256 hashes. The public PNG visibly shows 3/3 valid reproductions and 6/6 valid, correct controls. Q1 and S1 artifacts were independently hash-verified too; the 23-frame S1 replay was inspected locally and observed progressing on its public URL.

Disposition: complete this bounded exploratory cycle. Preserve the adverse S1 finding and the unresolved historical validation subtype. No additional sweep is justified merely to improve the score. Release the existing borrowed Dmarz host after shutdown; never destroy it. Formal research review and S2 remain future work.
