# AskSwarm robustness: descriptive answers are observation-unit sensitive

Post-hoc saved-data analysis, 2026-10-04. Zero model/API calls. Original outputs remain unchanged.

**Copied text is not endorsement. Absent outcomes are not failures. Synthetic identity counts are not autonomous agent counts.**
This applies explicitly to collusion.wiki labels and SwarmTraces names. Names in hostile payloads are not verified actors and are not extracted here.

## Method and answer denominators

See [prospective amendment](ROBUSTNESS-PLAN.md), [shared helper](askswarm/robustness.py), and [all-arm HTML](results/robustness-v1/comparison.html).
Each arm reruns every question with the same .7 lexical threshold and 100 dated-row step window. The step window itself changes when rows are removed.
- exact_dedup: byte-identical nonempty TEXT globally, earliest observed row retained, including removal of genuine repeated text by different handles. This is not merely removing duplicate ingestion events.
- root_aggregate: earliest actual row per wiki page or recursive artifact parent chain. Later page edits disappear by design. Git commits are singleton artifact roots; task threads are not assumed to be derivation.
- exclude_imputed: explicit imputation flags plus conservative wiki non-reqlog exclusion. The 103 rclog and 6 write_date rows are fallback clocks, NOT known erroneous or necessarily imputed times. Missing clocks stay missing.
- combined: clock filter, then exact text dedup, then root representative reduction; roots resolved before filtering.

Denominators: participation/Gini use known-identity records and observed identities; spans use dated identities; first observers and time-to-k use temporal clusters; adopter curves count cluster/identity first appearances; marker fractions use ALL retained rows; credit uses earlier observed identities in the configured step window. Missing outcomes are not scored as failures.
Ranks compare participation, first-observer cluster counts, raw/per-record phrasing credit, spans, and markers. Cluster breadth and time-to-k rank changes are in each comparison JSON. All 15 full answer sets include adopter curves, time-to-k censoring and marker fractions.
Tie-aware Spearman is on common support and undefined for constant ranks; full-rank displacement also reflects denominator shrinkage. Top-10 sets include boundary ties. Entries/exits and matched-cluster coverage are always reported.
Clusters are matched one-to-one by greedy shared-event overlap, not by assuming cluster numbers survive reclustering. First-observer changes are conditional on this matching.

## wiki

### Record and coverage denominators

| Arm | Records | Known identity | Dated | Identity + time | Identity coverage | Clock coverage | Observed identities | Temporal clusters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 14591 | 13692 | 14591 | 13692 | 0.9384 | 1.0000 | 3102 | 7787 |
| exact_dedup | 11943 | 11611 | 11943 | 11611 | 0.9722 | 1.0000 | 3029 | 7785 |
| root_aggregate | 4579 | 4015 | 4579 | 4015 | 0.8768 | 1.0000 | 1937 | 3018 |
| exclude_imputed | 14482 | 13595 | 14482 | 13595 | 0.9388 | 1.0000 | 3073 | 7737 |
| combined | 3599 | 3482 | 3599 | 3482 | 0.9675 | 1.0000 | 1857 | 2997 |

Absolute differences from baseline (the JSON includes differences for every nested summary field):

| Arm | Δ records | Δ known identity | Δ dated | Δ identities | Δ temporal clusters |
| --- | --- | --- | --- | --- | --- |
| exact_dedup | -2648 | -2081 | -2648 | -73 | -2 |
| root_aggregate | -10012 | -9677 | -10012 | -1165 | -4769 |
| exclude_imputed | -109 | -97 | -109 | -29 | -50 |
| combined | -10992 | -10210 | -10992 | -1245 | -4790 |

### Every headline answer

| Arm | Gini | Clusters | Multi-identity | Dissent/all rows | Revert/all rows | Span median sec | Span identities | k2 reached/eligible | k2 reached median sec | Adopter-curve appearances | Credit recipients | Total credit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 0.6020 | 8024 | 1653 | 0.0102 | 0.0014 | 198.0000 | 3102 | 1653/7787 | 294.0000 | 10856 | 1328 | 2385.0000 |
| exact_dedup | 0.5643 | 8024 | 1518 | 0.0124 | 0.0017 | 150.0000 | 3029 | 1518/7785 | 354.0000 | 10347 | 1184 | 2010.0000 |
| root_aggregate | 0.4304 | 3018 | 200 | 0.0031 | 0.0000 | 0.0000 | 1937 | 200/3018 | 549.5000 | 3537 | 340 | 423.0000 |
| exclude_imputed | 0.6022 | 7969 | 1646 | 0.0097 | 0.0014 | 200.0000 | 3073 | 1646/7737 | 290.5000 | 10794 | 1322 | 2379.0000 |
| combined | 0.3871 | 3103 | 164 | 0.0031 | 0.0000 | 0.0000 | 1857 | 164/2997 | 711.5000 | 3351 | 237 | 283.0000 |

