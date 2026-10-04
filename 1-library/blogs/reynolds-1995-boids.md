---
id: reynolds-1995-boids
type: blog
title: "Boids (Flocks, Herds, and Schools: a Distributed Behavioral Model)"
authors: [Craig Reynolds]
year: 1995
url: https://www.red3d.com/cwr/boids/
site: red3d.com
topics: [collective-motion, meta]
added_by: shadow/sol-w3
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Craig Reynolds' own home page for the boids model (counter "since June 29, 1995", body last updated September 6, 2001, link fixes 2006 and 2007). It recounts that he built the model in 1986, presented it as a SIGGRAPH '87 paper [[reynolds-1987-flocks]] alongside the short film "Stanley and Stella in: Breaking the Ice", and informally at Langton's first Artificial Life workshop. The model is three steering behaviours (separation, alignment, cohesion) computed only over flockmates inside a local neighbourhood defined by a distance and an angle from the heading; early versions added predictive obstacle avoidance and low-priority goal seeking. Reynolds frames boids as an individual-based model, notes that mixing nonlinear behaviours gives chaotic group dynamics while the negative feedback of the controllers keeps them ordered, and argues the result is "life-like": predictable over a second, unpredictable over minutes, which he ties to Langton's edge-of-chaos idea. He notes the naive algorithm is O(n^2) and can be brought near O(n) with a spatial data structure. The rest of the page is a large, mostly dead, link list of applications (Batman Returns 1992 bats and penguins, The Lion King stampede), press articles and other group-motion models.

## Key claims

- Flocking needs only local reactions: each boid steers from the positions and velocities of flockmates within a small distance-and-angle neighbourhood, ignoring the rest of the scene.
- Three behaviours suffice for the basic model: separation (avoid crowding), alignment (match heading), cohesion (move toward local centre).
- Group behaviour is short-term predictable and long-term unpredictable, which Reynolds presents as a signature of complex rather than chaotic or ordered systems (an interpretive claim, not measured).
- Naive neighbour search is O(n^2); spatial binning makes it nearly O(n), enabling real-time large flocks.

## Evidence quality

Author's own explanatory page, not a paper. No quantitative results; the claims about predictability are informal observations from running the applet. The technical source is the 1987 paper [[reynolds-1987-flocks]]. Many outbound links are from the late 1990s and now dead. Useful as primary history and as the author's own one-paragraph statement of the rules.

## Relevance to us

The canonical informal reference for the boids rules, from the author. Good for citing the exact neighbourhood definition (distance plus view angle, not topological k-nearest as in [[ballerini-2008-interaction]]) and for the provenance of "simple local rules, emergent global behaviour" language that LLM-swarm posts reuse loosely. Compare [[vicsek-1995-novel]] (alignment plus noise only) and [[couzin-2002-collective]] (zonal version). The 2026 follow-up [[reynolds-2026-evoflock]] is Reynolds' own later work.
