#!/usr/bin/env python3
"""Wikipedia skill — search and read Wikipedia articles via the MediaWiki API."""

import argparse
import html
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

API_URL = "https://en.wikipedia.org/w/api.php"
REST_URL = "https://en.wikipedia.org/api/rest_v1"
TIMEOUT = 15

# Build an SSL context — try default certs first, fall back to unverified
# (common on macOS where Python may not find system certs).
try:
    _ssl_ctx = ssl.create_default_context()
    # Quick test — if this fails, certs are missing
    urllib.request.urlopen("https://en.wikipedia.org/w/api.php?action=query&meta=siteinfo&format=json",
                           timeout=5, context=_ssl_ctx)
except Exception:
    _ssl_ctx = ssl.create_default_context()
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE


def api_request(params):
    """Make a request to the MediaWiki API."""
    params["format"] = "json"
    url = API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "ClaudeCodeWikipediaSkill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=_ssl_ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} — {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def rest_request(path):
    """Make a request to the Wikimedia REST API."""
    url = REST_URL + path
    req = urllib.request.Request(url, headers={
        "User-Agent": "ClaudeCodeWikipediaSkill/1.0",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=_ssl_ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} — {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def strip_html(text):
    """Remove HTML tags and unescape entities."""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def article_url(title):
    """Build a Wikipedia article URL from a title."""
    encoded = urllib.parse.quote(title.replace(" ", "_"), safe="/:()")
    return f"https://en.wikipedia.org/wiki/{encoded}"


def is_disambiguation(extract):
    """Heuristic check for disambiguation pages."""
    if not extract:
        return False
    lower = extract.lower()
    return "may refer to:" in lower or "can refer to:" in lower or "commonly refers to:" in lower


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_search(args):
    """Search Wikipedia articles."""
    data = api_request({
        "action": "query",
        "list": "search",
        "srsearch": args.query,
        "srlimit": args.limit,
    })
    results = data.get("query", {}).get("search", [])
    if not results:
        print("No results found.")
        return

    print(f"Search results for: {args.query}\n")
    for i, r in enumerate(results, 1):
        snippet = strip_html(r.get("snippet", ""))
        words = r.get("wordcount", 0)
        ts = r.get("timestamp", "")[:10]
        title = r.get("title", "")
        print(f"  {i}. {title}")
        print(f"     {snippet}")
        print(f"     Words: {words}  |  Updated: {ts}")
        print()


def cmd_summary(args):
    """Get article summary/extract."""
    data = api_request({
        "action": "query",
        "prop": "extracts|categories",
        "exintro": 1,
        "explaintext": 1,
        "cllimit": "max",
        "titles": args.title,
        "redirects": 1,
    })
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()))

    if page.get("missing") is not None:
        print(f"Article not found: {args.title}")
        return

    title = page.get("title", args.title)
    extract = page.get("extract", "").strip()
    categories = page.get("categories", [])

    if not extract:
        print(f"No summary available for: {title}")
        return

    print(f"=== {title} ===")
    print(f"URL: {article_url(title)}")
    print(f"Categories: {len(categories)}")
    if is_disambiguation(extract):
        print("Note: This appears to be a disambiguation page.")
    print()
    print(extract)


def cmd_article(args):
    """Get full article text."""
    if args.section is not None:
        # Use action=parse for specific section
        data = api_request({
            "action": "parse",
            "page": args.title,
            "section": args.section,
            "prop": "wikitext",
            "redirects": 1,
        })
        if "error" in data:
            print(f"Error: {data['error'].get('info', 'Unknown error')}")
            return
        title = data.get("parse", {}).get("title", args.title)
        wikitext = data.get("parse", {}).get("wikitext", {}).get("*", "")
        # Basic wikitext cleanup
        text = re.sub(r"\{\{[^}]*\}\}", "", wikitext)  # remove templates
        text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", text)  # [[link|text]] -> text
        text = re.sub(r"'{2,3}", "", text)  # remove bold/italic markup
        text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.DOTALL)  # remove refs
        text = re.sub(r"<ref[^/]*/>", "", text)  # remove self-closing refs
        text = re.sub(r"<[^>]+>", "", text)  # remove remaining HTML
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
    else:
        data = api_request({
            "action": "query",
            "prop": "extracts",
            "explaintext": 1,
            "titles": args.title,
            "redirects": 1,
        })
        pages = data.get("query", {}).get("pages", {})
        page = next(iter(pages.values()))
        if page.get("missing") is not None:
            print(f"Article not found: {args.title}")
            return
        title = page.get("title", args.title)
        text = page.get("extract", "").strip()

    if not text:
        print(f"No content available for: {args.title}")
        return

    print(f"=== {title} ===")
    print(f"URL: {article_url(title)}")
    if is_disambiguation(text):
        print("Note: This appears to be a disambiguation page.")
    print()

    max_chars = 5000
    if len(text) > max_chars:
        print(text[:max_chars])
        print(f"\n... [Truncated — showing {max_chars} of {len(text)} characters. Use --section to read specific sections.]")
    else:
        print(text)


