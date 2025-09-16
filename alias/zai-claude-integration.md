# Z.AI + Claude Code Integration Guide

This directory contains aliases and configurations for integrating Z.AI with the Claude Code harness, enabling enhanced AI-powered development workflows.

## Quick Setup

### Z.AI Claude Alias

Add this alias to your shell configuration (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
alias zz='export ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic; export ANTHROPIC_AUTH_TOKEN=key; claude --dangerously-skip-permissions'
```

### What This Does

1. **Sets Z.AI API Endpoint**: Routes Claude requests through Z.AI's enhanced API
2. **Authentication**: Uses your Z.AI API key for authentication
3. **Permissions Override**: Skips Claude's permission checks for streamlined development
4. **Instant Access**: Provides quick `zz` command for Z.AI-powered Claude sessions
