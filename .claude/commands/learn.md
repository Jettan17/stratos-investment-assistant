# /learn - Extract Reusable Patterns

Analyze the current session and extract valuable learnings using smart auto-detection.

## Usage

```bash
/learn                                    # Auto-detect mode from context
/learn This auth caching approach works   # Explicit pattern capture
/learn I kept forgetting to run tests     # Explicit reflection capture
/learn The 401 was because of token scope # Explicit eureka capture
```

---

## Smart Auto-Detection

`/learn` automatically detects what you need based on conversation context:

### Detection Logic

| Mode | Triggers | Output |
|------|----------|--------|
| **Pattern** | "works for", "approach", "technique", "how to" | Command file |
| **Reflection** | "improve", "mistake", "forgot", "next time" | CLAUDE.md suggestions |
| **Eureka** | "figured out", "realized", "turns out", "finally" | Quick insight file |

### Pattern Mode (Default)

When you describe a reusable technique or approach.

**Examples:**
- "I found a way to handle cyclic workflow state..."
- "This pattern works for caching API tokens..."
- "Here's how to debug Kailash connection errors..."

**Output:** Creates command file in `.claude/commands/learned/`

### Reflection Mode

When session analysis identifies improvements for future work.

**Examples:**
- "What did I learn from this session?"
- "I kept making the same mistake..."
- "How can I improve my workflow?"

**Output:** Suggestions for CLAUDE.md or instructions.md updates

### Eureka Mode

When capturing a single breakthrough insight.

**Examples:**
- "I finally figured out why auth was failing..."
- "The reason was the token scope was wrong..."
- "So THAT'S why the tests were flaky..."

**Output:** Quick insight saved to `.claude/commands/learned/insights/`

---

## What to Extract

### Pattern Extraction
1. **Error Resolution Patterns**
   - What error occurred?
   - What was the root cause?
   - What fixed it?
   - Is this reusable for similar errors?

2. **Debugging Techniques**
   - Non-obvious debugging steps
   - Tool combinations that worked
   - Diagnostic patterns

3. **Workarounds**
   - Library quirks
   - API limitations
   - Version-specific fixes

4. **Project-Specific Patterns**
   - Codebase conventions discovered
   - Architecture decisions made
   - Integration patterns

### Reflection Extraction
- Workflow improvements
- Common mistakes to avoid
- Tool configuration suggestions
- Documentation gaps identified

### Eureka Extraction
- Root cause discoveries
- Counter-intuitive behaviors
- Hidden dependencies
- Configuration gotchas

---

## Output Formats

### Pattern Output (`.claude/commands/learned/[pattern-name].md`)

```markdown
---
description: [Short description for autocomplete]
---

# [Descriptive Pattern Name]

**Extracted:** [Date]
**Context:** [Brief description of when this applies]

## Problem
[What problem this solves - be specific]

## Solution
[The pattern/technique/workaround]

## Example
[Code example if applicable]

## When to Use
[Trigger conditions - what should activate this skill]
```

### Reflection Output (Suggestions)

```markdown
## Proposed Addition to CLAUDE.md

### Section: [e.g., Development Workflow Phases]

Add the following:

> [New instruction or guideline]

### Reasoning
[Why this should be added based on session analysis]
```

### Eureka Output (`.claude/commands/learned/insights/insight-[date]-[topic].md`)

```markdown
---
description: [Quick insight description]
---

# Insight: [Title]

**Context:** [What was being investigated]
**Discovery:** [The breakthrough insight]
**Implication:** [How this changes approach going forward]
**Captured:** [Date]
```

---

## Process

1. Run `/learn` (or provide explicit context)
2. Auto-detect mode from conversation context
3. Extract the most valuable insight
4. Format according to mode template
5. Ask user to confirm before saving
6. Save to appropriate location

---

## Directory Structure

```
.claude/commands/learned/
├── patterns/
│   ├── debugging-kailash-connections.md
│   └── handling-cyclic-workflows.md
├── insights/
│   ├── insight-2024-01-15-token-caching.md
│   └── insight-2024-01-20-node-initialization.md
└── README.md  # Index of all learned patterns
```

---

## Notes

- Don't extract trivial fixes (typos, simple syntax errors)
- Don't extract one-time issues (specific API outages, etc.)
- Focus on patterns that will save time in future sessions
- Keep commands focused - one pattern per command
- Check for existing patterns before creating duplicates

---

## Agent Escalation

This command automatically escalates to specialized agents when:

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Any learning extraction | **deep-reflector** | Comprehensive analysis and formatting |
| Pattern validation | **documentation-validator** | Validate pattern format and accuracy |

### Escalation Triggers
- **deep-reflector**: Always invoked to analyze session context and format output
- **documentation-validator**: Use to ensure learned patterns are accurate and well-formatted
