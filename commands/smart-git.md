# Smart Git Commit & Push

Stage all local changes, create a commit message that documents local vs remote diffs, commit, and push upstream.

## Execution Steps

### 1. Fetch & Diff
- Get current branch:  
  ```bash
  BRANCH=$(git rev-parse --abbrev-ref HEAD)
  ```
- Fetch remote updates:  
  ```bash
  git fetch origin $BRANCH
  ```
- Gather diff summary:  
  ```bash
  DIFF_STAT=$(git diff origin/$BRANCH --stat)
  ```
- Gather detailed diff (limited for readability):  
  ```bash
  DIFF_DETAIL=$(git diff origin/"$BRANCH" --unified=3 | head -n 200)
  ```

### 2. Stage Changes
- Stage everything:  
  ```bash
  git add .
  ```

### 3. Commit with Inline Diffs
```bash
git commit -m "Sync local changes with remote on branch $BRANCH

Changes Summary:
$DIFF_STAT

Detailed Diffs (first 200 lines):
$DIFF_DETAIL

(All local changes staged and pushed by smart-commit)"
````

### 4. Push

* Push branch upstream:
  ```bash
  git push origin $BRANCH
  ```

### 5. Error Handling

* If push fails due to remote ahead → auto-rebase & retry:
  ```bash
  git pull --rebase origin $BRANCH && git push origin $BRANCH
  ```
  if it still fails, alert the user and wait for next steps. 

## Success Criteria

* Commit message contains file-level stats + truncated diff
* All local changes staged and committed
* Remote branch up to date with local

```

This way the **commit message itself** contains:  
- File-level summary (`git diff --stat`)  
- Inline diff (truncated for readability, e.g., 200 lines)  
- A fallback note explaining that everything was staged/pushed.  

---

Do you want the **diff detail truncated** (like above with `head -200`), or should it **always include full diffs** no matter how long?
