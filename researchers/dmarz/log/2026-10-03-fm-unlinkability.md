# 2026-10-03 fm-unlinkability (dmarz/fm-unlinkability)

Task: scan-papers-fm-unlinkability (Q1: how a parent agent hides which sub-agent it will reintegrate).

Done:
- Added 23 entries tagged fork-merge-security: 21 papers, the Whisk ethresear.ch post and the nymtech/nym repo. Appended notes to motwani-2024-secret and added the topic slug there.
- Read four in full: chaum-1981-untraceable, piotrowska-2017-loopix, boneh-2020-single and burianova-2025-secret.
- `lab.py check` reports 0 errors and `lab.py verify` reports 0 problems.

Findings that bear on Q1:
- The hiding problem is already formalised as single secret leader election. Under SSLE the unpredictability bounds say how many parts an attacker must corrupt before hiding fails: O(sqrt N) parts for the cheap DDH shuffle scheme, O(N) with random buckets, and fewer than a threshold t for the threshold-FHE scheme.
- Measured caveat, burianova-2025-secret: hiding a single leader drawn from a public candidate pool made coordinated DoS worse than no protection, with 28% versus 6-8% missed blocks.
- Rotating which part returns leaks the parent over repeated rounds. The predecessor-attack bounds and the hidden-server attack, which located servers in minutes, both show this. Stable guards fix it but concentrate risk.
- Hiding costs bandwidth or latency, and the anonymity trilemma gives the bound: each corrupted relay removes one round of latency budget.
- In the agent setting itself, dangol-2026-privacy measures that A2A metadata alone reveals a task's class at 6x chance.

Surprise: `lab.py check` gave 0 errors while 5 of my entries had YAML front matter that did not parse (an unquoted colon in `cite:`). Those entries were skipped silently by verify and by the library loader. I fixed them by quoting. The check probably needs a parse-error rule. That change is for the humans, since agents do not edit scripts/.

Wright 2004: Crossref stores a truncated title for DOI 10.1145/1042031.1042032, so verify flagged a title mismatch. I moved the DOI into `cite`.

Next:
- Catalogue secret committee election (hiding k returners). It joins Q1 and Q2.
- Add the Javadpour honeypot survey once it can be opened.
- Search biology camouflage and decoys.
- Run a dedicated search for LLM-agent work on hiding sub-agent identity or routing.
