---
name: cleanup
description: Weekly workspace audit — finds bloat, stale files, broken references, and organizational drift across all projects
auto-activate: false
---

# Ukentlig Rydding

Du er en rydde-agent. Skann Desktop, Downloads og prosjektmapper. Organiser, slett soeppel, rapporter.

## Del 1: Desktop

### Mappestruktur
```
~/Desktop/
  Prosjekter/           Undermapper per prosjekt (Noropti/, Royale/, etc.)
  Regnskap/             Kvitteringer, Kontrakter, bank, faktura, firmaattest
  Media/
    Videoer/            .mp4, .mov
    Bilder/             .jpg, .jpeg, .png (ikke screenshots)
    Skjermbilder/       Filer som starter med "Skjermbilde"
    Camera Gear/
  Boeker/               PDF-boeker
  Dokumenter/           Generelle dokumenter
  Scripts og Config/    .py, .sh, .command, .json, .csv, .zip
  Installatoerer/       .dmg, .pkg
```

### Sorteringsregler for loese filer
- `.mp4`, `.mov` → `Media/Videoer/`
- `Skjermbilde*.png` → `Media/Skjermbilder/`
- `.jpg`, `.jpeg`, `.png` → `Media/Bilder/`
- `.pdf` med bok-navn → `Boeker/`
- `.pdf` med faktura/kvittering/bank/firma → `Regnskap/`
- `.py`, `.sh`, `.command`, `.json`, `.csv`, `.zip` → `Scripts og Config/`
- `.xlsx` med bank/transaksjon/konto → `Regnskap/`
- `.dmg`, `.pkg` → `Installatoerer/`
- Filer med prosjektnavn (noropti, royale, varmepumpe, flytte, openclaw, nettside, markedsmateriell) → `Prosjekter/{navn}/`

## Del 2: Downloads

Slett filer eldre enn 30 dager:
```bash
find ~/Downloads -maxdepth 1 -type f -mtime +30 -not -name '.*'
```

Fjern duplikater — filer med `(1)`, `(2)` i navnet.

## Del 3: Soeppel

```bash
du -sh ~/.Trash 2>/dev/null
```
Toem hvis over 1 GB: `rm -rf ~/.Trash/*`

## Del 4: Prosjektmapper

Skann prosjektmapper for:
- Tomme mapper → slett
- CLAUDE.md over 80 linjer → flagg
- Broken file references → fiks
- Stale filer (60+ dager) → flagg

## Del 5: Synk Memory

Push oppdatert memory til Airtable `appFS5AKIFLWXTK6j` / `tblF0NayI7hd3SWUG`:
- Les alle filer fra `~/.claude/projects/-Applications-Claude-Code/memory/`
- Slett gamle records, insert oppdaterte med Type/Description/Notes/Date

## Rapport

```
=== Ukentlig Rydding — [dato] ===
Desktop:   X filer sortert
Downloads: X filer slettet (Y MB frigjort)
Soeppel:   toemt/ikke toemt (Z GB)
Mapper:    X problemer funnet
Memory:    synkronisert til Airtable
```

## Regler

1. Bruk `mv -n` — aldri overskriv eksisterende filer
2. Aldri slett filer fra Desktop — bare flytt
3. Downloads: bare slett filer eldre enn 30 dager
4. Aldri roer skjulte filer (starter med `.`)
5. Lag undermapper automatisk hvis de ikke finnes
6. Rapporter alltid hva som ble gjort
