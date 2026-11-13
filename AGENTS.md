# AGENTS.md — FunctionalPython

Guidance for AI agents (and humans) working in this repository.

## Project

FunctionalPython is a small, dependency-free teaching repo: FP examples in
Python (pure functions, higher-order functions, composition, laziness,
recursion, `Maybe`/`Result` monads), each covered by a unittest. Based on
*Functional Programming with Python* (O'Reilly).
Stack: Python ≥3.13 (`requires-python`), **standard library only** — no
third-party deps at all.

## Commands

Verified 2026-11-13 against CI (`.github/workflows/ci.yml`) and README.

| Task | Command |
|---|---|
| Test | `python3 -m unittest discover -s tests -v` (88 tests) |
| Install (optional) | `python3 -m pip install -e .` |
| Import check | `python -c "import functionalpython"` (CI also runs this) |

No build step, no lint config, no services. Tests need no venv or install.

## Architecture

Flat package `functionalpython/` — one module per FP concept, each
independent (no cross-imports between concept modules beyond `__init__`):

- `basics.py` — pure functions over sequences (map/filter/reduce style)
- `higher_order.py` — functions returning/taking functions, `partial_apply`
- `composition.py` — `compose`, `pipe`, `curry`
- `lazy.py` — generators + `itertools` (`naturals`, `fibonacci`, `take`,
  `chunks`, `unique_seen`)
- `recursion.py` — `factorial`, `memoize`, `trampoline`
- `maybe.py` — `Just`/`Nothing` monad (`map`, `bind`, `get_or_else`)
- `result.py` — `Ok`/`Err` monad (`map`, `map_err`, `bind`, `unwrap`,
  `safe` decorator)
- `tests/test_<module>.py` — one unittest file per module

## Conventions

- **Standard library only** — this is a hard constraint; `pyproject.toml`
  has no dependencies and CI verifies imports work bare.
- Each example must stay small, pure where possible, and doctest-readable —
  it's teaching material, clarity beats cleverness.
- Type hints are used where present; match the surrounding module's style.
- KISS: one concept per function; don't merge modules or add "utility"
  grab-bags.

## Landmines

- **Default branch is `master`, not `main`.**
- `requires-python = ">=3.13"` — the CI matrix was collapsed to a single
  3.13 job; don't re-add older versions without updating the pin.
- `lazy.py` contains *infinite* generators — never iterate them without
  `take`/bounds in tests or examples.
- `trampoline` exists specifically to avoid stack growth — recursion examples
  should use it for deep recursion, plain recursion for shallow cases.
- `__init__.py` re-exports; check it before adding a new public function.

## Agent rules

- Branch from `master`; name branches `feat/*`, `fix/*`, `chore/*`, `docs/*`.
- Docs-only changes still go through a PR; never commit to `master` directly.
- Verify before claiming: run `python3 -m unittest discover -s tests -v`
  and report the real result.
- Keep changes minimal and consistent with surrounding code. No drive-by
  refactors.
- Every new example function needs a test in the matching `tests/test_*.py`.
- Update AGENTS.md / docs/ARCHITECTURE.md when you add a module or change
  the zero-dependency constraint.
