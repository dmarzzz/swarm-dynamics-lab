---
id: data-juelich-crowd-2019
type: dataset
title: Motion through a dense and stationary crowd
authors:
- Benedikt Kleinmeier
- Gerta Köster
- John Drury
year: 2019
url: https://ped.fz-juelich.de/da/doku.php?id=motion_through_crowd
license: Archive wiki content CC-BY-4.0 unless otherwise noted; downloaded ZIP has no separate licence file, binary reuse terms not independently established
size: 'Primary description: 27 participants, 30 runs; each run tracks 14 participants
  (one walker, 13 waiting); video 25 fps, 73 minutes raw'
format: Per-run trajectories as text, participant XLSX, analysis Jupyter notebooks
topics:
- collective-motion
- crowds-and-traffic
- criticality-measurement
read_depth: ran
relevance: 4
papers: []
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

A controlled October 2018 experiment observes a walker passing through a dense stationary crowd, generating trajectory-based human coordination controls. Archive description and data layout make this a classical non-agent null model rather than evidence of an AI swarm.

## Access

Primary Jülich archive page opened via Exa and direct HTTP 2026-10-03. DOI 10.34735/ped.2019.1, related paper DOI 10.1098/rsif.2020.0396. Page supplies trajectory layout, companion notebooks and data access. Downloaded ExperimentDenseCrowd.zip via https://ped.fz-juelich.de/data/experiments/external/kleinmeier/motionThroughCrowd/ExperimentDenseCrowd.zip (19,551,151 bytes) and loaded a trajectory on 2026-10-03. The member ExperimentDenseCrowd/data/trajectories/waiting_area_trapezoid_group/40_data/Person10 contains 546 lines including two headers, with t/x/y/vx/vy/ax/ay and 0.04 s time steps. Basic loader: zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url).read())).read(member).decode().

Method: camera 1280x720 at 25 fps, optical correction and manual/Tracker trajectory extraction; one moving and 13 waiting participants in 2.64 square metres, reported density 5.30 pedestrians/m². Intro says 27 participants/30 runs; later mentions 45 participants in a waiting room. Preserve that internal inconsistency rather than silently merging population counts.

Licence footer explicitly CC-BY-4.0 for wiki content unless otherwise noted. Downloaded ZIP README describes student tracking and repository provenance but gives no separate licence; no COPYING/LICENCE file found. Verify binary reuse terms before redistribution, rather than treating the wiki-footer licence as conclusively licensing every bundled file. Companion [[data-lurebot-2023]] was actually downloaded and loaded under an explicit primary CC-BY-4.0 dataset licence.

## Relevance to us

Human-crowd trajectories for null models and coordination specificity. These tracks provide spatial interactions, not social-media authorship or malicious intent labels.
