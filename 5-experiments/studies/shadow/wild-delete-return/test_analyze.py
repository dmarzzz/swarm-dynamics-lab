import unittest
from analyze import select_assignments, summarize, utc

T = 100000


def event(ident='e1', page='wiki~p', offset=0, **kw):
    r = dict(event_id=ident, page_key=page, event_type='delete', success_observed=True,
             time=utc(T+offset), time_grade='reqlog', uncertainty_seconds=1)
    r.update(kw)
    return r


def save(ident, offset, page='wiki~p', **kw):
    r = dict(rev_id=ident, page_key=page, time=utc(T+offset), time_grade='reqlog', uncertainty_seconds=1)
    r.update(kw)
    return r


def anchors():
    return [save('left', -10000, 'anchor'), save('right', 10000, 'anchor')]


class WindowTests(unittest.TestCase):
    def test_guard_and_outer_boundaries(self):
        offsets = [-1801, -1800, -61, -60, 0, 60, 61, 1800, 1801]
        assignments, _ = select_assignments([event()], anchors()+[save(str(i), x) for i,x in enumerate(offsets)])
        w = assignments[0]['windows']['1800']
        self.assertEqual((w['before'], w['after']), (2,2))
        self.assertEqual(w['first_return_latency_seconds'], 61)

    def test_first_delete_before_quality_filter(self):
        assignments, _ = select_assignments([event(time_grade='write_date'),event('later',offset=500)], anchors())
        self.assertFalse(assignments[0]['eligible'])
        self.assertEqual(assignments[0]['exclusion'], 'ineligible_time_grade')

    def test_repeat_delete_not_new_unit(self):
        assignments, _ = select_assignments([event(),event('e2',offset=100)], anchors()+[save('r',200)])
        self.assertEqual(len(assignments),1)
        self.assertEqual(assignments[0]['successful_delete_events_for_page'],2)
        self.assertEqual(assignments[0]['first_delete_time'],utc(T))

    def test_unknown_earliest_not_replaced(self):
        assignments, _ = select_assignments([event(time=None),event('later',offset=10)], anchors())
        self.assertFalse(assignments[0]['eligible'])
        self.assertEqual(assignments[0]['exclusion'], 'unknown_first_deletion_missing_time')

    def test_exact_page_join(self):
        assignments, _ = select_assignments([event()], anchors()+[save('r',200,page='other~p')])
        self.assertEqual(assignments[0]['windows']['1800']['after'],0)

    def test_release_boundary(self):
        assignments, _ = select_assignments([event()], [save('left',-1799),save('right',2000)])
        self.assertFalse(assignments[0]['eligible'])
        self.assertEqual(assignments[0]['exclusion'],'primary_release_edge')

    def test_secondary_censoring_uses_primary_cohort(self):
        assignments, accounting = select_assignments([event()], [save('left',-2000),save('right',2000)])
        out=summarize(assignments,accounting)
        self.assertEqual(out['window_results']['1800']['pages'],1)
        self.assertEqual(out['window_results']['3600']['pages'],0)

    def test_bad_revision_clocks_excluded(self):
        assignments, accounting = select_assignments([event()], anchors()+[save('bad',120,uncertainty_seconds=2)])
        self.assertEqual(assignments[0]['windows']['1800']['after'],0)
        self.assertEqual(accounting['quality_counts']['revision_ineligible_uncertainty'],1)

    def test_failed_delete_not_selected(self):
        assignments, _ = select_assignments([event(success_observed=False),event('later',offset=200)],anchors())
        self.assertEqual(assignments[0]['first_delete_time'],utc(T+200))

    def test_zero_baseline_ratio_unavailable(self):
        assignments, accounting = select_assignments([event()],anchors()+[save('later',120)])
        primary=summarize(assignments,accounting)['window_results']['1800']
        self.assertEqual(primary['mean_after_minus_before'],1)
        self.assertIsNone(primary['after_before_ratio'])
        self.assertIsNone(primary['day_cluster_bootstrap_95_interval'])

    def test_duplicate_ids_fail(self):
        with self.assertRaises(ValueError):
            select_assignments([event(),event()],anchors())
        with self.assertRaises(ValueError):
            select_assignments([event()],anchors()+[save('left',0)])

    def test_determinism(self):
        events=[event(),event('another','wiki~q',offset=400)]
        revisions=anchors()+[save('r',120)]
        self.assertEqual(select_assignments(events,revisions),select_assignments(reversed(events),reversed(revisions)))

    def test_no_clock_coverage_blocks(self):
        with self.assertRaisesRegex(ValueError,'No admissible'):
            select_assignments([event()],[save('bad',0,time_grade='write_date')])


if __name__=='__main__':
    unittest.main()
