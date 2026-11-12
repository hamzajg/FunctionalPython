import unittest

from functionalpython import recursion


class FactorialTests(unittest.TestCase):
    def test_base_cases(self):
        self.assertEqual(1, recursion.factorial(0))
        self.assertEqual(1, recursion.factorial(1))

    def test_recurses(self):
        self.assertEqual(120, recursion.factorial(5))

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            recursion.factorial(-1)


class MemoizeTests(unittest.TestCase):
    def test_computes_once(self):
        calls = []

        @recursion.memoize
        def add(a, b):
            calls.append((a, b))
            return a + b

        self.assertEqual(3, add(1, 2))
        self.assertEqual(3, add(1, 2))
        self.assertEqual(1, len(calls))

    def test_caches_per_argument_tuple(self):
        @recursion.memoize
        def add(a, b):
            return a + b

        self.assertEqual(3, add(1, 2))
        self.assertEqual(7, add(3, 4))
        self.assertEqual(2, len(add.cache))


class TrampolineTests(unittest.TestCase):
    def test_runs_thunks_until_a_value_is_returned(self):
        def countdown(n, acc=0):
            if n == 0:
                return acc
            return lambda: countdown(n - 1, acc + n)

        fast = recursion.trampoline(countdown)

        # 1 + 2 + ... + 10000, deep enough to blow the stack if recursive.
        self.assertEqual(50005000, fast(10000))

    def test_decorated_function_may_recurse_through_thunks(self):
        @recursion.trampoline
        def countdown(n, acc=0):
            if n == 0:
                return acc
            return lambda: countdown(n - 1, acc + n)

        self.assertEqual(50005000, countdown(10000))

    def test_plain_return_value(self):
        @recursion.trampoline
        def constant():
            return 42

        self.assertEqual(42, constant())

    def test_arguments_are_forwarded(self):
        @recursion.trampoline
        def add(a, b):
            return lambda: a + b

        self.assertEqual(5, add(2, 3))

    def test_loop_state_does_not_leak_after_an_error(self):
        @recursion.trampoline
        def explode():
            raise ValueError("boom")

        with self.assertRaises(ValueError):
            explode()

        # A later call must still run (and unwrap) normally.
        @recursion.trampoline
        def ok():
            return lambda: 1

        self.assertEqual(1, ok())


if __name__ == "__main__":
    unittest.main()
