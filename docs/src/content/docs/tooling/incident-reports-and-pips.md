---
title: Incident Reports & PIP Notices
description: Enterprise incident reports, passive-aggressive error telemetry, and Performance Improvement Plans.
---

When code fails in Corp++, errors are not merely printed as generic stack traces. They are published as formal **Corporate Incident Reports** containing actionable Performance Improvement Plans (PIPs).

---

## Incident Report Anatomy

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

## Escalation Hierarchy

| Escalation Level | Description |
|---|---|
| `UNSCHEDULED_SYNTAX_ALIGNMENT_DEBACLE` | Syntax error / missing curly brace / invalid token. |
| `HOSTILE_TAKEOVER_VIOLATION` | Attempted mutation of an immutable `core_competency`. |
| `UNVETTED_RESOURCE_ALLOCATION` | Accessing an undeclared or laid-off variable. |
| `CROSS_FUNCTIONAL_TYPE_MISALIGNMENT` | Attempting incompatible operations across data types. |
| `ZERO_DIVIDEND_PERFORMANCE_ANOMALY` | Division by zero (incompatible with growth targets). |
| `OUT_OF_BOUNDS_BANDWIDTH_EXCEPTION` | Accessing array indices beyond allocated memory. |
