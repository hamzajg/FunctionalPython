import unittest

from functionalpython import composition


def inc(n):
    return n + 1


def double(n):
    return n * 2


class ComposeTests(unittest.TestCase):
    def test_composes_right_to_left(self):
        # compose(inc, double)(3) == inc(double(3)) == 7
        self.assertEqual(7, composition.compose(inc, double)(3))

    def test_empty_compose_is_identity(self):
        self.assertEqual(5, composition.compose()(5))


class PipeTests(unittest.TestCase):
    def test_composes_left_to_right(self):
        # pipe(inc, double)(3) == double(inc(3)) == 8
        self.assertEqual(8, composition.pipe(inc, double)(3))

    def test_empty_pipe_is_identity(self):
        self.assertEqual(5, composition.pipe()(5))


class CurryTests(unittest.TestCase):
    def test_supports_one_argument_at_a_time(self):
        add = composition.curry(lambda a, b, c: a + b + c)
        self.assertEqual(6, add(1)(2)(3))

    def test_supports_mixed_grouping(self):
        add = composition.curry(lambda a, b, c: a + b + c)
        self.assertEqual(6, add(1, 2)(3))

    def test_all_arguments_at_once(self):
        add = composition.curry(lambda a, b, c: a + b + c)
        self.assertEqual(6, add(1, 2, 3))

    def test_zero_arity_function_is_returned_unchanged(self):
        value = composition.curry(lambda: 42)
        self.assertEqual(42, value())

    def test_rejects_too_many_arguments(self):
        add = composition.curry(lambda a, b: a + b)
        with self.assertRaises(TypeError):
            add(1)(2)(3)

    def test_ignores_parameters_with_defaults(self):
        def add(a, b, c=10):
            return a + b + c

        self.assertEqual(13, composition.curry(add)(1)(2))


if __name__ == "__main__":
    unittest.main()
