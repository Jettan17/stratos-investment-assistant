# Update Documentation

Sync documentation from source-of-truth:

1. Read package.json scripts section
   - Generate scripts reference table
   - Include descriptions from comments

2. Read .env.example
   - Extract all environment variables
   - Document purpose and format

3. Generate docs/CONTRIB.md with:
   - Development workflow
   - Available scripts
   - Environment setup
   - Testing procedures

4. Generate docs/RUNBOOK.md with:
   - Deployment procedures
   - Monitoring and alerts
   - Common issues and fixes
   - Rollback procedures

5. Identify obsolete documentation:
   - Find docs not modified in 90+ days
   - List for manual review

6. Show diff summary

Single source of truth: package.json and .env.example

## Agent Escalation

This command automatically escalates to specialized agents when:

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Code examples need testing | **documentation-validator** | Test all code examples in documentation |
| Cross-reference validation | **documentation-validator** | Ensure docs match actual implementation |
| Complete doc validation | **documentation-validator** | Full documentation set validation |

### Escalation Triggers
- **documentation-validator**: Use when updating documentation with code examples, creating tutorials, or validating documentation accuracy against implementation
