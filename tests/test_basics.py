import unittest

from functionalpython import basics


class SquareAllTests(unittest.TestCase):
    def test_squares_each_item(self):
        self.assertEqual([1, 4, 9], basics.square_all([1, 2, 3]))

    def test_empty_input(self):
        self.assertEqual([], basics.square_all([]))

    def test_does_not_mutate_input(self):
        numbers = [1, 2, 3]
        basics.square_all(numbers)
        self.assertEqual([1, 2, 3], numbers)


class EvensTests(unittest.TestCase):
    def test_keeps_even_numbers_in_order(self):
        self.assertEqual([2, 4], basics.evens([1, 2, 3, 4, 5]))

    def test_negative_numbers(self):
        self.assertEqual([-4, 0], basics.evens([-3, -4, 0]))


class TotalTests(unittest.TestCase):
    def test_sums(self):
        self.assertEqual(6, basics.total([1, 2, 3]))

    def test_empty_is_zero(self):
        self.assertEqual(0, basics.total([]))


class DedupeTests(unittest.TestCase):
    def test_preserves_first_seen_order(self):
        self.assertEqual([3, 1, 2], basics.dedupe([3, 1, 3, 2, 1]))

    def test_works_with_unhashable_values(self):
        self.assertEqual([[1], [2]], basics.dedupe([[1], [2], [1]]))


class SortByTests(unittest.TestCase):
    def test_sorts_by_key(self):
        words = ["bbb", "a", "cc"]
        self.assertEqual(["a", "cc", "bbb"], basics.sort_by(words, key=len))

    def test_reverse(self):
        self.assertEqual(["bbb", "cc", "a"], basics.sort_by(["a", "bbb", "cc"], key=len, reverse=True))

    def test_is_stable(self):
        pairs = [(1, "b"), (1, "a"), (0, "c")]
        self.assertEqual([(0, "c"), (1, "b"), (1, "a")], basics.sort_by(pairs, key=lambda p: p[0]))


class PairsTests(unittest.TestCase):
    def test_zips(self):
        self.assertEqual([(1, "a"), (2, "b")], basics.pairs([1, 2], ["a", "b"]))

    def test_rejects_different_lengths(self):
        with self.assertRaises(ValueError):
            basics.pairs([1, 2], ["a"])


if __name__ == "__main__":
    unittest.main()
