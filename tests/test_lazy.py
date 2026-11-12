import unittest

from functionalpython import lazy


class NaturalsTests(unittest.TestCase):
    def test_infinite_stream(self):
        self.assertEqual([0, 1, 2, 3], lazy.take(4, lazy.naturals()))

    def test_starts_at_given_value(self):
        self.assertEqual([5, 6, 7], lazy.take(3, lazy.naturals(5)))


class TakeTests(unittest.TestCase):
    def test_limits_items(self):
        self.assertEqual([1, 2], lazy.take(2, [1, 2, 3, 4]))

    def test_returns_everything_when_shorter(self):
        self.assertEqual([1], lazy.take(10, [1]))

    def test_zero(self):
        self.assertEqual([], lazy.take(0, [1, 2]))

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            lazy.take(-1, [1])


class FibonacciTests(unittest.TestCase):
    def test_first_values(self):
        self.assertEqual([0, 1, 1, 2, 3, 5, 8], lazy.take(7, lazy.fibonacci()))


class ChunksTests(unittest.TestCase):
    def test_splits_into_chunks(self):
        self.assertEqual([[1, 2], [3, 4], [5]], list(lazy.chunks(range(1, 6), 2)))

    def test_is_lazy(self):
        # An infinite source must not be consumed eagerly.
        first = next(lazy.chunks(lazy.naturals(), 3))
        self.assertEqual([0, 1, 2], first)

    def test_rejects_non_positive_size(self):
        with self.assertRaises(ValueError):
            list(lazy.chunks([1], 0))


class UniqueSeenTests(unittest.TestCase):
    def test_yields_each_value_once(self):
        self.assertEqual([1, 2, 3], list(lazy.unique_seen([1, 1, 2, 1, 3])))

    def test_works_on_infinite_stream(self):
        repeated = (n % 2 for n in lazy.naturals())
        self.assertEqual([0, 1], lazy.take(2, lazy.unique_seen(repeated)))


if __name__ == "__main__":
    unittest.main()
