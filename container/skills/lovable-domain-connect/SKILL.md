---
name: lovable-domain-connect
description: Koble et egendefinert domene til et Lovable-prosjekt og legg inn DNS-records i Domeneshop. Trigger when user wants to connect a custom domain to a Lovable project, set up DNS records in Domeneshop, or publish an unpublished Lovable project to a custom domain.
---

# Lovable Domain Connect

Kobler et domene i Domeneshop til et Lovable-prosjekt via DNS-records.

## Informasjon du trenger først

Spør brukeren om disse hvis de ikke er oppgitt:
- **Lovable prosjekt-URL** eller prosjekt-ID (f.eks. `https://lovable.dev/projects/UUID/`)
- **Domenenavn** (f.eks. `mittdomene.no`)
- **Domeneshop-ID** for domenet (finnes i URL-en på Domeneshop: `?id=XXXXXXX`)

## Fremgangsmåte

### Steg 1 – Publiser prosjektet (hvis upublisert)
1. Naviger til `https://lovable.dev/projects/[PROSJEKT-ID]/settings?tab=domains`
2. Sjekk status på `[prosjektnavn].lovable.app` – er den "Unpublished"?
3. Klikk "Domain options" → "Publish project"
4. Bruk prosjektnavnet som subdomain, klikk "Publish"
5. Vent til status endres til "Live"

### Steg 2 – Koble domenet i Lovable
1. Klikk "Connect domain"
2. Skriv inn domenenavnet (f.eks. `mittdomene.no`)
3. Klikk "Connect domain" i dialogen
4. Når Entri-modalen åpner: klikk "Continue" → scroll ned → klikk "Can't find your provider? Go to our manual setup" ELLER la modalen laste og lukk den – DNS-records vises automatisk på siden
5. Noter DNS-records som vises:
   - **A-record**: Host `@`, Value `185.158.133.1`
   - **TXT-record**: Host `_lovable`, Value `lovable_verify=...` (unik per prosjekt)

### Steg 3 – Legg inn DNS-records i Domeneshop
1. Naviger til `https://domene.shop/admin?id=[DOMENESHOP-ID]&edit=dns&advanced=1`
2. **A-record**: La hostname-feltet være tomt (betyr `@`), type A, data = `185.158.133.1` → klikk "Legg til"
3. **TXT-record**: Hostname = `_lovable`, type = TXT, data = `lovable_verify=...` → klikk "Legg til"

### Steg 4 – Verifiser
- Tilbake i Lovable: klikk "Check status" på domenet
- DNS-propagering tar opptil 72 timer, men skjer ofte på minutter
- Besøk `https://[domenenavn]` for å bekrefte at siden er live med HTTPS

## Viktige noter
- A-record IP `185.158.133.1` er den samme for alle Lovable-prosjekter
- TXT-record verify-verdien er **unik per prosjekt** – hent den alltid fra Lovable-siden
- Domeneshop: tomt hostname-felt = root domain (`@`)
- Domeneshop er ikke støttet av Entri – bruk alltid manuell oppsett
