---
id: data-lurebot-2023
type: dataset
title: Preliminary biohybrid experiments with the Behavioral Observation & Biohybrid
  Interaction framework (featuring the LureBot)
authors:
- Vaios Papaspyros
- Daniel Burnier
- Raphael Cherfan
- Guy Theraulaz
- Clément Sire
- Francesco Mondada
year: 2023
url: https://zenodo.org/api/records/7802098
license: CC-BY-4.0
size: 17,299,802-byte Data.zip; 898 .dat trajectory members counted after download,
  including processed trajectories; advertised one-hour experiments with 1, 2 or 5
  fish/robot agents
format: ZIP containing whitespace-separated numeric .dat positions and companion _ridx.dat
  robot identity files
topics:
- collective-motion
- swarm-robotics
- criticality-measurement
read_depth: ran
relevance: 5
papers: []
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

LureBot trajectories pair living H. rhodostomus fish with a biomimetic robotic lure, including fish-only controls, open-loop circular or eightfold-rose motion and closed-loop interactions. Advertised experiments last one hour with single, pair or five-agent conditions. Sampling rate is not disclosed by the record.

## Access

Open Zenodo record, published 2023-04-03, CC-BY-4.0, no registration. Downloaded 2026-10-03 and loaded a trajectory. Archive contains 898 trajectory .dat members excluding _ridx and macOS metadata, not 898 independent experimental replicates. Selected processed member has 34 rows and two columns, all finite. Short processed segments must not be mistaken for whole one-hour trials.

```python
import io, urllib.request, zipfile, numpy as np
u = 'https://zenodo.org/api/records/7802098/files/Data.zip/content'
z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(u).read()))
a = np.loadtxt(io.BytesIO(z.read(
    'Biomimetic Interaction Model/single_agent/Fish/exp_9-13_processed_positions.dat')))
print(a.shape, np.isfinite(a).all())  # (34, 2), True
```

Licence verified from the primary record's metadata, not inferred from repository software. Download bytes measured locally; no binary data committed.

## Relevance to us

Runnable natural/robotic null models for coordination metrics, with matched fish-only and mixed-agent regimes. Small groups test analysis specificity, not large-LLM-swarm detection or operator attribution.
