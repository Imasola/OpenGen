# Contributing to OpenGen

Thank you for your interest in OpenGen. Every contribution helps build a better knowledge network.

---

## Ways to contribute

| Contribution | When available |
|-------------|---------------|
| **Code** | Now - fork, branch, PR |
| **Documentation** | Now - improve docs, fix typos, translate |
| **Ideas** | Now - open an issue or discussion |
| **Compute power** | Phase 4 - run the Worker program |
| **Knowledge review** | Phase 3 - vote on results at opengen.live |
| **Spread the word** | Now - star this repo, share the project |

---

## Code contributions

### Setup

```bash
git clone https://github.com/Imasola/OpenGen.git
cd opengen
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Workflow

1. Fork the repository
2. Create a branch from `main`: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests: `pytest`
5. Run linter: `ruff check .`
6. Commit with a clear message (see format below)
7. Push and open a Pull Request

### Branch naming

```
feature/add-semantic-search      # New feature
fix/critic-score-parsing         # Bug fix
docs/update-architecture         # Documentation
refactor/simplify-pipeline       # Code refactoring
test/add-graph-tests             # Tests
```

### Commit messages

```
Add: semantic search for knowledge graph
Fix: critic agent JSON parsing on malformed responses
Docs: update architecture with knowledge access section
Refactor: simplify pipeline runner loop logic
Test: add unit tests for trust score calculation
```

Start with a verb: `Add`, `Fix`, `Docs`, `Refactor`, `Test`, `Remove`, `Update`.

### Pull request process

1. Fill out the PR template (created automatically)
2. Link any related issues
3. Describe what changed and why
4. One PR per feature or fix — keep them focused
5. A maintainer will review and provide feedback

---

## Code style

- **Python 3.11+**
- Format with `ruff format .`
- Lint with `ruff check .`
- Type hints on all function signatures
- Docstrings on all public functions and classes
- Comments explain *why*, not *what*

---

## Reporting bugs

Use the **Bug report** issue template. Include:

1. What you expected to happen
2. What actually happened
3. Steps to reproduce
4. Your environment (OS, Python version)

---

## Suggesting features

Use the **Feature request** issue template. Include:

1. What problem does this solve?
2. How should it work?
3. Are there alternatives?

---

## Security vulnerabilities

**Do not open a public issue.** See [SECURITY.md](SECURITY.md).

---

## Code of conduct

All participants are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