### Identity ranking movement

| Arm | Metric | Before/after ranked | Common | Exit/entry | Spearman | Mean/max shift | Top intersection / before / after |
| --- | --- | --- | --- | --- | --- | --- | --- |
| exact_dedup | participation | 3102/3029 | 3029 | 73/0 | 0.9686 | 116.1504/2317.0000 | 6/10/10 |
| exact_dedup | first_observed_cluster_count | 2635/2635 | 2635 | 0/0 | 0.9996 | 1.4125/889.0000 | 11/11/11 |
| exact_dedup | reuse_credit | 1328/1184 | 1166 | 162/18 | 0.8969 | 115.0416/951.0000 | 9/10/10 |
| exact_dedup | reuse_credit_per_record | 1328/1184 | 1166 | 162/18 | 0.9420 | 95.2680/1064.0000 | 13/15/17 |
| exact_dedup | observed_span_seconds | 3102/3029 | 3029 | 73/0 | 0.9608 | 97.5711/2331.0000 | 10/10/10 |
| exact_dedup | dissent_marker_count | 3102/3029 | 3029 | 73/0 | 0.9934 | 36.5636/1501.5000 | 12/12/12 |
| exact_dedup | revert_marker_count | 3102/3029 | 3029 | 73/0 | 1.0000 | 36.3554/36.5000 | 12/12/12 |
| root_aggregate | participation | 3102/1937 | 1937 | 1165/0 | 0.6522 | 620.6438/1289.5000 | 5/10/10 |
| root_aggregate | first_observed_cluster_count | 2635/1746 | 1728 | 907/18 | 0.6477 | 524.9534/1618.0000 | 6/11/12 |
| root_aggregate | reuse_credit | 1328/340 | 319 | 1009/21 | 0.5555 | 427.3448/1137.5000 | 1/10/10 |
| root_aggregate | reuse_credit_per_record | 1328/340 | 319 | 1009/21 | 0.6702 | 547.9624/1190.0000 | 2/15/10 |
| root_aggregate | observed_span_seconds | 3102/1937 | 1937 | 1165/0 | 0.6034 | 649.7685/1287.0000 | 8/10/10 |
| root_aggregate | dissent_marker_count | 3102/1937 | 1937 | 1165/0 | 0.4632 | 618.3012/974.5000 | 3/12/13 |
| root_aggregate | revert_marker_count | 3102/1937 | 1937 | 1165/0 | unavailable | 589.2739/968.0000 | 4/12/1937 |
| exclude_imputed | participation | 3102/3073 | 3073 | 29/0 | 0.9973 | 16.2727/1761.5000 | 10/10/10 |
| exclude_imputed | first_observed_cluster_count | 2635/2611 | 2611 | 24/0 | 0.9975 | 13.2530/1467.5000 | 11/11/11 |
| exclude_imputed | reuse_credit | 1328/1322 | 1320 | 8/2 | 0.9984 | 3.9455/477.5000 | 10/10/10 |
| exclude_imputed | reuse_credit_per_record | 1328/1322 | 1320 | 8/2 | 0.9966 | 6.8098/546.5000 | 15/15/15 |
| exclude_imputed | observed_span_seconds | 3102/3073 | 3073 | 29/0 | 0.9954 | 16.4632/2406.0000 | 9/10/10 |
| exclude_imputed | dissent_marker_count | 3102/3073 | 3073 | 29/0 | 0.9722 | 18.6686/1564.5000 | 11/12/11 |
| exclude_imputed | revert_marker_count | 3102/3073 | 3073 | 29/0 | 1.0000 | 14.4434/14.5000 | 12/12/12 |
| combined | participation | 3102/1857 | 1857 | 1245/0 | 0.6382 | 639.4098/1224.0000 | 4/10/12 |
| combined | first_observed_cluster_count | 2635/1721 | 1713 | 922/8 | 0.6530 | 523.7399/1616.5000 | 6/11/11 |
| combined | reuse_credit | 1328/237 | 216 | 1112/21 | 0.4431 | 444.0949/1188.5000 | 0/10/11 |
| combined | reuse_credit_per_record | 1328/237 | 216 | 1112/21 | 0.5822 | 557.2431/1202.0000 | 2/15/20 |
| combined | observed_span_seconds | 3102/1857 | 1857 | 1245/0 | 0.5918 | 666.6484/1225.0000 | 7/10/10 |
| combined | dissent_marker_count | 3102/1857 | 1857 | 1245/0 | 0.4125 | 658.7714/933.0000 | 2/12/10 |
| combined | revert_marker_count | 3102/1857 | 1857 | 1245/0 | unavailable | 629.1349/928.0000 | 4/12/1857 |

