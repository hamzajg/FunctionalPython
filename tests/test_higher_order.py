import unittest

from functionalpython import higher_order


class ApplyTwiceTests(unittest.TestCase):
    def test_applies_function_twice(self):
        self.assertEqual(16, higher_order.apply_twice(lambda n: n * 2, 4))


class MakeMultiplierTests(unittest.TestCase):
    def test_closes_over_factor(self):
        triple = higher_order.make_multiplier(3)
        self.assertEqual(12, triple(4))

    def test_each_closure_is_independent(self):
        double = higher_order.make_multiplier(2)
        tenfold = higher_order.make_multiplier(10)
        self.assertEqual(4, double(2))
        self.assertEqual(20, tenfold(2))

    def test_rejects_non_int_factor(self):
        with self.assertRaises(TypeError):
            higher_order.make_multiplier(2.5)


class MapAllTests(unittest.TestCase):
    def test_maps(self):
        self.assertEqual([1, 4, 9], higher_order.map_all(lambda n: n * n, [1, 2, 3]))


class FilterAllTests(unittest.TestCase):
    def test_filters(self):
        self.assertEqual([2, 4], higher_order.filter_all(lambda n: n % 2 == 0, [1, 2, 3, 4]))


class ReduceAllTests(unittest.TestCase):
    def test_folds_with_initial(self):
        self.assertEqual(10, higher_order.reduce_all(lambda acc, n: acc + n, [1, 2, 3, 4], 0))

    def test_initial_is_used_for_empty_input(self):
        self.assertEqual("", higher_order.reduce_all(lambda acc, c: acc + c, [], ""))


class PartialApplyTests(unittest.TestCase):
    def test_binds_positional_arguments(self):
        def power(base, exponent):
            return base**exponent

        square = higher_order.partial_apply(power, exponent=2)
        self.assertEqual(9, square(3))

    def test_binds_keyword_arguments(self):
        def greet(greeting, name):
            return f"{greeting}, {name}"

        hello = higher_order.partial_apply(greet, "Hello")
        self.assertEqual("Hello, Ada", hello("Ada"))


if __name__ == "__main__":
    unittest.main()
