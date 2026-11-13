# Architecture — FunctionalPython

Current-state map. Descriptive, not aspirational; see `docs/adr/` for why.

## Shape

```
functionalpython/           one module per FP concept (flat, no deps)
  basics · higher_order · composition · lazy · recursion · maybe · result
       │
       ▼
tests/test_<module>.py      unittest per module — the only test style
       │
       ▼
pyproject.toml              packaging only; zero dependencies
```

## Design

- **Concept-per-module.** Each file teaches one FP idea and is readable
  top-to-bottom. Modules don't import each other — the package is a
  catalogue, not a layered system.
- **Purity by default.** Functions take data and return data; `lazy.py`
  uses generators for laziness; `maybe.py`/`result.py` model absence and
  failure as values instead of exceptions/`None`.
- **Explicit recursion control.** `trampoline` and `memoize` in
  `recursion.py` demonstrate stack-safe and cached recursion.
- **stdlib only.** `itertools`, `functools`, generators — nothing else.
  This keeps every example copy-paste runnable anywhere.

## Testing

`unittest` (not pytest) via `python3 -m unittest discover -s tests -v`.
Each module has a matching test file; CI runs the suite plus an import
check on Python 3.13 only.

## Public surface

`functionalpython/__init__.py` aggregates the module exports. There is no
versioned API promise — it's a teaching repo; still, keep names stable and
documented in the README table.
