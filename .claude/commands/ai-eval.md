---
description: AI feature evaluation harness - test LLM outputs, prompts, and AI-driven features
ecc_base_version: "5230892"
last_synced: "2026-01-27"
customizations: "Renamed from /eval to /ai-eval for clarity"
---

# /ai-eval - AI Feature Evaluation

Manage eval-driven development for AI/LLM features. Test prompts, outputs, and AI-driven functionality.

## Usage

```bash
/ai-eval define <name>     # Create new eval definition
/ai-eval check <name>      # Run and check evals
/ai-eval report <name>     # Generate full report
/ai-eval list              # Show all eval definitions
/ai-eval clean             # Remove old eval logs (keeps 10)
```

## When to Use

Use `/ai-eval` when:
- Testing LLM prompts and outputs
- Evaluating AI-generated content quality
- Measuring AI feature reliability
- Tracking AI capability improvements
- Ensuring AI features don't regress

**Note:** For standard code testing, use `/tdd` instead.

---

## Define Evals

`/ai-eval define feature-name`

Create a new eval definition at `.claude/evals/feature-name.md`:

```markdown
## EVAL: feature-name
Created: $(date)

### Capability Evals
- [ ] [Description of capability 1]
- [ ] [Description of capability 2]

### Regression Evals
- [ ] [Existing behavior 1 still works]
- [ ] [Existing behavior 2 still works]

### Success Criteria
- pass@3 > 90% for capability evals
- pass^3 = 100% for regression evals
```

---

## Check Evals

`/ai-eval check feature-name`

Run evals for a feature:

1. Read eval definition from `.claude/evals/feature-name.md`
2. For each capability eval:
   - Attempt to verify criterion
   - Record PASS/FAIL
   - Log attempt in `.claude/evals/feature-name.log`
3. For each regression eval:
   - Run relevant tests
   - Compare against baseline
   - Record PASS/FAIL
4. Report status:

```
EVAL CHECK: feature-name
========================
Capability: 4/5 passing
Regression: 3/3 passing
Status: IN PROGRESS
```

---

## Report Evals

`/ai-eval report feature-name`

Generate comprehensive eval report:

```
EVAL REPORT: feature-name
=========================
Generated: $(date)

CAPABILITY EVALS
----------------
[eval-1]: PASS (pass@1)
[eval-2]: PASS (pass@2) - required retry
[eval-3]: FAIL - see notes

REGRESSION EVALS
----------------
[test-1]: PASS
[test-2]: PASS
[test-3]: PASS

METRICS
-------
Capability pass@1: 67%
Capability pass@3: 100%
Regression pass^3: 100%

NOTES
-----
[Any issues, edge cases, or observations]

RECOMMENDATION
--------------
[SHIP / NEEDS WORK / BLOCKED]
```

---

## List Evals

`/ai-eval list`

Show all eval definitions:

```
EVAL DEFINITIONS
================
ai-search         [3/5 passing] IN PROGRESS
ai-summarize      [5/5 passing] READY
ai-translate      [0/4 passing] NOT STARTED
```

---

## Eval Metrics

| Metric | Definition | Use For |
|--------|------------|---------|
| **pass@1** | Passes on first attempt | Reliability |
| **pass@3** | Passes within 3 attempts | Capability |
| **pass^3** | Passes 3 consecutive times | Regression |

**Success Thresholds:**
- Capability evals: pass@3 > 90%
- Regression evals: pass^3 = 100%

---

## Example: Semantic Search Eval

```markdown
## EVAL: semantic-search
Created: 2026-01-27

### Capability Evals
- [ ] Returns relevant results for "election markets"
- [ ] Handles typos: "electoin" -> election results
- [ ] Understands synonyms: "voting" -> election results
- [ ] Empty query returns top trending

### Regression Evals
- [ ] Existing exact match still works
- [ ] Category filters still work
- [ ] Results limit respects parameter

### Success Criteria
- pass@3 > 90% for capability evals
- pass^3 = 100% for regression evals
```

---

## Arguments

| Argument | Description |
|----------|-------------|
| `define <name>` | Create new eval definition |
| `check <name>` | Run and check evals |
| `report <name>` | Generate full report |
| `list` | Show all eval definitions |
| `clean` | Remove old logs (keeps 10) |

---

## Agent Escalation

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Complex eval design | **ultrathink-analyst** | Deep analysis of evaluation criteria |
| Requirements validation | **requirements-analyst** | Ensure evals match requirements |
| Progress review | **intermediate-reviewer** | Review eval results |

---

## Related Commands

- `/tdd` - Standard code testing (use for non-AI features)
- `/design` - Plan AI feature implementation
- `/code-review` - Review AI feature code quality