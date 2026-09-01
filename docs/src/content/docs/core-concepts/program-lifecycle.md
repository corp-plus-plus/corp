---
title: Program Lifecycle & Alignment
description: Understanding the executive program lifecycle, namespaces, and clean exits in Corp++.
---

Every Corp++ program follows a disciplined corporate lifecycle designed to minimize unvetted operations.

---

## 1. The Main Entry Point: `sync_alignment`

The `sync_alignment` block serves as the single source of truth and entry point (`main()` equivalent) for your application:

```corp
sync_alignment {
    touch_base("Leadership team aligned. Executing sprint...");
    // Application business logic goes here
    hard_stop;
}
```

Top-level declarations (such as reusable `delegate` functions and `quarterly_deliverables` modules) are parsed and onboarded prior to `sync_alignment` execution.

---

## 2. Strategic Namespaces: `quarterly_deliverables`

To prevent cross-departmental scope collisions, use `quarterly_deliverables` to encapsulate modules:

```corp
quarterly_deliverables MarketingOps {
    core_competency BUDGET_CAP = 250000;

    delegate print_campaign_name(campaign) {
        touch_base("Launching Campaign:", campaign);
    }
}
```

---

## 3. Clean Departure: `hard_stop`

The `hard_stop` statement cleanly terminates the process, immediately exiting the runtime.

```corp
sync_alignment {
    action_item error_count = 0;

    as_per_our_discussion (error_count > 0) {
        broadcast_all_hands("Critical blockers found. Aborting.");
        hard_stop 1; // Exit code 1
    }

    touch_base("All objectives satisfied.");
    hard_stop; // Exit code 0
}
```
