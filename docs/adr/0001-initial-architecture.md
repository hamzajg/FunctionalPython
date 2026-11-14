# ADR 0001 — Initial architecture

Date: 2026-11-13 (baseline recorded retroactively)
Status: accepted (describes what is built)

## Context

FunctionalPython exists to teach functional programming in Python through
small, runnable examples based on *Functional Programming with Python*.

## Decisions

1. **Standard library only.** No third-party dependencies; `pyproject.toml`
   declares none. Rationale: examples must run anywhere Python is installed
   — zero install friction is the point.
2. **Concept-per-module, flat layout.** `basics`, `higher_order`,
   `composition`, `lazy`, `recursion`, `maybe`, `result` — each file is one
   chapter of the book. Rationale: mirrors the pedagogy; readers can open
   exactly the file they need.
3. **unittest, not pytest.** Tests use the standard library's unittest so
   `python3 -m unittest discover` works with no tooling. Rationale: same
   zero-dependency principle applied to the test suite.
4. **Monads as values (`Maybe`, `Result`).** `Just`/`Nothing` and
   `Ok`/`Err` model absence/failure explicitly with `map`/`bind`. Rationale:
   teaches FP's core idea — errors as data — without exceptions.
5. **Laziness via generators.** `lazy.py` uses generator functions +
   `itertools` rather than strict collections. Rationale: demonstrates
   laziness with language-native tools, no libs.
6. **Single supported interpreter line.** `requires-python >=3.13`, CI
   matrix collapsed to 3.13. Rationale: one verified target beats a matrix
   of unverified ones for a teaching repo.

## Consequences

- No packaging sophistication — `pip install -e .` is optional convenience.
- Examples favour clarity over performance; don't "optimise" them.
- Adding a dependency for any reason requires re-justifying decision 1.
