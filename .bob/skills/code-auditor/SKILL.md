---
name: code-auditor
description: Use when the user requests an architectural, security, or standards audit of code in the CampusRoute ecosystem. Scans for banned execution primitives (eval, exec, compile, os.system, subprocess), verifies standard library compliance, and checks domain exception design.
---

# Code Auditor Skill

Verifies software engineering standards, security constraints, and safety guidelines for the Bobathon repository.

## Audit Checklist
1. **Zero External Dependencies:** No `pip install`, `npm install`, or external downloads.
2. **Forbidden Primitives:** Zero occurrences of `eval()`, `exec()`, `compile()`, `os.system()`, or `subprocess` in application and interpreter code.
3. **Network & Binding:** Local services must strictly bind to `127.0.0.1`.
4. **Domain Exceptions:** Clear, actionable domain exceptions (`UnknownPlaceError`, `NoRouteError`, `ScheduleError`, `CampusDataError`).
5. **Test Integrity:** When tests fail, fix the implementation, never modify the expected test values.
