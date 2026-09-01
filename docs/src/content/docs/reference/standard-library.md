---
title: Standard Library Modules
description: Pre-built corporate standard libraries and helper delegates.
---

Corp++ includes standard corporate utility modules located in `corp/stdlib/`.

---

## 📈 1. `SynergyLib` (`corp/stdlib/synergy.corp`)

Provides mathematical and growth modeling delegates:

- `max_growth(a, b)`: Compares two projections and returns the higher growth metric.
- `min_risk(a, b)`: Returns the value with minimal exposure.
- `compound_interest(principal, rate, periods)`: Computes multi-period compound revenue acceleration.

---

## 👔 2. `ExecutiveHelpers` (`corp/stdlib/executive.corp`)

- `evaluate_roi(revenue, cost)`: Calculates return on investment. Throws an `opt_out` exception if cost basis is zero.
- `is_mission_critical(score)`: Evaluates if a project meets or exceeds the ESG threshold of 80 points.

---

## 🛠️ 3. Built-In Global Functions

- **`headcount(collection)`**: Returns the length of an array or string.
- **`range(start, stop)`**: Returns an array of sequential integers.
- **`corporate_string(val)`**: Converts any asset to its corporate string representation.
- **`synergy_number(val)`**: Parses numeric assets from strings.
