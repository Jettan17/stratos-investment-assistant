# JetFlux SDK

A Claude Code development environment using **everything-claude-code (ECC)** for structured development workflows.

## Features

- **18 Specialized Agents** - 9 core + 9 enhanced agents
- **18 Slash Commands** - Quick access to development workflows
- **6-Phase Development Workflow** - Structured approach from planning to deployment

## Quick Start

### 1. Install Plugin (if not installed)
```bash
/plugin marketplace add affaan-m/everything-claude-code
/plugin install everything-claude-code
/plugin list  # verify installation
```

### 2. Project Initialization
On first session, Claude prompts for project settings (scope, product type, objective). These are saved to `instructions.md`.

### 3. Running Commands
```
instructions.md (context) + /plan (command) → context-aware planning
```

## Slash Commands (18 total)

| Category | Commands |
|----------|----------|
| **Core** | `/tdd`, `/plan`, `/code-review`, `/e2e`, `/build-fix`, `/refactor-clean` |
| **Quality** | `/verify`, `/checkpoint`, `/test-coverage`, `/no-stubs`, `/real-testing` |
| **Operations** | `/deploy`, `/setup-pm` |
| **Documentation** | `/update-docs`, `/update-codemaps`, `/learn` |
| **Advanced** | `/eval`, `/orchestrate` |

## Complete Development Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 0: ORCHESTRATION (for complex tasks only)            │
├─────────────────────────────────────────────────────────────┤
│  /orchestrate  → Use when task touches 3+ areas or needs    │
│                  multiple agents working together           │
│                  Example: "Add authentication" (frontend,   │
│                  backend, database, tests all at once)      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: SETUP & PLANNING                                  │
├─────────────────────────────────────────────────────────────┤
│  /setup-pm        → Configure package manager (npm/pip)     │
│  /plan            → Design implementation approach          │
│  /update-codemaps → Document initial structure              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: IMPLEMENTATION (repeat for each feature)          │
├─────────────────────────────────────────────────────────────┤
│  /tdd             → Write tests FIRST, then implement       │
│  /no-stubs        → Verify no placeholder content           │
│  /checkpoint      → Save progress after milestone           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: TESTING & QUALITY                                 │
├─────────────────────────────────────────────────────────────┤
│  /e2e             → Generate end-to-end tests               │
│  /real-testing    → Verify tests use real services          │
│  /test-coverage   → Check coverage gaps                     │
│  /eval            → Test AI features (if applicable)        │
│  /verify          → Run full validation                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 4: REVIEW & CLEANUP                                  │
├─────────────────────────────────────────────────────────────┤
│  /code-review     → Quality and security review             │
│  /refactor-clean  → Remove dead code                        │
│  /build-fix       → Fix any build errors                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 5: DOCUMENTATION                                     │
├─────────────────────────────────────────────────────────────┤
│  /update-docs     → Sync documentation with code            │
│  /update-codemaps → Update architecture diagrams            │
│  /learn           → Extract patterns from session           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 6: DEPLOYMENT                                        │
├─────────────────────────────────────────────────────────────┤
│  /deploy          → Docker/Kubernetes setup                 │
│  /verify          → Final validation                        │
└─────────────────────────────────────────────────────────────┘
```

## Quick Reference by Situation

| When | Use |
|------|-----|
| Starting a project | `/setup-pm` → `/plan` |
| Adding a feature | `/plan` → `/tdd` → `/no-stubs` → `/checkpoint` |
| Complex cross-cutting work | `/orchestrate` (coordinates multiple phases) |
| Build broken | `/build-fix` |
| Before committing | `/code-review` → `/verify` |
| After major changes | `/update-codemaps` → `/update-docs` |
| Testing AI features | `/eval` |
| Cleaning up | `/refactor-clean` |
| Deploying | `/deploy` |

## Minimum Viable Workflow

For quick tasks:
```
/plan → /tdd → /verify → /code-review
```

## Directory Structure

```
jetflux-sdk/
├── .claude/
│   ├── agents/           # 9 enhanced agents
│   ├── skills/           # 18 workflow skills
│   │   └── 00-development-workflows/
│   ├── guides/           # Specialized guides
│   └── mcp-configs/      # MCP server configurations
├── CLAUDE.md             # Master directives
├── instructions.md       # Project setup template
└── README.md
```

## Available Agents

### Core Agents
Planner, Architect, TDD Guide, Code Reviewer, Security Reviewer, Build Error Resolver, E2E Runner, Refactor Cleaner, Doc Updater

### Enhanced Agents
| Agent | Purpose |
|-------|---------|
| ultrathink-analyst | Deep failure analysis |
| requirements-analyst | Requirements breakdown |
| framework-advisor | Tech stack decisions |
| intermediate-reviewer | Progress validation |
| todo-manager | Task management |
| gh-manager | GitHub Projects integration |
| deployment-specialist | Docker/K8s deployment |
| react-specialist | React 19/Next.js 15 |
| flutter-specialist | Flutter mobile |

## Documentation

- [CLAUDE.md](CLAUDE.md) - Master directives and all commands
- [instructions.md](instructions.md) - Project setup template
- [.claude/skills/00-development-workflows/](.claude/skills/00-development-workflows/) - All 18 skill files

## License

MIT
