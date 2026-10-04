import unittest
from fields import extract


def words(*rows):
    return [{'text': text, 'x': x, 'y': y*100, 'h': 20,
             'box': [x, y*100-10, 120, 20], 'confidence': 1}
            for y, row in enumerate(rows) for x, text in enumerate(row)]


class FieldsTests(unittest.TestCase):
    def test_quantity_annotation(self):
        for label in ('Total(Qty=60', 'Total (Qty=2)', 'Total(quantity=12)'):
            self.assertEqual(extract(words((label, '3.600.000')))['value'], '3600000.00')

    def test_ordinary_total_unchanged(self):
        self.assertEqual(extract(words(('Total', '17.000')))['value'], '17000.00')

    def test_corrupted_quantity_stays_missing(self):
        for label in ('Total (Qty-60', 'Total(Qty=', 'Total Qty 60', 'Total(Qty=60) refund'):
            self.assertIsNone(extract(words((label, '3.600.000')))['value'])

    def test_spurious_number_and_two_amounts(self):
        for row in (('Total(Qty=60', '1', '3.600.000'), ('Total(Qty=60', '3.600.000', '4.000.000')):
            self.assertIsNone(extract(words(row))['value'])

    def test_conflicting_totals(self):
        self.assertEqual(extract(words(('Total(Qty=2)', '100'), ('Total', '200')))['status'], 'ambiguous')

    def test_excluded_contexts(self):
        for prefix in ('Subtotal', 'Tax', 'Change', 'Discount', 'Cancelled'):
            self.assertIsNone(extract(words((prefix, 'Total(Qty=2)', '100')))['value'])

    def test_no_mutation(self):
        w=words(('Total(Qty=2)', '100')); extract(w)
        self.assertEqual(w[0]['text'], 'Total(Qty=2)')

if __name__ == '__main__': unittest.main()
