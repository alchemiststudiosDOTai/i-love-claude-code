#!/usr/bin/env python3
"""
Generic, idempotent Claude/LLM repo optimizer.
- the agents should use this but also update manually as needed
- Creates/updates .claude/* without duplicating existing data.
- Infers components from repo structure and languages by extension.
- Uses git + (optionally) gh to mine churn, tags, merged PRs, and bug fixes.
- Produces/updates: metadata/components.yml, metadata/hotspots.txt,
  anchors.json (file-level deterministic anchors), delta/YYYY-MM-DD-baseline.yml,
  delta/<prev>_to_<curr>.diff, qa/*.yml, README.md.
"""

import json, os, re, subprocess, hashlib, sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
try:
    import yaml  # pyyaml
except Exception as e:
    print("Requires PyYAML (pip install pyyaml)", file=sys.stderr)
    raise

# ---------- Helpers ----------
def sh(cwd: Path, *args: str) -> Optional[str]:
    try:
        out = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return None

def git(cwd: Path, *args: str) -> Optional[str]:
    return sh(cwd, "git", *args)

def gh(cwd: Path, *args: str) -> Optional[str]:
    return sh(cwd, "gh", *args)

def read_yaml(p: Path) -> Any:
    if not p.exists(): return None
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def write_yaml(p: Path, obj: Any):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(obj or {}, f, default_flow_style=False, sort_keys=False)

def read_json(p: Path) -> Any:
    if not p.exists(): return None
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def write_json(p: Path, obj: Any):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

# ---------- Core ----------
IGNORE_DIRS = {".git", ".github", ".claude", ".venv", "venv", "node_modules", "dist", "build", "__pycache__", ".idea", ".vscode", "target", ".mypy_cache", ".pytest_cache", ".cache", ".tox"}
LANG_BY_EXT = {
    ".py":"python",".js":"javascript",".ts":"typescript",".tsx":"typescript",".jsx":"javascript",
    ".go":"go",".rs":"rust",".c":"c",".h":"c",".cpp":"cpp",".hpp":"cpp",".cc":"cpp",
    ".java":"java",".kt":"kotlin",".rb":"ruby",".php":"php",".cs":"csharp",
    ".sh":"bash",".ps1":"powershell",".sql":"sql",".swift":"swift",".m":"objc",
    ".cmake":"cmake",".lua":"lua",".r":"r",".pl":"perl",".scala":"scala",".dart":"dart"
}

