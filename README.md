# Corp++ (`.corp`)
### *Where systems programming meets middle-management speak.*

[![Build Status](https://github.com/corp-plus-plus/corp/actions/workflows/ci.yml/badge.svg)](#)
[![Synergy](https://img.shields.io/badge/Synergy-100%25-brightgreen.svg)](#)
[![License](https://img.shields.io/badge/License-ViB_v4.1-blue.svg)](#)

---

## What is this?

**Corp++** is an esoteric programming language designed for when you want your code to sound like an all-hands slide deck.

Instead of `let`, `const`, `if`, `while`, and `try/catch`, everything is framed in pure corporate buzzwords:

- Variables are **`action_item`**
- Constants are **`core_competency`** (and mutating them triggers a `HOSTILE_TAKEOVER_VIOLATION`)
- `if` statements are **`as_per_our_discussion`**
- Loops are **`circle_back`**
- Functions are **`delegate`** routines that you **`loop_in`**
- Scope garbage collection is triggered with **`layoffs;`**
- Errors don't just crash — they file a **Performance Improvement Plan (PIP)** with HR

Built in pure Python with zero dependencies, packaged into a single standalone binary you can send to your friends.

---

## Quickstart & Standalone Binary

You don't need to install anything except Python 3. The compiler bundles into a standalone executable at `dist/corp`.

### 1. Build the Binary
```bash
make package
# or: python3 scripts/build_binary.py
```

### 2. Run a Script
```bash
./dist/corp run examples/01_onboarding.corp
```

### 3. Send to Friends
You can copy `dist/corp` anywhere on macOS/Linux and run it directly:
```bash
cp dist/corp /usr/local/bin/corp
corp run my_script.corp
```

---

## Syntax Cheatsheet

| Standard Keyword | Corp++ Equivalent | What it does |
|---|---|---|
| `main()` | `sync_alignment { ... }` | Mandatory entry point for your program. |
| `let x = 5` | `action_item x = 5;` | Mutable variable. |
| `const Y = 10` | `core_competency Y = 10;` | Immutable constant. Cannot be reassigned. |
| `x = 20` | `restructure x = 20;` | Reassign a variable. |
| `x++` / `x--` | `promote x;` / `demote x;` | Increment or decrement by 1. |
| `GC / free()` | `layoffs;` | Flushes all non-core mutable variables from active scope. |
| `if (cond)` | `as_per_our_discussion (cond) { ... }` | Conditional branch. |
| `else` | `pivot { ... }` | Fallback branch. |
| `while (cond)` | `circle_back (cond) { ... }` | Loop while condition is aligned (`true`). |
| `for (x of arr)` | `touch_every_base (x in arr) { ... }` | Iterate over arrays. |
| `break` | `table_this;` | Break out of a loop. |
| `continue` | `push_to_next_sprint;` | Skip to next loop iteration. |
| `print()` | `touch_base(...);` | Write to stdout. |
| `input()` | `please_advise("Prompt: ");` | Read from stdin. |
| `console.error()` | `broadcast_all_hands(...);` | Write to stderr. |
| `function fn()` | `delegate fn(...) { ... }` | Declare a function. |
| `fn(args)` | `loop_in(fn(args))` | Call a function. |
| `return x` | `deliverable x;` | Return a value. |
| `try { ... }` | `let's_take_this_offline { ... }` | Catch exceptions. |
| `catch (err)` | `mitigate_risk (err) { ... }` | Handle errors. |
| `throw err` | `opt_out "Reason";` | Raise runtime exception. |

---

## Code Examples

### 1. Employee Onboarding (`examples/01_onboarding.corp`)
```corp
sync_alignment {
    touch_base("Starting Q3 Stakeholder Alignment Meeting...");

    action_item employee_name = "Alex Vance";
    action_item current_level = 3;
    action_item annual_bonus = 15000;

    core_competency COMPANY_MISSION = "Delivering Hyper-Scalable Synergy";

    touch_base("Onboarding:", employee_name);
    touch_base("Initial Level:", current_level);
    touch_base("Mission Statement:", COMPANY_MISSION);

    promote current_level;
    restructure annual_bonus = annual_bonus + 5000;

    touch_base("Post-Review Level:", current_level);
    touch_base("Restructured Bonus:", annual_bonus);

    hard_stop;
}
```

### 2. Risk Mitigation & Protected Execution (`examples/02_risk_mitigation.corp`)
```corp
sync_alignment {
    let's_take_this_offline {
        action_item budget = 0;
        
        as_per_our_discussion (budget == 0) {
            broadcast_all_hands("Budget exhausted! Initiating executive opt-out.");
            opt_out "Severe bandwidth exhaustion in Project Apollo.";
        }
    } mitigate_risk (err) {
        touch_base("[RISK MITIGATED] Handled incident smoothly:", err);
    }

    hard_stop;
}
```

### 3. Corporate FizzBuzz (`examples/06_fizzbuzz_kpi.corp`)
```corp
sync_alignment {
    action_item kpi_index = 1;

    circle_back (kpi_index <= 15) {
        action_item is_div_3 = (kpi_index % 3 == 0);
        action_item is_div_5 = (kpi_index % 5 == 0);

        as_per_our_discussion (is_div_3 synergizes_with is_div_5) {
            touch_base("KPI", kpi_index, ": SYNERGY_OPTIMIZED (Divisible by 3 & 5)");
        } pivot as_per_our_discussion (is_div_3) {
            touch_base("KPI", kpi_index, ": SYNERGY (Divisible by 3)");
        } pivot as_per_our_discussion (is_div_5) {
            touch_base("KPI", kpi_index, ": OPTIMIZED (Divisible by 5)");
        } pivot {
            touch_base("KPI", kpi_index, ": Standard Performance Baseline");
        }

        promote kpi_index;
    }

    hard_stop;
}
```

---

## Error Telemetry & Incident Reports

When your code errors, Corp++ prints a full incident memo with passive-aggressive feedback:

```text
╔══════════════════════════════════════════════════════════════════════════╗
║  [CORP++ ENTERPRISE INCIDENT REPORT] ID: CORP-INC-10194                 ║
║  ESCALATION LEVEL: HOSTILE_TAKEOVER_VIOLATION                        ║
╚══════════════════════════════════════════════════════════════════════════╝
With all due respect to the leadership team, Hostile takeover attempt rejected! Cannot restructure 'CEO_COMPENSATION' as it is declared as a non-negotiable 'core_competency'.

Location: examples/07_hostile_takeover_error.corp:11:5

    11 |     restructure CEO_COMPENSATION = 50000;
       |     ^

Next Steps: Action Item: Escalate to your Level 2 Managing Director immediately.
```

---

## Interactive REPL: "The Boardroom"

Jump straight into a live alignment session:

```bash
./dist/corp repl
```

```text
corp[Q1]> action_item headcount = 5;
corp[Q2]> promote headcount;
corp[Q3]> touch_base("Current Headcount:", headcount);
Current Headcount: 6
corp[Q4]> /kpis
=== Active Corporate Scope Resources ===
Core Competencies: []
All Allocated Assets: ['headcount']
corp[Q5]> /layoffs
[CORP++ HR MEMO - SCOPE FLUSH] Restructuring executed in 'CorporateGlobalAlignment'. 1 non-core action items eliminated to streamline Q3 operational efficiency.
corp[Q6]> hard_stop
```

---

## CLI Commands

```bash
corp run file.corp        # Run with tree-walking interpreter
corp run file.corp --vm   # Run with stack-based bytecode virtual machine (CVM)
corp compile -d file.corp # View bytecode disassembly
corp audit file.corp      # Check code alignment and generate a synergy score
corp repl                 # Start interactive REPL
corp package              # Re-bundle the standalone binary to dist/corp
```

---

## Documentation

Full docs built with Astro Starlight are in the `docs/` folder:

```bash
make docs-dev
# Open http://localhost:4324
```

---

## License

Protected under [ViB License v4.1 — Restricted Use License](LICENSE).