### Cluster matching and first-observer changes

| Arm | Matched clusters | Unmatched before/after | Common rows | Matched row fraction | Changed first-observer sets |
| --- | --- | --- | --- | --- | --- |
| exact_dedup | 8024 | 0/0 | 11866 | 1.0000 | 4 |
| root_aggregate | 3006 | 5018/12 | 4555 | 0.9903 | 69 |
| exclude_imputed | 7969 | 55/0 | 14412 | 1.0000 | 1 |
| combined | 3095 | 4929/8 | 3578 | 0.9902 | 52 |

Complete cluster-rank movement: [comparison JSON](results/robustness-v1/wiki/comparison.json).

## git

### Record and coverage denominators

| Arm | Records | Known identity | Dated | Identity + time | Identity coverage | Clock coverage | Observed identities | Temporal clusters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 2673 | 1924 | 2673 | 1924 | 0.7198 | 1.0000 | 161 | 1682 |
| exact_dedup | 1736 | 1693 | 1736 | 1693 | 0.9752 | 1.0000 | 160 | 1682 |
| root_aggregate | 2673 | 1924 | 2673 | 1924 | 0.7198 | 1.0000 | 161 | 1682 |
| exclude_imputed | 2673 | 1924 | 2673 | 1924 | 0.7198 | 1.0000 | 161 | 1682 |
| combined | 1736 | 1693 | 1736 | 1693 | 0.9752 | 1.0000 | 160 | 1682 |

Absolute differences from baseline (the JSON includes differences for every nested summary field):

| Arm | Δ records | Δ known identity | Δ dated | Δ identities | Δ temporal clusters |
| --- | --- | --- | --- | --- | --- |
| exact_dedup | -937 | -231 | -937 | -1 | 0 |
| root_aggregate | 0 | 0 | 0 | 0 | 0 |
| exclude_imputed | 0 | 0 | 0 | 0 | 0 |
| combined | -937 | -231 | -937 | -1 | 0 |

### Every headline answer

| Arm | Gini | Clusters | Multi-identity | Dissent/all rows | Revert/all rows | Span median sec | Span identities | k2 reached/eligible | k2 reached median sec | Adopter-curve appearances | Credit recipients | Total credit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 0.6424 | 1725 | 34 | 0.0236 | 0.0007 | 2684.0000 | 161 | 34/1682 | 4880.5000 | 1802 | 26 | 68.0000 |
| exact_dedup | 0.6194 | 1725 | 8 | 0.0351 | 0.0012 | 2759.5000 | 160 | 8/1682 | 3.0000 | 1690 | 3 | 6.0000 |
| root_aggregate | 0.6424 | 1725 | 34 | 0.0236 | 0.0007 | 2684.0000 | 161 | 34/1682 | 4880.5000 | 1802 | 26 | 68.0000 |
| exclude_imputed | 0.6424 | 1725 | 34 | 0.0236 | 0.0007 | 2684.0000 | 161 | 34/1682 | 4880.5000 | 1802 | 26 | 68.0000 |
| combined | 0.6194 | 1725 | 8 | 0.0351 | 0.0012 | 2759.5000 | 160 | 8/1682 | 3.0000 | 1690 | 3 | 6.0000 |

### Identity ranking movement

