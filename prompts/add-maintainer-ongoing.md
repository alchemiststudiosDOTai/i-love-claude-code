### Instruction

**Role:** Repo optimizer for an **ongoing project**.
**Goal:** Set a **baseline today** and make the repo **Claude/LLM-friendly** going forward.
**Idempotency:** If targets already exist, **read/merge/update**—**no duplicates**.
**Autonomy:** **Do not ask questions.** Gather all context yourself from the repo and GitHub via **`git`** and **`gh`**.

Your task is to:

* Verify/create the `.claude/` layout and **update in place**.
* Create a **baseline delta** dated **today**; track future changes incrementally.
* Generate **deterministic anchors** for hot paths; backfill **recent** history only.
* Seed/update **QA/debug** entries from merged PRs and “fix/bug/hotfix” commits.
* Produce **concise, auditable diffs** with minimal churn.

**Data you MUST crawl automatically (no user prompts):**

* **Churn & tags:** `git log`, `git tag --sort=creatordate`, `git diff <prev> <curr>`.
* **PRs/issues:** `gh pr list --state merged`, `gh pr view <num> --json ...`, `gh issue list --state closed`.
* **Releases:** `gh release list`.
* **File intro SHAs:** `git log --diff-filter=A -1 --format=%H -- <path>`.

You MUST:

1. Detect existing `.claude/*` files/dirs and **merge** rather than overwrite.
2. Use **today’s date** for the baseline filename; if it exists, **update** its sets.
3. Generate anchor IDs: `sha1(path + symbol + first_seen_file_sha)`; fall back to **file-scope** when symbol history is hard.
4. Limit backfill to **last 3–6 months** or **since last tag/release** (whichever is shorter).
5. Favor **top-churn** components for first anchors.
6. Keep outputs **short, structured, diff-friendly** (YAML/JSON).
7. Ensure that your answer is unbiased and avoids relying on stereotypes.
8. **Never** duplicate files, rewrite large docs, or add unrelated content.

You will be penalized for: duplication, verbose narration, destructive rewrites, or ignoring `gh`/`git` evidence.

---

### Outputs (in this exact order)

1. **Plan (≤12 bullets)** — concrete steps you will execute, referencing the commands you’ll run.

2. **Idempotent Creator Script** — one **Python** file that:

   * Creates missing dirs only: `.claude/{metadata,code_index,debug_history,patterns,cheatsheets,qa,delta}`.
   * Runs `git`/`gh` via `subprocess` to gather:

     * churn → `.claude/metadata/hotspots.txt`
     * tags/releases/PRs → recent window selection
     * fixes → seed QA entries
   * Builds/merges:

     * `.claude/metadata/components.yml` (preserve existing keys; add missing).
     * `.claude/anchors.json` (merge; add new; mark tombstones when symbols disappear).
     * `.claude/delta/YYYY-MM-DD-baseline.yml` (create or update for today).
     * Raw diffs for last two tags in `.claude/delta/<prev>_to_<curr>.diff` **if absent**.
   * Never overwrites blindly; always **load → merge → write**.

3. **Files to Create/Update** — exact minimal templates/snippets, each in its own fenced block:

   * `./.claude/README.md` (if missing): one-screen directory overview.
   * `./.claude/metadata/components.yml` (merge example).
   * `./.claude/anchors.json` (schema + 2 sample entries).
   * `./.claude/delta/YYYY-MM-DD-baseline.yml` (template below).
   * `./.claude/qa/EXAMPLE.yml` (one seed entry tied to an anchor).

4. **Next PR Rules (5 bullets)** — the rules contributors follow to keep this system current.

---

### Baseline Templates (use these shapes exactly)

**`./.claude/delta/YYYY-MM-DD-baseline.yml`**

```yaml
version: 1
date: YYYY-MM-DD
scope: baseline
apis:
  - component: <name>
    public_symbols: [<AnchorID>, ...]
risks:
  - area: <component-or-file>
    notes: "<1–2 lines>"
migration_notes: []
```

**`./.claude/anchors.json` (schema)**

```json
{
  "version": 1,
  "anchors": [
    {
      "id": "<sha1>",
      "path": "src/module/file.py",
      "kind": "function|class|file",
      "symbol": "name-or-null",
      "since": "<git_sha_first_seen_for_file>",
      "status": "active|tombstone"
    }
  ]
}
```

**`./.claude/qa/EXAMPLE.yml`**

```yaml
id: qa-<short-id>
anchors: ["<AnchorID>", "..."]
problem: "<error signature>"
cause: "<root cause>"
fix: "<commit or PR #>"
notes: "<1–2 lines>"
```

---

### Operating Constraints

* Use **`gh`** for all GitHub data; degrade gracefully if missing by using local `git` only.
* If today’s baseline exists, **merge** into it; no new file.
* Keep every file under \~200 lines on first pass; link out rather than inlining long content.

---

### Output Primer

Plan:

1. …
2. …
3. …

(Idempotent Creator Script next, then **Files to Create/Update**, then **Next PR Rules**.)
