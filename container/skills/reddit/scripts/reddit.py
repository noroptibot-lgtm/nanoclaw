#!/usr/bin/env python3
"""Reddit browser using Reddit's public JSON API. No auth required."""

import argparse
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://www.reddit.com"
USER_AGENT = "python:claude-code-reddit:v1.0 (by /u/claude-code-skill)"
_last_request_time = 0

# Build SSL context: try default certs first, fall back to unverified if unavailable
try:
    _ssl_ctx = ssl.create_default_context()
    # Quick test that the cert store loaded
    urllib.request.urlopen(
        urllib.request.Request("https://www.reddit.com/r/all.json?limit=1",
                               headers={"User-Agent": USER_AGENT}),
        timeout=5, context=_ssl_ctx,
    ).close()
except Exception:
    _ssl_ctx = ssl.create_default_context()
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE


def _fetch(path, params=None):
    """Fetch JSON from Reddit's public API."""
    global _last_request_time

    # Rate limiting: at least 1 second between requests
    elapsed = time.time() - _last_request_time
    if _last_request_time > 0 and elapsed < 1.0:
        time.sleep(1.0 - elapsed)

    url = f"{BASE_URL}{path}.json"
    if params:
        # Filter out None values
        params = {k: v for k, v in params.items() if v is not None}
        if params:
            url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15, context=_ssl_ctx) as resp:
            _last_request_time = time.time()
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: Not found (404). Check that the subreddit, user, or post exists.", file=sys.stderr)
        elif e.code == 429:
            print(f"Error: Rate limited by Reddit (429). Wait a moment and try again.", file=sys.stderr)
        elif e.code == 403:
            print(f"Error: Forbidden (403). The resource may be private.", file=sys.stderr)
        else:
            print(f"Error: HTTP {e.code} — {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Could not connect to Reddit — {e.reason}", file=sys.stderr)
        sys.exit(1)


def _relative_time(unix_ts):
    """Convert unix timestamp to relative time string like '2h ago'."""
    if not unix_ts:
        return "unknown"
    diff = int(time.time() - unix_ts)
    if diff < 0:
        return "just now"
    if diff < 60:
        return f"{diff}s ago"
    if diff < 3600:
        return f"{diff // 60}m ago"
    if diff < 86400:
        return f"{diff // 3600}h ago"
    if diff < 2592000:
        return f"{diff // 86400}d ago"
    if diff < 31536000:
        return f"{diff // 2592000}mo ago"
    return f"{diff // 31536000}y ago"


def _truncate(text, length=200):
    """Truncate text to a max length."""
    if not text:
        return ""
    text = text.replace("\n", " ").strip()
    if len(text) <= length:
        return text
    return text[:length - 3] + "..."


def _extract_post_id(id_or_url):
    """Extract a Reddit post ID from a post ID string or full URL."""
    # Full URL like https://www.reddit.com/r/python/comments/abc123/some_title/
    m = re.search(r"/comments/([a-z0-9]+)", id_or_url)
    if m:
        return m.group(1)
    # Just the ID, possibly with t3_ prefix
    if id_or_url.startswith("t3_"):
        return id_or_url[3:]
    return id_or_url


def _print_posts(posts):
    """Print a list of post data dicts."""
    if not posts:
        print("No posts found.")
        return
    for i, p in enumerate(posts, 1):
        print(f"[{i}] {p['title']}")
        print(f"    Score: {p['score']}  |  Comments: {p['num_comments']}  |  By: u/{p['author']}  |  {_relative_time(p.get('created_utc'))}")
        print(f"    ID: {p.get('id', 'N/A')}  |  r/{p.get('subreddit', 'N/A')}")
        if p.get('selftext'):
            print(f"    {_truncate(p['selftext'])}")
        if p.get('url') and not p['url'].startswith(f"{BASE_URL}/r/"):
            print(f"    Link: {p['url']}")
        print(f"    Permalink: {BASE_URL}{p.get('permalink', '')}")
        print()


def cmd_posts(args):
    """List posts from a subreddit."""
    params = {"limit": args.limit}
    if args.sort == "top" and args.time:
        params["t"] = args.time
    data = _fetch(f"/r/{args.subreddit}/{args.sort}", params)
    children = data.get("data", {}).get("children", [])
    posts = [c["data"] for c in children if c.get("kind") == "t3"]
    _print_posts(posts)


def cmd_search(args):
    """Search posts on Reddit."""
    params = {
        "q": args.query,
        "sort": args.sort,
        "limit": args.limit,
        "restrict_sr": "on" if args.subreddit else None,
    }
    path = f"/r/{args.subreddit}/search" if args.subreddit else "/search"
    data = _fetch(path, params)
    children = data.get("data", {}).get("children", [])
    posts = [c["data"] for c in children if c.get("kind") == "t3"]
    _print_posts(posts)


