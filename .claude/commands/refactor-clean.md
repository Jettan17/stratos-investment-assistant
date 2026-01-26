# Refactor Clean

Safely identify and remove dead code with test verification:

1. Run dead code analysis tools:
   - knip: Find unused exports and files
   - depcheck: Find unused dependencies
   - ts-prune: Find unused TypeScript exports

2. Generate comprehensive report in .reports/dead-code-analysis.md

3. Categorize findings by severity:
   - SAFE: Test files, unused utilities
   - CAUTION: API routes, components
   - DANGER: Config files, main entry points

4. Propose safe deletions only

5. Before each deletion:
   - Run full test suite
   - Verify tests pass
   - Apply change
   - Re-run tests
   - Rollback if tests fail

6. Show summary of cleaned items

Never delete code without running tests first!

## Agent Escalation

This command automatically escalates to specialized agents when:

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Large-scale refactoring | **architect** | Architectural impact analysis |
| Quality verification | **code-reviewer** | Review refactored code quality |
| Pattern compliance | **gold-standards-validator** | Ensure refactored code follows standards |

### Escalation Triggers
- **architect**: Use for significant structural changes
- **code-reviewer**: Use to verify refactoring maintains quality
- **gold-standards-validator**: Use to validate pattern compliance after refactoring
