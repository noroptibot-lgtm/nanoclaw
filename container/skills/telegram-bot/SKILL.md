---
name: telegram-bot
description: "Check for new Telegram messages and send replies. Use when: the /loop cron fires and you need to check for incoming Telegram messages, or when you need to send a reply back to the user on Telegram."
---

# Telegram Bot Skill

Send and receive messages via a personal Telegram bot.

## Scripts

### Get new messages (filtered to allowed user)
```bash
bash ~/.claude/skills/telegram-bot/get-messages.sh
```

### Get ALL messages (from any user)
```bash
bash ~/.claude/skills/telegram-bot/get-messages.sh --all
```

### Send a message
```bash
bash ~/.claude/skills/telegram-bot/send-message.sh <chat_id> "<message>"
```

## Output format

Each message is one JSON line:
```json
{"chat_id": 123, "user_id": 456, "from": "Albert", "username": "albert", "text": "Hello", "date": 1234567890}
```

## Environment Variables

Set in `~/.zshrc`:
```
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_ALLOWED_USER="your_telegram_user_id"
```

## Notes

- Offset tracked in `~/.claude-telegram-offset` to avoid reprocessing
- Without `--all`, only returns messages from `TELEGRAM_ALLOWED_USER`
- Supports Markdown in sent messages
