---
title: Corporate VM & Bytecode Architecture
description: Deep dive into the Corporate Virtual Machine (CVM), stack layout, and instruction opcodes.
---

Corp++ includes both a tree-walking interpreter and a dedicated stack-based **Corporate Virtual Machine (CVM)**.

---

## ⚡ Corporate Instruction Set Architecture (CISA)

The compiler translates AST structures into compact bytecode instructions:

```text
=== Strategic Bytecode Chunk: <main> ===
0000  OP_LOAD_CONST          0
0001  OP_DECLARE_VAR         'headcount'
0002  OP_PROMOTE             ('headcount', 1)
0003  OP_LOAD_VAR            'headcount'
0004  OP_TOUCH_BASE          1
0005  OP_HARD_STOP          
```

---

## 📦 Core Opcodes

| Opcode | Description |
|---|---|
| `OP_LOAD_CONST` | Pushes constant index from constant pool to operand stack. |
| `OP_DECLARE_VAR` | Pops value and binds mutable `action_item` in active scope. |
| `OP_DECLARE_CORE` | Pops value and binds immutable `core_competency`. |
| `OP_STORE_VAR` | Assigns top stack value to variable. |
| `OP_PROMOTE` / `OP_DEMOTE` | Unary in-place metric mutation. |
| `OP_LAYOFFS` | Purges mutable bindings from the active scope frame. |
| `OP_JUMP_IF_FALSE` | Conditional jump for `as_per_our_discussion`. |
| `OP_CALL` / `OP_RETURN` | Pushes/pops `CallFrame` on the call stack. |
| `OP_PUSH_TRY` / `OP_POP_TRY` | Exception handler registration for risk mitigation. |

---

## 🚀 Running with CVM

To force bytecode execution on the CVM:

```bash
corp run file.corp --vm
```