def cmd_comments(args):
    """Get comments on a post."""
    post_id = _extract_post_id(args.post_id)
    data = _fetch(f"/comments/{post_id}", {"limit": args.limit, "depth": 1})

    # Reddit returns a list: [post_listing, comments_listing]
    if not isinstance(data, list) or len(data) < 2:
        print("Error: Unexpected response format.", file=sys.stderr)
        sys.exit(1)

    # Print post info first
    post_children = data[0].get("data", {}).get("children", [])
    if post_children:
        p = post_children[0].get("data", {})
        print(f"Post: {p.get('title', 'N/A')}")
        print(f"By: u/{p.get('author', 'N/A')}  |  Score: {p.get('score', 0)}  |  Comments: {p.get('num_comments', 0)}  |  {_relative_time(p.get('created_utc'))}")
        if p.get("selftext"):
            print(f"\n{_truncate(p['selftext'], 500)}")
        print()
        print("-" * 60)
        print()

    # Print comments
    comment_children = data[1].get("data", {}).get("children", [])
    comments = [c["data"] for c in comment_children if c.get("kind") == "t1"]
    if not comments:
        print("No comments found.")
        return
    for i, c in enumerate(comments, 1):
        body = _truncate(c.get("body", ""), 500)
        print(f"[{i}] u/{c.get('author', '[deleted]')}  |  Score: {c.get('score', 0)}  |  {_relative_time(c.get('created_utc'))}")
        print(f"    {body}")
        print()


def cmd_trending(args):
    """Show trending/popular posts across Reddit."""
    data = _fetch("/r/popular/hot", {"limit": args.limit})
    children = data.get("data", {}).get("children", [])
    posts = [c["data"] for c in children if c.get("kind") == "t3"]
    _print_posts(posts)


def cmd_user(args):
    """View a user's recent posts and comments."""
    username = args.username.lstrip("u/").lstrip("/u/")

    if args.type in ("posts", "both"):
        print(f"=== Recent Posts by u/{username} ===\n")
        data = _fetch(f"/user/{username}/submitted", {"limit": args.limit, "sort": "new"})
        children = data.get("data", {}).get("children", [])
        posts = [c["data"] for c in children if c.get("kind") == "t3"]
        _print_posts(posts)

    if args.type in ("comments", "both"):
        print(f"=== Recent Comments by u/{username} ===\n")
        data = _fetch(f"/user/{username}/comments", {"limit": args.limit, "sort": "new"})
        children = data.get("data", {}).get("children", [])
        comments = [c["data"] for c in children if c.get("kind") == "t1"]
        if not comments:
            print("No comments found.")
        for i, c in enumerate(comments, 1):
            body = _truncate(c.get("body", ""), 500)
            sub = c.get("subreddit", "?")
            link_title = c.get("link_title", "")
            print(f"[{i}] r/{sub} — {link_title}")
            print(f"    Score: {c.get('score', 0)}  |  {_relative_time(c.get('created_utc'))}")
            print(f"    {body}")
            print()


def cmd_subreddit(args):
    """Get subreddit info."""
    data = _fetch(f"/r/{args.name}/about")
    info = data.get("data", {})
    if not info:
        print("Error: Could not retrieve subreddit info.", file=sys.stderr)
        sys.exit(1)

    name = info.get("display_name_prefixed", f"r/{args.name}")
    title = info.get("title", "")
    desc = info.get("public_description") or info.get("description", "")
    subs = info.get("subscribers", 0)
    active = info.get("accounts_active", 0)
    created = info.get("created_utc")
    nsfw = info.get("over18", False)

    print(f"{name}")
    if title:
        print(f"Title: {title}")
    print(f"Subscribers: {subs:,}")
    print(f"Active users: {active:,}")
    if created:
        print(f"Created: {_relative_time(created)}")
    print(f"NSFW: {'Yes' if nsfw else 'No'}")
    if desc:
        print(f"\nDescription:\n{_truncate(desc, 1000)}")
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="reddit",
        description="Browse Reddit from the terminal using the public JSON API.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # posts
    p_posts = subparsers.add_parser("posts", help="List posts from a subreddit")
    p_posts.add_argument("subreddit", help="Subreddit name (without r/)")
    p_posts.add_argument("--sort", choices=["hot", "new", "top", "rising"], default="hot", help="Sort order (default: hot)")
    p_posts.add_argument("--time", choices=["hour", "day", "week", "month", "year", "all"], default="day", help="Time filter for top sort (default: day)")
    p_posts.add_argument("--limit", type=int, default=10, help="Number of posts (default: 10)")

    # search
    p_search = subparsers.add_parser("search", help="Search posts on Reddit")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--subreddit", help="Limit search to a specific subreddit")
    p_search.add_argument("--sort", choices=["relevance", "hot", "top", "new"], default="relevance", help="Sort order (default: relevance)")
    p_search.add_argument("--limit", type=int, default=10, help="Number of results (default: 10)")

    # comments
    p_comments = subparsers.add_parser("comments", help="Get comments on a post")
    p_comments.add_argument("post_id", help="Post ID or full Reddit URL")
    p_comments.add_argument("--limit", type=int, default=10, help="Number of comments (default: 10)")

    # trending
    p_trending = subparsers.add_parser("trending", help="Show trending/popular posts across Reddit")
    p_trending.add_argument("--limit", type=int, default=10, help="Number of posts (default: 10)")

    # user
    p_user = subparsers.add_parser("user", help="View a user's recent activity")
    p_user.add_argument("username", help="Reddit username (with or without u/)")
    p_user.add_argument("--type", choices=["posts", "comments", "both"], default="both", help="Type of content (default: both)")
    p_user.add_argument("--limit", type=int, default=10, help="Number of items (default: 10)")

    # subreddit
    p_subreddit = subparsers.add_parser("subreddit", help="Get subreddit info")
    p_subreddit.add_argument("name", help="Subreddit name (without r/)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "posts": cmd_posts,
        "search": cmd_search,
        "comments": cmd_comments,
        "trending": cmd_trending,
        "user": cmd_user,
        "subreddit": cmd_subreddit,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
