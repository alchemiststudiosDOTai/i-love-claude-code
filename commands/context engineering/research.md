# Research Codebase

You are tasked with conducting comprehensive research across the codebase to answer user questions by spawning parallel sub-agents and synthesizing their findings. All research documents must be stored in the `memory-bank/research/` directory, following the YAML frontmatter and content structure below.

## Initial Setup:

When this command is invoked, respond with:
```
I'm ready to research the codebase. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring relevant components and connections.
```

Then wait for the user's research query.

## Steps to follow after receiving the research query:

1. **Read any directly mentioned files first:**
   - If the user mentions specific files (tickets, docs, JSON), read them FULLY first
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files
   - **CRITICAL**: Read these files yourself in the main context before spawning any sub-tasks
   - This ensures you have full context before decomposing the research

2. **Analyze and decompose the research question:**
   - Break down the user's query into composable research areas
   - Take time to ultrathink about the underlying patterns, connections, and architectural implications the user might be seeking
   - Identify specific components, patterns, or concepts to investigate
   - Create a research plan using TodoWrite to track all subtasks
   - Consider which directories, files, or architectural patterns are relevant

3. **Spawn parallel sub-agent tasks for comprehensive research:**
   - Strictly limit to a maximum of 3 Task agents per research query. You may not spawn more than two sub-agents for any research query, regardless of the number of aspects or subtasks. This is a hard limit.
   - Only reference files and resources that are part of the current codebase or workspace. Do not reference or include any files, tickets, or resources that are external or not present in this workspace.


   YOU MUST DEPLOY THESE 3 IN PARELLEL
   YOU WILL BE PUNISHED FOR NOT DEPLOYING SUBAGENTS IN PARELLEL

   **For codebase research:**
   - Use the **codebase-locator** agent to find WHERE files and components live
   - Use the **codebase-analyzer** agent to understand HOW specific code works
   - Use the **context-synthesis** agent to find context as needed

   The key is to use these agents intelligently:
   - Start with locator agents to find what exists
   - Then use analyzer and synthesis agents on the most promising findings
   - Run agents in parallel only if they are searching for different things, and never exceed two concurrent sub-agents.
   - Each agent knows its job - just tell it what you're looking for
   - Don't write detailed prompts about HOW to search - the agents already know

4. **Wait for all sub-agents to complete and synthesize findings:**
   - IMPORTANT: Wait for ALL sub-agent tasks to complete before proceeding
   - Compile all sub-agent results (both codebase and thoughts findings)
   - Prioritize live codebase findings as primary source of truth
   - Use thoughts/ findings as supplementary historical context
   - Connect findings across different components
   - Include specific file paths and line numbers for reference
   - Verify all thoughts/ paths are correct (e.g., thoughts/allison/ not thoughts/shared/ for personal files)
   - Highlight patterns, connections, and architectural decisions
   - Answer the user's specific questions with concrete evidence

5. **Gather metadata for the research document:**
   - Filename: `memory-bank/research/YYYY-MM-DD_HH-MM-SS_topic.md`

6. **Generate research document:**
      - Use the metadata gathered in step 4
      - Structure the document in the following format and store in `memory-bank/research/`:
         ```markdown
         # Research – <TASK_NAME>
         **Date:** {{date}}
         **Owner:** {{agent or user}}
         **Phase:** Research

         ## Goal
         Summarize all *existing knowledge* before any new work.

         
         - Additional Search:
            - `grep -ri "<term>" .claude/`

         ## Findings
         - Relevant files & why they matter:
            - `<file>` → `<reason>`
            - `<file>` → `<reason>`

         ## Key Patterns / Solutions Found
         - `<pattern>`: short description, relevance

         ## Knowledge Gaps
         - Missing context or details for next phase

         ## References
         - Links or filenames for full review
         ```

7. **Add GitHub permalinks (if applicable):**
    - Check if on main branch or if commit is pushed: `git branch --show-current` and `git status`
    - If on main/master or pushed, generate GitHub permalinks:
       - Get repo info: `gh repo view --json owner,name`
       - Create permalinks: `https://github.com/{owner}/{repo}/blob/{commit}/{file}#L{line}`
    - Replace local file references with permalinks in the document
    - For research documents, update references to use `memory-bank/research/` paths where applicable.



9. **Handle follow-up questions:**
   - If the user has follow-up questions, append to the same research document
   - Update the frontmatter fields `last_updated` and `last_updated_by` to reflect the update
   - Add `last_updated_note: "Added follow-up research for [brief description]"` to frontmatter
   - Add a new section: `## Follow-up Research [timestamp]`
   - Spawn new sub-agents as needed for additional investigation
   - Continue updating the document and syncing

## Important notes:
- Always use parallel Task agents to maximize efficiency and minimize context usage
- Always run fresh codebase research - never rely solely on existing research documents
- The thoughts/ directory provides historical context to supplement live findings
- Focus on finding concrete file paths and line numbers for developer reference
- Research documents should be self-contained with all necessary context
- Each sub-agent prompt should be specific and focused on read-only operations
- Consider cross-component connections and architectural patterns
- Include temporal context (when the research was conducted)
- Link to GitHub when possible for permanent references
- Keep the main agent focused on synthesis, not deep file reading
- Encourage sub-agents to find examples and usage patterns, not just definitions
- Explore all of thoughts/ directory, not just research subdirectory
- **File reading**: Always read mentioned files FULLY (no limit/offset) before spawning sub-tasks
- **Critical ordering**: Follow the numbered steps exactly
  - ALWAYS read mentioned files first before spawning sub-tasks (step 1)
  - ALWAYS wait for all sub-agents to complete before synthesizing (step 4)
  - ALWAYS gather metadata before writing the document (step 5 before step 6)
  - NEVER write the research document with placeholder values
- **Path handling**: The thoughts/searchable/ directory contains hard links for searching
  - Always document paths by removing ONLY "searchable/" - preserve all other subdirectories

  - NEVER change allison/ to shared/ or vice versa - preserve the exact directory structure
  - This ensures paths are correct for editing and navigation
- **Frontmatter consistency**:
  - Always include frontmatter at the beginning of research documents
  - Keep frontmatter fields consistent across all research documents
  - Update frontmatter when adding follow-up research
  - Use snake_case for multi-word field names (e.g., `last_updated`, `git_commit`)
  - Tags should be relevant to the research topic and components studied


  DO NOT CODE YOU WILL BE PUNISHED FOR CODING 

  SAVE THE DOCUMENT YOU MUST SAVE IN THE CORRECT FORMAT FOR THE NEXT DEV

  ALWAYS FOLLOW BEST PRACTISES