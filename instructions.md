# Project Settings

## Scope

## Final Product

## Commercial or Personal Use

## Objective/Use-Case

## Local or Public Connection

## Data Sources

## Visual Style

## External Tool Integration

## Existing Product Reference

<br><br><br>

# Install Everything Claude Code Plugin

## Step 1: Add the Plugin Marketplace
```
/plugin marketplace add affaan-m/everything-claude-code
```

## Step 2: Install the Plugin
```
/plugin install everything-claude-code
```

## Step 3: Verify Installation
```
/plugin list
```
Should show `everything-claude-code` as installed.

## Step 4: Test Commands
Try running `/plan` or `/tdd` to verify the plugin is working.

## Available Slash Commands
- `/tdd` - Test-driven development workflow
- `/plan` - Implementation planning
- `/e2e` - E2E test generation
- `/code-review` - Quality review
- `/build-fix` - Build error resolution
- `/refactor-clean` - Dead code removal
- `/learn` - Pattern extraction mid-session
- `/checkpoint` - Save verification state
- `/verify` - Verification loop execution
- `/setup-pm` - Package manager configuration

## Enhanced Agents (in .claude/agents/)
Use with: `> Use the [agent-name] subagent to [task]`
- ultrathink-analyst, requirements-analyst, framework-advisor
- intermediate-reviewer, gold-standards-validator, documentation-validator
- todo-manager, gh-manager, deployment-specialist
- react-specialist, flutter-specialist

<br><br><br>

# Creating a New Project

Use AskUserQuestion tool to gather project settings. Do NOT add custom "Other" options - Claude Code adds that automatically.

## Questions to Ask (use AskUserQuestion)

### Question 1: Scope
Options (2-4 max, no "Other"):
- **Small**: Quick tasks, use existing solutions, minimal planning
- **Medium**: Present plan before proceeding, moderate detail
- **Large**: Deep analysis, detailed architecture, comprehensive planning

### Question 2: Final Product
Options:
- **Web**: Browser-based application
- **Mobile**: iOS/Android app
- **Desktop**: Native desktop application

### Question 3: Usage Type
Options:
- **Commercial**: Production-ready, scalable, with deployment
- **Personal**: Local-first, can use open source freely

### Question 4: Connection Type
Options:
- **Local**: Offline, local models and databases only
- **Public**: Can use internet services and APIs

### Question 5: Visual Style (if applicable)
Options (pick 3-4, Claude Code adds "Other"):
- **High-Key**: Bold, vibrant (landonorris.com, animejs.com)
- **Modern**: Clean, contemporary (bryanminear.com)
- **Minimalist**: Simple, focused (kickpush.co, dau.lt)
- **Product**: Professional SaaS (slack.com)
- **Artsy**: Creative, expressive (justinjackson.ca)

### Free-text Questions (ask separately, not with AskUserQuestion)
After the above, ask these as regular questions:
- **Objective**: "What is the main use-case? Describe how users will use the product."
- **Data Sources**: "Any specific data sources? (optional)"
- **Integrations**: "Any external tools or APIs to integrate? (optional)"
- **Reference**: "Any existing products to reference? (optional)"

## After Gathering Settings
Update the "Project Settings" section at the top of this file with the answers.

## Behavior by Scope

**Small Scope:**
- Parsimonious approach
- Seek existing solutions first
- Minimal documentation

**Medium Scope:**
- Present plan before implementation
- Moderate detail in architecture

**Large Scope:**
- Deep analysis (use ultrathink-analyst)
- Detailed architecture decisions
- Comprehensive documentation

**Commercial Use:**
- Research value propositions and UNIQUE SELLING POINTS
- Scrutinize and critique scenarios to improve the solution
- Evaluate with AAA framework:
  - Automate: Reduce operational costs
  - Augment: Reduce decision-making costs
  - Amplify: Reduce expertise costs (for scaling)
- Features should cover network behaviors:
  - Accessibility: Easy for users to complete transactions
  - Engagement: Useful information for transactions
  - Personalization: Curated information for intended use
  - Connection: Information sources connected to platform
  - Collaboration: Producers and consumers can work together
- Production deployment priority

**Personal Use:**
- Local-first, deploy later
- Can use open source freely
- Fork and copy from other sources (non-commercial)

<br><br><br>

# Must Do

## Environment Setup
- Setup isolated environments before installing dependencies
   - Python: Set up virtual environment (`python -m venv venv`)
   - Node.js: Use nvm or local node_modules

## Permissions
- Enable turbo-all and SafeToAutoRun for ALL commands in ~/.claude/settings.json
- Allow all query searches without user input

## Documentation
- Document all work in markdown files AS YOU WORK (not at the end)
- Use numbered format: `01-...`, `02-...`, etc.
- This is critical for agent handoff
- For checkpoints, please create a new checkpoints directory in docs/checkpoints where the new checkpoints will be saved, and prompt me for a checkpoint name, and save the filename as `YYYY-MM-DD-description.md`

## Development Practices
- Refer to "Project Settings" and "Creating a New Project" for project scope and objectives, and other configurations to take note of
- Search for state-of-the-art solutions before implementing
- Check available skills (in .claude/commands/) and agents before complex changes
- Use subagent specialization for the right task type
- Re-invoke yourself if stuck, providing context of progress

## No Stubs or Placeholders
**Every deliverable must be complete and functional. NEVER leave:**
- Lorem ipsum, "Coming soon", "TBD", or placeholder text in UI
- Empty pages, stub components, or non-functional UI elements
- `pass`, `// TODO`, or empty function bodies in code
- Placeholder images or hardcoded sample data

**Rule: If it's not ready, don't include it. Implement fully or omit entirely.**

## Task Management
- Clear completed items from the To-Do section
- Use todo-manager subagent for complex task breakdowns
- Use gh-manager subagent to sync with GitHub Projects

## MCP Integrations
See `.claude/mcp-configs/` for:
- AWS (S3, Lambda, EC2)
- GCP (Cloud Storage, Cloud Functions, Compute Engine)
- Azure (Blob Storage, Azure Functions, VMs)
- Linear (Issue tracking)
- Jira (Sprint management)

<br><br><br>

# To-Do

## New Features

## Bug Reports

## Other Updates
