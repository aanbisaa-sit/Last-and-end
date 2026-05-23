# Contributing to Last and End

Thank you for considering contributing to Last and End!

## Development setup

1. Clone the repository:
```bash
git clone https://github.com/aanbisaa-sit/Last-and-end.git
cd Last-and-end
```

2. Install development dependencies:
```bash
make install
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

## Running tests

```bash
make test          # run test suite
make test-cov      # run with coverage report
make lint          # check code style
make typecheck     # run mypy type checker
make all           # format + lint + typecheck + test
```

## Code style

- Follow PEP 8 conventions
- Use type hints for all function signatures
- Keep functions focused and single-purpose
- Write docstrings for public APIs

## Pull request process

1. Create a feature branch from `main`
2. Make your changes with clear, atomic commits
3. Add tests for new functionality
4. Ensure all tests pass and linting is clean
5. Update documentation if needed
6. Submit a pull request with a clear description

## Commit message format

Use conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `test:` test additions or changes
- `refactor:` code refactoring
- `chore:` maintenance tasks
- `ci:` CI/CD changes

## Questions?

Open an issue for discussion before starting major changes.