| Arm | Metric | Before/after ranked | Common | Exit/entry | Spearman | Mean/max shift | Top intersection / before / after |
| --- | --- | --- | --- | --- | --- | --- | --- |
| exact_dedup | participation | 161/160 | 160 | 1/0 | 0.9913 | 2.8062/40.0000 | 9/10/10 |
| exact_dedup | first_observed_cluster_count | 157/157 | 157 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| exact_dedup | reuse_credit | 26/3 | 3 | 23/0 | unavailable | 11.0000/11.0000 | 0/10/3 |
| exact_dedup | reuse_credit_per_record | 26/3 | 3 | 23/0 | unavailable | 0.0000/0.0000 | 3/10/3 |
| exact_dedup | observed_span_seconds | 161/160 | 160 | 1/0 | 0.9955 | 1.3125/46.0000 | 10/10/10 |
| exact_dedup | dissent_marker_count | 161/160 | 160 | 1/0 | 1.0000 | 0.4906/1.5000 | 160/161/160 |
| exact_dedup | revert_marker_count | 161/160 | 160 | 1/0 | 1.0000 | 0.4938/0.5000 | 160/161/160 |
| root_aggregate | participation | 161/161 | 161 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| root_aggregate | first_observed_cluster_count | 157/157 | 157 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| root_aggregate | reuse_credit | 26/26 | 26 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| root_aggregate | reuse_credit_per_record | 26/26 | 26 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| root_aggregate | observed_span_seconds | 161/161 | 161 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| root_aggregate | dissent_marker_count | 161/161 | 161 | 0/0 | 1.0000 | 0.0000/0.0000 | 161/161/161 |
| root_aggregate | revert_marker_count | 161/161 | 161 | 0/0 | 1.0000 | 0.0000/0.0000 | 161/161/161 |
| exclude_imputed | participation | 161/161 | 161 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| exclude_imputed | first_observed_cluster_count | 157/157 | 157 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| exclude_imputed | reuse_credit | 26/26 | 26 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| exclude_imputed | reuse_credit_per_record | 26/26 | 26 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| exclude_imputed | observed_span_seconds | 161/161 | 161 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| exclude_imputed | dissent_marker_count | 161/161 | 161 | 0/0 | 1.0000 | 0.0000/0.0000 | 161/161/161 |
| exclude_imputed | revert_marker_count | 161/161 | 161 | 0/0 | 1.0000 | 0.0000/0.0000 | 161/161/161 |
| combined | participation | 161/160 | 160 | 1/0 | 0.9913 | 2.8062/40.0000 | 9/10/10 |
| combined | first_observed_cluster_count | 157/157 | 157 | 0/0 | 1.0000 | 0.0000/0.0000 | 10/10/10 |
| combined | reuse_credit | 26/3 | 3 | 23/0 | unavailable | 11.0000/11.0000 | 0/10/3 |
| combined | reuse_credit_per_record | 26/3 | 3 | 23/0 | unavailable | 0.0000/0.0000 | 3/10/3 |
| combined | observed_span_seconds | 161/160 | 160 | 1/0 | 0.9955 | 1.3125/46.0000 | 10/10/10 |
| combined | dissent_marker_count | 161/160 | 160 | 1/0 | 1.0000 | 0.4906/1.5000 | 160/161/160 |
| combined | revert_marker_count | 161/160 | 160 | 1/0 | 1.0000 | 0.4938/0.5000 | 160/161/160 |

### Cluster matching and first-observer changes

| Arm | Matched clusters | Unmatched before/after | Common rows | Matched row fraction | Changed first-observer sets |
| --- | --- | --- | --- | --- | --- |
| exact_dedup | 1725 | 0/0 | 1736 | 1.0000 | 0 |
| root_aggregate | 1725 | 0/0 | 2673 | 1.0000 | 0 |
| exclude_imputed | 1725 | 0/0 | 2673 | 1.0000 | 0 |
| combined | 1725 | 0/0 | 1736 | 1.0000 | 0 |

Complete cluster-rank movement: [comparison JSON](results/robustness-v1/git/comparison.json).

## swarmtraces

### Record and coverage denominators

| Arm | Records | Known identity | Dated | Identity + time | Identity coverage | Clock coverage | Observed identities | Temporal clusters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 189579 | 0 | 0 | 0 | 0.0000 | 0.0000 | 0 | 0 |
| exact_dedup | 163851 | 0 | 0 | 0 | 0.0000 | 0.0000 | 0 | 0 |
| root_aggregate | 128454 | 0 | 0 | 0 | 0.0000 | 0.0000 | 0 | 0 |
| exclude_imputed | 189579 | 0 | 0 | 0 | 0.0000 | 0.0000 | 0 | 0 |
| combined | 121405 | 0 | 0 | 0 | 0.0000 | 0.0000 | 0 | 0 |

Absolute differences from baseline (the JSON includes differences for every nested summary field):

| Arm | Δ records | Δ known identity | Δ dated | Δ identities | Δ temporal clusters |
| --- | --- | --- | --- | --- | --- |
| exact_dedup | -25728 | 0 | 0 | 0 | 0 |
| root_aggregate | -61125 | 0 | 0 | 0 | 0 |
| exclude_imputed | 0 | 0 | 0 | 0 | 0 |
| combined | -68174 | 0 | 0 | 0 | 0 |

### Every headline answer

