---
description: Enforce no placeholder content. Verify all code is complete - no Lorem ipsum, TODO, Coming soon, or empty functions.
---

# /no-stubs - No Stubs or Placeholders

Validate that all code and UI is complete - no placeholder content allowed.

## Forbidden Patterns

### UI/Frontend
- Lorem ipsum or placeholder text
- "Coming soon", "Under construction", "TBD"
- Empty pages or stub components
- Placeholder images
- Non-functional buttons/links

### Code
- `pass` statements without implementation
- `// TODO: implement` comments
- Empty function bodies
- `throw new Error("Not implemented")`
- Commented-out code for "later"

## Validation Checklist

Run these checks:

```bash
# Check for forbidden patterns
grep -r "lorem ipsum" src/ --ignore-case
grep -r "coming soon" src/ --ignore-case
grep -r "TODO:" src/
grep -r "pass$" src/*.py
grep -r "NotImplementedError" src/
```

## The Rule

**If a feature isn't ready, don't include it at all.**

- Implement fully, OR
- Don't add to codebase

## Execution

When running /no-stubs:

1. Scan codebase for forbidden patterns
2. Report any violations found
3. Suggest fixes or removal
4. Verify all UI elements are functional
5. Confirm no placeholder content remains

## Agent Escalation

This command automatically escalates to specialized agents when:

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Standards compliance | **gold-standards-validator** | Full codebase compliance scan |
| UI completeness check | **ui-engineer** | React component completeness validation |
| Documentation stubs | **documentation-validator** | Validate documentation completeness |

### Escalation Triggers
- **gold-standards-validator**: Use for comprehensive stub/placeholder detection
- **ui-engineer**: Use for React UI completeness validation
- **documentation-validator**: Use to ensure documentation has no placeholders
