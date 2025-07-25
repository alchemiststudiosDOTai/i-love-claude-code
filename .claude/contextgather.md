Here’s a **stand‑alone slash command** called **`/context/gather`** that spins up a **multi‑agent context‑gathering workflow**: planner → searcher → synthesizer → QA (with up to 3 corrective loops, then asks you). Drop it at:

```
.claude/commands/context/gather.md
```

````md
---
description: Multi-agent context gatherer — plan, search (code+docs+web), synthesize, QA, and loop up to 3x before asking the user.
allowed-tools: Bash(*), Read(*), Edit(*)
---

# /context/gather — Multi‑Agent Context Collector

**Goal:** The user describes an issue/bug/feature. We (LLM) gather *all* relevant context: file locations, call paths, endpoints, configs, logs, tests, and any linked docs, then produce a single, timestamped Markdown dossier. If anything is still unclear after 3 QA loops, **ask the user**.

**Input:** `$ARGUMENTS` — short description of the issue/bug/feature.

---

## Agents & Responsibilities

1. **Planner Agent (A1) – Plan & Questions**
   - Clarify the request. If anything is missing (env, repro steps, stack, branch, service, endpoints), **ask the user first**.
   - Emit a concrete **Search Plan**: code globs, ripgrep patterns, files/dirs to open, APIs to inspect, configs to read, web/docs to consult.
   - Define the **naming** of the final report:  
     `.claude/context/context-$SLUG-$(date +%Y-%m-%d).md`

2. **Search Agent (A2) – Execute Searches**
   - Run the plan with **local search tools** (`rg`, `git grep`, `fd/find`, `ctags`/`ripgrep`), `task-master search` if available, and **Read(**)** for key files.
   - Pull **project docs**: `.claude/metadata`, `/docs`, `/openapi*`, `README*`, `/contracts`, `/interfaces`, etc.
   - Optionally query the **web/MCP tools** for external docs/specs if the plan requires it (framework/lib APIs, vendor SDKs, known bugs).
   - Produce a **raw dump of findings** (paths, code snippets, signatures, endpoints, env vars, configs, test names, failing logs).

3. **Synthesizer Agent (A3) – Write the Context Dossier**
   - Aggregate A2’s findings into a single **Markdown report**:
     - **Title / Date / Hash / Branch**
     - **Problem Statement (from user)**
     - **System Map (high-level architecture, services, files)**
     - **Relevant Files & Symbols (with paths & brief roles)**
     - **Data/Control Flow (where the bug/feature lives)**
     - **APIs & Endpoints involved (incl. wrong vs correct if suspected)**
     - **Config/Env flags impacting the behavior**
     - **Tests touching this area (+ current state)**
     - **Open Questions / Assumptions**
   - Save it to: `.claude/context/context-$SLUG-$(date +%Y-%m-%d).md`.

4. **QA Agent (A4) – Validate & Loop (≤ 3x)**
   - Run logic checks: wrong endpoints, stale paths, dead code, incorrect assumptions, missing migrations, version mismatches, test gaps.
   - If inconsistencies found:
     - **Instruct a fresh Search pass** (spawn A2 again) with the specific gaps to fill.
     - Repeat **max 3 times**.
   - If still unsure after 3 loops → **ask the user precise, minimal questions** and wait.

---

## Required Steps (what you, Claude, must do)

### 0) Intake & Clarification (A1)
- If `$ARGUMENTS` is vague, ask:
  - Runtime / service / branch?
  - Repro steps & exact error?
  - Expected vs actual behavior?
  - Any logs / test failures?
  - Which API(s) or module(s) likely involved?

### 1) Emit the **Search Plan** (A1)
Include:
- **Code queries** (`rg -n -S "pattern"` on suspected symbols/paths)
- **Directories** to scan
- **Docs** to read
- **External/web docs** to consult (framework/vendor)
- **Output structure** for the final dossier

### 2) Execute Searches (A2)
Examples (adjust to project):
```bash
!rg -n -S "($ERROR_CODE|$ENDPOINT|$FUNC_NAME)" -g '!**/node_modules/**' -g '!**/dist/**'
!git grep -n "SUSPECT_SYMBOL"
!fd -H -t f "(openapi|swagger|postman).*\\.(ya?ml|json|md)" .
!cat path/to/config.env
!task-master search "$ARGUMENTS"   # if available
````

Use **Read(**)\*\* for large files instead of Bash `cat` when needed.

### 3) Synthesize the Dossier (A3)

Create and write to:

```
.claude/context/context-$SLUG-$(date +%Y-%m-%d).md
```

Mandatory sections:

* Problem statement
* Architecture map (minimal, but accurate)
* File list (path → purpose)
* Call/data flow relevant to the issue
* Endpoints / external services
* Tests & coverage around the issue
* Key config/env flags
* Open questions / uncertainties

### 4) QA & Loop (A4)

* Validate endpoints, function names, paths, config keys.
* If mismatch found → **spawn A2 again** with precise search deltas.
* **Max 3 cycles**. After that, ask user for the specific missing bits.

### 5) Finish

* Print final dossier path.
* Summarize what’s still ambiguous (if anything) and the exact questions for the user.

---

## Conventions

* **Never silently assume** — document assumptions & surface them in the “Open questions” section.
* Prefer **exact paths / line numbers / symbols** over prose.
* Keep every loop short and surgical.

---

## Notes

* This shape follows Anthropic’s **custom slash command** pattern (frontmatter + `allowed-tools`) and their **agentic coding best practices** (bash/MCP/tools + iterative validation). It also borrows the planning/execution rigor popularized by **Task Master**. .claude/commands are officially supported, with `$ARGUMENTS` injection and tool whitelisting. If Bash permission prompts don’t appear, there’s a known bug—grant Bash globally or run `/allowedTools` first.

```

**Sources:** Anthropic’s **slash commands** syntax & CLI docs, **best practices** for agentic coding, **common workflows**, **allowed-tools** usage guidance, and the **Task Master** workflow/repos. :contentReference[oaicite:0]{index=0}

Want a matching **`/context/show-latest`** (to quickly open the newest dossier) and **`/context/qa`** (to re-run only the QA loop) too? I can ship those next.
::contentReference[oaicite:1]{index=1}
```
