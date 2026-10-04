---
id: querejeta-azurmendi-2021-zksense
type: paper
title: "ZKSENSE: A Friction-less Privacy-Preserving Human Attestation Mechanism for Mobile Devices"
authors: [Iñigo Querejeta-Azurmendi, Panagiotis Papadopoulos, Matteo Varvello, Antonio Nappa, Jiexin Zhang, Benjamin Livshits]
year: 2021
venue: Proceedings on Privacy Enhancing Technologies (PoPETs), 2021(4), pp. 6-29
url: https://arxiv.org/abs/1911.07649
doi: 10.2478/popets-2021-0058
arxiv: "1911.07649"
cite: "Querejeta-Azurmendi, I., Papadopoulos, P., Varvello, M., Nappa, A., Zhang, J., & Livshits, B. (2021). ZKSENSE: A Friction-less Privacy-Preserving Human Attestation Mechanism for Mobile Devices. Proceedings on Privacy Enhancing Technologies, 2021(4), 6-29. https://doi.org/10.2478/popets-2021-0058"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "2 (Crossref, 2026-10-03)"
code: []
---

## Summary

Earlier arXiv title: "ZKSENSE: a Privacy-Preserving Mechanism for Bot Detection in Mobile Devices" (arXiv v1 lists Papadopoulos first; the PoPETs version lists Querejeta-Azurmendi first, followed here). Motivated by the claim that 20.4% of internet traffic comes from automated agents and that CAPTCHAs are slow (visual 9.8 s, audio 28.4 s average), inaccurate and, in the case of reCAPTCHA v3, privacy-invasive, the paper moves humanness attestation onto the user's phone. An Android service continuously observes screen touches together with motion-sensor traces (accelerometer, gyroscope) around each touch; a classifier trained on human and automated click data (automated clicks show e.g. 8.5x greater maximum linear acceleration anomalies and no micro-motion) decides whether the actor is human. Crucially the sensor data never leaves the device: the classifier is an SVM evaluated inside a zero-knowledge proof (Pedersen commitments plus inner-product proofs in the Bulletproofs style, which the authors call ZK SVM, compared against a general-purpose ZoKrates ZK-SNARK that is far slower), and the device presents a proof of humanness that is then exchanged for blinded tokens usable anonymously across sites, in the Privacy Pass pattern. Evaluation: 91% accuracy across a range of attack scenarios (replayed and synthetic touch/sensor streams, automation frameworks); on a two-year-old Samsung S9 a full attestation takes about 3 seconds end to end with negligible battery cost. Read from the arXiv v3 full text: abstract, introduction and design goals, threat model, ZK SVM construction overview, evaluation headline numbers and attack scenarios, comparison with ZK-SNARKs, conclusion; cryptographic proofs skimmed.

## Contribution

First zero-knowledge, on-device, continuous humanness attestation: bot detection as a private proof rather than a server-side behavioural profile, with a practical ZK-SVM that runs in seconds on a mid-range phone.

## Key results

- 91% accuracy distinguishing human from automated interaction across attack scenarios.
- ~3 s per attestation on a Samsung S9 vs 9.8 s for visual CAPTCHAs; negligible battery.
- ZK SVM orders of magnitude cheaper than a generic ZK-SNARK (ZoKrates) for the same classifier.
- Output is a blinded token, so attestations are unlinkable across sites.

## Methods and models

Android sensor + touch telemetry, SVM classifier, Pedersen commitments and inner-product arguments for ZK inference, blind-token issuance, dataset from a small group of real users plus synthetic attacks.

## Limitations and open questions

91% accuracy means 9% error at scale; requires a device with sensors and trusted-enough OS to not fabricate sensor streams (an attacker with a rooted device can feed synthetic sensor data, which the paper partially addresses in attack scenarios); it attests "a human is touching this device", not "one human, one identity", so it rate-limits bots rather than preventing Sybils; small training population.

## Relevance to us

A concrete, deployed-style design for the agent-vs-human boundary that swarm-detection needs: attest humanness privately and issue capped tokens, which is the mechanism behind "humans get N free actions, agents must pay or be labelled". Combine with per-identity rate limiting as in [[akama-2024-scrappy]] and the uniqueness layer in [[abdolmaleki-2026-attribute]] for a full stack; proof-of-personhood context in [[ford-2020-identity]] and [[siddarth-2020-who]]. For LLM-agent swarms the threat side is that agents driving real devices (or emulators with synthetic sensors) can try to pass; the 91% figure is the current bar. Root: [[douceur-2002-sybil]].
