import unittest
from analyze import census, length_bin, render_html, render_svg


def row(ident, kind='payload', parent=None, text='fixture', time=None):
    return dict(id=ident, kind=kind, parent_id=parent, text=text, time_utc=time)


class CensusTests(unittest.TestCase):
    def test_direct_and_indirect_are_distinct(self):
        data = [row('p'), row('r', 'recovered_text', 'p'), row('s', 'response', 'r'),
                row('p2'), row('s2', 'response', 'p2'), row('p3')]
        out = census(data)
        self.assertEqual(out['payload_direct_response_coverage']['numerator'], 1)
        self.assertEqual(out['payload_response_descendant_coverage']['numerator'], 2)
        self.assertEqual(out['graph']['components'], 3)
        self.assertEqual(out['graph']['max_component_rows'], 3)
        self.assertEqual(out['response_rows_with_direct_payload_parent']['fraction'], .5)

    def test_all_categories(self):
        data = [row('p1'), row('r', 'recovered_text', 'p1'), row('p2'), row('s', 'response', 'p2'),
                row('p3'), row('p4'), row('p5', parent='p4')]
        self.assertEqual(census(data)['payload_descendant_categories'], {
            'response_descendant': 1, 'recovered_without_response': 1,
            'other_descendants_only': 1, 'no_descendants': 2})

    def test_orphan_is_preserved(self):
        out = census([row('p'), row('r', 'response', 'missing')])
        self.assertEqual(out['graph']['orphan_parent_rows'], 1)
        self.assertEqual(out['graph']['components'], 2)
        self.assertEqual(out['payload_direct_response_coverage']['numerator'], 0)

    def test_duplicates_not_components(self):
        out = census([row('a'), row('b'), row('c', 'response')])
        self.assertEqual(out['graph']['components'], 3)
        self.assertEqual(out['text_sensitivity']['distinct_nonempty_released_texts'], 1)
        self.assertEqual(out['text_sensitivity']['redundant_rows'], 2)
        self.assertEqual(out['text_sensitivity']['cross_kind_shared_text_hashes']['payload__response'], 1)
        self.assertEqual(out['kinds']['payload']['redundant_text_rows'], 1)

    def test_null_and_empty_not_events(self):
        out = census([row('a', text=None), row('b', text=''), row('c', text=' ')])
        self.assertEqual(out['text_sensitivity']['nonempty_rows'], 1)
        self.assertEqual(out['kinds']['payload']['null_text_rows'], 1)
        self.assertEqual(out['kinds']['payload']['empty_text_rows'], 1)
        self.assertEqual(out['nonnull_timestamp_rows'], 0)

    def test_cycle_fails(self):
        with self.assertRaisesRegex(ValueError, 'Cyclic'):
            census([row('a', parent='b'), row('b', parent='a')])

    def test_self_link_fails(self):
        with self.assertRaisesRegex(ValueError, 'Self-linked'):
            census([row('a', parent='a')])

    def test_duplicate_ids_fail(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            census([row('a'), row('a')])

    def test_unknown_kind_fails(self):
        with self.assertRaisesRegex(ValueError, 'Unknown'):
            census([row('a', 'person')])

    def test_empty_corpus(self):
        out = census([])
        self.assertIsNone(out['payload_direct_response_coverage']['fraction'])
        self.assertIn('unavailable', render_svg(out))

    def test_bins_boundary(self):
        self.assertEqual([length_bin(n) for n in (0, 1, 255, 256, 1023, 1024, 4095, 4096)],
                         ['0', '1-255', '1-255', '256-1023', '256-1023', '1024-4095', '1024-4095', '4096+'])

    def test_deterministic_and_order_independent(self):
        data = [row('a', text='A'), row('b', 'response', 'a', 'B')]
        self.assertEqual(census(data), census(reversed(data)))

    def test_render_escaping(self):
        out = census([row('a')])
        out['scope'] = '<script>alert(1)</script>'
        self.assertNotIn('<script>', render_html(out))
        self.assertIn('&lt;script&gt;', render_html(out))

    def test_deep_graph_without_recursion(self):
        data = [row(str(i), parent=str(i-1) if i else None) for i in range(1500)]
        data.append(row('response', 'response', '1499'))
        out = census(data)
        self.assertEqual(out['payload_direct_response_coverage']['numerator'], 1)
        self.assertEqual(out['payload_response_descendant_coverage']['numerator'], 1500)
        self.assertEqual(out['graph']['max_component_rows'], 1501)

    def test_nonnull_timestamp_counts_but_no_order_inferred(self):
        out = census([row('a', time='2026-07-01'), row('b')])
        self.assertEqual(out['nonnull_timestamp_rows'], 1)
        self.assertNotIn('duration', out)


if __name__ == '__main__':
    unittest.main()
