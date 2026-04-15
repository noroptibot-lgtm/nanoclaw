#!/usr/bin/env python3
"""Hacker News CLI — browse stories, search, read comments, view user profiles."""

import argparse
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from html.parser import HTMLParser

# Build an SSL context — try default certs first, fall back to unverified
# if the system has no certificate bundle configured (common on macOS).
try:
    _ssl_ctx = ssl.create_default_context()
    # Quick smoke test — will raise if no certs are loadable
    urllib.request.urlopen(
        urllib.request.Request("https://hacker-news.firebaseio.com/v0/maxitem.json",
                               headers={"User-Agent": "HN-CLI/1.0"}),
        timeout=5, context=_ssl_ctx,
    )
except Exception:
    _ssl_ctx = ssl.create_default_context()
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE

FIREBASE_BASE = "https://hacker-news.firebaseio.com/v0"
ALGOLIA_BASE = "https://hn.algolia.com/api/v1"
TIMEOUT = 15


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class HTMLStripper(HTMLParser):
    """Strip HTML tags and decode entities into plain text."""

    def __init__(self):
        super().__init__()
        self.pieces = []

    def handle_data(self, data):
        self.pieces.append(data)

    def handle_entityref(self, name):
        mapping = {"amp": "&", "lt": "<", "gt": ">", "quot": '"', "apos": "'"}
        self.pieces.append(mapping.get(name, f"&{name};"))

    def handle_charref(self, name):
        try:
            if name.startswith("x"):
                self.pieces.append(chr(int(name[1:], 16)))
            else:
                self.pieces.append(chr(int(name)))
        except (ValueError, OverflowError):
            self.pieces.append(f"&#{name};")

    def get_text(self):
        return "".join(self.pieces)


def strip_html(html_text):
    if not html_text:
        return ""
    # Replace <p> and <br> with newlines before stripping
    text = re.sub(r"<br\s*/?>", "\n", html_text, flags=re.IGNORECASE)
    text = re.sub(r"<p>", "\n", text, flags=re.IGNORECASE)
    stripper = HTMLStripper()
    stripper.feed(text)
    return stripper.get_text().strip()


def relative_time(unix_ts):
    if not unix_ts:
        return "?"
    diff = int(time.time()) - unix_ts
    if diff < 0:
        return "just now"
    if diff < 60:
        return f"{diff}s ago"
    if diff < 3600:
        return f"{diff // 60}m ago"
    if diff < 86400:
        return f"{diff // 3600}h ago"
    days = diff // 86400
    if days < 30:
        return f"{days}d ago"
    if days < 365:
        return f"{days // 30}mo ago"
    return f"{days // 365}y ago"


def domain_of(url):
    if not url:
        return ""
    # Simple domain extraction without urllib.parse for brevity
    url = url.split("://", 1)[-1]
    url = url.split("/", 1)[0]
    url = url.split("?", 1)[0]
    if url.startswith("www."):
        url = url[4:]
    return url


