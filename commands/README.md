# Claude Code Slash Commands

This directory contains slash commands organized by category for easy discovery and management.

## Directory Structure

```
commands/
├── python/                   # Python development commands
├── web/                      # Web development commands
├── devops/                   # DevOps and infrastructure commands
├── context engineering/      # Context engineering workflow (Research-Plan-Execute)
├── quality-assurance/        # QA and testing commands
├── integration/              # Third-party integration commands
├── utilities/                # Utility and productivity commands
├── COMMANDS.md               # Complete guide to creating slash commands
└── README.md                 # This file
```

## Categories

### [python/](python/)
Python-specific commands for API development, testing, and code generation.

### [web/](web/)
Web development commands for React components, PWA conversion, and frontend tasks.

### [devops/](devops/)
DevOps commands for Docker optimization, Kubernetes migration, and infrastructure.

### [context engineering/](context%20engineering/)
The Research-Plan-Execute workflow for systematic codebase analysis and implementation:
- `research.md` - Conduct comprehensive research across the codebase
- `plan.md` - Generate executable implementation plans from research
- `execute.md` - Execute implementation plans with quality gates

### [quality-assurance/](quality-assurance/)
QA commands including Fagan inspection for formal code review.

### [integration/](integration/)
Third-party integrations:
- `linear-continue-debugging.md` - Linear issue debugging
- `linear-continue-work.md` - Linear issue workflow continuation
- `coderabbitai.md` - GitHub issue analysis

### [utilities/](utilities/)
Utility commands:
- `context-compact.md` - Compress context when approaching token limits
- `phase-planner.md` - Strategic project planning
- `smart-git.md` - Git workflow automation

## Creating New Commands

See [COMMANDS.md](COMMANDS.md) for a comprehensive guide to creating slash commands including:
- Minimum requirements
- Frontmatter fields reference
- Best practices and examples
- Testing and validation

## Validation

Run the validator to check command syntax:
```bash
python validate_commands.py commands/
```
