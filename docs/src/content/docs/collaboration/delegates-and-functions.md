---
title: Delegates & Cross-Functional Work
description: Defining modular delegates, capturing lexical closures, and looping in stakeholders.
---

Complex corporate initiatives require cross-functional collaboration. In Corp++, functions are declared as **`delegate`** routines and called by **`loop_in`**.

---

## 1. Declaring a Function: `delegate`

```corp
delegate calculate_comp(base_salary, bonus_multiplier) {
    action_item total = base_salary * bonus_multiplier;
    deliverable total;
}
```

- Parameters are defined inside parentheses `(param1, param2)`.
- The **`deliverable`** statement returns the computed value back to the caller.

---

## 2. Looping in Stakeholders: `loop_in(...)`

To invoke a delegate and receive its deliverable:

```corp
sync_alignment {
    // Standard invocation via loop_in:
    action_item alex_comp = loop_in(calculate_comp(120000, 1.25));
    touch_base("Total Annual Compensation Package:", alex_comp);

    hard_stop;
}
```

---

## 3. Lexical Closures & Scope Retention

Delegates retain references to their outer environment:

```corp
delegate create_multiplier(factor) {
    delegate multiply(val) {
        deliverable val * factor;
    }
    deliverable multiply;
}
```
