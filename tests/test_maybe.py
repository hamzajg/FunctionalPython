import unittest

from functionalpython import maybe


class JustTests(unittest.TestCase):
    def test_map_transforms_the_value(self):
        self.assertEqual(maybe.Just(6), maybe.Just(3).map(lambda n: n * 2))

    def test_bind_uses_a_maybe_returning_function(self):
        half = lambda n: maybe.Just(n // 2) if n % 2 == 0 else maybe.Nothing()
        self.assertEqual(maybe.Just(4), maybe.Just(8).bind(half))
        self.assertEqual(maybe.Nothing(), maybe.Just(3).bind(half))

    def test_bind_rejects_non_maybe(self):
        with self.assertRaises(TypeError):
            maybe.Just(1).bind(lambda n: n)

    def test_get_or_else_returns_the_value(self):
        self.assertEqual(1, maybe.Just(1).get_or_else(99))

    def test_is_just(self):
        self.assertTrue(maybe.Just(0).is_just())


class NothingTests(unittest.TestCase):
    def test_map_is_a_no_op(self):
        self.assertEqual(maybe.Nothing(), maybe.Nothing().map(lambda n: n * 2))

    def test_bind_is_a_no_op(self):
        self.assertEqual(maybe.Nothing(), maybe.Nothing().bind(lambda n: maybe.Just(n)))

    def test_get_or_else_returns_the_default(self):
        self.assertEqual(99, maybe.Nothing().get_or_else(99))

    def test_is_not_just(self):
        self.assertFalse(maybe.Nothing().is_just())


class ChainingTests(unittest.TestCase):
    def test_safe_division_chain(self):
        def safe_divide(numerator, denominator):
            if denominator == 0:
                return maybe.Nothing()
            return maybe.Just(numerator / denominator)

        result = maybe.Just(10).bind(lambda n: safe_divide(n, 2)).map(lambda n: n + 1)
        self.assertEqual(maybe.Just(6.0), result)

        failed = maybe.Just(10).bind(lambda n: safe_divide(n, 0)).map(lambda n: n + 1)
        self.assertEqual(maybe.Nothing(), failed)


if __name__ == "__main__":
    unittest.main()
