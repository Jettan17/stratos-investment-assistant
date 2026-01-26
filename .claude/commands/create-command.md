---
description: Create new Claude Code custom commands interactively.
---

# Create Command

Interactive wizard to create new slash commands.

## Usage

`/create-command [name]`

## What This Does

1. Prompt for command name (if not provided)
2. Ask for description (short, for autocomplete)
3. Ask for functionality (what the command should do)
4. Generate command markdown file
5. Save to `.claude/commands/[name].md`

## Example

```
/create-command my-workflow

> Name: my-workflow
> Description: Run my custom build workflow
> What should it do: Run lint, test, build in sequence, stop on first failure

Creating .claude/commands/my-workflow.md... Done!

New command /my-workflow is now available.
```

## Generated File Format

The wizard generates a properly formatted command file:

```markdown
---
description: [Your description here]
---

# [Command Name]

[Your functionality description]

## What This Does

[Detailed steps based on your input]

## Usage

`/[command-name] [arguments if any]`
```

## Tips

- Keep descriptions short (shown in autocomplete)
- Be specific about what the command should do
- Include any arguments the command should accept
- Consider adding agent escalation if complex

## When to Use

- Creating project-specific workflows
- Automating repetitive tasks
- Building team-specific commands
- Prototyping new command ideas
