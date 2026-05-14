#!/usr/bin/env python3
"""
MJ-series Python pre-pass — file-system ops, git queries, path resolution.

Claude tokens are reserved for reasoning.  This script handles everything
that can be answered deterministically: plugin paths, partner skill paths,
git state, flag parsing.

Sub-commands
  ceo-preflight               → plugin + partner paths + context7 status
  end-preflight [FLAGS...]    → flag parsing + author check + initial git state
  git-status <dir>            → push status for one repo (run after git push)
  resolve-partner <name>      → dynamic SKILL.md path lookup
  plugin-versions             → latest dir for every CS plugin
  session-digest [FLAGS...]   → session pre-pass: domain usage, BTW pending, knowhow index, stale entries
"""

import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
MARKETPLACE = HOME / ".claude/plugins/marketplaces/MJnCompany_2-0"
BASE = MARKETPLACE / "plugins"


# ── low-level helpers ─────────────────────────────────────────────────────────

def latest_plugin(prefix: str) -> str:
    dirs = sorted(BASE.glob(f"{prefix}v*"), key=lambda p: p.name)
    if not dirs:
        # prefix without trailing dash (e.g. "mj-smart-run")
        exact = BASE / prefix
        return str(exact) if exact.is_dir() else ""
    return str(dirs[-1])


_SKIP_DIRS = {".bak", "node_modules", ".git", "__pycache__", ".cache", ".DS_Store"}


def find_skill(name: str) -> str:
    """Search known locations for <name>/SKILL.md, skipping unsafe dirs."""
    roots = [
        BASE,
        HOME / ".claude/plugins/marketplaces",
        HOME / ".claude/plugins/cache",
        HOME / ".claude/skills",
    ]
    for root in roots:
        root_str = str(root)
        if not os.path.isdir(root_str):
            continue
        for dirpath, dirnames, filenames in os.walk(root_str, onerror=lambda _: None):
            dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
            if os.path.basename(dirpath) == name and "SKILL.md" in filenames:
                return os.path.join(dirpath, "SKILL.md")
    return ""


