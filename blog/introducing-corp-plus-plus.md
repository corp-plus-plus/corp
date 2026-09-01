# Announcing Corp++: Why Middle Management is the Future of Systems Programming

I got tired of hearing tech leads explain stack traces while executives asked for "cross-functional synergy."

So I built **Corp++** (`.corp`): an esoteric programming language that forces your code to sound like an all-hands slide deck.

---

## The Joke That Got Out of Hand

Most programming languages are built around math or logic. Corp++ is built around corporate bureaucracy.

Instead of declaring variables with `let` or `const`, you allocate an `action_item` or establish an immutable `core_competency`. If you try to change a `core_competency`, the compiler doesn't just throw an error — it halts execution with a `HOSTILE_TAKEOVER_VIOLATION` and issues a Performance Improvement Plan (PIP).

Here's what actual Corp++ code looks like:

```corp
sync_alignment {
    core_competency COMPANY_MISSION = "Hyper-Scalable Synergies";
    action_item headcount = 12;

    promote headcount;
    touch_base("Strategic Headcount Target:", headcount);

    hard_stop;
}
```

---

## How it Actually Works

Under the hood, Corp++ isn't just a toy regex replacer. It has a full compiler pipeline:

1. **Lexer & Parser**: A recursive descent parser that constructs an Abstract Syntax Tree (AST) from corporate tokens.
2. **Interpreter & Virtual Machine**: You can run scripts either via the tree-walking interpreter (`corp run file.corp`) or compile them to bytecode and execute on a stack-based Corporate Virtual Machine (`corp run file.corp --vm`).
3. **Memory Management via Layoffs**:
   When memory gets tight, you don't call `free()`. You call `layoffs;`.
   ```corp
   {
       core_competency SURVIVING_STRATEGY = "Core Platform Resiliency";
       action_item temp_contractor_1 = "Contractor Alpha";
       action_item temp_contractor_2 = "Contractor Beta";

       // Purges all non-core mutable variables in active scope
       layoffs;

       // Accessing temp_contractor_1 now throws an Unvetted Resource error!
   }
   ```
4. **Passive-Aggressive Error Reporting**:
   Runtime errors format like real executive emails:
   ```text
   ╔══════════════════════════════════════════════════════════════════════════╗
   ║  [CORP++ ENTERPRISE INCIDENT REPORT] ID: CORP-INC-89412                 ║
   ║  ESCALATION LEVEL: ZERO_DIVIDEND_PERFORMANCE_ANOMALY                 ║
   ╚══════════════════════════════════════════════════════════════════════════╝
   Per my last email, Division by zero is not aligned with our Q3 growth objectives.

   Location: src/finance.corp:14:18

       14 |     action_item margin = total_profit / zero_cost;
          |                  ^

   Next Steps: Action Item: A Performance Improvement Plan (PIP) has been automatically scheduled with HR.
   ```

---

## Single Binary: Send it to your Team

I built Corp++ with zero third-party dependencies using Python standard libraries.

Running `make package` creates a single, self-contained executable binary at `dist/corp`. You can drop it into `/usr/local/bin` or zip it and send it to your coworkers.

```bash
# Run any file
./dist/corp run examples/01_onboarding.corp

# Open "The Boardroom" interactive REPL
./dist/corp repl

# Audit your code's synergy score
./dist/corp audit examples/05_q3_financials.corp
```

---

## Full Docs

Full documentation is built with Astro Starlight in `docs/`:

```bash
cd docs && npm install && npm run dev
```

Check out the repo, write some `.corp` files, and remember: *align early, touch base often, and protect core competencies.*
