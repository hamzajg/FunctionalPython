# FunctionalPython

Small, dependency-free examples of functional programming in Python, each one
covered by a test. The code follows the ideas in *Functional Programming with
Python* (O'Reilly): pure functions, higher-order functions, composition,
laziness, recursion, and the `Maybe` and `Result` monads.

Everything uses the standard library only, so the examples run anywhere
Python 3.9+ is installed.

## Running the tests

```bash
python3 -m unittest discover -s tests -v
```

No installation or virtualenv is required. To install the package locally:

```bash
python3 -m pip install -e .
```

## What is inside

| Module | Ideas |
|---|---|
| [`functionalpython/basics.py`](functionalpython/basics.py) | Pure functions over sequences: `square_all`, `evens`, `total`, `dedupe`, `sort_by`, `pairs` |
| [`functionalpython/higher_order.py`](functionalpython/higher_order.py) | Functions that take or return functions: `apply_twice`, `make_multiplier`, `map_all`, `filter_all`, `reduce_all`, `partial_apply` |
| [`functionalpython/composition.py`](functionalpython/composition.py) | `compose` (right to left), `pipe` (left to right), and `curry` |
| [`functionalpython/lazy.py`](functionalpython/lazy.py) | Generators and `itertools`: infinite `naturals`, `fibonacci`, `take`, `chunks`, `unique_seen` |
| [`functionalpython/recursion.py`](functionalpython/recursion.py) | `factorial`, `memoize`, and `trampoline` for recursion without growing the stack |
| [`functionalpython/maybe.py`](functionalpython/maybe.py) | `Just` / `Nothing` with `map`, `bind`, and `get_or_else` |
| [`functionalpython/result.py`](functionalpython/result.py) | `Ok` / `Err` for error handling without exceptions, with `map`, `map_err`, `bind`, `unwrap`, and a `safe` decorator |

## Examples

Compose small functions instead of writing loops:

```python
from functionalpython import compose, pipe, curry

inc = lambda n: n + 1
double = lambda n: n * 2

compose(inc, double)(3)   # 7  -> inc(double(3))
pipe(inc, double)(3)      # 8  -> double(inc(3))

add = curry(lambda a, b, c: a + b + c)
add(1)(2)(3)              # 6
add(1, 2)(3)              # 6
```

Work with infinite sequences lazily:

```python
from functionalpython import naturals, take, chunks, unique_seen

take(5, naturals())            # [0, 1, 2, 3, 4]
take(7, fibonacci())           # [0, 1, 1, 2, 3, 5, 8]
next(chunks(naturals(), 3))    # [0, 1, 2] — nothing else is read
take(2, unique_seen(n % 2 for n in naturals()))   # [0, 1]
```

Keep deep recursion off the stack with a trampoline:

```python
from functionalpython import trampoline

@trampoline
def countdown(n, acc=0):
    if n == 0:
        return acc
    return lambda: countdown(n - 1, acc + n)

countdown(10_000)   # 50005000, no RecursionError
```

Represent optional values without `None` checks:

```python
from functionalpython import Just, Nothing

def half(n):
    return Just(n // 2) if n % 2 == 0 else Nothing()

Just(8).bind(half).map(lambda n: n + 1)   # Just(5)
Just(3).bind(half).get_or_else(0)         # 0
```

Carry failures as values instead of raising:

```python
from functionalpython import Err, Ok, safe

@safe
def parse(text):
    return int(text)

parse("42")                  # Ok(42)
parse("forty-two")           # Err(ValueError(...))

parse("42").map(lambda n: n * 2)        # Ok(84)
parse("x").map(lambda n: n * 2)         # Err(...) — map is skipped
parse("42").ok()                        # Just(42)
parse("42").unwrap()                    # 42
parse("x").get_or_else(0)               # 0
```

A failure short-circuits a `bind` chain exactly like an exception, but the
outcome stays a value the caller can look at, recover from with `map_err`, or
turn into a `Maybe` with `ok()` / `err()`.

## Layout

```
functionalpython/   the examples (one module per topic)
tests/              unittest suites, one per module
pyproject.toml      packaging metadata
```

## License

See [LICENSE](LICENSE).
