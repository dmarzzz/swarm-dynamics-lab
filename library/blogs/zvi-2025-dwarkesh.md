---
id: zvi-2025-dwarkesh
type: blog
title: On Dwarkesh Patel's Podcast With Richard Sutton
authors: [Zvi Mowshowitz]
year: 2025
url: https://thezvi.wordpress.com/2025/09/29/on-dwarkesh-patels-podcast-with-richard-sutton/
site: Don't Worry About the Vase (thezvi.wordpress.com; also on Substack and LessWrong), 2025-09-29
topics: [fork-merge-security, meta]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

A point-by-point commentary on [[sutton-2025-father]], posted under the byline TheZvi, mostly paraphrase with the author's responses nested. On the fork-merge passage he questions the premise that knowledge must return as weight changes: "why can't they learn via reading? Wouldn't they also get very good at knowing how to describe what they know?" He adds that "You should be able to merge deltas directly in various ways we already know about", and that "Even if nothing else works, you can simply have the 'base' version of the ASI in question rerun the relevant experiences once it is verified that they led to something worthwhile". On corruption he writes that it "Seems fun to think about, but nothing an army of ASIs couldn't handle", and that the "'mind viruses' in this scenario" are not "fundamentally different than the problems with memetics and hazardous information we experience today, although they'll be at a higher level."

## Key claims

- Knowledge can return through text the parent reads, not only through weights.
- Weight deltas can already be merged by known methods.
- Fallback merge: the parent re-runs a child's experiences after verifying they were worthwhile.
- Corruption risk is continuous with today's memetic hazards.

## Evidence quality

Opinion commentary, no citations for the merge-deltas claim.

## Relevance to us

The first public response to Sutton's corruption point found in this lane, and it is dismissive, which is useful to record as a position. Two of its claims bear on Q3. The "learn by reading" channel does not remove Sutton's risk; it relocates it to prompt injection and persuasion, where the parent ingests attacker-influenced text (see [[christiano-2016-security]] on unreasonably compelling arguments). The "rerun the experiences once verified" fallback is a genuine defence design: the parent re-derives knowledge from raw observations itself rather than accepting a child's conclusions, so a child can corrupt only by selecting which experiences to forward, not by writing into the parent. It still leaves the verification step and the raw data as attack surfaces, and costs roughly the child's original compute. The claim that an "army of ASIs" can handle it is untested.
