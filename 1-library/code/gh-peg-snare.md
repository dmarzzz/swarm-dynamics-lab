---
id: gh-peg-snare
type: code
title: "snare: canary credentials planted in an AI agent host (AWS, SSH, kube, git, npm) that alert when a hijacked agent uses them"
repo: peg/snare
url: https://github.com/peg/snare
authors: ["peg"]
year: 2026
language: Go
license: "Apache-2.0"
stars: 5
last_commit: 2026-09-12
topics: [swarm-detection, fork-merge-security]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Go CLI that plants fake but realistic credentials in the standard places an agent host keeps them (~/.aws/config, ~/.ssh/config, a kubeconfig, ~/.gitconfig, ~/.npmrc) and fires a webhook when one is used. The AWS canary uses `credential_process`, so the alert fires when the SDK resolves the profile, before any API call (README claims T+0.01 s, before CloudTrail sees anything). The alert reports IP, ASN and user agent, and flags requests from cloud ASNs as 'likely AI agent'. Default 'precision mode' plants only canaries that fire on active use of a planted fake target, to stay quiet while legitimate agents work.

## What it can do for us

A different branch of detection from honeypots that attract outside agents: canaries inside our own fleet that reveal when one of our agents has been hijacked or is acting outside its task. Pairs with the fork-and-merge corruption question: a sub-agent that touches a canary is evidence of compromise before merge.

## Run notes

Not run (install is `curl | sh` or Homebrew, and it writes into ~/.aws and ~/.ssh, which I did not want to modify on this machine).

## Limitations

Tiny project (5 stars). The 'likely AI agent' label is an ASN heuristic, not agent detection; a human attacker on a cloud VM looks the same. Requires the hosted snare.sh callback service or self-hosting. No measured detection data.