def _git(repo: str, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", repo, *args],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def push_status(repo: str) -> dict:
    if not repo or not Path(repo).is_dir():
        return {"state": "na", "ahead": "0", "behind": "0", "branch": "", "remote": ""}
    ahead  = _git(repo, "rev-list", "--count", "@{u}..HEAD") or "0"
    behind = _git(repo, "rev-list", "--count", "HEAD..@{u}") or "0"
    branch = _git(repo, "branch", "--show-current")
    r_url  = _git(repo, "remote", "get-url", "origin")
    slug   = ""
    if r_url and "github.com" in r_url:
        slug = r_url.split("github.com")[-1].lstrip(":/")
        if slug.endswith(".git"):
            slug = slug[:-4]
    state = "pushed" if ahead == "0" else "unpushed"
    return {"state": state, "ahead": ahead, "behind": behind, "branch": branch, "remote": slug}


# ── sub-commands ──────────────────────────────────────────────────────────────

def cmd_ceo_preflight() -> dict:
    plugins = {
        "test":         latest_plugin("MJ-test-"),
        "plan":         latest_plugin("MJ-plan-"),
        "review":       latest_plugin("MJ-codebase-review-"),
        "design":       latest_plugin("mj-design-"),
        "smartrun":     latest_plugin("mj-smart-run"),
        "clarify":      latest_plugin("mj-clarify-"),
        "experiencing": latest_plugin("mj-experiencing-"),
    }

    # superpowers
    sp_base = ""
    cache = HOME / ".claude/plugins/cache"
    if cache.is_dir():
        candidates = sorted(
            [p for p in cache.rglob("superpowers/*/skills") if p.is_dir()],
            key=lambda p: p.parent.name,
        )
        sp_base = str(candidates[-1]) if candidates else ""

    # omc (oh-my-claudecode) — exclude src/skills test-only dir
    omc_base = ""
    if cache.is_dir():
        candidates = sorted(
            [
                p for p in cache.rglob("oh-my-claudecode/*/skills")
                if p.is_dir() and "src/skills" not in str(p)
            ],
            key=lambda p: p.parent.name,
        )
        omc_base = str(candidates[-1]) if candidates else ""

    # gstack
    gstack = ""
    for candidate in [
        HOME / ".claude/skills/gstack/SKILL.md",
        HOME / ".claude/plugins/marketplaces/gstack/skills/gstack/SKILL.md",
    ]:
        if candidate.exists():
            gstack = str(candidate)
            break
    if not gstack:
        gstack = find_skill("gstack")

    # context7
    c7 = str(HOME / ".claude/skills/context7-auto-research/SKILL.md")
    if not Path(c7).exists():
        c7 = find_skill("context7-auto-research")

    bkit = HOME / ".claude/plugins/marketplaces/bkit-marketplace"
    clarify_dir = plugins["clarify"]

    def sp(skill: str) -> str:
        return f"{sp_base}/{skill}/SKILL.md" if sp_base else ""

    def omc(skill: str) -> str:
        return f"{omc_base}/{skill}/SKILL.md" if omc_base else ""

    return {
        "plugins": plugins,
        "partners": {
            "superpowers": {
                "base":                 sp_base,
                "brainstorming":        sp("brainstorming"),
                "writing_plans":        sp("writing-plans"),
                "executing_plans":      sp("executing-plans"),
                "systematic_debugging": sp("systematic-debugging"),
                "dispatching_parallel": sp("dispatching-parallel-agents"),
            },
            "bkit": {
                "pdca": str(bkit / "skills/pdca/SKILL.md"),
                "qa":   str(bkit / "skills/qa-phase/SKILL.md"),
            },
            "omc": {
                "base":         omc_base,
                "deep_dive":    omc("deep-dive"),
                "autoresearch": omc("autoresearch"),
                "autopilot":    omc("autopilot"),
            },
            "gstack":  gstack,
            "clarify": f"{clarify_dir}/skills/mj-clarify/SKILL.md" if clarify_dir else "",
            "context7": c7,
        },
        "context7_installed": bool(c7 and Path(c7).exists()),
    }


def cmd_end_preflight(argv: list) -> dict:
    explicit_project = ""
    no_push = False
    no_compact = False
    learning_only = False
    no_decay_check = False
    explicit_domains = ""

    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--project="):
            explicit_project = a[len("--project="):]
        elif a == "--project" and i + 1 < len(argv):
            i += 1
            explicit_project = argv[i]
        elif a == "--no-push":
            no_push = True
        elif a == "--no-compact":
            no_compact = True
        elif a == "--learning-only":
            learning_only = True
        elif a == "--no-decay-check":
            no_decay_check = True
        elif a.startswith("--domains="):
            explicit_domains = a[len("--domains="):]
        elif a == "--domains" and i + 1 < len(argv):
            i += 1
            explicit_domains = argv[i]
        i += 1

    marketplace_dir = str(MARKETPLACE)
    remote = _git(marketplace_dir, "remote", "get-url", "origin")
    auto_no_push = "nh-investment-squad1" not in remote

    if not explicit_project:
        cwd_top = _git(os.getcwd(), "rev-parse", "--show-toplevel")
        if cwd_top and cwd_top != marketplace_dir:
            explicit_project = cwd_top

    return {
        "flags": {
            "explicit_project":  explicit_project,
            "no_push":           no_push or auto_no_push,
            "no_compact":        no_compact,
            "learning_only":     learning_only,
            "auto_no_push":      auto_no_push,
            "no_decay_check":    no_decay_check,
            "explicit_domains":  explicit_domains,
        },
        "git": {
            "marketplace": push_status(marketplace_dir),
            "project":     push_status(explicit_project) if explicit_project else {"state": "na"},
        },
        "paths": {
            "marketplace":  marketplace_dir,
            "project":      explicit_project,
            "project_name": Path(explicit_project).name if explicit_project else "",
        },
    }


def cmd_session_digest(argv: list) -> dict:
    """
    Session Pre-Pass Digest — LSTM Attention/KV-Cache pattern.

    Extracts a compact JSON digest shared by all Phase 1 agents, eliminating
    4x redundant full-history reads.

    Returns:
      domains_used    – CS domains active this session (git-diff heuristic)
      skill_snapshot  – knowhow index (number, title, date, tier) — NOT full body
      btw_pending     – list of pending BTW items
      btw_count       – total pending BTW count
      stale_entries   – knowhow entries flagged for decay review (Forget Gate)
    """
    skill_path = ""
    btw_file = str(HOME / ".claude" / ".experiencing-btw.json")

    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--skill" and i + 1 < len(argv):
            i += 1
            skill_path = argv[i]
        elif a.startswith("--skill="):
            skill_path = a[len("--skill="):]
        elif a == "--btw-file" and i + 1 < len(argv):
            i += 1
            btw_file = argv[i]
        elif a.startswith("--btw-file="):
            btw_file = a[len("--btw-file="):]
        i += 1

    # ── 1. Knowhow index (titles + dates only, no full body) ──────────────────
    skill_snapshot: list[dict] = []
    if skill_path and Path(skill_path).is_file():
        text = Path(skill_path).read_text(encoding="utf-8", errors="ignore")
        # Match: ### N. Title (YYYY-MM-DD)
        # Also capture optional <!-- tier: principle|tactical --> comment
        header_re = re.compile(
            r"^### (\d+)\.\s+(.+?)\s+\((\d{4}-\d{2}-\d{2})\)",
            re.MULTILINE,
        )
        tier_re = re.compile(r"<!--\s*tier:\s*(principle|tactical)\s*-->")
        entries = list(header_re.finditer(text))
        for m in entries:
            n, title, date_str = m.group(1), m.group(2).strip(), m.group(3)
            # Look for tier comment in the 3 lines after the header
            after = text[m.end():m.end() + 200]
            tier_match = tier_re.search(after)
            tier = tier_match.group(1) if tier_match else "tactical"  # default = tactical
            skill_snapshot.append({"n": int(n), "title": title, "date": date_str, "tier": tier})

    # ── 2. BTW pending items ──────────────────────────────────────────────────
    btw_pending: list[dict] = []
    if Path(btw_file).is_file():
        try:
            items = json.loads(Path(btw_file).read_text(encoding="utf-8"))
            if isinstance(items, list):
                btw_pending = [
                    {"id": it.get("id"), "idea": it.get("idea", ""), "date": it.get("date", "")}
                    for it in items
                    if isinstance(it, dict) and it.get("status") == "pending"
                ]
        except (json.JSONDecodeError, OSError):
            pass

    # ── 3. Domain usage (GRU Update Gate) — git diff heuristic ───────────────
    DOMAIN_PATTERNS: dict[str, list[str]] = {
        "test":   ["MJ-test-v", "/MJ-test/"],
        "plan":   ["MJ-plan-v", "/MJ-plan/"],
        "review": ["MJ-codebase-review-v", "/MJ-codebase-review/"],
        "design": ["mj-design-v", "/mj-design/"],
        "ceo":    ["mj-ceo-v", "/mj-ceo/"],
        "clarify":["mj-clarify-v", "/mj-clarify/"],
        "ship":   ["mj-ship-v", "/mj-ship/"],
    }
    marketplace_dir = str(MARKETPLACE)
    changed_files = _git(marketplace_dir, "diff", "--name-only", "HEAD~5..HEAD")
    domains_used = [
        domain
        for domain, patterns in DOMAIN_PATTERNS.items()
        if any(p in changed_files for p in patterns)
    ]
    # Always include mj-end itself if its files changed
    if "mj-end-v" in changed_files or "/mj-end/" in changed_files:
        if "mj-end" not in domains_used:
            domains_used.append("mj-end")

    # ── 4. Knowledge Decay check (Forget Gate) ────────────────────────────────
    TODAY = datetime.date.today()
    STALE_THRESHOLD_DAYS = 30
    DECAY_KEYWORDS = [
        "osascript", "window.open", "bun --watch", "clipboarditem",
        "v4", "v5", "config.toml", ".env", "api key",
        "bun.write", "bun.spawn", "osascript -e",
    ]
    stale_entries: list[dict] = []
    for entry in skill_snapshot:
        if entry["tier"] == "principle":
            continue
        try:
            entry_date = datetime.date.fromisoformat(entry["date"])
        except ValueError:
            continue
        age = (TODAY - entry_date).days
        if age < STALE_THRESHOLD_DAYS:
            continue
        title_lower = entry["title"].lower()
        if any(kw.lower() in title_lower for kw in DECAY_KEYWORDS):
            stale_entries.append({
                "n":    entry["n"],
                "title": entry["title"],
                "date":  entry["date"],
                "age_days": age,
            })

    return {
        "domains_used":    domains_used,
        "skill_snapshot":  skill_snapshot,
        "btw_pending":     btw_pending,
        "btw_count":       len(btw_pending),
        "stale_entries":   stale_entries,
        "stale_count":     len(stale_entries),
    }


def cmd_git_status(argv: list) -> dict:
    if not argv:
        return {"error": "git-status requires a directory argument"}
    return push_status(argv[0])


def cmd_resolve_partner(argv: list) -> dict:
    if not argv:
        return {"error": "resolve-partner requires a skill name"}
    name = argv[0]
    path = find_skill(name)
    return {"name": name, "path": path, "found": bool(path)}


def cmd_plugin_versions() -> dict:
    prefixes = [
        ("MJ-test",             "MJ-test-"),
        ("MJ-plan",             "MJ-plan-"),
        ("MJ-codebase-review",  "MJ-codebase-review-"),
        ("mj-design",           "mj-design-"),
        ("mj-smart-run",        "mj-smart-run"),
        ("mj-clarify",          "mj-clarify-"),
        ("mj-experiencing",     "mj-experiencing-"),
        ("mj-end",              "mj-end-"),
        ("mj-ceo",              "mj-ceo-"),
    ]
    return {name: latest_plugin(prefix) for name, prefix in prefixes}


# ── dispatch ──────────────────────────────────────────────────────────────────

COMMANDS = {
    "ceo-preflight":   lambda rest: cmd_ceo_preflight(),
    "end-preflight":   lambda rest: cmd_end_preflight(rest),
    "git-status":      lambda rest: cmd_git_status(rest),
    "resolve-partner": lambda rest: cmd_resolve_partner(rest),
    "plugin-versions": lambda rest: cmd_plugin_versions(),
    "session-digest":  lambda rest: cmd_session_digest(rest),
}


def main() -> None:
    argv = sys.argv[1:]
    if not argv or argv[0] not in COMMANDS:
        available = ", ".join(COMMANDS)
        print(json.dumps({"error": f"unknown subcommand. available: {available}"}))
        sys.exit(1)

    result = COMMANDS[argv[0]](argv[1:])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