def cmd_sections(args):
    """List sections of an article."""
    data = api_request({
        "action": "parse",
        "page": args.title,
        "prop": "sections",
        "redirects": 1,
    })
    if "error" in data:
        print(f"Error: {data['error'].get('info', 'Unknown error')}")
        return

    title = data.get("parse", {}).get("title", args.title)
    sections = data.get("parse", {}).get("sections", [])

    if not sections:
        print(f"No sections found for: {title}")
        return

    print(f"Sections of: {title}\n")
    for s in sections:
        level = int(s.get("toclevel", 1))
        indent = "  " * (level - 1)
        index = s.get("index", "")
        line = s.get("line", "")
        print(f"  {indent}[{index}] {line}")


def cmd_random(args):
    """Get a random article summary."""
    data = api_request({
        "action": "query",
        "list": "random",
        "rnnamespace": 0,
        "rnlimit": 1,
    })
    results = data.get("query", {}).get("random", [])
    if not results:
        print("Could not fetch a random article.")
        return

    title = results[0].get("title", "")

    # Now fetch the summary
    data = api_request({
        "action": "query",
        "prop": "extracts",
        "exintro": 1,
        "explaintext": 1,
        "titles": title,
        "redirects": 1,
    })
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()))
    extract = page.get("extract", "").strip()

    print(f"=== {title} ===")
    print(f"URL: {article_url(title)}")
    print()
    if extract:
        print(extract)
    else:
        print("(No extract available for this article.)")


def cmd_today(args):
    """Show featured article and 'On this day' events."""
    now = datetime.now()
    yyyy = now.strftime("%Y")
    mm = now.strftime("%m")
    dd = now.strftime("%d")

    data = rest_request(f"/feed/featured/{yyyy}/{mm}/{dd}")

    # Featured article
    tfa = data.get("tfa")
    if tfa:
        title = tfa.get("title", tfa.get("normalizedtitle", "Unknown"))
        extract = tfa.get("extract", "")
        print(f"=== Featured Article: {title} ===")
        print(f"URL: {article_url(title)}")
        print()
        print(extract)
        print()

    # On this day
    otd = data.get("onthisday", [])
    if otd:
        print(f"=== On This Day ({mm}/{dd}) ===\n")
        for event in otd[:5]:
            year = event.get("year", "?")
            text = event.get("text", "")
            print(f"  {year} — {text}")
        if len(otd) > 5:
            print(f"\n  ... and {len(otd) - 5} more events.")
    elif not tfa:
        print("No featured content available for today.")


def cmd_links(args):
    """Show internal links from an article."""
    data = api_request({
        "action": "query",
        "prop": "links",
        "titles": args.title,
        "pllimit": args.limit,
        "plnamespace": 0,
        "redirects": 1,
    })
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()))

    if page.get("missing") is not None:
        print(f"Article not found: {args.title}")
        return

    title = page.get("title", args.title)
    links = page.get("links", [])

    if not links:
        print(f"No links found in: {title}")
        return

    print(f"Links from: {title}\n")
    for i, link in enumerate(links, 1):
        lt = link.get("title", "")
        print(f"  {i}. {lt}")


def cmd_langs(args):
    """Show available languages for an article."""
    data = api_request({
        "action": "query",
        "prop": "langlinks",
        "titles": args.title,
        "lllimit": "max",
        "redirects": 1,
    })
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()))

    if page.get("missing") is not None:
        print(f"Article not found: {args.title}")
        return

    title = page.get("title", args.title)
    langs = page.get("langlinks", [])

    if not langs:
        print(f"No other languages found for: {title}")
        return

    print(f"Languages for: {title} ({len(langs)} languages)\n")
    for lang in langs:
        code = lang.get("lang", "")
        foreign_title = lang.get("*", "")
        print(f"  {code:>8}  {foreign_title}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Search and read Wikipedia articles.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # search
    p = sub.add_parser("search", help="Search Wikipedia articles")
    p.add_argument("query", help="Search query")
    p.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")

    # summary
    p = sub.add_parser("summary", help="Get article summary/extract")
    p.add_argument("title", help="Article title")

    # article
    p = sub.add_parser("article", help="Get full article text")
    p.add_argument("title", help="Article title")
    p.add_argument("--section", type=int, default=None, help="Section index (use 'sections' command to list)")

    # sections
    p = sub.add_parser("sections", help="List sections of an article")
    p.add_argument("title", help="Article title")

    # random
    sub.add_parser("random", help="Get a random article summary")

    # today
    sub.add_parser("today", help="Featured article and 'On this day' events")

    # links
    p = sub.add_parser("links", help="Show links from an article")
    p.add_argument("title", help="Article title")
    p.add_argument("--limit", type=int, default=20, help="Max links (default: 20)")

    # langs
    p = sub.add_parser("langs", help="Show available languages for an article")
    p.add_argument("title", help="Article title")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "search": cmd_search,
        "summary": cmd_summary,
        "article": cmd_article,
        "sections": cmd_sections,
        "random": cmd_random,
        "today": cmd_today,
        "links": cmd_links,
        "langs": cmd_langs,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
