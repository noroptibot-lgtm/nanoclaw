#!/bin/bash
# Send a Telegram message
# Usage: bash send-message.sh <chat_id> "<message>"

BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
CHAT_ID="$1"
MESSAGE="$2"

if [ -z "$BOT_TOKEN" ]; then
  echo "ERROR: TELEGRAM_BOT_TOKEN not set in ~/.zshrc"
  exit 1
fi

if [ -z "$CHAT_ID" ] || [ -z "$MESSAGE" ]; then
  echo "Usage: send-message.sh <chat_id> \"<message>\""
  exit 1
fi

RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": ${CHAT_ID}, \"text\": $(echo "$MESSAGE" | jq -Rs .), \"parse_mode\": \"Markdown\"}")

if echo "$RESPONSE" | jq -e '.ok == true' > /dev/null 2>&1; then
  echo "Sent to chat_id ${CHAT_ID}"
else
  echo "ERROR: $(echo "$RESPONSE" | jq -r '.description')"
  exit 1
fi
