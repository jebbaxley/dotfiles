# Reusable AI Prompt: Python Library Code (DRY, High-Performance, Readable)

Purpose
-------
This file is a reusable prompt template and instruction set for AI agents (LLMs, copilots, code generators) that will produce Python code intended to:  
1) be DRY (Don't Repeat Yourself),  
2) be high-performance and efficient,  
3) be designed to be combined into a larger library of reusable Python utilities,  
4) be easy to read and understand, and  
5) contain comments describing all aspects of the code.

How to use
----------
- Copy the prompt template below into the input for an AI agent.  
- Fill the placeholders with project-specific details (file paths, input shapes, constraints).  
- Require the agent to produce: source files, unit tests, brief performance notes, and a README usage snippet.

Prompt Template (copy-paste and fill placeholders)
-------------------------------------------------
Goal: {one-sentence goal — what the code should do or provide, targeted to library design}
Context: {repo: owner/repo and relevant file paths; existing modules to integrate with; any architectural notes}
Public API: {names, signatures, and intended behavior of public functions/classes}
Inputs: {types, shapes, example values; performance expectations like max size}
Outputs: {types, formats, side effects, error modes}
Constraints: {python_version, allowed_third_party_libs, no-network, memory/latency targets}
Style & Quality: {type hints, docstring style (Google/Numpy), black formatting, mypy strictness, comments for every non-trivial step}
Performance: {big-O targets, vectorization vs loops, concurrency model (async/multi-threading/multiprocessing), use of memoryviews/arrays}
DRY Requirements: {reusable helper functions, single-responsibility functions, avoid duplicated logic, prefer composition over inheritance}
Comments: {require comment blocks for modules and inline comments for algorithms, explanations of tradeoffs and alternatives}
Tests: {specific pytest cases, property-based tests, benchmarking snippets, edge cases}
Deliverables: {paths and filenames to create or modify (e.g., mypkg/module.py, tests/test_module.py, docs/USAGE.md)}
Examples: {input -> output short examples}
Benchmark: {small micro-benchmark script or pytest-benchmark cases and expected relative performance}
What to do if uncertain: {ask one clarifying question before implementing or make assumptions and list them at top of the file}

Agent Execution Rules (strict)
---------------------------
- ALWAYS include type hints on all public functions and classes.
- ALWAYS include a module-level docstring that explains the purpose and public API.
- Write Google-style or NumPy-style docstrings for each public function (choose project-wide and be consistent).
- Write comments that describe why code exists and why it's implemented that way (not just what it does).
- Keep functions small (prefer < 60 lines). If complexity grows, refactor into helpers.
- Ensure no duplicated logic across files: if two pieces of code are similar, extract a shared helper.
- Prefer clear names over clever but opaque code. Add short explanatory comments when using advanced techniques.
- Prefer iterators/generators for streaming/large data. Use memoryview/array for tight loops on bytes.
- For numeric or array operations prefer vectorized libraries (numpy) when allowed and benchmark both approaches if uncertain.
- Add explicit complexity analysis comment for non-trivial algorithms (time and space).
- Include pytest unit tests that cover normal cases, edge cases, and invalid inputs. Aim for 100% coverage for new modules.
- Add a small benchmark (timeit or pytest-benchmark) comparing at least two approaches where performance matters.
- Add a short README usage snippet demonstrating the public API and how to run tests and benchmarks.
- Provide a simple GitHub Actions workflow (optional but recommended) that runs tests and linting (black/mypy).

Structure and File Conventions
------------------------------
- Place library code under a package (e.g., mypkg/) with __init__.py exposing a minimal public API.
- Tests under tests/ with parallelizable test cases.
- Benchmarks under benchmarks/ or tests/benchmarks.py.
- Docs/usage examples under docs/ or README snippet in the module docstring.

Style and Tooling Preferences (suggested)
----------------------------------------
- Python version: prefer 3.11 unless project requires otherwise.
- Formatter: black.
- Linter/static typing: mypy (strict for public API), flake8 for style warnings.
- Testing: pytest.
- Benchmarks: pytest-benchmark or simple timeit scripts.
- CI: GitHub Actions with matrix for Python versions (3.10, 3.11).

Example Minimal Prompt (concrete)
--------------------------------
Goal: Implement function `fast_group_by(iterable: Iterable[T], key: Callable[[T], K]) -> Iterator[Tuple[K, List[T]]]` that groups consecutive items with the same key, yielding (key, list) lazily.
Context: New module under lib/collections_fast.py to be added to an existing library package `lib`. No external libs allowed.
Public API: fast_group_by(iterable: Iterable[T], key: Callable[[T], K]) -> Iterator[Tuple[K, List[T]]]
Inputs: iterable of items (can be generator), key function; typical sizes up to 1e7 items streamed.
Outputs: iterator yielding (key, list-of-items) for each group (lists should be small and reused carefully).
Constraints: Python 3.11; stdlib only; memory usage must be O(group_size) not O(n); must support generators and not rewind the input.
Style: type hints, docstrings, inline comments for algorithmic decisions, pytest tests including benchmarks.
Deliverables: lib/collections_fast.py, tests/test_collections_fast.py, benchmarks/bench_collections_fast.py, README snippet.
If uncertain: Ask one question about expected group size or assume groups are typically small (< 1000) and list copies are acceptable; document that assumption.

Example of Required Output Format from Agent
-------------------------------------------
- Provide files as code blocks with file path headers.
- Include tests and a brief explanation of performance tradeoffs.
- Include commands to run tests and run benchmarks (e.g., `pytest -q`, `python -m timeit -n 10 -r 3`).

Checklist (copy into prompt)
---------------------------
- [ ] Single-sentence goal
- [ ] Context and file paths
- [ ] Public API signatures
- [ ] Inputs and outputs with examples
- [ ] Performance constraints and targets
- [ ] Style and tooling rules (black, mypy, docstring style)
- [ ] Tests + benchmarks
- [ ] README usage snippet
- [ ] Ask clarifying question if uncertain

Notes on Comments and Readability
--------------------------------
- For every function with non-trivial logic, include a short header comment block explaining the algorithm, its complexity, and why this approach was chosen.
- Inline comments should explain intent, boundary conditions, and any micro-optimizations.
- Put non-obvious tradeoffs in a `# Tradeoffs:` comment block within the file or function.
- Where appropriate include `# Example:` usage comments showing quick calls and expected output.

Security and Safety
-------------------
- Avoid eval/exec or shell calls unless explicitly required and sandboxed.
- Validate inputs on public APIs and fail fast with clear exceptions.
- Avoid embedding secrets or credentials in code or tests.

What this file provides for maintainers
--------------------------------------
- A consistent, enforceable prompt to generate new Python modules that are DRY, high-performance, and library-ready.
- Explicit expectations for documentation, comments, tests, and benchmarks.
- A template that can be copied and filled in by maintainers or CI to generate new modules with predictable quality.

