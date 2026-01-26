# Claude Code SDK - Master Directives

This project uses the **everything-claude-code (ECC)** plugin for structured development workflows.

---

## ⚠️ CRITICAL: Project Initialization Check

**At the start of EVERY session, you MUST:**

1. **Read `instructions.md`** to load project context
2. **Check if Project Settings are empty** (Scope, Final Product, Objective are blank)
3. **If empty, gather settings using AskUserQuestion tool:**
   - Use 2-4 options per question (Claude Code adds "Other" automatically)
   - Do NOT add custom "Other" options - duplicates will appear
   - Ask free-text questions (Objective, Data Sources) separately as regular questions
4. **Update `instructions.md`** with their responses
5. **Always reference Project Settings** when running commands

**If Project Settings ARE filled**, acknowledge them and proceed with the user's request.

## Quick Start

### Plugin Status: INSTALLED ✓
The everything-claude-code plugin is installed at `~/.claude/plugins/everything-claude-code/`

### Available Slash Commands (19 total)
| Command | Description |
|---------|-------------|
| `/tdd` | Test-driven development workflow |
| `/plan` | Implementation planning |
| `/e2e` | E2E test generation |
| `/code-review` | Quality review (local, PR, issue fix modes) |
| `/build-fix` | Build error resolution |
| `/refactor-clean` | Dead code removal |
| `/learn` | Pattern extraction with auto-detection |
| `/checkpoint` | Verification state saving |
| `/verify` | Verification loop execution |
| `/setup-pm` | Package manager configuration |
| `/eval` | Evaluation harness |
| `/orchestrate` | Multi-agent orchestration |
| `/test-coverage` | Test coverage analysis |
| `/update-codemaps` | Update code maps |
| `/update-docs` | Update documentation |
| `/no-stubs` | Enforce no placeholder content |
| `/real-testing` | Real infrastructure testing (NO MOCKING) |
| `/deploy` | Docker/Kubernetes deployment |
| `/create-command` | Create new custom commands interactively |

---

## Specialized Subagents

### Core Agents
| Agent | Purpose |
|-------|---------|
| **Planner** | Feature implementation planning |
| **Architect** | System design decisions |
| **TDD Guide** | Test-driven development methodology |
| **Code Reviewer** | Quality and security assessment |
| **Build Error Resolver** | Construction failure fixing |
| **E2E Runner** | Playwright testing automation |
| **Refactor Cleaner** | Dead code elimination |
| **Doc Updater** | Documentation synchronization |

### Enhanced Agents (13 total)
| Agent | Purpose | When to Use |
|-------|---------|-------------|
| **ultrathink-analyst** | Deep failure analysis | Complex features, systemic issues |
| **requirements-analyst** | Requirements breakdown, ADR creation | Architecture decisions |
| **framework-advisor** | Technology selection guidance | Tech stack decisions |
| **intermediate-reviewer** | Checkpoint reviews | Progress validation |
| **todo-manager** | Task management | Development task lists |
| **gh-manager** | GitHub Projects integration | Sprint management |
| **deployment-specialist** | Docker/Kubernetes deployment | Production deployments |
| **ui-engineer** | UI/UX specialist (React 19, Next.js 15, accessibility) | Frontend implementation |
| **flutter-specialist** | Flutter mobile patterns | Mobile/desktop apps |
| **security-auditor** | OWASP Top 10, vulnerability scanning | Security reviews |
| **deep-reflector** | Session analysis, learning capture | Pattern extraction |
| **gold-standards-validator** | Code compliance enforcement | Standards validation |
| **documentation-validator** | Documentation accuracy checking | Doc validation |

---

## Development Workflow Phases

### Phase 1: Analysis & Planning
```
1. Run /plan to design implementation approach
2. > Use ultrathink-analyst for complex requirements
3. > Use todo-manager to create task breakdown
```

### Phase 2: Implementation (TDD)
```
For each component:
1. Run /tdd to write tests first
2. Implement to pass tests
3. Run /no-stubs to verify completeness
4. > Use intermediate-reviewer for progress review
```

### Phase 3: Testing & Quality
```
1. Run /e2e for end-to-end tests
2. Run /real-testing to verify integration tests use real services
3. Run /test-coverage to check coverage
4. Run /verify for full validation
```

### Phase 4: Deployment
```
1. Run /deploy for Docker/Kubernetes setup
2. > Use deployment-specialist for production configuration
```

### Phase 5: Release
```
1. Run /code-review for final quality check
2. Run /update-docs to sync documentation
3. Create PR with proper documentation
```

---

## Success Factors

### What Works Well
1. **Systematic Task Completion** - Finish each task completely before moving on
2. **Test-First Development** - Write tests before implementation
3. **Real Infrastructure Testing** - NO MOCKING policy for integration tests
4. **Evidence-Based Tracking** - Use file:line references for clear audit trails
5. **Comprehensive Documentation** - Document as you go, not at the end
6. **Subagent Specialization** - Use the right agent for each task type
7. **Design System Foundation** - Create design system BEFORE features

