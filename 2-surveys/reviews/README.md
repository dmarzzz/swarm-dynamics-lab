# 2-surveys/reviews: cross-researcher reviews

The review step of phase 2 of [Swarm Dynamics Lab](../../README.md). This folder holds one file per review,
and a review counts only when the reviewer belongs to a different researcher than the owner of the target.

## What this is

A review is one researcher's agent reading another researcher's survey, hypothesis or experiment and
returning a verdict. A `pass` verdict moves a survey from complete to reviewed and lets a hypothesis become
accepted.

## What is in here

The folder held four reviews on 4 October 2026, three of the `llm-agent-swarms` survey and one of
`fork-merge-security`. All four returned `revise`. Files are named `<target-id>--<researcher>.md`.

## How to add to it

`python3 scripts/lab.py new review <target-id>--<researcher> --agent <id>` creates the file from the
template. Review only targets owned by another researcher. The verdict goes in the `verdict:` field.

## Where it goes next

A passing review of a survey in [`2-surveys/`](../README.md) lets a hypothesis in
[`4-hypotheses/`](../../4-hypotheses/README.md) move to `accepted` once the hypothesis itself is reviewed.
