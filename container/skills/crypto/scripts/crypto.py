#!/usr/bin/env python3
"""Cryptocurrency price checker and market data tool using the free CoinGecko API."""

import argparse
import json
import ssl
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

BASE_URL = "https://api.coingecko.com/api/v3"
TIMEOUT = 15

# Build SSL context — try system certs first, fall back to unverified if needed
try:
    import certifi
    _ssl_ctx = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _ssl_ctx = ssl.create_default_context()
    # If default context also fails (common on macOS), allow unverified as last resort
    try:
        urllib.request.urlopen("https://api.coingecko.com", timeout=5, context=_ssl_ctx)
    except Exception:
        _ssl_ctx = ssl._create_unverified_context()


def api_get(endpoint, params=None):
    """Make a GET request to the CoinGecko API."""
    url = BASE_URL + endpoint
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "CryptoSkill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=_ssl_ctx) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print("Error: Rate limit exceeded. CoinGecko free API allows 10-30 calls/minute. Please wait and retry.")
        else:
            print(f"Error: HTTP {e.code} - {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Could not connect to CoinGecko API - {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def fmt_number(n, decimals=2):
    """Format a number with commas and specified decimal places."""
    if n is None:
        return "N/A"
    if abs(n) < 0.01 and n != 0:
        return f"{n:.8f}"
    if abs(n) < 1 and n != 0:
        return f"{n:.6f}"
    return f"{n:,.{decimals}f}"


def fmt_large(n):
    """Format large numbers as $1.2T, $45.3B, $123.4M etc."""
    if n is None:
        return "N/A"
    if abs(n) >= 1_000_000_000_000:
        return f"${n / 1_000_000_000_000:.2f}T"
    if abs(n) >= 1_000_000_000:
        return f"${n / 1_000_000_000:.2f}B"
    if abs(n) >= 1_000_000:
        return f"${n / 1_000_000:.2f}M"
    if abs(n) >= 1_000:
        return f"${n / 1_000:.2f}K"
    return f"${n:,.2f}"


def fmt_pct(n):
    """Format percentage with + or - prefix."""
    if n is None:
        return "N/A"
    sign = "+" if n >= 0 else ""
    return f"{sign}{n:.2f}%"


def fmt_price(n, currency="usd"):
    """Format a price value with appropriate precision and currency symbol."""
    if n is None:
        return "N/A"
    sym = "$" if currency == "usd" else currency.upper() + " "
    if abs(n) < 0.01 and n != 0:
        return f"{sym}{n:.8f}"
    if abs(n) < 1 and n != 0:
        return f"{sym}{n:.6f}"
    return f"{sym}{n:,.2f}"


def pad_right(s, width):
    """Pad string to width."""
    s = str(s)
    if len(s) >= width:
        return s[:width]
    return s + " " * (width - len(s))


def pad_left(s, width):
    """Right-align string to width."""
    s = str(s)
    if len(s) >= width:
        return s
    return " " * (width - len(s)) + s


# ── Commands ──────────────────────────────────────────────────────────────────


def cmd_price(args):
    """Get current price of one or more coins."""
    coins = args.coins.lower().strip()
    currency = args.currency.lower().strip()
    data = api_get("/simple/price", {
        "ids": coins,
        "vs_currencies": currency,
        "include_24hr_change": "true",
        "include_market_cap": "true",
    })
    if not data:
        print("No data returned. Check that the coin IDs are valid (e.g. bitcoin, ethereum, shiba-inu).")
        return

    print()
    print(f"  {'Coin':<20} {'Price':>18} {'24h Change':>14} {'Market Cap':>16}")
    print(f"  {'─' * 20} {'─' * 18} {'─' * 14} {'─' * 16}")
    for coin_id in coins.split(","):
        coin_id = coin_id.strip()
        if coin_id not in data:
            print(f"  {pad_right(coin_id, 20)} {'Not found':>18}")
            continue
        d = data[coin_id]
        price = d.get(currency)
        change = d.get(f"{currency}_24h_change")
        mcap = d.get(f"{currency}_market_cap")
        print(f"  {pad_right(coin_id, 20)} {fmt_price(price, currency):>18} {fmt_pct(change):>14} {fmt_large(mcap):>16}")
    print()


def cmd_top(args):
    """Show top coins by market cap."""
    currency = args.currency.lower().strip()
    data = api_get("/coins/markets", {
        "vs_currency": currency,
        "order": "market_cap_desc",
        "per_page": str(args.limit),
        "page": "1",
        "sparkline": "false",
    })
    if not data:
        print("No data returned.")
        return

    print()
    print(f"  {'#':>4}  {'Name':<22} {'Symbol':<8} {'Price':>16} {'24h Change':>12} {'Market Cap':>14}")
    print(f"  {'─' * 4}  {'─' * 22} {'─' * 8} {'─' * 16} {'─' * 12} {'─' * 14}")
    for coin in data:
        rank = coin.get("market_cap_rank", "?")
        name = coin.get("name", "?")
        symbol = coin.get("symbol", "?").upper()
        price = coin.get("current_price")
        change = coin.get("price_change_percentage_24h")
        mcap = coin.get("market_cap")
        print(f"  {str(rank):>4}  {pad_right(name, 22)} {pad_right(symbol, 8)} {fmt_price(price, currency):>16} {fmt_pct(change):>12} {fmt_large(mcap):>14}")
    print()


def cmd_search(args):
    """Search for a coin by name."""
    data = api_get("/search", {"query": args.query})
    coins = data.get("coins", [])
    if not coins:
        print(f"No results found for '{args.query}'.")
        return

    print()
    print(f"  {'Name':<30} {'Symbol':<10} {'Market Cap Rank':>16}")
    print(f"  {'─' * 30} {'─' * 10} {'─' * 16}")
    for coin in coins[:20]:
        name = coin.get("name", "?")
        symbol = coin.get("symbol", "?").upper()
        rank = coin.get("market_cap_rank")
        rank_str = str(rank) if rank else "N/A"
        cid = coin.get("id", "")
        print(f"  {pad_right(name, 30)} {pad_right(symbol, 10)} {rank_str:>16}   id: {cid}")
    print()


def cmd_trending(args):
    """Show trending coins."""
    data = api_get("/search/trending")
    coins = data.get("coins", [])
    if not coins:
        print("No trending data available.")
        return

    print()
    print("  Trending Coins on CoinGecko")
    print()
    print(f"  {'#':>4}  {'Name':<25} {'Symbol':<10} {'Rank':>6} {'Price (BTC)':>18}")
    print(f"  {'─' * 4}  {'─' * 25} {'─' * 10} {'─' * 6} {'─' * 18}")
    for i, entry in enumerate(coins, 1):
        item = entry.get("item", {})
        name = item.get("name", "?")
        symbol = item.get("symbol", "?").upper()
        rank = item.get("market_cap_rank")
        rank_str = str(rank) if rank else "N/A"
        btc_price = item.get("price_btc")
        btc_str = f"{btc_price:.10f}" if btc_price else "N/A"
        print(f"  {i:>4}  {pad_right(name, 25)} {pad_right(symbol, 10)} {rank_str:>6} {btc_str:>18}")
    print()


def cmd_info(args):
    """Get detailed info about a coin."""
    coin_id = args.coin_id.lower().strip()
    data = api_get(f"/coins/{coin_id}", {
        "localization": "false",
        "tickers": "false",
        "community_data": "false",
        "developer_data": "false",
    })

    name = data.get("name", "?")
    symbol = data.get("symbol", "?").upper()
    md = data.get("market_data", {})

    print()
    print(f"  {name} ({symbol})")
    print(f"  {'─' * 60}")

    price = md.get("current_price", {}).get("usd")
    ath = md.get("ath", {}).get("usd")
    ath_date = md.get("ath_date", {}).get("usd", "")
    atl = md.get("atl", {}).get("usd")
    atl_date = md.get("atl_date", {}).get("usd", "")
    mcap = md.get("market_cap", {}).get("usd")
    rank = data.get("market_cap_rank")
    change_24h = md.get("price_change_percentage_24h")

    print(f"  {'Price:':<20} {fmt_price(price)}")
    print(f"  {'24h Change:':<20} {fmt_pct(change_24h)}")
    print(f"  {'Market Cap:':<20} {fmt_large(mcap)}")
    print(f"  {'Rank:':<20} #{rank}" if rank else f"  {'Rank:':<20} N/A")
    print(f"  {'ATH:':<20} {fmt_price(ath)}  ({ath_date[:10] if ath_date else 'N/A'})")
    print(f"  {'ATL:':<20} {fmt_price(atl)}  ({atl_date[:10] if atl_date else 'N/A'})")

    # Description
    desc_data = data.get("description", {})
    desc = desc_data.get("en", "") if isinstance(desc_data, dict) else ""
    if desc:
        # Strip HTML tags simply
        import re
        desc_clean = re.sub(r"<[^>]+>", "", desc)
        desc_short = desc_clean[:300].strip()
        if len(desc_clean) > 300:
            desc_short += "..."
        print(f"\n  Description:")
        # Wrap at ~80 chars
        words = desc_short.split()
        line = "  "
        for w in words:
            if len(line) + len(w) + 1 > 80:
                print(line)
                line = "  " + w
            else:
                line += " " + w if line.strip() else "  " + w
        if line.strip():
            print(line)

    # Links
    links = data.get("links", {})
    homepage = links.get("homepage", [])
    homepage_urls = [u for u in homepage if u] if homepage else []
    repos = links.get("repos_url", {})
    github = repos.get("github", []) if repos else []
    github_urls = [u for u in github if u] if github else []

    if homepage_urls or github_urls:
        print(f"\n  Links:")
        for url in homepage_urls[:2]:
            print(f"    Homepage: {url}")
        for url in github_urls[:2]:
            print(f"    GitHub:   {url}")
    print()


def cmd_history(args):
    """Get historical price for a coin on a specific date."""
    coin_id = args.coin_id.lower().strip()
    date = args.date.strip()

    # Validate date format DD-MM-YYYY
    try:
        parsed = datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        print("Error: Date must be in DD-MM-YYYY format (e.g. 25-12-2024).")
        sys.exit(1)

    data = api_get(f"/coins/{coin_id}/history", {"date": date})

    name = data.get("name", coin_id)
    symbol = data.get("symbol", "?").upper()
    md = data.get("market_data")

    print()
    print(f"  {name} ({symbol}) on {parsed.strftime('%B %d, %Y')}")
    print(f"  {'─' * 50}")

    if not md:
        print("  No market data available for this date.")
        print()
        return

    price = md.get("current_price", {}).get("usd")
    mcap = md.get("market_cap", {}).get("usd")
    volume = md.get("total_volume", {}).get("usd")

    print(f"  {'Price:':<20} {fmt_price(price)}")
    print(f"  {'Market Cap:':<20} {fmt_large(mcap)}")
    print(f"  {'24h Volume:':<20} {fmt_large(volume)}")
    print()


def cmd_convert(args):
    """Convert between currencies/crypto."""
    amount = args.amount
    from_cur = args.from_currency.lower().strip()
    to_cur = args.to_currency.lower().strip()

    # Known fiat currencies supported by CoinGecko as vs_currencies
    fiat_codes = {
        "usd", "eur", "gbp", "jpy", "aud", "cad", "chf", "cny", "hkd", "nzd",
        "sek", "krw", "sgd", "nok", "mxn", "inr", "rub", "zar", "try", "brl",
        "twd", "dkk", "pln", "thb", "idr", "huf", "czk", "ils", "clp", "php",
        "aed", "sar", "myr", "ars", "btc", "eth", "bnb", "xrp", "sol", "dot",
    }

    from_is_fiat = from_cur in fiat_codes
    to_is_fiat = to_cur in fiat_codes

    if not from_is_fiat and not to_is_fiat:
        # Both are crypto - get both in usd and compute
        data = api_get("/simple/price", {
            "ids": f"{from_cur},{to_cur}",
            "vs_currencies": "usd",
        })
        from_price = data.get(from_cur, {}).get("usd")
        to_price = data.get(to_cur, {}).get("usd")
        if not from_price or not to_price:
            print(f"Error: Could not get price for '{from_cur}' or '{to_cur}'. Use CoinGecko coin IDs.")
            sys.exit(1)
        rate = from_price / to_price
        result = amount * rate
        print()
        print(f"  {fmt_number(amount)} {from_cur} = {fmt_number(result, 8)} {to_cur}")
        print(f"  Rate: 1 {from_cur} = {fmt_number(rate, 8)} {to_cur}")
        print()

    elif not from_is_fiat:
        # Crypto to fiat/crypto vs_currency
        data = api_get("/simple/price", {
            "ids": from_cur,
            "vs_currencies": to_cur,
        })
        rate = data.get(from_cur, {}).get(to_cur)
        if rate is None:
            print(f"Error: Could not get conversion rate from '{from_cur}' to '{to_cur}'.")
            sys.exit(1)
        result = amount * rate
        print()
        print(f"  {fmt_number(amount)} {from_cur} = {fmt_number(result)} {to_cur.upper()}")
        print(f"  Rate: 1 {from_cur} = {fmt_number(rate)} {to_cur.upper()}")
        print()

    elif not to_is_fiat:
        # Fiat to crypto - get crypto price in that fiat, then invert
        data = api_get("/simple/price", {
            "ids": to_cur,
            "vs_currencies": from_cur,
        })
        crypto_price = data.get(to_cur, {}).get(from_cur)
        if crypto_price is None:
            print(f"Error: Could not get conversion rate from '{from_cur}' to '{to_cur}'.")
            sys.exit(1)
        rate = 1.0 / crypto_price
        result = amount * rate
        print()
        print(f"  {fmt_number(amount)} {from_cur.upper()} = {fmt_number(result, 8)} {to_cur}")
        print(f"  Rate: 1 {from_cur.upper()} = {fmt_number(rate, 8)} {to_cur}")
        print()

    else:
        # Both fiat - use bitcoin as intermediary to get exchange rate
        data = api_get("/simple/price", {
            "ids": "bitcoin",
            "vs_currencies": f"{from_cur},{to_cur}",
        })
        btc = data.get("bitcoin", {})
        from_price = btc.get(from_cur)
        to_price = btc.get(to_cur)
        if not from_price or not to_price:
            print(f"Error: Could not get exchange rate between '{from_cur}' and '{to_cur}'.")
            sys.exit(1)
        rate = to_price / from_price
        result = amount * rate
        print()
        print(f"  {fmt_number(amount)} {from_cur.upper()} = {fmt_number(result)} {to_cur.upper()}")
        print(f"  Rate: 1 {from_cur.upper()} = {fmt_number(rate, 6)} {to_cur.upper()}")
        print()


def cmd_global(args):
    """Show global crypto market stats."""
    data = api_get("/global")
    gd = data.get("data", {})

    total_mcap = gd.get("total_market_cap", {}).get("usd")
    total_vol = gd.get("total_volume", {}).get("usd")
    btc_dom = gd.get("market_cap_percentage", {}).get("btc")
    eth_dom = gd.get("market_cap_percentage", {}).get("eth")
    active_coins = gd.get("active_cryptocurrencies")
    markets = gd.get("markets")
    mcap_change = gd.get("market_cap_change_percentage_24h_usd")

    print()
    print("  Global Cryptocurrency Market")
    print(f"  {'─' * 50}")
    print(f"  {'Total Market Cap:':<30} {fmt_large(total_mcap)}")
    print(f"  {'24h Volume:':<30} {fmt_large(total_vol)}")
    print(f"  {'Market Cap Change (24h):':<30} {fmt_pct(mcap_change)}")
    print(f"  {'BTC Dominance:':<30} {fmt_number(btc_dom)}%")
    if eth_dom:
        print(f"  {'ETH Dominance:':<30} {fmt_number(eth_dom)}%")
    print(f"  {'Active Cryptocurrencies:':<30} {fmt_number(active_coins, 0) if active_coins else 'N/A'}")
    print(f"  {'Markets:':<30} {fmt_number(markets, 0) if markets else 'N/A'}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Cryptocurrency price checker and market data tool (CoinGecko API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s price bitcoin,ethereum
  %(prog)s top --limit 10
  %(prog)s search solana
  %(prog)s trending
  %(prog)s info bitcoin
  %(prog)s history bitcoin --date 25-12-2024
  %(prog)s convert 1.5 bitcoin usd
  %(prog)s global
""",
    )
    sub = parser.add_subparsers(dest="command", help="Command to run")

    # price
    p_price = sub.add_parser("price", help="Get current price of one or more coins")
    p_price.add_argument("coins", help="Comma-separated coin IDs (e.g. bitcoin,ethereum)")
    p_price.add_argument("--currency", default="usd", help="Fiat currency (default: usd)")

    # top
    p_top = sub.add_parser("top", help="Show top coins by market cap")
    p_top.add_argument("--limit", type=int, default=20, help="Number of coins (default: 20)")
    p_top.add_argument("--currency", default="usd", help="Fiat currency (default: usd)")

    # search
    p_search = sub.add_parser("search", help="Search for a coin by name")
    p_search.add_argument("query", help="Search query")

    # trending
    sub.add_parser("trending", help="Show trending coins")

    # info
    p_info = sub.add_parser("info", help="Get detailed info about a coin")
    p_info.add_argument("coin_id", help="Coin ID (e.g. bitcoin)")

    # history
    p_hist = sub.add_parser("history", help="Get historical price on a specific date")
    p_hist.add_argument("coin_id", help="Coin ID (e.g. bitcoin)")
    p_hist.add_argument("--date", required=True, help="Date in DD-MM-YYYY format")

    # convert
    p_conv = sub.add_parser("convert", help="Convert between currencies")
    p_conv.add_argument("amount", type=float, help="Amount to convert")
    p_conv.add_argument("from_currency", help="Source currency (coin ID or fiat code)")
    p_conv.add_argument("to_currency", help="Target currency (coin ID or fiat code)")

    # global
    sub.add_parser("global", help="Show global crypto market stats")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "price": cmd_price,
        "top": cmd_top,
        "search": cmd_search,
        "trending": cmd_trending,
        "info": cmd_info,
        "history": cmd_history,
        "convert": cmd_convert,
        "global": cmd_global,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
