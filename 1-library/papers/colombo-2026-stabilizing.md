---
id: colombo-2026-stabilizing
type: paper
title: "Stabilizing Role of Uninformed Participants in Collective Decision Making"
authors: ["Leonardo Colombo", "María Emma Eyrea Irazú", "Laura P. Schaposnik", "James Unwin"]
year: 2026
venue: "arXiv preprint"
url: "https://arxiv.org/abs/2606.11259"
doi: null
arxiv: "2606.11259"
cite: "Colombo, L., Eyrea Irazú, M. E., Schaposnik, L. P., & Unwin, J. (2026). Stabilizing Role of Uninformed Participants in Collective Decision Making. arXiv preprint arXiv:2606.11259. https://arxiv.org/abs/2606.11259"
topics: ["collective-decision", "sync-consensus"]
added_by: dmarz/collective-decision-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "0 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Second-order network model of directional consensus written as a port-contact-Hamiltonian system: informed agents pull toward preferred headings, uninformed agents contribute only damping. Under low conflict there is a unique, exponentially stable compromise heading. On a modular network, increasing conflict ends the compromise branch at a saddle-node fold rather than a smooth symmetry-breaking pitchfork, and uninformed agents' damping delays escape past the fold's ghost, pushing the observed onset of polarisation to larger conflicts.

## Contribution

Proposes a new mechanism for the stabilising effect of uninformed individuals reported by [[couzin-2011-uninformed]]: not dilution of the minority through connectivity, but direction-free dissipation acting on the slowest collective modes. It contrasts with the pitchfork picture in [[leonard-2012-decision]] and [[bizyaeva-2023-nonlinear]].

## Key results

- Low conflict and enough connectivity: unique, locally exponentially stable compromise equilibrium (theorem).
- Modular network: compromise is lost through a saddle-node fold; polarised states sit on separate branches (bifurcation analysis).
- Damping does not move the static threshold but lengthens the bottleneck passage, shifting the observable transition (finite-time simulation).
- No experimental data.

## Methods and models

Agents carry heading theta_i, momentum p_i and a contact variable z_i; contact Hamiltonian K_i = p_i^2/2 - alpha_i cos(theta_i - phi_i) - kappa sum_j a_ij cos(theta_j - theta_i) + gamma_i z_i, giving a damped second-order Kuramoto system. Uninformed agents have alpha_i near 0. Algebraic connectivity lambda_2 of the graph Laplacian sets the weakest coordination mode. I skimmed the introduction and model sections.

## Limitations and open questions

Second-order inertia is assumed rather than measured; modular networks are stylised; no comparison with fish or other data. Preprint, not peer reviewed.

## Relevance to us

Offers a testable alternative explanation for the uninformed-individual effect: vary agents' damping independently of their connectivity in a swarm simulation and see which one controls the polarisation threshold. Related: [[couzin-2011-uninformed]], [[hartnett-2016-heterogeneous]], [[leonard-2024-fast]].
