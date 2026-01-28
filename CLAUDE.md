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
5. **Always reference Project Settings and Must Do** when running commands

**If Project Settings ARE filled**, acknowledge them and proceed with the user's request.

## Quick Start

### Plugin Status: INSTALLED ✓
The everything-claude-code plugin is installed at `~/.claude/plugins/everything-claude-code/`

### Available Slash Commands (14 total)
| Command | Description |
|---------|-------------|
| `/sdk` | Initialize new project or update SDK files |
| `/tdd` | Test-driven development (unit, integration, E2E, coverage) |
| `/design` | Implementation planning |
| `/code-review` | Quality review + dead code cleanup (local, PR, issue fix modes) |
| `/build-fix` | Build error resolution |
| `/verify` | Verification loop execution |
| `/checkpoint` | Verification state saving |
| `/deploy` | Deploy to Docker, K8s, Vercel, Railway, Fly.io |
| `/setup-pm` | Package manager configuration |
| `/update-docs` | Sync all documentation (README, codemaps, API) |
| `/learn` | Pattern extraction with auto-detection |
| `/ai-eval` | AI feature evaluation harness |
| `/orchestrate` | Multi-agent orchestration |
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
1. Run /design to design implementation approach
2. > Use ultrathink-analyst for complex requirements
3. > Use todo-manager to create task breakdown
```

### Phase 2: Implementation (TDD)
```
For each component:
1. Run /tdd to write tests first (includes no-stubs check)
2. Implement to pass tests
3. Run /tdd e2e for end-to-end tests
4. > Use intermediate-reviewer for progress review
```

### Phase 3: Testing & Quality
```
1. Run /tdd --full for comprehensive testing
2. Run /tdd coverage to check coverage gaps
3. Run /verify for full validation
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
8. **Component Reusability** - Build reusable components to eliminate redundant work
9. **Responsive-First Design** - Build responsive patterns from the start
10. **Dark Mode Built-In** - Support dark mode in all components from day 1

### Lessons Learned
1. **Documentation Early** - Write guides during/after implementation
2. **Pattern Consistency** - Follow same structure across examples
3. **Incremental Validation** - Verify tests pass immediately
4. **Deprecation Fixes** - Address all deprecations immediately
5. **Responsive Testing** - Test at all breakpoints for every feature
6. **Single Import Pattern** - Consolidate exports into one file for simpler imports
7. **Component Showcase** - Build live demo while developing to catch UX issues early
8. **Real Device Testing** - Test on actual devices, not just simulators

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

### Destructive Operations (rm, delete, etc.)
**Defer all file/directory deletions until the END of the task.**

- Complete ALL other work in the user's request first (writes, edits, builds, tests)
- Only attempt deletions as the final step, after everything else succeeds
- This prevents getting stuck waiting for permission mid-task
- If deletion fails or is blocked, report it and move on - the main work is already done

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

| Command | Category | Description |
|---------|----------|-------------|
| `/sdk` | Operations | Initialize project or update SDK |
| `/tdd` | Core | Test-driven development (unit, integration, E2E, coverage) |
| `/design` | Core | Implementation planning |
| `/code-review` | Core | Quality review + dead code cleanup |
| `/build-fix` | Core | Build error resolution |
| `/verify` | Quality | Verification loop |
| `/checkpoint` | Quality | Save verification state |
| `/deploy` | Operations | Deploy to Docker, K8s, Vercel, Railway, etc. |
| `/setup-pm` | Operations | Package manager setup |
| `/update-docs` | Documentation | Sync all docs (README, codemaps, API) |
| `/learn` | Documentation | Pattern extraction (auto-detect) |
| `/ai-eval` | Advanced | AI feature evaluation harness |
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
/tdd              # TDD workflow (unit, integration, E2E, coverage)
/tdd e2e          # E2E tests with Playwright
/tdd coverage     # Analyze and fill coverage gaps
/tdd --full       # All tests + coverage + no-stubs check
/design           # Plan implementation
/code-review      # Review code quality
/orchestrate      # Multi-agent orchestration

# Quality
/verify           # Run verification loop
/verify --full    # Full verification with E2E
/checkpoint       # Save verification state

# Deployment & Operations
/deploy           # Auto-detect best platform
/deploy vercel    # Deploy to Vercel
/deploy railway   # Deploy to Railway
/setup-pm         # Configure package manager

# Maintenance
/build-fix        # Fix build errors
/update-docs      # Sync all documentation

# Learning & AI
/learn            # Extract patterns from session
/ai-eval          # AI feature evaluation
```

---

## Environment Setup

### Must Do Before Starting
1. Set up isolated environments (venv for Python, node for Node.js)
2. Enable turbo-all and SafeToAutoRun for common commands
3. Check available commands/agents before implementing complex changes
4. Document all work in markdown files as you progress

---

## When Stuck or Blocked

**If you encounter an issue you cannot resolve:**

1. **Ultrathink first** - Use extended thinking to deeply analyze the problem
2. **Search the web** - Use WebSearch to find documentation, Stack Overflow, GitHub issues, or blog posts related to the error/issue
3. **Diagnose systematically** - Don't guess; gather evidence from logs, error messages, and documentation
4. **Try multiple angles** - If one approach fails, search for alternative solutions before asking the user

**Never spin on the same approach repeatedly.** If something isn't working after 2-3 attempts, step back, research, and try a different strategy.
