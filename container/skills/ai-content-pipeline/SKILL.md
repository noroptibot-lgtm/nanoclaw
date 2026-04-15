---
name: ai-content-pipeline
description: Automatisert pipeline som hver dag scraper tweets fra AI-influencere via Apify, genererer videomanus med Claude, og laster opp Google Docs til Drive. Kjøres via PM2. Bruk når brukeren vil sette opp eller kjøre denne pipelinen (repo grandamenium/ai-content-pipeline).
user_invocable: true
---

# AI Content Pipeline (X/Twitter → Claude → Google Docs)

Automatisert pipeline i `~/Projects/ai-content-pipeline` (fra `github.com/grandamenium/ai-content-pipeline`).

> **Før du kjører noe:**
> ```bash
> cd ~/Projects/ai-content-pipeline
> ```

## Hva gjør den

Tre trinn hver dag:
1. **Apify** skraper tweets fra en konfigurerbar liste AI-influencere (5–7 min)
2. **Claude API** analyserer tweets → genererer videomanus (~30 sek)
3. **Google Docs/Drive** – formaterer og laster opp som dokument

Planlegges via PM2 (default 16:00 daglig).

## Første oppsett (én gang)

Sjekk deretter `SETUP_GUIDE.md` i prosjektet for detaljer, men i hovedsak:

1. **Sjekk credentials** — trenger:
   - `APIFY_TOKEN` (Apify → Settings → Integrations)
   - `ANTHROPIC_API_KEY` (console.anthropic.com)
   - `GOOGLE_DRIVE_FOLDER_ID` (fra URL-en til Drive-mappen)
   - `config/oauth-credentials.json` (Google OAuth Desktop app JSON)

2. **Installer avhengigheter og autoriser Google:**
   ```bash
   npm install
   node scripts/authorize-google.js   # engangs OAuth-flow i nettleser
   ```

3. **Test med ett kjør:**
   ```bash
   npm start
   ```
   Sjekk at et dokument dukker opp i konfigurert Google Drive-mappe.

## Daglig planlegging med PM2

```bash
npm install -g pm2                   # første gang
pm2 start ecosystem.config.js
pm2 save
pm2 startup                          # kjør kommandoen PM2 skriver ut
```

Default tid: kl 16:00. Endres i `ecosystem.config.js` (cron-syntax).

## Nyttige kommandoer

```bash
pm2 list                             # status
pm2 logs content-pipeline            # se logs
pm2 trigger content-pipeline run     # kjør manuelt nå
pm2 restart content-pipeline         # restart etter config-endring
pm2 describe content-pipeline        # full status
pm2 stop content-pipeline            # stopp
```

## Feilsøking (fra repo README)

| Problem | Løsning |
|---|---|
| `APIFY_TOKEN not set` | sjekk `.env` |
| `ANTHROPIC_API_KEY not set` | sjekk `.env` |
| "Access blocked" under Google auth | legg Gmail som test user i OAuth consent screen |
| Dokumenter dukker ikke opp i Drive | verifiser `GOOGLE_DRIVE_FOLDER_ID` |
| Pipeline starter ikke | `pm2 describe content-pipeline` |

## Når du blir invitert inn

Hvis bruker skriver `/ai-content-pipeline` eller ber om å kjøre denne pipelinen:
1. `cd ~/Projects/ai-content-pipeline` først
2. Sjekk `.env` eksisterer (ikke bare `.env.example`)
3. Hvis ikke: vis setup-veien over og spør hvilke credentials som mangler
4. Hvis `.env` finnes: foreslå `pm2 status` først, deretter relevante handlinger

Repo: https://github.com/grandamenium/ai-content-pipeline
