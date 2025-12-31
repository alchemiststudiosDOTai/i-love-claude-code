# Claude Code Agents

This directory contains specialized AI agents organized by category.

## Directory Structure

```
agents/
├── analysis/                # Code analysis and investigation agents
├── development/            # Code development and refactoring agents
├── documentation/          # Documentation generation agents
├── research/               # Research and information gathering agents
├── security/               # Security analysis agents
├── performance/            # Performance optimization agents
├── README.md               # This file
└── guide.md                # Comprehensive subagent guide
```

## Categories

### [analysis/](analysis/)
Agents for analyzing and understanding code:
- `codebase-locator.md` - Find WHERE code lives in a codebase
- `codebase-analyzer.md` - Understand HOW code works
- `code-synthesis-analyzer.md` - Analyze recently implemented code changes

### [development/](development/)
Agents for code development tasks:
- `tdd-python.md` - Test-Driven Development for Python
- `code-clarity-refactorer.md` - Apply refactoring rules for clarity
- `bug-issue-creator.md` - Analyze bugs and create GitHub issues

### [documentation/](documentation/)
Agents for documentation tasks:
- `git-diff-documentation-agent.md` - Document changes from git diffs
- `tech-docs-maintainer.md` - Maintain technical documentation
- `technical-docs-orchestrator.md` - Multi-stage documentation creation
- `prompt-engineer.md` - Optimize and improve prompts

### [research/](research/)
Agents for research tasks:
- `web-docs-researcher.md` - Search web for official documentation
- `multi-agent-synthesis-orchestrator.md` - Orchestrate multiple research agents

### [security/](security/)
Agents for security analysis:
- `security-orchestrator.md` - Comprehensive security investigations

### [performance/](performance/)
Agents for performance optimization:
- `memory-profiler.md` - Identify memory leaks and optimization opportunities

## Using Agents

See [guide.md](guide.md) for detailed information about creating, configuring, and using subagents effectively.

## Benefits of Subagents

1. **Clean Context Isolation** - Each subagent starts with a fresh context window
2. **Parallel Processing** - Multiple subagents can work simultaneously
3. **Specialized Expertise** - Agents are optimized for specific tasks
4. **Consistent Results** - Predictable behavior across sessions
