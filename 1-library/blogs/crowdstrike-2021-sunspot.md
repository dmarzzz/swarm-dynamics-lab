---
id: crowdstrike-2021-sunspot
type: blog
title: "SUNSPOT: An Implant in the Build Process"
authors: ["CrowdStrike Intelligence Team"]
year: 2021
url: https://www.crowdstrike.com/blog/sunspot-malware-technical-analysis/
site: CrowdStrike blog
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Vendor technical analysis (January 11, 2021) of SUNSPOT, the implant the StellarParticle actor used to insert the SUNBURST backdoor into SolarWinds Orion builds. SUNSPOT ran on the build system disguised as taskhostsvc.exe, watched for MsBuild.exe processes (identified by an ElfHash of the process name, 0x53D525), read the target solution path from MsBuild's process memory, and swapped the source file InventoryManager.cs for a backdoored version only for the duration of the build, wrapping the inserted code in "#pragma warning disable" to avoid compiler warnings. It checked MD5 hashes (the backdoored source hash is given as 5f40b59ee2a9ac94ddb6ab9e3bd776ca) so that a mismatch would not break the build and expose it, and logged to an encrypted file named like a VMware dump. The binary's build timestamp is 2020-02-20 11:40:02; the exact active period is not established. I read the post through a fetch-and-summarise tool, so the details above are as reported by that tool from the page.

## Key claims

- The source repository stayed clean; the malicious code existed only transiently during compilation on the build host.
- The implant took care to avoid build failures, because a failed build would draw attention.
- Detection would require comparing the shipped binary to an independent build from the same source.

## Evidence quality

Vendor incident-response analysis based on recovered malware; specific indicators (hashes, names) are given. It is a primary technical source for the build-time mechanism but not peer reviewed. Academic framing of the incident appears in [[lamb-2022-reproducible]] and [[ladisa-2022-taxonomy]].

## Relevance to us

Q3: a real, well-documented case where the attacker corrupts the process that turns trusted inputs into an output, not the inputs themselves, and engineers the corruption to be invisible to the checks the victim actually ran. For a sub-agent in a hostile domain the analogue is corrupting its tools, retrieval or execution environment so that its stated instructions and identity remain intact while its returned conclusions are altered. Q2: the defence that would have caught it, independent rebuild and compare, is a k-of-n check over execution, as in [[lamb-2022-reproducible]] and the threshold steps of [[torres-arias-2019-in-toto]].
