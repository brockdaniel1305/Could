# COULD? – Lernprotokoll

Alles, was der Creator gewünscht, korrigiert oder abgelehnt hat, und was sich technisch bewährt hat.
**Jede Regel hier gilt für jede neue Folge**, sie hat Vorrang vor FORMAT.md und STYLE.md.
Neue Einträge oben in die passende Rubrik, mit Datum und Folge.

## Wünsche des Creators (verbindlich)
- 2026-10-28 · ab 003 · **Jedes Video endet mit dem Satz: "Could you imagine another scenario that we should do next? Write it in the comments."**
  Outro-Banner: NEXT CASE / "Could you imagine another scenario?", Karte: WRITE IT IN THE COMMENTS ↓ ↓ ↓.
- 2026-10-28 · 002 · "perfekt, genau so müssen die Videos aussehen": 002 (Bolt vs T-Rex) ist zusammen mit 001 v2 die Referenz.
  Gedankenexperimente "im gleichen lustigen Stil" erzählen: Headline → beide vorstellen → drei Anläufe/Abschnitte mit Stats → Urteil.
- 2026-10-28 · 001 · **Der Stil von 001 v2 ist "perfekt" und gilt als Referenz für alle Folgen**: Vollbild-Cartoon, fliegende Fakten-Karten,
  Kapitel-Banner, Karaoke-Untertitel, Stempel im Urteil, Kommentar-Aufruf am Ende. Nicht ohne Wunsch des Creators ändern.
- 2026-10-28 · 002 · Ablauf, den der Creator für Duelle/Rennen vorgibt: **Headline zuerst → beide Parteien vorstellen → das Ereignis mit Stats
  durchgehen → am Ende, wer gewinnt.** Bei Rennen ersetzen die Rennabschnitte (0–30 m, 30–80 m, 80–100 m) die Pläne A/B/C.
- 2026-10-28 · 001 · **Kein Info-Feld/Rahmen um die Animation.** Nur die Animation im Vollbild. Die Infos sind fest in der Animation
  integriert: Sie fliegen als Karten hinein und verschwinden wieder. Die Animation selbst gefiel ("super"), also beibehalten.
- 2026-10-28 · 001 · Stimme aus VoiceStudio nutzen (siehe unten). Standard ist `"voice": "fable"` (eingebauter Name, VoiceStudio bildet ihn
  auf die Standardstimme der Engine ab). Sobald der Creator eine Profil-ID nennt, diese eintragen.
- 2026-10-28 · Kanal: Englisch, Dokumentarstil, jede Folge heißt "Could … do …?", Themen absichtlich überspitzt.
  Beide Parteien werden trocken vorgestellt, dann folgt ein "rationaler", aber absurder Vergleich, am Ende eine Konklusion.
- 2026-10-28 · Videos werden mit **HyperFrames** gebaut (`npx skills add heygen-com/hyperframes`), nicht mit eigenen Render-Skripten.
- 2026-10-28 · Das Ereignis wird als **Cartoon in witziger Darstellung live nachverfolgt**, die Fakten des Erzählers erscheinen als Schrift (heute: fliegende Karten in der Animation, siehe oben).
- 2026-10-28 · Stimme: Der Creator nutzt **VoiceStudio** (lokale Desktop-App, OpenAI-kompatible API auf Port 3900).
  In `narration.json` `"provider": "voicestudio"` und `"voice": "<Profil-ID>"` setzen. Die Profil-ID muss der Creator noch nennen.
  In der Cloud-Sandbox ist VoiceStudio nicht erreichbar, dort entsteht nur eine Kokoro-Vorschau (immer dazusagen).
- 2026-10-28 · Neue Folgen sollen nur aus einer Idee entstehen: frühere Anpassungen gelten automatisch (dieses Dokument).

