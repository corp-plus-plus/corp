---
title: Standard I/O & Town Hall Telemetry
description: Transparent communication channels, user input sign-off, and all-hands broadcast alerts.
---

In Corp++, clear communication is the foundation of high synergy.

---

## 1. Standard Output: `touch_base(...)`

Prints arguments to `stdout` separated by spaces and terminated by a newline:

```corp
touch_base("Q3 Revenue:", 1500000, "EBITDA Margin:", "36.6%");
```

---

## 2. Standard Input: `please_advise([prompt])`

Requests interactive user input from `stdin`:

```corp
action_item user_name = please_advise("Please submit employee ID:");
touch_base("Welcome aboard,", user_name);
```

---

## 3. Emergency Alerts: `broadcast_all_hands(...)`

Emits an urgent alert to `stderr` formatted with a high-visibility corporate warning banner:

```corp
as_per_our_discussion (available_runway_months < 3) {
    broadcast_all_hands("RUNWAY CRITICAL: Immediate freeze on offsite catering.");
}
```