### Lessons Learned
1. **Documentation Early** - Write guides during/after implementation
2. **Pattern Consistency** - Follow same structure across examples
3. **Incremental Validation** - Verify tests pass immediately
4. **Deprecation Fixes** - Address all deprecations immediately
5. **Responsive Testing** - Test at all breakpoints for every feature

---

## Critical Rules

### Code Quality
- Always prefer editing existing files over creating new ones
- Avoid over-engineering - only make directly requested changes
- Don't add features, refactor code, or make "improvements" beyond what was asked
- Remove unused code completely - no backward-compatibility hacks

### No Stubs or Placeholders (CRITICAL)
**NEVER leave incomplete or placeholder content in any deliverable:**

#### Forbidden in UI/Frontend:
- ❌ Lorem ipsum or any placeholder text
- ❌ "Coming soon", "Under construction", "TBD", "TODO" visible to users
- ❌ Empty pages, blank sections, or stub components
- ❌ Placeholder images (gray boxes, "image here" text)
- ❌ Non-functional buttons, links, or form elements
- ❌ Hardcoded sample data that should be dynamic

#### Forbidden in Code:
- ❌ `pass` statements in Python without implementation
- ❌ `// TODO: implement` comments left in production code
- ❌ Empty function bodies or stub methods
- ❌ `throw new Error("Not implemented")` patterns
- ❌ Commented-out code blocks meant for "later"

#### The Rule:
**If a feature isn't ready, don't include it at all.** Either:
1. Implement it fully, OR
2. Don't add it to the codebase

This applies to all scopes (Small/Medium/Large) and all project types.

### Testing
- Write tests before implementation (TDD)
- NO MOCKING in integration tests - use real infrastructure
- Test at all breakpoints (mobile/tablet/desktop)

### Documentation
- Document work in markdown as you go
- Use numbered format: `01-...`, `02-...`, etc.
- Include file:line references for code locations

### Security
- Never commit secrets (.env, credentials)
- Validate at system boundaries (user input, external APIs)
- Check for OWASP top 10 vulnerabilities

---

## MCP Integrations

### Base (from everything-claude-code)
- GitHub
- Supabase
- Vercel
- Railway

### Additional (configured in .claude/mcp-configs/)
- AWS (S3, Lambda, EC2)
- GCP (Cloud Storage, Cloud Functions, Compute Engine)
- Azure (Blob Storage, Azure Functions, VMs)
- Linear (Issue tracking)
- Jira (Sprint management)

See `.claude/mcp-configs/` for setup instructions.

---

## Slash Commands

All commands are in `.claude/commands/`:

| Skill | Category | Description |
|-------|----------|-------------|
| `/tdd` | Core | Test-driven development |
| `/plan` | Core | Implementation planning |
| `/code-review` | Core | Quality review |
| `/e2e` | Core | E2E test generation |
| `/build-fix` | Core | Build error resolution |
| `/refactor-clean` | Core | Dead code removal |
| `/checkpoint` | Quality | Save verification state |
| `/verify` | Quality | Verification loop |
| `/test-coverage` | Quality | Coverage analysis |
| `/no-stubs` | Quality | No placeholder content |
| `/real-testing` | Quality | Real infrastructure testing |
| `/deploy` | Operations | Docker/K8s deployment |
| `/setup-pm` | Operations | Package manager setup |
| `/update-docs` | Documentation | Documentation sync |
| `/update-codemaps` | Documentation | Code map updates |
| `/learn` | Documentation | Pattern extraction (auto-detect) |
| `/eval` | Advanced | Evaluation harness |
| `/orchestrate` | Advanced | Multi-agent coordination |
| `/create-command` | Advanced | Create custom commands |

---

## Project Setup Template

When starting a new project, configure these in `instructions.md`:
- **Scope**: Small / Medium / Large
- **Final Product**: Web / Mobile / Desktop / Open-Ended
- **Commercial or Personal Use**
- **Objective/Use-Case**
- **Data Sources**
- **Visual Style**
- **External Tool Integration**
- **Existing Product Reference**

---

## Quick Commands Reference

```bash
# Development
/tdd              # Start test-driven development
/plan             # Plan implementation
/code-review      # Review code quality
/orchestrate      # Multi-agent orchestration

# Testing & Quality
/e2e              # Generate E2E tests
/verify           # Run verification loop
/test-coverage    # Analyze test coverage
/no-stubs         # Enforce no placeholder content
/real-testing     # Real infrastructure testing
/eval             # Run evaluation harness

# Deployment & Operations
/deploy           # Docker/Kubernetes deployment
/setup-pm         # Configure package manager

# Maintenance
/build-fix        # Fix build errors
/refactor-clean   # Remove dead code
/update-codemaps  # Update code maps
/update-docs      # Update documentation

# Learning & State
/learn            # Extract patterns from session
/checkpoint       # Save verification state
```

---

## Environment Setup

### Must Do Before Starting
1. Set up isolated environments (venv for Python, node for Node.js)
2. Enable turbo-all and SafeToAutoRun for common commands
3. Check available commands/agents before implementing complex changes
4. Document all work in markdown files as you progress
