# Claude Code Commands Directory

This directory contains example slash commands and documentation for creating custom commands in Claude Code.

## What are Slash Commands?

Slash commands are custom automation workflows that you can invoke in Claude Code by typing `/command-name`. They help automate repetitive tasks and create reusable workflows.

## Files in this Directory

- `creating-slash-commands.md` - Comprehensive guide on how to create your own slash commands

## Quick Example

To create a simple command, add a markdown file here:

```bash
echo 'Deploy to production: $ARGUMENTS' > deploy.md
```

Now you can use `/deploy production` in Claude Code!

## Command Format

Basic command structure:
```markdown
# Command Title
Description of what this command does

## Steps
1. First action
2. Second action

## Your task
$ARGUMENTS
```

## Learn More

Read the full guide: [creating-slash-commands.md](creating-slash-commands.md)