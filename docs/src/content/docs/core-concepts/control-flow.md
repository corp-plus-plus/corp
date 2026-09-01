---
title: Control Flow & Strategic Pivots
description: Decision branching, circular loops, collection traversal, and sprint deferrals in Corp++.
---

Corporate strategy is dynamic. Corp++ provides expressive branching and looping primitives to navigate shifting market conditions.

---

## 1. Conditional Branching: `as_per_our_discussion` & `pivot`

### Basic Conditional (`if` / `else`)
```corp
as_per_our_discussion (ebitda > 500000) {
    touch_base("Target exceeded. Performance bonuses approved.");
} pivot {
    broadcast_all_hands("Target missed. Initiating immediate restructuring.");
}
```

### Chained Multi-Tier Discussions (`else if`)
```corp
as_per_our_discussion (performance_score >= 90) {
    touch_base("Rating: Exceeds High Expectations (Top Tier)");
} pivot as_per_our_discussion (performance_score >= 70) {
    touch_base("Rating: Meets Expectations");
} pivot {
    touch_base("Rating: Performance Improvement Plan required");
}
```

---

## 2. Iterative Alignment: `circle_back` (`while` loop)

Use `circle_back` to repeat a block while a condition remains `aligned` (`true`):

```corp
action_item iteration = 1;

circle_back (iteration <= 5) {
    touch_base("Completing Sprint Cycle:", iteration);
    promote iteration;
}
```

---

## 3. Stakeholder Traversal: `touch_every_base` (`for..in` loop)

To iterate over arrays and collections:

```corp
action_item workstreams = ["Frontend", "Core VM", "Telemetry", "Investor Relations"];

touch_every_base (dept in workstreams) {
    touch_base("Conducting 1-on-1 review with:", dept);
}
```

---

## 4. Loop Control

- **`table_this;`**: Immediately breaks out of the active loop (`break`).
- **`push_to_next_sprint;`**: Skips the remaining operations and jumps to the next iteration (`continue`).

```corp
action_item tickets = [101, 102, 103, 104];

touch_every_base (ticket in tickets) {
    as_per_our_discussion (ticket == 102) {
        touch_base("Ticket 102 is blocked. Pushing to next sprint.");
        push_to_next_sprint;
    }

    as_per_our_discussion (ticket == 104) {
        touch_base("Budget exhausted. Tabling remaining backlog.");
        table_this;
    }

    touch_base("Resolving ticket:", ticket);
}
```
