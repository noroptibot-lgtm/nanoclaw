#!/usr/bin/env python3
"""Manage Obsidian vaults as plain markdown files. No external dependencies."""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Vault discovery
# ---------------------------------------------------------------------------

OBSIDIAN_CONFIG = Path.home() / "Library" / "Application Support" / "obsidian" / "obsidian.json"


def _load_obsidian_config():
    """Return parsed obsidian.json or None."""
    if OBSIDIAN_CONFIG.exists():
        try:
            return json.loads(OBSIDIAN_CONFIG.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
    return None


def discover_vaults():
    """Return list of dicts with 'name', 'path', 'open' from obsidian.json."""
    cfg = _load_obsidian_config()
    if not cfg or "vaults" not in cfg:
        return []
    vaults = []
    for vid, info in cfg["vaults"].items():
        vpath = Path(info.get("path", ""))
        vaults.append({
            "id": vid,
            "name": vpath.name,
            "path": str(vpath),
            "open": info.get("open", False),
        })
    return vaults


def resolve_vault(args_vault=None):
    """Determine vault root Path from flag, env var, or auto-detect.

    Priority: --vault flag > OBSIDIAN_VAULT env > first open vault > first vault.
    """
    # Explicit flag
    if args_vault:
        p = Path(args_vault).expanduser().resolve()
        if p.is_dir():
            return p
        # Maybe it's a vault name, not a path
        for v in discover_vaults():
            if v["name"].lower() == args_vault.lower():
                return Path(v["path"])
        _die(f"Vault not found: {args_vault}")

    # Env var
    env = os.environ.get("OBSIDIAN_VAULT")
    if env:
        p = Path(env).expanduser().resolve()
        if p.is_dir():
            return p
        _die(f"OBSIDIAN_VAULT path does not exist: {env}")

    # Auto-detect from obsidian.json
    vaults = discover_vaults()
    if not vaults:
        _die("No vaults found. Set OBSIDIAN_VAULT or pass --vault.")
    # Prefer open vault
    for v in vaults:
        if v["open"]:
            return Path(v["path"])
    return Path(vaults[0]["path"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _die(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def _md_files(vault: Path):
    """Yield all .md files in vault, skipping .obsidian and hidden dirs."""
    for p in vault.rglob("*.md"):
        parts = p.relative_to(vault).parts
        if any(part.startswith(".") for part in parts):
            continue
        yield p


def _relative(path: Path, vault: Path) -> str:
    """Return relative path string from vault root."""
    try:
        return str(path.relative_to(vault))
    except ValueError:
        return str(path)


def _parse_frontmatter(text: str):
    """Extract YAML frontmatter as raw string and end index. Returns (dict-like, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_raw = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    # Minimal YAML parsing for tags (no pyyaml needed)
    fm = {}
    for line in fm_raw.splitlines():
        m = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            fm[key] = val
    # Parse tags list (handle both inline and multi-line)
    tags = []
    in_tags = False
    for line in fm_raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("tags:"):
            in_tags = True
            # Inline list: tags: [a, b, c] or tags: a, b
            rest = stripped[5:].strip()
            if rest.startswith("["):
                items = rest.strip("[]").split(",")
                tags.extend(t.strip().strip("'\"") for t in items if t.strip())
                in_tags = False
            elif rest:
                tags.extend(t.strip().strip("'\"") for t in rest.split(",") if t.strip())
                in_tags = False
            continue
        if in_tags:
            if stripped.startswith("- "):
                tags.append(stripped[2:].strip().strip("'\""))
            else:
                in_tags = False
    fm["_tags"] = tags
    return fm, body


def _inline_tags(text: str):
    """Find all #tag occurrences in text (not inside code blocks)."""
    # Strip code blocks
    cleaned = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    cleaned = re.sub(r"`[^`]+`", "", cleaned)
    return set(re.findall(r"(?:^|(?<=\s))#([\w][\w/-]*)", cleaned))


def _build_frontmatter(tags):
    """Build YAML frontmatter string for given tags list."""
    lines = ["---"]
    if tags:
        lines.append("tags:")
        for t in tags:
            lines.append(f"  - {t}")
    lines.append(f"date: {date.today().isoformat()}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def _ensure_md(path_str: str) -> str:
    """Ensure path string ends with .md."""
    if not path_str.lower().endswith(".md"):
        return path_str + ".md"
    return path_str


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_vaults(args):
    vaults = discover_vaults()
    if not vaults:
        print("No Obsidian vaults found.")
        print(f"Looked in: {OBSIDIAN_CONFIG}")
        return
    for v in vaults:
        marker = " (open)" if v["open"] else ""
        print(f"  {v['name']}{marker}")
        print(f"    {v['path']}")


def cmd_notes(args):
    vault = resolve_vault(args.vault)
    notes = sorted(_md_files(vault), key=lambda p: p.name.lower())
    if args.search:
        pattern = args.search.lower()
        notes = [n for n in notes if pattern in n.name.lower()]
    if not notes:
        print("No notes found.")
        return
    for n in notes:
        print(_relative(n, vault))


def cmd_read(args):
    vault = resolve_vault(args.vault)
    target = vault / _ensure_md(args.path)
    if not target.exists():
        _die(f"Note not found: {_relative(target, vault)}")
    print(target.read_text(encoding="utf-8"))


def cmd_create(args):
    vault = resolve_vault(args.vault)
    rel = _ensure_md(args.path)
    target = vault / rel
    if target.exists() and not args.force:
        _die(f"Note already exists: {rel}  (use --force to overwrite)")
    target.parent.mkdir(parents=True, exist_ok=True)

    content = ""
    if args.tags:
        content += _build_frontmatter(args.tags)
    if args.content:
        content += args.content
    if not content:
        content = ""

    target.write_text(content, encoding="utf-8")
    print(f"Created: {rel}")


def cmd_daily(args):
    vault = resolve_vault(args.vault)
    today = date.today().isoformat()  # YYYY-MM-DD
    daily_dir = vault / "Daily Notes"
    daily_dir.mkdir(parents=True, exist_ok=True)
    target = daily_dir / f"{today}.md"

    if target.exists():
        print(f"Daily note exists: Daily Notes/{today}.md")
        print(target.read_text(encoding="utf-8"))
        return

    content = _build_frontmatter(["daily-note"])
    content += f"# {today}\n\n"
    content += "## Tasks\n\n- [ ] \n\n## Notes\n\n"
    target.write_text(content, encoding="utf-8")
    print(f"Created daily note: Daily Notes/{today}.md")


def cmd_search(args):
    vault = resolve_vault(args.vault)
    query = args.query.lower()
    found = 0
    for md in sorted(_md_files(vault)):
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if query in line.lower():
                rel = _relative(md, vault)
                print(f"{rel}:{i}: {line.rstrip()}")
                found += 1
    if found == 0:
        print("No matches found.")
    else:
        print(f"\n{found} match(es) found.")


def cmd_tags(args):
    vault = resolve_vault(args.vault)
    all_tags: dict[str, int] = {}
    for md in _md_files(vault):
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # Frontmatter tags
        fm, body = _parse_frontmatter(text)
        for t in fm.get("_tags", []):
            all_tags[t] = all_tags.get(t, 0) + 1
        # Inline tags
        for t in _inline_tags(text):
            all_tags[t] = all_tags.get(t, 0) + 1

    if not all_tags:
        print("No tags found.")
        return
    for tag, count in sorted(all_tags.items(), key=lambda x: (-x[1], x[0])):
        print(f"  #{tag}  ({count})")


def cmd_links(args):
    vault = resolve_vault(args.vault)
    target_path = _ensure_md(args.path)
    target_name = Path(target_path).stem  # Note name without .md

    backlinks = []
    for md in _md_files(vault):
        if md == vault / target_path:
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # Match [[Note Name]] or [[path/Note Name]] or [[Note Name|alias]]
        wikilinks = re.findall(r"\[\[([^\]]+?)(?:\|[^\]]+?)?\]\]", text)
        for link in wikilinks:
            link_name = Path(link).stem
            if link_name.lower() == target_name.lower():
                backlinks.append(_relative(md, vault))
                break

    if not backlinks:
        print(f"No backlinks to: {target_path}")
        return
    print(f"Backlinks to {target_path}:")
    for bl in sorted(backlinks):
        print(f"  {bl}")


def cmd_recent(args):
    vault = resolve_vault(args.vault)
    notes = list(_md_files(vault))
    notes.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    limit = args.limit if hasattr(args, "limit") and args.limit else 10
    for n in notes[:limit]:
        from datetime import datetime
        mtime = datetime.fromtimestamp(n.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"  {mtime}  {_relative(n, vault)}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="obsidian",
        description="Manage Obsidian vaults as plain markdown files.",
    )
    parser.add_argument("--vault", help="Vault path or name (overrides auto-detect)")
    sub = parser.add_subparsers(dest="command")

    # vaults
    sub.add_parser("vaults", help="List discovered Obsidian vaults")

    # notes
    p_notes = sub.add_parser("notes", help="List notes in the vault")
    p_notes.add_argument("--search", "-s", help="Filter notes by filename substring")

    # read
    p_read = sub.add_parser("read", help="Read a note's contents")
    p_read.add_argument("path", help="Relative path to the note inside the vault")

    # create
    p_create = sub.add_parser("create", help="Create a new note")
    p_create.add_argument("path", help="Relative path for the new note")
    p_create.add_argument("content", nargs="?", default="", help="Note content")
    p_create.add_argument("--tags", nargs="+", help="Tags to add in frontmatter")
    p_create.add_argument("--force", action="store_true", help="Overwrite if exists")

    # daily
    sub.add_parser("daily", help="Create or open today's daily note")

    # search
    p_search = sub.add_parser("search", help="Full-text search across vault")
    p_search.add_argument("query", help="Search query (case-insensitive)")

    # tags
    sub.add_parser("tags", help="List all tags used in the vault")

    # links
    p_links = sub.add_parser("links", help="Show backlinks to a note")
    p_links.add_argument("path", help="Relative path to the note")

    # recent
    p_recent = sub.add_parser("recent", help="Show recently modified notes")
    p_recent.add_argument("--limit", "-n", type=int, default=10, help="Number of notes (default 10)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "vaults": cmd_vaults,
        "notes": cmd_notes,
        "read": cmd_read,
        "create": cmd_create,
        "daily": cmd_daily,
        "search": cmd_search,
        "tags": cmd_tags,
        "links": cmd_links,
        "recent": cmd_recent,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
