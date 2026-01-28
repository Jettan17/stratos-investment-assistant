---
description: Run comprehensive verification on current codebase
ecc_base_version: "5230892"
last_synced: "2026-01-27"
customizations: "Enhanced flags documentation"
---

# /verify - Verification Command

Run comprehensive verification on current codebase state.

## Usage

```bash
/verify                 # Full verification (default)
/verify quick           # Build + types only
/verify pre-commit      # Checks for commits
/verify pre-pr          # Full + security scan
/verify --e2e           # Include E2E tests
/verify --full          # All checks including E2E
```

## Verification Steps

Execute in this exact order:

### 1. Build Check
- Run the build command for this project
- If it fails, report errors and STOP

### 2. Type Check
- Run TypeScript/type checker
- Report all errors with file:line

### 3. Lint Check
- Run linter
- Report warnings and errors

### 4. Test Suite
- Run all tests
- Report pass/fail count
- Report coverage percentage

### 5. Console.log Audit
- Search for console.log in source files
- Report locations

### 6. Git Status
- Show uncommitted changes
- Show files modified since last commit

---

## Arguments

| Argument | What It Does |
|----------|--------------|
| *(none)* | Full verification (build + types + lint + tests) |
| `quick` | Build + types only (fast) |
| `pre-commit` | Checks relevant for commits |
| `pre-pr` | Full + security scan |
| `--e2e` | Include E2E tests in verification |
| `--full` | All checks including E2E and coverage analysis |

---

## Output

Produce a concise verification report:

```
VERIFICATION: [PASS/FAIL]

Build:    [OK/FAIL]
Types:    [OK/X errors]
Lint:     [OK/X issues]
Tests:    [X/Y passed, Z% coverage]
Secrets:  [OK/X found]
Logs:     [OK/X console.logs]

Ready for PR: [YES/NO]
```

If any critical issues, list them with fix suggestions.

---

## Examples

```bash
# Quick check before committing
/verify quick

# Full check before PR
/verify pre-pr

# Include E2E tests
/verify --e2e

# Everything including E2E and coverage
/verify --full
```

---

## Agent Escalation

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Standards compliance | **gold-standards-validator** | Pattern compliance, coding standards |
| Security scan | **security-auditor** | Vulnerability analysis |

---

## Related Commands

- `/tdd` - Run tests with TDD workflow
- `/build-fix` - Fix build errors
- `/code-review` - Quality review before PR
