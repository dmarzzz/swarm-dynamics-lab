---
id: alahi-2016-social
type: paper
title: 'Social LSTM: Human Trajectory Prediction in Crowded Spaces'
authors:
- Alexandre Alahi
- Kratarth Goel
- Vignesh Ramanathan
- Alexandre Robicquet
- Li Fei-Fei
- Silvio Savarese
year: 2016
venue: IEEE Conference on Computer Vision and Pattern Recognition (CVPR) 2016
url: https://openaccess.thecvf.com/content_cvpr_2016/html/Alahi_Social_LSTM_Human_CVPR_2016_paper.html
doi: 10.1109/cvpr.2016.110
arxiv: null
cite: 'Alahi, A., Goel, K., Ramanathan, V., Robicquet, A., Fei-Fei, L., & Savarese, S. (2016). Social LSTM: Human trajectory prediction in crowded spaces. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 961–971. https://doi.org/10.1109/CVPR.2016.110'
topics:
- crowds-and-traffic
- marl-emergence
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 2925 (Crossref, 2026-10-03)
code: []
---

## Summary

Learns human–human interactions for trajectory prediction instead of hand-crafting them as social forces. One LSTM per person, with a pooling layer that shares hidden states of neighbouring trajectories, predicts future positions jointly. On public pedestrian datasets it outperforms prior forecasting methods by more than 42% (as stated in the abstract) and learns behaviours such as collision avoidance and group movement.

## Contribution

Launched the deep-learning line of crowd trajectory prediction (Social GAN, Trajectron++, AgentFormer and others), now a large ML community parallel to physics-based crowd modelling.

## Key results

- Measured (abstract): more than 42% improvement over previous forecasting methods on public datasets.
- Qualitative: learned avoidance and group behaviours.

## Methods and models

One LSTM per trajectory; a pooling layer shares hidden representations of neighbouring trajectories. CVPR 2016 pp. 961–971; open access version at the CVF page.

## Limitations and open questions

Prediction, not mechanism; generalisation and physical plausibility are known problems (see comparisons in Korbmacher and Tordeux 2022, not catalogued). Abstract only.

## Relevance to us

Represents the ML community's vocabulary for crowd interactions. Useful baseline if the hackathon learns interaction rules from data; contrast with physics-informed learning in [[he-2025-learning]] and [[minartz-2025-discovering]].
