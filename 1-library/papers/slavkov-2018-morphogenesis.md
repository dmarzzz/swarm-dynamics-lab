---
id: slavkov-2018-morphogenesis
type: paper
title: "Morphogenesis in robot swarms"
authors: ["I. Slavkov", "D. Carrillo-Zapata", "N. Carranza", "X. Diego", "F. Jansson", "J. Kaandorp", "S. Hauert", "J. Sharpe"]
year: 2018
venue: "Science Robotics"
url: https://doi.org/10.1126/scirobotics.aau9178
doi: "10.1126/scirobotics.aau9178"
arxiv: null
cite: "Slavkov, I., Carrillo-Zapata, D., Carranza, N., Diego, X., Jansson, F., Kaandorp, J., Hauert, S., & Sharpe, J. (2018). Morphogenesis in robot swarms. Science Robotics, 3(25), eaau9178."
topics: [swarm-robotics, active-matter]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "213 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Implements purely self-organising morphogenesis in a swarm of 300 robots: every robot runs the same
reaction-diffusion (Turing-type) gene circuit and interacts only with neighbours, and the resulting pattern
drives where the swarm grows. No robot self-localises. Swarms of 300 robots self-construct organic, adaptable shapes
that are robust to damage (they regrow after parts are cut away).

## Contribution

Brings developmental-biology self-organisation (Turing patterns) into a physical swarm, the bottom-up
alternative to the coordinate-based shape assembly of [[rubenstein-2014-programmable]].

## Key results

- Measured: 300-robot swarms form emergent, organic shapes without self-localisation, robust to damage.
- Shapes are emergent rather than user-specified (a limitation [[sun-2023-mean]] targets).

## Methods and models

Kilobots running an identical reaction-diffusion (Turing) gene-circuit model with local exchange between
neighbours; robot motion couples to the pattern. Abstract read; motion rules not checked.

## Limitations and open questions

Shapes cannot be precisely specified; growth is slow; sensitivity to Turing parameters not checked by me.

## Relevance to us

A ready-made example linking pattern-formation physics to robot swarms; candidate for a simulation where we
sweep reaction-diffusion parameters and swarm size.