class RepoOptimizer:
    def __init__(self, root: str = "."):
        self.root = Path(root).resolve()
        self.dotc = self.root/".claude"
        self.today = datetime.now().strftime("%Y-%m-%d")

    # ---- setup ----
    def ensure_dirs(self):
        for d in ["metadata","code_index","debug_history","patterns","cheatsheets","qa","delta"]:
            (self.dotc/d).mkdir(parents=True, exist_ok=True)

    # ---- discovery ----
    def list_top_components(self) -> Dict[str, Dict[str, Any]]:
        """Infer components from top-level directories (excluding ignored)."""
        components: Dict[str, Dict[str, Any]] = {}
        for p in sorted(self.root.iterdir()):
            if not p.is_dir(): 
                continue
            name = p.name
            if name in IGNORE_DIRS or name.startswith("."): 
                continue
            lang_counts: Dict[str,int] = {}
            for fp in p.rglob("*"):
                if fp.is_dir(): 
                    continue
                ext = fp.suffix.lower()
                lang = LANG_BY_EXT.get(ext)
                if lang:
                    lang_counts[lang] = lang_counts.get(lang,0)+1
            lang = max(lang_counts, key=lang_counts.get) if lang_counts else "mixed"
            components[name] = {
                "paths": [f"{name}/"],
                "description": f"Auto-inferred component rooted at {name}/",
                "language": lang
            }
        # fallback for monorepos with src/
        src = self.root/"src"
        if src.exists() and "src" not in components:
            components["src"] = {
                "paths":["src/"],
                "description":"Auto-inferred component rooted at src/",
                "language":"mixed"
            }
        return components

    def get_hotspots(self, months:int=6, limit:int=50) -> List[tuple]:
        out = git(self.root, "log", f"--since={months} months ago","--name-only","--pretty=format:")
        if not out: return []
        counts: Dict[str,int] = {}
        for ln in out.splitlines():
            ln = ln.strip()
            if not ln or ln.startswith(" "): 
                continue
            if ln.startswith(".claude/") or ln.startswith(".git/"):
                continue
            counts[ln] = counts.get(ln,0)+1
        return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:limit]

    def write_hotspots(self):
        hs = self.get_hotspots()
        lines = ["# High-churn files (last 6 months)",""]
        for path,count in hs[:100]:
            lines.append(f"{count:3d} {path}")
        (self.dotc/"metadata"/"hotspots.txt").write_text("\n".join(lines), encoding="utf-8")

    def first_sha_for_file(self, path:str) -> str:
        out = git(self.root, "log","--diff-filter=A","-1","--format=%H","--", path)
        return (out or "unknown")[:12]

    # ---- anchors ----
    def build_or_merge_anchors(self):
        anchors_path = self.dotc/"anchors.json"
        existing = read_json(anchors_path) or {"version":1,"anchors":[]}
        by_id = {a["id"]:a for a in existing.get("anchors",[])}

        # target files = hotspots top N (no binaries)
        hotspots = [p for p,_ in self.get_hotspots(limit=200)]
        text_like = [p for p in hotspots if Path(self.root/p).is_file()]

        new: List[Dict[str,Any]] = []
        seen_ids: Set[str] = set()

        for p in text_like[:120]:
            intro = self.first_sha_for_file(p)
            aid = sha1(f"{p}:file:{intro}")[:12]
            seen_ids.add(aid)
            if aid in by_id:
                # refresh path/status if needed
                a = by_id[aid]
                if a.get("status") != "active":
                    a["status"]="active"
                if a.get("path") != p:
                    a["path"]=p
                new.append(a)
            else:
                new.append({
                    "id": aid,
                    "path": p,
                    "kind": "file",
                    "symbol": None,
                    "since": intro,
                    "status": "active"
                })

        # tombstone any anchors whose files disappeared
        for a in existing.get("anchors",[]):
            if a["id"] not in {x["id"] for x in new}:
                fp = self.root / a.get("path","")
                if not fp.exists():
                    a["status"]="tombstone"
                new.append(a)

        write_json(anchors_path, {"version":1,"anchors": new})

    # ---- components.yml ----
    def merge_components(self):
        components_file = self.dotc/"metadata"/"components.yml"
        inferred = self.list_top_components()
        current = read_yaml(components_file) or {}
        merged = {"version":1, "components": {}}
        # keep existing
        if "components" in current:
            merged["components"].update(current["components"])
        # add inferred if missing
        for k,v in inferred.items():
            merged["components"].setdefault(k, v)
        write_yaml(components_file, merged)

    # ---- baseline + diffs ----
    def last_two_tags(self) -> Optional[List[str]]:
        tags = git(self.root, "tag","--sort=creatordate")
        if not tags: return None
        arr = [t for t in tags.splitlines() if t.strip()]
        return arr[-2:] if len(arr)>=2 else None

    def write_tag_diff_once(self):
        pair = self.last_two_tags()
        if not pair: return
        a,b = pair[0], pair[1]
        out_file = self.dotc/"delta"/f"{a}_to_{b}.diff"
        if out_file.exists(): return
        diff = git(self.root, "diff", a, b) or ""
        out_file.write_text(diff, encoding="utf-8")

    def write_or_update_baseline(self):
        baseline = self.dotc/"delta"/f"{self.today}-baseline.yml"
        cur = read_yaml(baseline) or {}
        anchors = read_json(self.dotc/"anchors.json") or {"anchors":[]}
        anchor_ids = [a["id"] for a in anchors.get("anchors",[]) if a.get("status")=="active"]

        comps = read_yaml(self.dotc/"metadata"/"components.yml") or {}
        comp_names = list((comps.get("components") or {}).keys())

        apis = []
        # spread a few anchors across components deterministically
        for i, c in enumerate(comp_names[:8]):
            chunk = anchor_ids[i::len(comp_names[:8])][:5] if comp_names else []
            apis.append({"component": c, "public_symbols": chunk})

        base = {
            "version": 1,
            "date": self.today,
            "scope": "baseline",
            "apis": apis,
            "risks": cur.get("risks", []),
            "migration_notes": cur.get("migration_notes", [])
        }
        write_yaml(baseline, base)

    # ---- QA seeding from commits/PRs ----
    def recent_fix_commits(self) -> List[Dict[str,str]]:
        out = git(self.root, "log","--since=90 days ago","--grep=fix\\|bug\\|hotfix","-i","--format=%H|%s","-n","50")
        if not out: return []
        arr=[]
        for ln in out.splitlines():
            if "|" in ln:
                sha,msg = ln.split("|",1)
                arr.append({"sha":sha[:8], "message":msg.strip()})
        return arr

    def recent_merged_prs(self) -> List[Dict[str,Any]]:
        data=[]
        j = gh(self.root, "pr","list","--state","merged","--limit","50","--json","number,title,mergedAt,labels")
        if j:
            try:
                arr = json.loads(j)
                for pr in arr:
                    data.append({
                        "number": pr.get("number"),
                        "title": pr.get("title",""),
                        "mergedAt": pr.get("mergedAt",""),
                        "labels": [l.get("name") for l in pr.get("labels",[])]
                    })
            except Exception:
                pass
        return data

    def seed_qa(self):
        qa_dir = self.dotc/"qa"
        qa_dir.mkdir(parents=True, exist_ok=True)

        anchors = read_json(self.dotc/"anchors.json") or {"anchors":[]}
        anchor_paths = {a.get("path",""): a.get("id") for a in anchors.get("anchors",[]) if a.get("status")=="active"}

        # From commits
        for fx in self.recent_fix_commits()[:10]:
            sig = fx["message"][:72]
            # crude path guess: look for filenames in message
            hit_anchors = []
            for path, aid in anchor_paths.items():
                base = os.path.basename(path)
                if base and base in fx["message"]:
                    hit_anchors.append(aid)
                    if len(hit_anchors)>=3: break

            qa = {
                "id": f"qa-{fx['sha']}",
                "anchors": hit_anchors,
                "problem": sig,
                "cause": "unknown (auto-seeded)",
                "fix": fx["sha"],
                "notes": "Auto-seeded from recent fix commit"
            }
            out = qa_dir/f"{qa['id']}.yml"
            if not out.exists():
                write_yaml(out, qa)

        # From merged PRs (if gh available)
        for pr in self.recent_merged_prs():
            title = pr["title"]
            if not any(k in title.lower() for k in ["fix","bug","issue","regression"] + (pr.get("labels") or [])):
                continue
            pid = f"qa-pr-{pr['number']}"
            qa = {
                "id": pid,
                "anchors": [],
                "problem": title[:72],
                "cause": "unknown (from merged PR)",
                "fix": f"PR#{pr['number']}",
                "notes": f"Merged at {pr.get('mergedAt','')}"
            }
            out = qa_dir/f"{qa['id']}.yml"
            if not out.exists():
                write_yaml(out, qa)

    # ---- README ----
    def write_readme_once(self):
        p = self.dotc/"README.md"
        if p.exists(): return
        p.write_text(
            "# .claude layout (auto-generated)\n\n"
            "- `metadata/` – components & hotspots\n"
            "- `anchors.json` – deterministic IDs for files/symbols\n"
            "- `delta/` – baselines and release diffs\n"
            "- `qa/` – bug patterns and fixes (per YAML)\n"
            "- `code_index/`, `patterns/`, `cheatsheets/` – reserved for future use\n\n"
            "Idempotent: re-run `python claude_repo_optimizer.py` to update.\n",
            encoding="utf-8"
        )

    # ---- run ----
    def run(self):
        print(f"Optimizing: {self.root}")
        self.ensure_dirs()
        self.write_hotspots()
        self.merge_components()
        self.build_or_merge_anchors()
        self.write_tag_diff_once()
        self.write_or_update_baseline()
        self.seed_qa()
        self.write_readme_once()
        print(f"Done. Updated {.0} .claude".format(""))

if __name__ == "__main__":
    RepoOptimizer().run()
