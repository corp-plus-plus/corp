---
title: Installation & Standalone Binary
description: How to install, build, and distribute the Corp++ toolchain and standalone executable binary.
---

Corp++ requires **Python 3.8+** with standard libraries. It ships with a standalone single-file executable binary (`dist/corp`) that has zero external dependencies.

---

## Fast Track: Using the Pre-Built Binary

If you already have the repository cloned:

```bash
# Execute directly from root:
./dist/corp --version
```

### Install into your System PATH

To make the `corp` command available across your entire operating system:

```bash
# Copy to /usr/local/bin (or ~/.local/bin)
sudo cp dist/corp /usr/local/bin/corp

# Verify global access:
corp --version
```

---

## "Send to Friends" Binary Distribution

Because Corp++ is bundled using Python's executable archive packaging (`zipapp`), the compiled binary in `dist/corp` is a single file containing the entire compiler, runtime interpreter, bytecode VM, and corporate error telemetry engine.

You can send `dist/corp` over Slack, Email, or AirDrop to any team member. They can run it immediately:

```bash
chmod +x corp
./corp run my_script.corp
```

---

## Building the Toolchain from Source

To package a fresh standalone executable binary:

```bash
# Using Make:
make package

# Or using the Python build script:
python3 scripts/build_binary.py
```

### Running Test Validation

Verify that all corporate competencies pass quality assurance:

```bash
make test
```
