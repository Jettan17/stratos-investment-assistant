# Claude Code SDK Subagents

This directory contains specialized subagents for the Claude Code SDK development environment.

## Available Agents (13 total)

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| **deep-reflector** | Session analysis and learning capture | `/learn` command, pattern extraction |
| **deployment-specialist** | Docker/Kubernetes deployment | Production deployments, CI/CD setup |
| **documentation-validator** | Documentation validation | Testing code examples, doc accuracy |
| **flutter-specialist** | Flutter mobile/desktop apps | Cross-platform mobile development |
| **framework-advisor** | Framework selection guidance | Technology stack decisions |
| **gh-manager** | GitHub project management | Issue tracking, project boards, PRs |
| **gold-standards-validator** | Compliance checking | Code validation, standards enforcement |
| **intermediate-reviewer** | Checkpoint reviews | Progress validation, milestone critiques |
| **requirements-analyst** | Requirements breakdown | ADRs, systematic analysis |
| **security-auditor** | Security analysis | Vulnerability scanning, OWASP Top 10 |
| **todo-manager** | Task management | Todo lists, project tracking |
| **ui-engineer** | UI/UX specialist | React, accessibility, design systems |
| **ultrathink-analyst** | Deep failure analysis | Complex features, risk analysis |

---

## Workflow Phases

### Phase 1: Analysis & Planning
```
1. > Use ultrathink-analyst for complex requirement analysis
2. > Use requirements-analyst for systematic breakdown
3. > Use framework-advisor for technology decisions
```

### Phase 2: Task Management
```
1. > Use todo-manager to create task breakdown
2. > Use gh-manager to sync with GitHub Projects
3. > Use intermediate-reviewer to validate plan
```

### Phase 3: Implementation
```
For each component:
1. Run /tdd for test-first development
2. > Use ui-engineer for frontend components
3. > Use flutter-specialist for mobile components
4. > Use gold-standards-validator to ensure compliance
5. > Use intermediate-reviewer to review progress
```

### Phase 4: Testing & Documentation
```
1. Run /e2e for end-to-end tests
2. > Use documentation-validator to verify docs
3. > Use todo-manager to update task status
```

### Phase 5: Deployment
```
1. Run /deploy for Docker/Kubernetes setup
2. > Use deployment-specialist for production config
```

### Phase 6: Release
```
1. Run /code-review for final quality check
2. > Use security-auditor for security scan
3. > Use intermediate-reviewer for final critique
```

---

## Quick Debugging

```
When facing issues:
1. > Use ultrathink-analyst for deep analysis
2. > Use ui-engineer for frontend issues
3. > Use flutter-specialist for mobile issues
4. > Use deployment-specialist for infrastructure issues
```

---

## Agent Files

All agent files are in `.claude/agents/`:

| File | Agent |
|------|-------|
| `deep-reflector.md` | Session analysis and learning capture |
| `deployment-specialist.md` | Docker/Kubernetes deployment |
| `documentation-validator.md` | Documentation validation |
| `flutter-specialist.md` | Flutter mobile/desktop apps |
| `framework-advisor.md` | Framework selection guidance |
| `gh-manager.md` | GitHub project management |
| `gold-standards-validator.md` | Compliance checking |
| `intermediate-reviewer.md` | Checkpoint reviews |
| `requirements-analyst.md` | Requirements breakdown |
| `security-auditor.md` | Security analysis |
| `todo-manager.md` | Task management |
| `ui-engineer.md` | UI/UX specialist |
| `ultrathink-analyst.md` | Deep failure analysis |