## Erfahrungen aus den Folgen
- 003 · Physik-Gags gewinnen, wenn das Bild maßstabsgetreu ist (100 px/m, Höhenlineal am Rand) und die Bahnen echt gerechnet werden
  (`episodes/003-curry-wall/src/shot.py`). Querverweise auf frühere Folgen ("Faster than Usain Bolt") verbinden die Serie.
- 003 · Auch Bauwerke bekommen ein selbstgefälliges Gesicht (Mauer), das passt zum Running Gag mit Eisberg und T-Rex.
- 002 · Der Creator schrieb "Can …", der Kanal heißt aber COULD?. Die Headline wurde zu "Could …" vereinheitlicht (beim Creator nachgefragt: offen).
- 002 · Rennen aus einem echten Modell (Zwischenzeiten + Geschwindigkeit) treiben, in Zeitlupe, mit Rennuhr-Karte. So stimmen alle
  Zahlen (Führungswechsel, Abstand im Ziel) mit dem Bild überein. Vorlage: `episodes/002-bolt-trex/src/race.py`.
- 002 · Unter den Untertiteln eine Live-Grafik ohne Text (Fortschrittsbalken 0–100 m mit Symbolen) füllt die untere Hälfte sinnvoll.
- 001 · Die erste Version (Piper-Stimme, Standbilder) war mit 133 s zu lang und zu statisch. Ziel sind 90–115 s mit Bewegung auf jedem Satz.
- 001 · Keine echten Fotos von Personen: Karikatur als Cartoon-Figur ist sicherer und passt zum Stil.
- 001 · Kunstpause vor dem Urteil ("Titanic? ||0.8|| No. ||0.9|| But …") macht die Pointe. Kokoro macht sonst keine Pausen.

## Technik (bewährt)
- `src/build_all.sh` baut nur `s[0-9]*.py`. Hilfsmodule der Folge (z. B. `race.py`, `shot.py`) dürfen also nicht mit `s<Ziffer>` beginnen.
- Dreht sich eine Figur mit `scaleX: -1` um, auch die Rückennummer (`PFX-num`) zurückspiegeln.
- Bei schräg gestellten Karten meldet `check` eine Überlappung zwischen Beschriftung und Wert. Karten tragen deshalb `data-layout-allow-overlap`.
- Die vordere Wellenschicht ist nur ein schmaler Streifen, sonst verdeckt sie die Unterwasserwelt (Eisberg-Unterteil, Fische).
- Die untere Bildhälfte nie leer lassen: Unterwasserwelt, Rasen mit Strafraum usw. zeichnen (unter 1330 px nur Bild, kein Text).
- Der Kokoro-Mix landet bei etwa −18 LUFS, deshalb nach dem Render `loudnorm` auf −15 LUFS anwenden (steht im Skill).
- Render von 110 s dauert in der Cloud-Sandbox etwa 6 Minuten (Software-GPU, 1 Worker).
- Schriften Playfair Display und IBM Plex Mono werden ohne `@font-face` nicht geladen, deshalb liegen sie als Dateien in `channel/kit/fonts`. `build_episode.py` kopiert sie in jede Folge.
- Whisper schreibt Namen falsch ("Nuer"). Der Untertitel-Text kommt deshalb immer aus dem Skript, aus der Transkription nur die Zeiten.
- `impact-bass-2` übersteuert (true peak 0 dB). Für Schläge und Stempel `impact-bass-1` nehmen (Spitze nach 0,07 s).
- GSAP: mehrere `fromTo` auf derselben Eigenschaft sind ok, weil `scene.py` die Timeline einmal ans Ende und zurück spult.
  Für Wiederholungen immer `Math.max(0, Math.floor(D / cycle) - 1)` verwenden (sonst Lint-Warnung oder Endlosschleife).
- Text im Cartoon mindestens 28 px, Deko-Text bekommt `data-layout-ignore`.
- Lange Untertitel-Gruppen brechen auf zwei Zeilen um und überdecken die Bühne: maximal 4 Wörter oder 22 Zeichen.