def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HN-CLI/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=_ssl_ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} fetching {url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def fetch_firebase_item(item_id):
    return fetch_json(f"{FIREBASE_BASE}/item/{item_id}.json")


def fetch_story_ids(endpoint):
    return fetch_json(f"{FIREBASE_BASE}/{endpoint}.json")


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_stories(items, start_rank=1):
    for i, item in enumerate(items, start=start_rank):
        if item is None:
            continue
        title = item.get("title", "(no title)")
        url = item.get("url", "")
        dom = f" ({domain_of(url)})" if url else ""
        points = item.get("score", 0)
        author = item.get("by", "?")
        num_comments = item.get("descendants", 0)
        ts = relative_time(item.get("time"))
        item_id = item.get("id", "")

        print(f"  {i:>3}. {title}{dom}")
        print(f"       {points} pts | {num_comments} comments | by {author} | {ts} | id:{item_id}")
        print()


def print_search_results(hits):
    for i, hit in enumerate(hits, 1):
        title = hit.get("title", "(no title)")
        url = hit.get("url", "")
        dom = f" ({domain_of(url)})" if url else ""
        points = hit.get("points") or 0
        num_comments = hit.get("num_comments") or 0
        created = hit.get("created_at", "")
        # Parse ISO date to something short
        date_str = created[:10] if created else "?"
        object_id = hit.get("objectID", "")

        print(f"  {i:>3}. {title}{dom}")
        print(f"       {points} pts | {num_comments} comments | {date_str} | id:{object_id}")
        print()


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_stories(args, endpoint, label):
    ids = fetch_story_ids(endpoint)
    ids = ids[: args.limit]
    print(f"\n  {label} ({len(ids)} stories)\n")
    items = []
    for sid in ids:
        items.append(fetch_firebase_item(sid))
    print_stories(items)


def cmd_top(args):
    cmd_stories(args, "topstories", "Top Stories")


def cmd_new(args):
    cmd_stories(args, "newstories", "New Stories")


def cmd_best(args):
    cmd_stories(args, "beststories", "Best Stories")


def cmd_ask(args):
    cmd_stories(args, "askstories", "Ask HN")


def cmd_show(args):
    cmd_stories(args, "showstories", "Show HN")


def cmd_jobs(args):
    ids = fetch_story_ids("jobstories")
    ids = ids[: args.limit]
    print(f"\n  Job Postings ({len(ids)} listings)\n")
    for i, sid in enumerate(ids, 1):
        item = fetch_firebase_item(sid)
        if item is None:
            continue
        title = item.get("title", "(no title)")
        url = item.get("url", "")
        dom = f" ({domain_of(url)})" if url else ""
        ts = relative_time(item.get("time"))
        print(f"  {i:>3}. {title}{dom}")
        print(f"       {ts} | id:{item.get('id', '')}")
        print()


def cmd_search(args):
    query = urllib.request.quote(args.query)
    if args.sort == "date":
        endpoint = f"{ALGOLIA_BASE}/search_by_date?query={query}&tags=story&hitsPerPage={args.limit}"
    else:
        endpoint = f"{ALGOLIA_BASE}/search?query={query}&tags=story&hitsPerPage={args.limit}"
    data = fetch_json(endpoint)
    hits = data.get("hits", [])
    sort_label = "by date" if args.sort == "date" else "by popularity"
    print(f"\n  Search: \"{args.query}\" ({sort_label}, {len(hits)} results)\n")
    if not hits:
        print("  No results found.\n")
        return
    print_search_results(hits)


def cmd_comments(args):
    data = fetch_json(f"{ALGOLIA_BASE}/items/{args.story_id}")
    title = data.get("title", "(no title)")
    print(f"\n  Comments on: {title} (id:{args.story_id})\n")
    children = data.get("children", [])
    if not children:
        print("  No comments found.\n")
        return
    for i, child in enumerate(children, 1):
        author = child.get("author") or "[deleted]"
        text = strip_html(child.get("text", ""))
        points = child.get("points")
        pts_str = f"{points} pts | " if points else ""
        ts = relative_time(child.get("created_at_i"))
        if not text:
            text = "[deleted]"
        # Indent comment text
        wrapped = text.replace("\n", "\n       ")
        print(f"  {i:>3}. {author} | {pts_str}{ts}")
        print(f"       {wrapped}")
        print()


def cmd_user(args):
    data = fetch_json(f"{FIREBASE_BASE}/user/{args.username}.json")
    if data is None:
        print(f"\n  User '{args.username}' not found.\n")
        sys.exit(1)
    username = data.get("id", args.username)
    karma = data.get("karma", 0)
    created = data.get("created")
    about = strip_html(data.get("about", ""))
    submitted = data.get("submitted", [])

    created_str = ""
    if created:
        created_str = datetime.fromtimestamp(created, tz=None).strftime("%Y-%m-%d")
        created_str += f" ({relative_time(created)})"

    print(f"\n  User: {username}")
    print(f"  Karma: {karma:,}")
    print(f"  Created: {created_str}")
    print(f"  Submissions: {len(submitted):,}")
    if about:
        print(f"  About: {about}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Browse Hacker News from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="command to run")

    p_top = sub.add_parser("top", help="Top stories from HN front page")
    p_top.add_argument("--limit", type=int, default=15, help="Number of stories (default: 15)")
    p_top.set_defaults(func=cmd_top)

    p_new = sub.add_parser("new", help="Newest stories")
    p_new.add_argument("--limit", type=int, default=15, help="Number of stories (default: 15)")
    p_new.set_defaults(func=cmd_new)

    p_best = sub.add_parser("best", help="Best stories")
    p_best.add_argument("--limit", type=int, default=15, help="Number of stories (default: 15)")
    p_best.set_defaults(func=cmd_best)

    p_ask = sub.add_parser("ask", help="Ask HN posts")
    p_ask.add_argument("--limit", type=int, default=10, help="Number of posts (default: 10)")
    p_ask.set_defaults(func=cmd_ask)

    p_show = sub.add_parser("show", help="Show HN posts")
    p_show.add_argument("--limit", type=int, default=10, help="Number of posts (default: 10)")
    p_show.set_defaults(func=cmd_show)

    p_jobs = sub.add_parser("jobs", help="Job postings")
    p_jobs.add_argument("--limit", type=int, default=10, help="Number of listings (default: 10)")
    p_jobs.set_defaults(func=cmd_jobs)

    p_search = sub.add_parser("search", help="Search HN stories")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--sort", choices=["date", "popularity"], default="popularity", help="Sort order (default: popularity)")
    p_search.add_argument("--limit", type=int, default=15, help="Number of results (default: 15)")
    p_search.set_defaults(func=cmd_search)

    p_comments = sub.add_parser("comments", help="Show comments on a story")
    p_comments.add_argument("story_id", help="Story ID")
    p_comments.set_defaults(func=cmd_comments)

    p_user = sub.add_parser("user", help="Show user profile")
    p_user.add_argument("username", help="HN username")
    p_user.set_defaults(func=cmd_user)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