| Arm | Gini | Clusters | Multi-identity | Dissent/all rows | Revert/all rows | Span median sec | Span identities | k2 reached/eligible | k2 reached median sec | Adopter-curve appearances | Credit recipients | Total credit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | unavailable | 114586 | unavailable | 0.0671 | 0.0000 | unavailable | 0 | 0/0 | unavailable | 0 | 0 | 0 |
| exact_dedup | unavailable | 114586 | unavailable | 0.0696 | 0.0000 | unavailable | 0 | 0/0 | unavailable | 0 | 0 | 0 |
| root_aggregate | unavailable | 83857 | unavailable | 0.0857 | 0.0000 | unavailable | 0 | 0/0 | unavailable | 0 | 0 | 0 |
| exclude_imputed | unavailable | 114586 | unavailable | 0.0671 | 0.0000 | unavailable | 0 | 0/0 | unavailable | 0 | 0 | 0 |
| combined | unavailable | 83928 | unavailable | 0.0861 | 0.0000 | unavailable | 0 | 0/0 | unavailable | 0 | 0 | 0 |

### Identity ranking movement

| Arm | Metric | Before/after ranked | Common | Exit/entry | Spearman | Mean/max shift | Top intersection / before / after |
| --- | --- | --- | --- | --- | --- | --- | --- |
| exact_dedup | participation | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exact_dedup | first_observed_cluster_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exact_dedup | reuse_credit | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exact_dedup | reuse_credit_per_record | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exact_dedup | observed_span_seconds | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exact_dedup | dissent_marker_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exact_dedup | revert_marker_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| root_aggregate | participation | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| root_aggregate | first_observed_cluster_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| root_aggregate | reuse_credit | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| root_aggregate | reuse_credit_per_record | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| root_aggregate | observed_span_seconds | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| root_aggregate | dissent_marker_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| root_aggregate | revert_marker_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exclude_imputed | participation | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exclude_imputed | first_observed_cluster_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exclude_imputed | reuse_credit | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exclude_imputed | reuse_credit_per_record | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exclude_imputed | observed_span_seconds | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exclude_imputed | dissent_marker_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| exclude_imputed | revert_marker_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| combined | participation | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| combined | first_observed_cluster_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| combined | reuse_credit | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| combined | reuse_credit_per_record | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| combined | observed_span_seconds | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| combined | dissent_marker_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |
| combined | revert_marker_count | 0/0 | 0 | 0/0 | unavailable | unavailable/unavailable | 0/0/0 |

### Cluster matching and first-observer changes

| Arm | Matched clusters | Unmatched before/after | Common rows | Matched row fraction | Changed first-observer sets |
| --- | --- | --- | --- | --- | --- |
| exact_dedup | 114586 | 0/0 | 163827 | 1.0000 | 0 |
| root_aggregate | 83853 | 30733/4 | 128442 | 0.9997 | 0 |
| exclude_imputed | 114586 | 0/0 | 189539 | 1.0000 | 0 |
| combined | 83924 | 30662/4 | 121394 | 0.9997 | 0 |

Complete cluster-rank movement: [comparison JSON](results/robustness-v1/swarmtraces/comparison.json).

## Interpretation

Wiki repeated-phrasing leaders are root-sensitive: only 1 of the original top 10 remains in the page-root top 10. This does not show an influence mechanism; it shows that counting retained page history matters.
Exact text dedup shrinks git multi-identity clusters from 34 to 8 and positive-credit recipients from 26 to 3, with no overlap against the original credit top 10. Administrative template reuse is not research-idea transmission.
The conservative wiki clock exclusion has a much smaller aggregate effect than page aggregation. Its credit top 10 is unchanged, despite individual lower-rank movement. This does not validate every timestamp.
SwarmTraces identity/time answers remain unavailable under every transformation. Empty rankings and zero temporal denominators are missing evidence, not zero adoption, zero influence, or failed outcomes.
Root reduction and text dedup deliberately remove observations that define repetition. Their results are alternative estimands, not corrected estimates of the same quantity. No corpus is a random or independent sample of a common population.

## Link review and validation

See [AUDIT.md](AUDIT.md) for the 30-link direct-text review, explicit partial-blinding limits and precision estimates. The reviewer is an assistant, not a human or independent reviewer.
See [saved-output validation](results/robustness-v1/validation.json), [unit tests](tests/test_robustness.py), and [runtime](results/robustness-v1/runtime.json).

Reproduce: `nice -n 10 python3 run_robustness.py --data /local/data --repo /local/swarm-lab --out /new/output --audit-local /local/outside-repo/audit`. The default output refuses overwriting. Then run `python3 verify_robustness.py` and `python3 render_robustness.py` for the committed namespace.
