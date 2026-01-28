---
description: Sync all documentation - README, codemaps, API docs, and project guides.
ecc_base_version: "5230892"
last_synced: "2026-01-27"
customizations: "Consolidated: update-codemaps, update-readme into single command"
---

# /update-docs - Update Documentation

Comprehensive documentation sync command covering README, codemaps, and project guides.

## Usage

```bash
/update-docs                # Sync all documentation
/update-docs --readme       # Generate/update README only
/update-docs --codemaps     # Update architecture codemaps only
/update-docs --api          # Update API documentation only
/update-docs --all          # Full documentation suite
/update-docs preview        # Preview changes without writing
```

---

## What This Command Does

### Default Mode (All Documentation)

1. **Sync from source-of-truth** (package.json, .env.example)
2. **Update README.md** with project info
3. **Update codemaps** with architecture diagrams
4. **Generate contribution guide** (docs/CONTRIB.md)
5. **Generate runbook** (docs/RUNBOOK.md)
6. **Identify obsolete docs** (90+ days old)

---

## Mode: `--readme`

Analyze codebase and generate/update README.md.

### 1. Detect Project Type & Stack

| File | Stack Detection |
|------|-----------------|
| `package.json` | Node.js, React/Next.js/Vue |
| `requirements.txt` / `pyproject.toml` | Python |
| `pubspec.yaml` | Flutter/Dart |
| `go.mod` | Go |
| `Cargo.toml` | Rust |

### 2. Analyze Project Structure

Scan for:
- Source directories (`src/`, `lib/`, `app/`)
- Entry points (`index.ts`, `main.py`)
- API routes (`app/api/`, `routes/`)
- Components and services
- Configuration files
- Tests

### 3. Generate README Sections

```markdown
# {Project Name}
{Description}

## Tech Stack
{Badges}

## Prerequisites
- Node.js >= {version}
- {Package manager}

## Getting Started
### Installation
{install command}

### Environment Setup
| Variable | Description | Required |

### Development
{dev command}

## Available Scripts
| Script | Description |

## Project Structure
{directory tree}

## API Reference
{endpoints if detected}

## Deployment
{Docker/K8s if detected}
```

### 4. Preserve Custom Sections

Mark sections to keep unchanged:
```markdown
<!-- keep -->
## Custom Section
This won't be overwritten
<!-- /keep -->
```

---

## Mode: `--codemaps`

Analyze codebase structure and update architecture documentation.

### Generated Files

| File | Content |
|------|---------|
| `codemaps/architecture.md` | Overall architecture |
| `codemaps/backend.md` | Backend structure |
| `codemaps/frontend.md` | Frontend structure |
| `codemaps/data.md` | Data models and schemas |

### Process

1. Scan all source files for imports/exports/dependencies
2. Generate token-lean architecture diagrams
3. Calculate diff percentage from previous version
4. If changes > 30%, request user approval
5. Add freshness timestamp to each codemap
6. Save diff report to `.reports/codemap-diff.txt`

---

## Mode: `--api`

Update API documentation from source.

### Sources
- OpenAPI/Swagger specs
- Route handlers (`app/api/`, `routes/`)
- JSDoc/TSDoc comments
- Python docstrings

### Output
- `docs/API.md` - Full API reference
- Endpoint tables with methods, params, responses

---

## Additional Generated Docs

### docs/CONTRIB.md
- Development workflow
- Available scripts
- Environment setup
- Testing procedures

### docs/RUNBOOK.md
- Deployment procedures
- Monitoring and alerts
- Common issues and fixes
- Rollback procedures

---

## Arguments

| Argument | Description |
|----------|-------------|
| `--readme` | Update README.md only |
| `--codemaps` | Update architecture codemaps only |
| `--api` | Update API documentation only |
| `--all` | Full documentation suite |
| `preview` | Show changes without writing |
| `force` | Write without confirmation |
| `section <name>` | Update specific section only |

---

## Examples

```bash
# Sync all documentation
/update-docs

# Preview README changes
/update-docs --readme preview

# Update only codemaps
/update-docs --codemaps

# Update README scripts section only
/update-docs --readme section scripts

# Force update without confirmation
/update-docs --all force
```

---

## Source of Truth

Documentation is synced from these authoritative sources:

| Source | Used For |
|--------|----------|
| `package.json` | Scripts, dependencies, project info |
| `.env.example` | Environment variables |
| `tsconfig.json` | Build configuration |
| `Dockerfile` | Deployment info |
| Route files | API documentation |
| Source code | Codemaps, architecture |

---

## Obsolete Doc Detection

Identifies documentation not modified in 90+ days:
- Lists files for manual review
- Suggests removal or update
- Shows last modified date

---

## Agent Escalation

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Code examples need testing | **documentation-validator** | Test all code examples |
| Cross-reference validation | **documentation-validator** | Ensure docs match implementation |
| Architecture analysis | **architect** | Deep architectural understanding |
| Complex project structure | **architect** | Monorepos, microservices |
| API documentation | **documentation-validator** | Validate API docs accuracy |

---

## Related Commands

- `/design` - Plan features (generates initial docs)
- `/code-review` - Review changes (may need doc updates)
- `/learn` - Extract patterns (updates learnings)