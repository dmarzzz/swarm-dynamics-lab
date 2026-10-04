#!/usr/bin/env python3
"""Render all answer denominators and ranking movements from immutable saved output."""
import json
from pathlib import Path

ROOT = Path('results/robustness-v1')
ARMS = ('baseline', 'exact_dedup', 'root_aggregate', 'exclude_imputed', 'combined')


def fmt(value):
    if value is None:
        return 'unavailable'
    return f'{value:.4f}' if isinstance(value, float) else str(value)


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |'] +
                     ['| ' + ' | '.join(fmt(v) for v in row) + ' |' for row in rows])


def main():
    out = ['# AskSwarm robustness: descriptive answers are observation-unit sensitive',
           '', 'Post-hoc saved-data analysis, 2026-10-04. Zero model/API calls. Original outputs remain unchanged.',
           '', '**Copied text is not endorsement. Absent outcomes are not failures. Synthetic identity counts are not autonomous agent counts.**',
           'This applies explicitly to collusion.wiki labels and SwarmTraces names. Names in hostile payloads are not verified actors and are not extracted here.',
           '', '## Method and answer denominators', '',
           'See [prospective amendment](ROBUSTNESS-PLAN.md), [shared helper](askswarm/robustness.py), and [all-arm HTML](results/robustness-v1/comparison.html).',
           'Each arm reruns every question with the same .7 lexical threshold and 100 dated-row step window. The step window itself changes when rows are removed.',
           '- exact_dedup: byte-identical nonempty TEXT globally, earliest observed row retained, including removal of genuine repeated text by different handles. This is not merely removing duplicate ingestion events.',
           '- root_aggregate: earliest actual row per wiki page or recursive artifact parent chain. Later page edits disappear by design. Git commits are singleton artifact roots; task threads are not assumed to be derivation.',
           '- exclude_imputed: explicit imputation flags plus conservative wiki non-reqlog exclusion. The 103 rclog and 6 write_date rows are fallback clocks, NOT known erroneous or necessarily imputed times. Missing clocks stay missing.',
           '- combined: clock filter, then exact text dedup, then root representative reduction; roots resolved before filtering.',
           '', 'Denominators: participation/Gini use known-identity records and observed identities; spans use dated identities; first observers and time-to-k use temporal clusters; adopter curves count cluster/identity first appearances; marker fractions use ALL retained rows; credit uses earlier observed identities in the configured step window. Missing outcomes are not scored as failures.',
           'Ranks compare participation, first-observer cluster counts, raw/per-record phrasing credit, spans, and markers. Cluster breadth and time-to-k rank changes are in each comparison JSON. All 15 full answer sets include adopter curves, time-to-k censoring and marker fractions.',
           'Tie-aware Spearman is on common support and undefined for constant ranks; full-rank displacement also reflects denominator shrinkage. Top-10 sets include boundary ties. Entries/exits and matched-cluster coverage are always reported.',
           'Clusters are matched one-to-one by greedy shared-event overlap, not by assuming cluster numbers survive reclustering. First-observer changes are conditional on this matching.', '']
    for source in ('wiki', 'git', 'swarmtraces'):
        reports = {arm: json.loads((ROOT / source / arm / 'metrics.json').read_text()) for arm in ARMS}
        comparison = json.loads((ROOT / source / 'comparison.json').read_text())
        out += ['## ' + source, '', '### Record and coverage denominators', '']
        out += [table(['Arm','Records','Known identity','Dated','Identity + time','Identity coverage','Clock coverage','Observed identities','Temporal clusters'],
                      [[a] + [reports[a]['summary'][k] for k in ('records','known_identity_records','dated_records','identity_and_time_records','identity_coverage','time_coverage','identities','temporal_clusters')] for a in ARMS]), '']
        out += ['Absolute differences from baseline (the JSON includes differences for every nested summary field):', '',
                table(['Arm','Δ records','Δ known identity','Δ dated','Δ identities','Δ temporal clusters'],
                      [[a] + [comparison['comparisons'][a]['summary_deltas'][k]['delta'] for k in ('records','known_identity_records','dated_records','identities','temporal_clusters')] for a in ARMS[1:]]), '']
        out += ['### Every headline answer', '',
                table(['Arm','Gini','Clusters','Multi-identity','Dissent/all rows','Revert/all rows','Span median sec','Span identities','k2 reached/eligible','k2 reached median sec','Adopter-curve appearances','Credit recipients','Total credit'],
                      [[a, r['summary']['participation_gini'],r['summary']['clusters'],r['summary']['multi_identity_clusters'],
                        r['summary']['dissent_marker_fraction'],r['summary']['revert_marker_fraction'],
                        r['summary']['identity_span_seconds']['median'],r['summary']['identity_span_seconds']['n'],
                        str(r['summary']['time_to_k']['2']['reached'])+'/'+str(r['summary']['temporal_clusters']),
                        r['summary']['time_to_k']['2']['seconds_among_reached']['median'],
                        sum(x['clusters'] for x in r['adoption_events_by_elapsed_hour_and_rank']),
                        len(r['influence']),sum(x['fractional_new_adopter_credit'] for x in r['influence'])] for a,r in reports.items()]), '']
        out += ['### Identity ranking movement', '', table(['Arm','Metric','Before/after ranked','Common','Exit/entry','Spearman','Mean/max shift','Top intersection / before / after'],
            [[a,m,f"{v['before_ranked']}/{v['after_ranked']}",v['common'],f"{v['exited']}/{v['entered']}",v['common_spearman'],
              f"{fmt(v['mean_absolute_rank_shift'])}/{fmt(v['max_absolute_rank_shift'])}",
              f"{v['top_overlap']}/{v['before_top_including_ties']}/{v['after_top_including_ties']}"]
             for a,c in comparison['comparisons'].items() for m,v in c['identity_rankings'].items()]), '']
        out += ['### Cluster matching and first-observer changes', '', table(['Arm','Matched clusters','Unmatched before/after','Common rows','Matched row fraction','Changed first-observer sets'],
                    [[a,c['matched_clusters'],f"{c['unmatched_before']}/{c['unmatched_after']}",c['common_text_records'],c['matched_record_fraction'],c['first_observer_sets_changed']]
                     for a,co in comparison['comparisons'].items() for c in [co['cluster_comparison']]]), '',
                f'Complete cluster-rank movement: [comparison JSON](results/robustness-v1/{source}/comparison.json).', '']
    out += ['## Interpretation', '',
            'Wiki repeated-phrasing leaders are root-sensitive: only 1 of the original top 10 remains in the page-root top 10. This does not show an influence mechanism; it shows that counting retained page history matters.',
            'Exact text dedup shrinks git multi-identity clusters from 34 to 8 and positive-credit recipients from 26 to 3, with no overlap against the original credit top 10. Administrative template reuse is not research-idea transmission.',
            'The conservative wiki clock exclusion has a much smaller aggregate effect than page aggregation. Its credit top 10 is unchanged, despite individual lower-rank movement. This does not validate every timestamp.',
            'SwarmTraces identity/time answers remain unavailable under every transformation. Empty rankings and zero temporal denominators are missing evidence, not zero adoption, zero influence, or failed outcomes.',
            'Root reduction and text dedup deliberately remove observations that define repetition. Their results are alternative estimands, not corrected estimates of the same quantity. No corpus is a random or independent sample of a common population.', '',
            '## Link review and validation', '',
            'See [AUDIT.md](AUDIT.md) for the 30-link direct-text review, explicit partial-blinding limits and precision estimates. The reviewer is an assistant, not a human or independent reviewer.',
            'See [saved-output validation](results/robustness-v1/validation.json), [unit tests](tests/test_robustness.py), and [runtime](results/robustness-v1/runtime.json).', '',
            'Reproduce: `nice -n 10 python3 run_robustness.py --data /local/data --repo /local/swarm-lab --out /new/output --audit-local /local/outside-repo/audit`. The default output refuses overwriting. Then run `python3 verify_robustness.py` and `python3 render_robustness.py` for the committed namespace.', '']
    Path('ROBUSTNESS.md').write_text('\n'.join(out))


if __name__ == '__main__':
    main()
