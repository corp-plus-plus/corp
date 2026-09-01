---
title: Corporate CLI (corp) Reference
description: Complete reference guide for the Corp++ command-line toolchain.
---

The `corp` executable provides a unified interface for running, compiling, auditing, and packaging Corp++ programs.

---

## 📋 Command Matrix

| Command | Syntax | Description |
|---|---|---|
| **Run Deliverable** | `corp run <file.corp> [--vm]` | Executes a `.corp` program using the tree-walking interpreter (or `--vm` for the virtual machine). |
| **Compile / Disassemble** | `corp compile <file.corp> [-d]` | Compiles AST to bytecode instructions or outputs full disassembly (`-d`). |
| **Interactive Boardroom** | `corp repl` | Launches "The Boardroom" interactive alignment REPL session. |
| **KPI & ESG Audit** | `corp audit <file.corp>` | Performs static analysis and generates a corporate governance audit score. |
| **Package Standalone Binary**| `corp package` | Bundles the toolchain into a single-file executable at `dist/corp`. |

---

## 🚀 Examples

### Running a script
```bash
corp run examples/01_onboarding.corp
```

### Running with the Corporate Virtual Machine (CVM)
```bash
corp run examples/05_q3_financials.corp --vm
```

### Disassembling Bytecode
```bash
corp compile -d examples/01_onboarding.corp
```

### Running Static Compliance Audit
```bash
corp audit examples/05_q3_financials.corp
```
