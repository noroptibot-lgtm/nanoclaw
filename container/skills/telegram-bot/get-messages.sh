#!/bin/bash
# Get new Telegram messages
# Usage: bash get-messages.sh [--all]
# --all flag returns messages from ALL users (default: only allowed user)

BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
ALLOWED_USER="${TELEGRAM_ALLOWED_USER}"
OFFSET_FILE="$HOME/.claude-telegram-offset"
ALL_USERS=false

if [ "$1" = "--all" ]; then
  ALL_USERS=true
fi

if [ -z "$BOT_TOKEN" ]; then
  echo "ERROR: TELEGRAM_BOT_TOKEN not set in ~/.zshrc"
  exit 1
fi

OFFSET=$(cat "$OFFSET_FILE" 2>/dev/null || echo "0")

RESPONSE=$(curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getUpdates?offset=${OFFSET}&timeout=5")

if echo "$RESPONSE" | jq -e '.ok == false' > /dev/null 2>&1; then
  echo "ERROR: $(echo "$RESPONSE" | jq -r '.description')"
  exit 1
fi

# Update offset
NEW_OFFSET=$(echo "$RESPONSE" | jq '.result[-1].update_id + 1 // empty')
if [ -n "$NEW_OFFSET" ]; then
  echo "$NEW_OFFSET" > "$OFFSET_FILE"
fi

# Filter or return all
if [ "$ALL_USERS" = true ] || [ -z "$ALLOWED_USER" ]; then
  MESSAGES=$(echo "$RESPONSE" | jq '[.result[] | select(.message != null)]')
else
  MESSAGES=$(echo "$RESPONSE" | jq --arg uid "$ALLOWED_USER" '[.result[] | select(.message.from.id == ($uid | tonumber))]')
fi

MSG_COUNT=$(echo "$MESSAGES" | jq 'length')
if [ "$MSG_COUNT" -gt 0 ]; then
  echo "$MESSAGES" | jq -c '.[] | {
    chat_id: .message.chat.id,
    user_id: .message.from.id,
    from: .message.from.first_name,
    username: .message.from.username,
    text: .message.text,
    date: .message.date
  }'
fi
