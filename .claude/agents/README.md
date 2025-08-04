# Agents

This directory contains specialized agents for various tasks. Each agent is defined in a markdown file with metadata and instructions.

## Available Agents

### [bug-issue-creator](bug-issue-creator.md)
- **Description**: Analyzes bugs, gathers comprehensive context, and creates GitHub issues for tracking
- **Color**: Green
- **Use Case**: When you need to document a bug with proper investigation and create a GitHub issue

### [git-diff-documentation-agent](git-diff-documentation-agent.md)
- **Name**: git-diff-documenter
- **Description**: Analyzes git differences and documents changes in the .claude/ directory
- **Color**: Red
- **Use Case**: After code changes are made to capture what was modified and create proper documentation

### [security-orchestrator](security-orchestrator.md)
- **Description**: Conducts comprehensive security investigations including issue discovery, documentation, and quality assurance
- **Color**: Not specified
- **Use Case**: When you need to perform security audits or investigate potential vulnerabilities

### [tdd-python](tdd-python.md)
- **Name**: tdd-python-implementer
- **Description**: Implements Python code following Test-Driven Development (TDD) methodology
- **Color**: Yellow
- **Model**: Opus
- **Use Case**: When you want to implement Python features using TDD principles

### [technical-docs-orchestrator](technical-docs-orchestrator.md)
- **Name**: technical-docs-orchestrator
- **Description**: Creates comprehensive technical documentation by researching, gathering context, and synthesizing information
- **Color**: Blue
- **Model**: Sonnet
- **Use Case**: When you need to create detailed technical documentation through multi-stage research

### [web-docs-researcher](web-docs-researcher.md)
- **Description**: Searches the web for official documentation, latest updates, or authoritative information about technical issues
- **Color**: Yellow
- **Use Case**: When you need to find official documentation or recent information about technologies

### [code-clarity-refactorer](code-clarity-refactorer.md)
- **Name**: code-clarity-refactorer
- **Description**: Analyzes code for clarity improvements and applies 10 key refactoring rules
- **Color**: Purple
- **Tools**: read, write, bash
- **Use Case**: Use PROACTIVELY when code is modified, reviewed, or when clarity improvements are discussed

### [code-synthesis-analyzer](code-synthesis-analyzer.md)
- **Name**: code-synthesis-analyzer
- **Description**: Analyzes recently implemented code changes to identify issues, inconsistencies, or areas needing fixes
- **Color**: Green
- **Model**: Sonnet
- **Use Case**: When you need to verify implementation quality and identify issues that require fixing after code changes

## Usage

Each agent file contains:
- Metadata (name, description, color, model)
- Detailed instructions for the agent
- Examples of when to use the agent
- Commentary explaining the reasoning

To use an agent, reference it by name in your task description and the system will deploy the appropriate agent based on the context and requirements.


## How Separate Context Windows Benefit Developers

**The fundamental advantage** is that each subagent starts with a completely clean slate - its own fresh context window that's independent from your main conversation with Claude Code. This architectural choice provides several crucial benefits:

### 1. **Prevents Context Pollution**
When you're working on multiple tasks in a single conversation, the context can become cluttered with irrelevant information. For example, if you're debugging an authentication issue, then switching to optimize database queries, then reviewing API documentation - all that mixed context can confuse the AI and lead to less accurate responses. 

With subagents, each specialized task gets its own clean workspace. The database optimization subagent doesn't need to know about your authentication debugging, and vice versa.

### 2. **Maintains Focus and Precision**
A subagent with its own context window can dive deep into a specific problem without distraction. Consider a code review subagent:
- In the main conversation, you might have discussed architecture decisions, bug fixes, and new features
- The review subagent starts fresh, focusing solely on analyzing the code quality of the specific files you're reviewing
- This focused context leads to more thorough and relevant feedback

### 3. **Enables Parallel Processing**
Since each subagent has its own context, multiple subagents can theoretically work on different aspects of your project simultaneously without interfering with each other:
- A testing subagent can generate test cases for one module
- A documentation subagent can update API docs for another module  
- A performance analysis subagent can profile a third module
- None of these tasks contaminate each other's context

### 4. **Preserves Main Conversation Clarity**
Your main conversation with Claude Code remains high-level and strategic. Instead of filling it with detailed debugging logs, test outputs, or lengthy code reviews, these details stay within their respective subagent contexts. You get back only the essential results and recommendations.

### 5. **Improves Consistency and Reliability**
Because each subagent starts with the same clean context every time it's invoked, you get more predictable behavior. A debugging subagent will approach problems the same way whether it's your first or fiftieth debugging session, unaffected by previous conversations.

### Real-World Example:
Imagine you're developing a web application:
1. You ask Claude Code to help design a new feature
2. Claude delegates to a **requirements-analysis** subagent (fresh context)
3. You then need to debug a production issue  
4. Claude delegates to a **debugger** subagent (separate fresh context)
5. Finally, you want to review the code before deployment
6. Claude delegates to a **code-reviewer** subagent (another fresh context)

Each subagent works in isolation, preventing the feature design discussion from influencing the debugging process, and the debugging details from cluttering the code review. Your main conversation maintains a clear narrative of what you accomplished without getting bogged down in implementation details.

This separation of concerns through independent context windows is what makes subagents so powerful - they can be truly specialized experts that maintain focus and deliver consistent, high-quality results for their specific domains.

## Comprehensive Guide

For detailed information about creating, configuring, and using subagents effectively, see the [Comprehensive Guide to Claude Code Subagents](guide.md).