---
title: The Boardroom REPL
description: Real-time corporate alignment, memory inspection, and live evaluation in the terminal.
---

"The Boardroom" is Corp++'s interactive REPL environment for real-time prototyping and synergy testing.

---

## Launching the Boardroom

```bash
corp repl
```

```text
╔══════════════════════════════════════════════════════════════════════╗
║               CORP++ ENTERPRISE BOARDROOM REPL (v1.0)                ║
║  "Where Systems Programming Meets Unapologetic Middle-Management"   ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## Special Executive Commands

Inside the REPL, you can execute special slash commands:

- **`/help`**: Prints the corporate command menu.
- **`/kpis`**: Dumps all allocated variables, active competencies, and memory bindings in the current scope.
- **`/layoffs`**: Manually triggers an immediate memory flush in the active scope.
- **`/exit`** or **`hard_stop`**: Concludes the executive session.

---

## Example Session

```text
corp[Q1]> action_item team_size = 6;
corp[Q2]> core_competency SPRINT_DURATION = 14;
corp[Q3]> promote team_size;
corp[Q4]> touch_base("Current Team Size:", team_size);
Current Team Size: 7
corp[Q5]> /kpis
=== Active Corporate Scope Resources ===
Core Competencies: ['SPRINT_DURATION']
All Allocated Assets: ['team_size', 'SPRINT_DURATION']
corp[Q6]> /layoffs
[CORP++ HR MEMO - SCOPE FLUSH] Restructuring executed in 'CorporateGlobalAlignment'. 1 non-core action items eliminated to streamline Q3 operational efficiency.
corp[Q7]> hard_stop
Leadership alignment concluded. Have a productive sprint!
```
