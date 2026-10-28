# COULD? – Lernprotokoll

Alles, was der Creator gewünscht, korrigiert oder abgelehnt hat, und was sich technisch bewährt hat.
**Jede Regel hier gilt für jede neue Folge**, sie hat Vorrang vor FORMAT.md und STYLE.md.
Neue Einträge oben in die passende Rubrik, mit Datum und Folge.

## Wünsche des Creators (verbindlich)
- 2026-10-28 · Kanal: Englisch, Dokumentarstil, jede Folge heißt "Could … do …?", Themen absichtlich überspitzt.
  Beide Parteien werden trocken vorgestellt, dann folgt ein "rationaler", aber absurder Vergleich, am Ende eine Konklusion.
- 2026-10-28 · Videos werden mit **HyperFrames** gebaut (`npx skills add heygen-com/hyperframes`), nicht mit eigenen Render-Skripten.
- 2026-10-28 · Das Ereignis wird als **Cartoon in witziger Darstellung live nachverfolgt**, die Fakten des Erzählers
  laufen **nebenher als Schrift** (Fakten-Panel über der Cartoon-Bühne).
- 2026-10-28 · Neue Folgen sollen nur aus einer Idee entstehen: frühere Anpassungen gelten automatisch (dieses Dokument).

## Erfahrungen aus den Folgen
- 001 · Die erste Version (Piper-Stimme, Standbilder) war mit 133 s zu lang und zu statisch. Ziel sind 90–115 s mit Bewegung auf jedem Satz.
- 001 · Keine echten Fotos von Personen: Karikatur als Cartoon-Figur ist sicherer und passt zum Stil.
- 001 · Kunstpause vor dem Urteil ("Titanic? ||0.8|| No. ||0.9|| But …") macht die Pointe. Kokoro macht sonst keine Pausen.

## Technik (bewährt)
- Der Kokoro-Mix landet bei etwa −18 LUFS, deshalb nach dem Render `loudnorm` auf −15 LUFS anwenden (steht im Skill).
- Render von 110 s dauert in der Cloud-Sandbox etwa 6 Minuten (Software-GPU, 1 Worker).
- Schriften Playfair Display und IBM Plex Mono werden ohne `@font-face` nicht geladen, deshalb liegen sie als Dateien in `channel/kit/fonts`. `build_episode.py` kopiert sie in jede Folge.
- Whisper schreibt Namen falsch ("Nuer"). Der Untertitel-Text kommt deshalb immer aus dem Skript, aus der Transkription nur die Zeiten.
- `impact-bass-2` übersteuert (true peak 0 dB). Für Schläge und Stempel `impact-bass-1` nehmen (Spitze nach 0,07 s).
- GSAP: mehrere `fromTo` auf derselben Eigenschaft sind ok, weil `scene.py` die Timeline einmal ans Ende und zurück spult.
  Für Wiederholungen immer `Math.max(0, Math.floor(D / cycle) - 1)` verwenden (sonst Lint-Warnung oder Endlosschleife).
- Text im Cartoon mindestens 28 px, Deko-Text bekommt `data-layout-ignore`.
- Lange Untertitel-Gruppen brechen auf zwei Zeilen um und überdecken die Bühne: maximal 4 Wörter oder 22 Zeichen.
