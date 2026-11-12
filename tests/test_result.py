import unittest

from functionalpython import maybe
from functionalpython import result


class OkTests(unittest.TestCase):
    def test_map_transforms_the_value(self):
        self.assertEqual(result.Ok(6), result.Ok(3).map(lambda n: n * 2))

    def test_map_err_is_a_no_op(self):
        self.assertEqual(result.Ok(3), result.Ok(3).map_err(str.upper))

    def test_bind_uses_a_result_returning_function(self):
        half = lambda n: result.Ok(n // 2) if n % 2 == 0 else result.Err("odd")
        self.assertEqual(result.Ok(4), result.Ok(8).bind(half))
        self.assertEqual(result.Err("odd"), result.Ok(3).bind(half))

    def test_bind_rejects_non_result(self):
        with self.assertRaises(TypeError):
            result.Ok(1).bind(lambda n: n)

    def test_get_or_else_returns_the_value(self):
        self.assertEqual(1, result.Ok(1).get_or_else(99))

    def test_unwrap_returns_the_value(self):
        self.assertEqual(1, result.Ok(1).unwrap())

    def test_unwrap_err_raises(self):
        with self.assertRaises(ValueError):
            result.Ok(1).unwrap_err()

    def test_ok_bridges_to_maybe(self):
        self.assertEqual(maybe.Just(1), result.Ok(1).ok())
        self.assertEqual(maybe.Nothing(), result.Ok(1).err())

    def test_is_ok_and_truthiness(self):
        self.assertTrue(result.Ok(0).is_ok())
        self.assertFalse(result.Ok(0).is_err())
        self.assertTrue(result.Ok(0))


class ErrTests(unittest.TestCase):
    def test_map_is_a_no_op(self):
        self.assertEqual(result.Err("bad"), result.Err("bad").map(lambda n: n * 2))

    def test_map_err_transforms_the_error(self):
        self.assertEqual(result.Err("BAD"), result.Err("bad").map_err(str.upper))

    def test_bind_is_a_no_op(self):
        self.assertEqual(result.Err("bad"), result.Err("bad").bind(lambda n: result.Ok(n)))

    def test_get_or_else_returns_the_default(self):
        self.assertEqual(99, result.Err("bad").get_or_else(99))

    def test_unwrap_raises(self):
        with self.assertRaises(ValueError):
            result.Err("bad").unwrap()

    def test_unwrap_err_returns_the_error(self):
        self.assertEqual("bad", result.Err("bad").unwrap_err())

    def test_err_bridges_to_maybe(self):
        self.assertEqual(maybe.Nothing(), result.Err("bad").ok())
        self.assertEqual(maybe.Just("bad"), result.Err("bad").err())

    def test_is_err_and_truthiness(self):
        self.assertTrue(result.Err("bad").is_err())
        self.assertFalse(result.Err("bad").is_ok())
        self.assertFalse(result.Err("bad"))


class SafeTests(unittest.TestCase):
    def test_returns_ok_for_a_successful_call(self):
        divide = result.safe(lambda a, b: a / b)
        self.assertEqual(result.Ok(2.0), divide(4, 2))

    def test_returns_err_for_a_raised_exception(self):
        divide = result.safe(lambda a, b: a / b)
        failed = divide(1, 0)
        self.assertTrue(failed.is_err())
        self.assertIsInstance(failed.unwrap_err(), ZeroDivisionError)

    def test_passes_positional_and_keyword_arguments(self):
        subtract = result.safe(lambda a, b=0: a - b)
        self.assertEqual(result.Ok(3), subtract(5, b=2))


class ChainingTests(unittest.TestCase):
    def test_parse_then_divide(self):
        def parse(text):
            return result.Ok(int(text)) if text.strip().lstrip("-").isdigit() else result.Err("not a number")

        def reciprocal(n):
            return result.Ok(1 / n) if n != 0 else result.Err("division by zero")

        self.assertEqual(result.Ok(0.25), parse("4").bind(reciprocal))
        self.assertEqual(result.Err("division by zero"), parse("0").bind(reciprocal))
        self.assertEqual(result.Err("not a number"), parse("four").bind(reciprocal))

    def test_error_can_be_recovered_with_map_err_and_get_or_else(self):
        failed = result.Err("boom").map_err(lambda message: f"{message}!").map(len)
        self.assertEqual("boom!", failed.unwrap_err())
        self.assertEqual(0, failed.get_or_else(0))


if __name__ == "__main__":
    unittest.main()
