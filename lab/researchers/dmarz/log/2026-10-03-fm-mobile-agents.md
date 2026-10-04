# 2026-10-03 fm-mobile-agents (dmarz/fm-mobile-agents)

Task: scan-papers-fm-mobile-agents (fork-merge-security lane: mobile agents visiting hostile hosts, Byzantine state merge, supply chain, attestation).

- Added 22 entries (19 papers, 1 blog, 2 code), 8 read in full; ran ept/byzantine-eventual (tests pass, evaluation output identical to committed data). check and verify clean (8 papers have no DOI or arXiv id to verify: tech reports and USENIX papers).
- Semantic Scholar, OpenAlex and the arXiv API were rate-limited (429) all session. Recovered 1990s preprints from the Wayback Machine as PostScript and extracted text locally; IBM's 1995 report was EBCDIC-encoded.
- What surprised me: the 1996-1998 papers already state dmarz's attack almost verbatim. Sander-Tschudin and Yee call it "brainwashing" (the host edits the agent's memory of where it has been and what it saw). Farmer et al. say a migrating agent "can become malicious by virtue of its state getting corrupted". Yee also criticises replication-based thresholds because replicas fail together, the same point Schneider-Zhou make in 2005 for distributed trust.
- Most useful Q2 result: Kleppmann-Howard's BEC theorem. Any number of Byzantine contributors can be merged safely exactly when the updates are I-confluent with the invariants. Non-I-confluent updates (goal changes, deletions) need a quorum and an honest-fraction bound. Minsky et al. 1996 is the concrete k-of-n design for returning agents: vote at each stage and re-share secrets at each vote.
- Q1 (hiding which part returns) is thin in this lane; the route-anonymity papers were not reachable.
- Next: open Roth 2002 "Programming Satan's agents" and Westhoff 1999 route protection once access allows; follow forward citations of Minsky 1996 and the black-hole-search line (Byzantine companions).
