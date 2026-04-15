---
name: mac-mini-always-on
description: Configure a Mac Mini to never sleep, always restart after power failure, and always be accessible via SSH and screen sharing. Use when setting up a Mac Mini as a remote server or when it keeps becoming inaccessible after reboots.
---

Set up a Mac Mini to always be on and remotely accessible, surviving power failures and reboots without manual intervention.

## The prompt (paste into Claude Code on the Mac Mini)

```
Denne Mac Mini skal aldri slå seg av eller sove, uansett hva som skjer. Bruk osascript med administrator privileges for alle sudo-kommandoer (unngå terminal-passord-problem). Gjør dette:

1. Skru av absolutt all søvn:
   osascript -e 'do shell script "pmset -a sleep 0 disksleep 0 displaysleep 0 hibernatemode 0 standby 0 autopoweroff 0 womp 1 autorestart 1" with administrator privileges'
   osascript -e 'do shell script "systemsetup -setrestartpowerfailure on" with administrator privileges'
   osascript -e 'do shell script "systemsetup -setwakeonnetworkaccess on" with administrator privileges'

2. Aktiver SSH og skjermdeling:
   osascript -e 'do shell script "systemsetup -setremotelogin on" with administrator privileges'
   osascript -e 'do shell script "launchctl load -w /System/Library/LaunchDaemons/com.apple.screensharing.plist" with administrator privileges'

3. Slå av FileVault (viktigst — hindrer maskin fra å henge på innloggingsskjerm etter strømbrudd):
   Bruk osascript dialog til å be om passord, deretter:
   echo "PASSORD" | fdesetup disable -inputplist (eller tilsvarende metode)
   Bekreft med: fdesetup status

4. Aktiver auto-login:
   Bruk osascript dialog til å be om passord og sett autoLoginUser via defaults write

5. Verifiser alt:
   pmset -g | grep -E "sleep|standby|autopoweroff|hibernatemode|womp|autorestart"
   fdesetup status
   sudo systemsetup -getremotelogin
   defaults read /Library/Preferences/com.apple.loginwindow autoLoginUser

Rapporter status i en tabell på slutten.
```

## Hva som løses

| Problem | Løsning |
|---------|---------|
| Maskinen sover | pmset sleep 0 overalt |
| Starter ikke etter strømbrudd | autorestart 1 + setrestartpowerfailure on |
| Henger på innloggingsskjerm | FileVault off + auto-login aktivert |
| Kan ikke SSH inn | systemsetup -setremotelogin on |
| Kan ikke skjermdele | screensharing LaunchDaemon lastet |

## Viktige noter

- **FileVault** er den vanligste årsaken til at maskinen blir utilgjengelig etter strømbrudd — den henger på krypteringsskjermen og ingen tjenester starter
- **osascript med administrator privileges** viser et GUI passord-vindu — fungerer der `sudo` feiler i Claude Code
- **autorestart 1** gjør at maskinen starter seg selv etter strømbrudd
- Etter FileVault er slått av tar diskkrypteringen litt tid å dekryptere i bakgrunnen — maskinen fungerer normalt mens dette skjer

## Wake-on-LAN (hvis maskinen er helt av)

```bash
brew install wakeonlan
wakeonlan <MAC-ADRESSE>
```

Se memory for MAC-adresser til spesifikke maskiner.
