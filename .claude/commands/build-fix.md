# Build and Fix

Incrementally fix TypeScript and build errors:

1. Run build: npm run build or pnpm build

2. Parse error output:
   - Group by file
   - Sort by severity

3. For each error:
   - Show error context (5 lines before/after)
   - Explain the issue
   - Propose fix
   - Apply fix
   - Re-run build
   - Verify error resolved

4. Stop if:
   - Fix introduces new errors
   - Same error persists after 3 attempts
   - User requests pause

5. Show summary:
   - Errors fixed
   - Errors remaining
   - New errors introduced

Fix one error at a time for safety!

## Agent Escalation

This command automatically escalates to specialized agents when:

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Complex build failures | **build-error-resolver** | Deep analysis of systemic build issues |
| React build errors | **ui-engineer** | Next.js/React 19 build configurations |
| Type system issues | **architect** | TypeScript architecture decisions |

### Escalation Triggers
- **build-error-resolver**: Use for persistent or complex build failures
- **ui-engineer**: Use for Next.js/React specific build issues
- **architect**: Use when build errors indicate architectural problems
