# Contributing to Corp++

Welcome to the **Corp++ Contributor Onboarding Program**! We welcome cross-functional synergy from engineers, architects, and strategic stakeholders worldwide.

---

## The Corporate Contribution Workflow

1. **Alignment (Fork & Branch)**:
   Fork the repository and create an aligned feature branch:
   ```bash
   git checkout -b feature/strategic-initiative-name
   ```

2. **Compliance & Quality Assurance**:
   Ensure all changes pass our automated quality assurance suite:
   ```bash
   make test
   make package
   make run-examples
   ```

3. **Documentation Alignment**:
   If introducing new keywords, update the documentation in `docs/` and verify the build:
   ```bash
   make docs
   ```

4. **Executive Sign-Off (PR)**:
   Submit a Pull Request targeting `main` using our PR template.

---

## Tone & Style Guidelines

- **Zero Tolerance for Slang**: All error messages and logs must sound like passive-aggressive executive communications.
- **Strict Immutability**: `core_competency` declarations must never be mutable.
- **Clean Architecture**: Keep the compiler and runtime modular, fast, and free of external vendor dependencies.
