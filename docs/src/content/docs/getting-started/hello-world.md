---
title: Your First Q3 Deliverable (Hello World)
description: Step-by-step tutorial on writing, aligning, and executing your first Corp++ deliverable.
---

Let's onboard a new employee and write your first official Corp++ program!

---

## 1. Create the File

Create a new file named `onboarding.corp`:

```corp
// ==========================================
// Deliverable: onboarding.corp
// ==========================================

sync_alignment {
    // Standard Output Broadcast
    touch_base("Welcome to the Q3 Stakeholder Kickoff!");

    // Allocate resources
    action_item candidate_name = "Jordan Vance";
    action_item starting_level = 3;
    core_competency DEPARTMENT = "Strategic Synergy";

    touch_base("Onboarding:", candidate_name);
    touch_base("Department:", DEPARTMENT);
    touch_base("Initial Level:", starting_level);

    // Promote after positive review
    promote starting_level;
    touch_base("Post-Review Level:", starting_level);

    // Clean exit
    hard_stop;
}
```

---

## 2. Execute the Deliverable

Run the script using the `corp` CLI:

```bash
./dist/corp run onboarding.corp
```

### Output:
```text
Welcome to the Q3 Stakeholder Kickoff!
Onboarding: Jordan Vance
Department: Strategic Synergy
Initial Level: 3
Post-Review Level: 4
```

---

## 3. Executive Breakdown of What Happened

1. **`sync_alignment { ... }`**: Initiates the primary execution thread. Unaligned code outside this block is considered rogue operational expense.
2. **`touch_base(...)`**: Transmits deliverables to `stdout`.
3. **`action_item candidate_name = ...`**: Allocates a mutable variable in the active scope.
4. **`core_competency DEPARTMENT = ...`**: Allocates an immutable constant.
5. **`promote starting_level;`**: Increments the integer value by 1.
6. **`hard_stop;`**: Concludes the program with exit status `0`.
