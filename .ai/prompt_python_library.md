# AI Prompt: Python Library (Compact & Fast)

Purpose
-------
A minimal, high-signal prompt template for AI agents to generate DRY, high-performance, readable Python library code quickly.

How to use
----------
Paste and fill the placeholders. Keep the filled prompt <= 10 short bullets to reduce LLM context and speed generation.

Template (fill placeholders)
- Goal: {one-sentence goal}
- Context: {repo path(s) or files to integrate}
- Public API: {function/class names and signatures}
- Inputs: {types, expected sizes, example}
- Outputs: {types, error modes}
- Constraints: {python_version, allowed libs, no-network, perf targets}
- Tests: {1–3 pytest cases + 1 small benchmark}
- Deliverables: {file paths to create/modify}
- If uncertain: Ask 1 clarifying Q or state assumptions at top of file

Strict rules (short)
- Always: type hints for public API; module docstring; short docstrings for public functions.
- Keep functions small; extract helpers for repeated logic.
- Comment why (tradeoffs) for every non-obvious decision.
- Prefer streaming (iterators/generators) for large inputs.
- Include pytest tests and one micro-benchmark for performance-sensitive code.
- Add a single-line complexity note for non-trivial algorithms.

Minimal example (one-paragraph)
- Goal: fast_group_by(iterable, key) -> Iterator[(key, list)] grouping consecutive equal keys lazily.
- Context: add lib/collections_fast.py (stdlib only).
- Deliverables: lib/collections_fast.py, tests/test_collections_fast.py, benchmarks/bench_collections_fast.py

Checklist (copy into prompt)
- [ ] Goal
- [ ] Context
- [ ] API
- [ ] Inputs/Outputs
- [ ] Constraints
- [ ] Tests/Benchmark
- [ ] Deliverables
- [ ] Clarifying question if needed

Notes
-----
Keep the prompt short and focused on the API, constraints, and tests — the LLM will produce code fastest when given a tight specification and a small number of concrete unit tests to validate behavior.