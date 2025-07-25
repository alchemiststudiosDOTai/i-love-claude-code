

````md
---
description: Run the full Task Master flow on a task (ID or description) and manage notes with scratchpad.sh
allowed-tools: Bash(*), Edit(*), Read(*)
---

# /tm/work — Task Master + scratchpad.sh

Drive one task end‑to‑end using **Task Master** plus your `scratchpad.sh` workflow.

## Args

**$ARGUMENTS** = task IDs (comma‑sep), empty (pick next), or free‑text (create task).

---

## 0) Pre‑flight

1. Verify Task Master is installed/available (MCP or CLI).
2. Verify `./scratchpad.sh` exists and is executable.

---

## 1) Resolve what to work on

**A) Numeric IDs**

```bash
!task-master show $ARGUMENTS
```
````

If under‑specified:

```bash
!task-master expand $ARGUMENTS
```

**B) Empty args → next task**

```bash
!task-master next
```

**C) Free text → create**

```bash
!task-master add "$ARGUMENTS"
```

---

## 2) Open a scratchpad

```bash
!./scratchpad.sh new task "<Resolved Task Title>"
```

Append progress as you go:

```bash
!./scratchpad.sh append <filename> "status update"
```

---

## 3) Implement via TM loop

1. **Plan** – ask TM for concrete implementation steps.
2. **Code** – use Edit/Read with small, sequential diffs.
3. **Doc delta** – summarize in the scratchpad for later filing.

---

## 5) Close the loop

1. Mark the TM task **done** (or next state).
2. File the scratchpad in the correct dir:

   ```bash
   !./scratchpad.sh complete <file>
   !./scratchpad.sh filed <file>
   ```

---

## Errors / edges

- **No tasks** → create from `$ARGUMENTS`.
- **Push conflicts** → pull/rebase, resolve, retry.

```

**Sources:** Anthropic’s Claude Code **slash command** docs and best‑practices, plus the **Task Master** repository. :contentReference[oaicite:0]{index=0}
::contentReference[oaicite:1]{index=1}
```
