import unittest
from askswarm import Event, analyze
from askswarm.robustness import (exact_deduplicate, root_ids, aggregate_roots,
                                exclude_imputed, variants, rank_change, robustness)


def row(i, text='same', actor='a', time=1, **meta):
    return Event(actor, time, text, event_id=i, metadata=meta)


class RobustnessTests(unittest.TestCase):
    def test_exact_means_exact_not_normalized(self):
        rows = [row('3', time=3), row('1', time=1), row('2', 'Same'), row('4', ''), row('5', '')]
        self.assertEqual({r.event_id for r in exact_deduplicate(rows)}, {'1', '2', '4', '5'})

    def test_root_parent_recursive(self):
        rows = [row('a', parent_id=None), row('b', parent_id='a'), row('c', parent_id='b')]
        self.assertEqual(len(set(root_ids(rows).values())), 1)
        self.assertEqual(len(aggregate_roots(rows)), 1)

    def test_absent_parent_and_unknown_root(self):
        rows = [row('a', parent_id='missing'), row('b', parent_id='missing'), row('c'), row('d')]
        self.assertEqual(len(aggregate_roots(rows)), 3)

    def test_cycles_fail_closed(self):
        with self.assertRaises(ValueError):
            root_ids([row('a', parent_id='b'), row('b', parent_id='a')])

    def test_root_representative_not_composite(self):
        rows = [row('a', actor='A', time=None, root_id='p'), row('b', actor='B', time=3, root_id='p')]
        self.assertEqual(aggregate_roots(rows), [rows[1]])

    def test_clock_policy_missing_stays_missing(self):
        rows = [row('a', time=None), row('b', time_imputed=True), row('c', time_imputed='false'),
                row('d', root_basis='wiki_page', time_grade='rclog'), row('e', root_basis='wiki_page', time_grade='reqlog')]
        self.assertEqual([r.event_id for r in exclude_imputed(rows)], ['a', 'c', 'e'])

    def test_missing_wiki_clock_not_a_fallback_timestamp(self):
        event = row('missing', time=None, root_basis='wiki_page', time_grade=None)
        self.assertEqual(exclude_imputed([event]), [event])

    def test_combined_resolves_roots_before_filtering(self):
        rows = [row('a', 'a'), row('b', 'b', parent_id='a', time_imputed=True), row('c', 'c', parent_id='b')]
        arms, receipts = variants(rows)
        self.assertEqual(len(arms['combined']), 1)
        self.assertEqual(receipts['combined']['removed_records'], 2)

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            variants([row('a'), row('a')])

    def test_rank_loss_and_ties(self):
        r = rank_change({'a': 2, 'b': 2, 'c': 1}, {'b': 1, 'c': 2})
        self.assertEqual(r['exited'], 1)
        self.assertEqual(r['common_spearman'], -1)
        self.assertEqual(rank_change({'a': 1}, {})['common_spearman'], None)
        tied = rank_change({'a': 2, 'b': 2}, {'a': 2, 'b': 2}, top_k=1)
        self.assertEqual(tied['before_top_including_ties'], 2)
        self.assertEqual(tied['mean_absolute_rank_shift'], 0)

    def test_reuse_links_reconcile_credit(self):
        rows = [row('a', actor='A', time=0), row('b', actor='B', time=0), row('c', actor='C', time=1)]
        result = analyze(rows, include_evidence=True)
        self.assertEqual(len(result['_reuse_links']), 2)
        self.assertEqual(sum(x['credit'] for x in result['_reuse_links']), 1)
        clean = analyze(rows)
        self.assertEqual({k:v for k,v in result.items() if not k.startswith('_')}, clean)

    def test_every_answer_and_zero_coverage(self):
        result = robustness([row('a', actor=None, time=None), row('b', actor=None, time=None)])
        self.assertEqual(result['reports']['exact_dedup']['summary']['records'], 1)
        self.assertIsNone(result['reports']['exact_dedup']['summary']['participation_gini'])
        self.assertEqual(result['comparisons']['exact_dedup']['identity_rankings']['participation']['common'], 0)
        self.assertEqual(result['comparisons']['exact_dedup']['cluster_comparison']['matched_clusters'], 1)


if __name__ == '__main__':
    unittest.main()
