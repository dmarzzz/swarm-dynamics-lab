---
id: juels-2013-honeywords
type: paper
title: Honeywords
authors:
- Ari Juels
- Ronald L. Rivest
year: 2013
venue: Proceedings of the 2013 ACM SIGSAC conference on Computer & communications
  security - CCS '13
url: https://dspace.mit.edu/handle/1721.1/90627
doi: 10.1145/2508859.2516671
arxiv: null
cite: Ari Juels; Ronald L. Rivest. (2013). Honeywords. Proceedings of the 2013 ACM
  SIGSAC conference on Computer & communications security - CCS '13, 145-160. https://doi.org/10.1145/2508859.2516671
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Honeywords stores decoy password hashes alongside the real password for each account. A stolen hash database therefore creates uncertainty about which cracked value is valid; an auxiliary honeychecker detects login attempts using a decoy and raises an alarm.

## Contribution

Proposes storing decoy password hashes plus a separate honeychecker so that use of a cracked decoy reveals a breach.

## Key results

- The abstract proposes a breach-detection mechanism but provides no deployment detection rate.

## Methods and models

Decoy passwords, hashed storage, and a separate honeychecker.

## Limitations and open questions

Security depends on decoy indistinguishability and separation of the honeychecker; this is password-theft detection rather than swarm attribution.

## Relevance to us

Background only: a decoy-credential pattern that agent honeypots reuse, but no swarm or coordination content.

## Access provenance

Crossref metadata and the abstract at the recorded URL were opened directly or through Exa content extraction on 2026-10-03. Any non-null citation count is OpenAlex cited_by_count on that date. Abstract depth is deliberate even where an open PDF was found.


## Notes from shadow/sol-w5

Added in parallel from pipeline batch #77; this id was taken first by shadow/sol-g51, so my entry is folded in here. My reading depth: skim (source opened: https://people.csail.mit.edu/rivest/pubs/JR13.pdf).

### Summary

Proposes storing, for every user account, k-1 decoy passwords ("honeywords") alongside the real one, all hashed identically, so an attacker who steals and cracks the password file cannot tell which of the k "sweetwords" is real. The index of the real password lives only on a separate, hardened "honeychecker" server that does nothing but store the index c(i), answer "is index j correct for user i", and raise an alarm when a honeyword is submitted. Logging in with a cracked honeyword therefore reliably signals that the hash file was stolen. They define security as flatness: a generator is epsilon-flat if no adversary guesses the true index with probability above epsilon (ideal 1/k; they recommend k = 20, so a blind guess gets caught 95% of the time). Generation methods: chaffing by tweaking digits/characters, chaffing with a password model, "tough nuts" (very hard honeywords), a modified-UI "take-a-tail" scheme that appends a random three-digit tail, and a hybrid. Also covers typo safety, old passwords, storage, denial-of-service (an attacker who knows a real password can trip honeywords on purpose; picking 19 honeywords from 1000 tail variants cuts that to about 2%) and attacks on the honeychecker. Skimmed: setup, security definitions, generation methods, DoS, open problems.

### Contribution

Turns honeypot accounts into per-account decoys, making offline password cracking detectable at the first online use, with a minimal separate trust component (the honeychecker) and a clean flatness definition for decoy quality.

### Key results

- Formal flatness metric for decoy generators; k = 20 recommended.
- Design argument and analysis, no user study or deployment data: the authors call it "an initial stab".
- Explicit DoS trade-off for tweak-based generators and a mitigation by random subset selection.

### Methods and models

Security game for honeyword generation, design of the honeychecker interface (Set and Check commands), analysis of generation methods against general and targeted guessing.

### Limitations and open questions

Authors list: active attacks on the computer system or honeychecker, persistent observation of submitted passwords, targeted attacks using knowledge of the user, quantifying flatness experimentally, how attackers should handle tough nuts. Follow-up work on how distinguishable honeywords are in practice was not checked for this entry.

### Relevance to us

The cleanest formal template for decoy-based detection of automated adversaries: plant indistinguishable bait that only an illegitimate actor would ever use, keep the ground truth in a separate minimal component, and measure decoy quality as the adversary's best distinguishing probability. That transfers to canaries and honeypots for agent swarms (fake credentials, fake endpoints, fake instructions in content). Related decoy work: [[bowen-2009-baiting]], [[gh-thinkst-canarytokens]], [[farooqi-2020-canarytrap]], [[gh-palisaderesearch-llm-honeypot]].
