# Agentic Engineering Guidelines

1. **Verify with Tests First:** Always run test suites before and after making code changes.
2. **Standard Library Only:** Never import third-party packages or trigger external downloads.
3. **Defense in Depth:** Disallow arbitrary execution primitives (`eval`, `exec`, `subprocess`).
4. **Idempotent Changes:** Every file edit should be clean, self-contained, and reproducible.
5. **Clear Explanations:** Provide human-readable rationale and actionable hints.
