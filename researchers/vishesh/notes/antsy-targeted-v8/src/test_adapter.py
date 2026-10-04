import unittest
from adapter import easyocr_words
from fields import extract


class Adapter(unittest.TestCase):
    def test_documented_shape_to_contract(self):
        rows = [
            ([[0, 0], [60, 0], [60, 20], [0, 20]], "TOTAL", 0.9),
            ([[100, 0], [180, 0], [180, 20], [100, 20]], "30,000", 0.8),
        ]
        self.assertEqual(extract(easyocr_words(rows))["value"], "30000.00")

    def test_empty_stays_missing(self):
        self.assertEqual(extract(easyocr_words([]))["status"], "missing")

    def test_invalid_coordinates_fail(self):
        for box in [[], [[0, 0]] * 4, [[0, 0], [1, 0], [1, float("nan")], [0, 1]]]:
            with self.subTest(box=box), self.assertRaises(ValueError):
                easyocr_words([(box, "TOTAL", 0.9)])

    def test_confidence_not_a_truth_probability(self):
        for score in [-1, 2, float("inf")]:
            with self.subTest(score=score), self.assertRaises(ValueError):
                easyocr_words([([[0, 0], [2, 0], [2, 2], [0, 2]], "TOTAL", score)])


if __name__ == "__main__":
    unittest.main()
