#!/bin/bash
# Long-polling Telegram bot — responds near-instantly using Claude CLI
# Usage: bash long-poll.sh

BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
ALLOWED_USER="${TELEGRAM_ALLOWED_USER}"
OFFSET_FILE="$HOME/.claude-telegram-offset"

if [ -z "$BOT_TOKEN" ]; then
  echo "ERROR: TELEGRAM_BOT_TOKEN not set"
  exit 1
fi

echo "🤖 Telegram long-poll startet. Trykk Ctrl+C for å stoppe."

while true; do
  OFFSET=$(cat "$OFFSET_FILE" 2>/dev/null || echo "0")

  # Long poll — venter opptil 60 sek på nye meldinger
  RESPONSE=$(curl -s --max-time 70 \
    "https://api.telegram.org/bot${BOT_TOKEN}/getUpdates?offset=${OFFSET}&timeout=60")

  if ! echo "$RESPONSE" | jq -e '.ok == true' > /dev/null 2>&1; then
    echo "API-feil, prøver igjen om 5 sek..."
    sleep 5
    continue
  fi

  # Oppdater offset
  NEW_OFFSET=$(echo "$RESPONSE" | jq '.result[-1].update_id + 1 // empty')
  if [ -n "$NEW_OFFSET" ]; then
    echo "$NEW_OFFSET" > "$OFFSET_FILE"
  fi

  # Hent meldinger fra tillatt bruker
  MESSAGES=$(echo "$RESPONSE" | jq --arg uid "$ALLOWED_USER" \
    '[.result[] | select(.message != null and (.message.from.id == ($uid | tonumber)))]')

  MSG_COUNT=$(echo "$MESSAGES" | jq 'length')

  if [ "$MSG_COUNT" -gt 0 ]; then
    echo "$MESSAGES" | jq -c '.[]' | while read -r msg; do
      CHAT_ID=$(echo "$msg" | jq -r '.message.chat.id')
      TEXT=$(echo "$msg" | jq -r '.message.text // ""')
      FROM=$(echo "$msg" | jq -r '.message.from.first_name')

      if [ -z "$TEXT" ]; then
        continue
      fi

      echo "📩 Melding fra $FROM: $TEXT"

      # Generer svar med Claude CLI
      REPLY=$(echo "$TEXT" | claude --print --model claude-haiku-4-5-20251001 \
        "Du er en hjelpsom AI-assistent som svarer på norsk. Svar kort og naturlig på denne meldingen fra $FROM:" 2>/dev/null)

      if [ -z "$REPLY" ]; then
        REPLY="Beklager, fikk ikke generert svar akkurat nå."
      fi

      # Send svar
      curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\": $CHAT_ID, \"text\": $(echo "$REPLY" | jq -Rs .), \"parse_mode\": \"Markdown\"}" \
        > /dev/null

      echo "✅ Svarte: $REPLY"
    done
  fi
done
