# Contributing to Corp++

Thanks for checking out Corp++! Whether you're fixing a bug, adding a new corporate keyword, or improving documentation, contributions are welcome.

---

## Getting Started

1. **Fork and clone the repo**:
   ```bash
   git clone https://github.com/corp-plus-plus/corp.git
   cd corp
   ```

2. **Run tests**:
   Make sure everything is passing locally before making changes:
   ```bash
   make test
   ```

3. **Make your changes**:
   - Write your code in `corp/`
   - Add a test in `tests/`
   - If adding examples or docs, update `examples/` and `docs/`

4. **Verify your build**:
   ```bash
   make test
   make package
   make run-examples
   ```

5. **Open a PR**:
   Submit your pull request against `main`. Keep your PR focused and descriptive.

---

## Guidelines

- **Keep error messages corporate**: Any new compiler or runtime error should sound like an email from HR or middle management.
- **Zero external dependencies**: The core toolchain must remain pure Python using only standard library modules.
- **Make sure tests pass**: We run automated GitHub Actions across Python 3.9 through 3.12.
