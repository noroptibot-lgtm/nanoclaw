---
name: crypto
description: Cryptocurrency prices, bitcoin, ethereum, crypto market data, exchange rates, currency conversion, portfolio tracking, trending coins
---

# Crypto & Currency Price Skill

Get real-time cryptocurrency prices, market data, and currency conversion using the free CoinGecko API.

## Setup

No setup needed. Uses free public APIs with no authentication required.

- CoinGecko API: free tier, 10-30 calls/minute rate limit
- Python 3 stdlib only (urllib, json, argparse)

## Quick Reference

```bash
# Get price of bitcoin and ethereum
python3 ~/.claude/skills/crypto/scripts/crypto.py price bitcoin,ethereum

# Top 20 coins by market cap
python3 ~/.claude/skills/crypto/scripts/crypto.py top

# Search for a coin
python3 ~/.claude/skills/crypto/scripts/crypto.py search solana

# Trending coins
python3 ~/.claude/skills/crypto/scripts/crypto.py trending

# Detailed coin info
python3 ~/.claude/skills/crypto/scripts/crypto.py info bitcoin

# Historical price on a specific date
python3 ~/.claude/skills/crypto/scripts/crypto.py history bitcoin --date 25-12-2024

# Convert between currencies
python3 ~/.claude/skills/crypto/scripts/crypto.py convert 1.5 bitcoin usd

# Global market stats
python3 ~/.claude/skills/crypto/scripts/crypto.py global
```

## Commands

### price

Get current price of one or more cryptocurrencies.

```bash
python3 ~/.claude/skills/crypto/scripts/crypto.py price bitcoin,ethereum
python3 ~/.claude/skills/crypto/scripts/crypto.py price bitcoin --currency eur
```

- **coins**: Comma-separated CoinGecko coin IDs (e.g. bitcoin, ethereum, shiba-inu)
- **--currency**: Fiat currency for pricing (default: usd)

Shows: price, 24h change %, market cap.

### top

Show top coins ranked by market cap.

```bash
python3 ~/.claude/skills/crypto/scripts/crypto.py top
python3 ~/.claude/skills/crypto/scripts/crypto.py top --limit 10 --currency eur
```

- **--limit**: Number of coins to show (default: 20)
- **--currency**: Fiat currency for pricing (default: usd)

Shows: rank, name, symbol, price, 24h change %, market cap.

### search

Search for a coin by name or symbol.

```bash
python3 ~/.claude/skills/crypto/scripts/crypto.py search solana
python3 ~/.claude/skills/crypto/scripts/crypto.py search "shiba inu"
```

- **query**: Search term

Shows: name, symbol, market cap rank.

### trending

Show currently trending coins on CoinGecko.

```bash
python3 ~/.claude/skills/crypto/scripts/crypto.py trending
```

No arguments. Shows: name, symbol, market cap rank, price in BTC.

### info

Get detailed information about a specific coin.

```bash
python3 ~/.claude/skills/crypto/scripts/crypto.py info bitcoin
python3 ~/.claude/skills/crypto/scripts/crypto.py info ethereum
```

- **coin_id**: CoinGecko coin ID

Shows: name, symbol, current price, ATH, ATL, market cap, rank, description (truncated), homepage and GitHub links.

### history

Get historical price for a coin on a specific date.

```bash
python3 ~/.claude/skills/crypto/scripts/crypto.py history bitcoin --date 25-12-2024
python3 ~/.claude/skills/crypto/scripts/crypto.py history ethereum --date 01-01-2023
```

- **coin_id**: CoinGecko coin ID
- **--date**: Date in DD-MM-YYYY format (as CoinGecko expects)

Shows: price, market cap, 24h volume on that date.

### convert

Convert between cryptocurrencies and fiat currencies.

```bash
python3 ~/.claude/skills/crypto/scripts/crypto.py convert 1.5 bitcoin usd
python3 ~/.claude/skills/crypto/scripts/crypto.py convert 100 usd eur
python3 ~/.claude/skills/crypto/scripts/crypto.py convert 1000 ethereum btc
```

- **amount**: Numeric amount to convert
- **from_currency**: Source currency (coin ID or fiat code)
- **to_currency**: Target currency (coin ID or fiat code)

For crypto-to-fiat and crypto-to-crypto, uses CoinGecko pricing. For fiat-to-fiat, uses CoinGecko supported vs_currencies.

### global

Show global cryptocurrency market statistics.

```bash
python3 ~/.claude/skills/crypto/scripts/crypto.py global
```

No arguments. Shows: total market cap, 24h volume, BTC dominance, number of active coins, number of markets.

## Common Workflows

### Quick portfolio check

```bash
python3 ~/.claude/skills/crypto/scripts/crypto.py price bitcoin,ethereum,solana,cardano
```

### Research a new coin

```bash
python3 ~/.claude/skills/crypto/scripts/crypto.py search "coin name"
python3 ~/.claude/skills/crypto/scripts/crypto.py info <coin_id>
python3 ~/.claude/skills/crypto/scripts/crypto.py history <coin_id> --date 01-01-2024
```

### Market overview

```bash
python3 ~/.claude/skills/crypto/scripts/crypto.py global
python3 ~/.claude/skills/crypto/scripts/crypto.py top --limit 10
python3 ~/.claude/skills/crypto/scripts/crypto.py trending
```

## Notes

- CoinGecko coin IDs are lowercase and hyphenated: bitcoin, ethereum, shiba-inu, binancecoin
- Use the `search` command to find the correct coin ID if unsure
- Free API rate limit is 10-30 calls/minute; avoid rapid repeated calls
- All requests have a 15-second timeout
