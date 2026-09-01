---
title: State, Core Competencies & Layoffs
description: Master mutable variables, immutable constants, hostile takeover defense, and layoffs memory flush.
---

Corp++ implements enterprise-grade memory safety through strict governance rules.

---

## 1. Mutable Allocation: `action_item`

An `action_item` represents a mutable variable allocated within the local scope:

```corp
action_item quarterly_bonus = 5000;
action_item team_size = 8;
action_item is_launched = misaligned; // false
```

### Mutating with `restructure`
Reassignment requires explicit strategic intent via `restructure`:

```corp
restructure quarterly_bonus = quarterly_bonus + 2500;
```

---

## 2. Immutable Constants: `core_competency`

A `core_competency` represents an unalterable strategic pillar (`const` equivalent):

```corp
core_competency MAX_ALLOWABLE_EXPENSE = 1000000;
core_competency HEADQUARTERS_CITY = "New York";
```

### 🚨 Hostile Takeover Protection
Attempting to mutate a `core_competency` will immediately abort execution and trigger an enterprise incident report:

```corp
core_competency CEO_BONUS = 50000000;
restructure CEO_BONUS = 0; // THROWS: HOSTILE_TAKEOVER_VIOLATION!
```

---

## 3. Scope Restructuring & Garbage Collection: `layoffs`

The `layoffs` statement acts as a localized scope purge. It terminates all non-core mutable `action_item` allocations in the active scope while preserving immutable `core_competency` declarations:

```corp
{
    core_competency LONG_TERM_VISION = "Sustainable Profitability";
    action_item temp_contractor_1 = "Contractor Alpha";
    action_item temp_contractor_2 = "Contractor Beta";

    touch_base("Pre-Layoffs Assets in Scope:");
    touch_base("Contractors:", temp_contractor_1, temp_contractor_2);

    // Trigger scope memory flush
    layoffs;

    // LONG_TERM_VISION is preserved
    touch_base("Surviving Asset:", LONG_TERM_VISION);

    // Accessing temp_contractor_1 now throws UNVETTED_RESOURCE_ALLOCATION!
}
```

---

## 4. Unary Performance Adjustments

- **`promote <var>;`**: Increments an integer or float by 1 (`+= 1`).
- **`demote <var>;`**: Decrements an integer or float by 1 (`-= 1`).

```corp
action_item rating = 4;
promote rating; // rating is now 5
demote rating;  // rating is back to 4
```
