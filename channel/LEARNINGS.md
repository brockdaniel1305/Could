# COULD? – Lernprotokoll

Alles, was der Creator gewünscht, korrigiert oder abgelehnt hat, und was sich technisch bewährt hat.
**Jede Regel hier gilt für jede neue Folge**, sie hat Vorrang vor FORMAT.md und STYLE.md.
Neue Einträge oben in die passende Rubrik, mit Datum und Folge.

## Wünsche des Creators (verbindlich)
- 2026-10-29 · 008 · **Kein Barometer/Stimmungs-Meter** unter den Untertiteln mehr (und keine Sounds dazu), "stört das Video".
  Die untere Hälfte stattdessen mit der Szene selbst füllen (Boden, Menge, Wasser …). Ersetzt die Erfahrung aus 005 (Stimmungs-Barometer).
- 2026-10-29 · 008 · Lieber **kürzer** (008: ~80 s statt 105 s) und vor allem ein **kurzes Ende**. Pointen über bekannte Eigenschaften
  der Person (Tempo, Jubel, Rolle im Verein) kommen besser an als Vertrags-/Verwaltungs-Gags ("das mit dem Vertrag finde ich komisch").
  Ein Schluss, der die Person in ihre Gegenwart zurückholt (Mbappé → Elfmeter bei Real Madrid), ist gewünscht.
- 2026-10-29 · 007 · **Mehr Soundeffekte**, damit es spannender und ansehnlicher wird: jede Aktion im Cartoon bekommt einen Sound
  (Schritte, Kicks, Drehen, Schwindel, Pfiff, Netz, Domino, Wind, Herzschlag, Trommelwirbel, Jubel). 007 hat ~120 SFX auf 106 s.
  Eigene Bibliothek: `channel/kit/sfx/` (gebaut von `tools/make_sfx.py`, synthetisch, lizenzfrei), `build_episode.py` findet sie per Name.
  Viele SFX aus einem Zeitplan erzeugen statt von Hand (z. B. `episodes/007-rome-messi/src/sfx.py`).
- 2026-10-29 · 007 · Pointen-Szenen nicht überladen: nach dem Höhepunkt reicht ein kurzer Schlusssatz ("This is when they all realised …"),
  der Creator strich die lange Urteils-Szene.
- 2026-10-29 · 007 · **Vor jedem Video zuerst das fertige Skript schicken** (Erzählertext + was die Animation pro Szene zeigt)
  als `episodes/<ep>/SCRIPT.md` und im Chat. Erst nach dem OK des Creators Stimme, Szenen und Render bauen.
- 2026-10-29 · 007 · **Die Animation soll noch genauer zeigen, was wirklich passiert:** jede Aussage wird wörtlich gespielt
  (Zähler zählt mit, Tricks wie Übersteiger/Tunnel sind als echte Bewegung zu sehen, Ursache → Wirkung sichtbar).
- 2026-10-28 · 006 · **Das Ergebnis darf nicht von Anfang an offensichtlich sein** ("a little bit boring … obvious from the beginning").
  → Vor dem Skript prüfen: Weiß der Zuschauer nach dem Vorstellen schon die Antwort? Dann umbauen, z. B. "Best of three" mit
    Score-Bug, bei dem jede Runde anders ausgeht und die letzte bis zum Sprung offen bleibt (006 v2), oder ein überraschendes "Yes".
  → Bei größeren Umbauten zuerst die Idee vorschlagen und auf das OK warten (so gewünscht).
- 2026-10-28 · 006 · Der Running Gag "der Zug ist immer zu spät" (Deutsche Bahn) kam gut an. Verspätung als eigene Runde/Lösung nutzen.
- 2026-10-28 · 004 · **Der Erzähler darf nicht nach KI klingen:** keine unnötigen Stopps, Namen korrekt aussprechen.
  → Pausen-Marker `||x||` nur für echte Pointen (vor dem Urteil, vor "Mostly."), sonst durchsprechen lassen.
  → Jeder Name, den die Stimme falsch sagt, kommt in `channel/pronunciation.json` (gilt für alle Folgen) und wird per
    tts + transcribe geprüft (die Transkription muss den echten Namen zurückliefern).
- 2026-10-28 · 004 · Bei Fußballer-Folgen darf (und soll, wenn gewünscht) der Erzähler **stark sarkastisch** loben
  ("one of the best centre backs in the world right now. Genuinely."). Die Karten spielen mit ("SARCASM LEVEL: Genuinely zero", "*mostly").
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
- 2026-10-29 · TikTok: Die ersten 4 Uploads direkt nach Kontoerstellung bekamen 0 Aufrufe (Konto galt als Bot). Erstes Video danach:
  800 Aufrufe / 15 Likes nach 3 h. Neue Konten erst "aufwärmen", Uploads verteilen. Re-Uploads alter Folgen als echte neue Fassung (v3):
  neue Erzählerspur, Pflicht-Outro, SFX-Layer (`tools/auto_sfx.py`), neuer Einstieg (Punch-in) → `renders/<ep>-v3-final.mp4`.
- 006 · Gefährliche Szenarien (Züge, Höhe, Feuer …): nie den Unfall zeigen (vorher schneiden), die Lösung ungefährlich machen
  ("he takes the train") und am Ende ein klarer Satz "Please do not try this." (TikTok-Richtlinien zu gefährlichen Handlungen).
- 006 · Querverweise zahlen sich aus: die benötigten 7 m Sprunghöhe = Höhe der Chinesischen Mauer aus 003 (gleiches Part wiederverwendet).
- 005 · Running Gags aus dem echten Leben der Person tragen eine ganze Folge (Haalands Meditations-Jubel als Lösung gegen den Löwen,
  "in the back of the net" gegen den Retiarius).
- 004 · Historische Kriege/NS-Zeit: nie Hitler als Figur, nie NS-Symbole oder Abzeichen (§ 86a StGB, TikTok-Richtlinien), Panzer neutral grau.
  Der Witz zielt nur auf den "Helden" der Folge. Den Creator vorher kurz auf das Reichweiten-Risiko solcher Titel hinweisen.
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
- Ein Gegenstand in der Hand (Heugabel) gehört NICHT in die Arm-Gruppe: `scene.py` dreht Arme um die Mitte oben ihrer Bounding-Box,
  ein langer Gegenstand verschiebt diesen Punkt und der Arm "fliegt" weg. Gegenstand als eigene Gruppe an der Hand zeichnen.
- `pitch-day` mit `GY=1010`, wenn die Figuren bei y 1200 stehen sollen (sonst stehen sie auf der Tribünenkante).
- Openverse (SFX-Suche) ist aus der Cloud nicht erreichbar, deshalb eigene synthetische SFX (`tools/make_sfx.py`).
- Läuft die Session auf einer neuen Maschine, kann `whisper-cli` mit SIGILL abstürzen (für eine andere CPU gebaut). Fix:
  `cd ~/.cache/hyperframes/whisper/whisper.cpp && rm -rf build && cmake -B build -DGGML_NATIVE=ON && cmake --build build -j4 --target whisper-cli`.
- Große Menge (Armee): eine Figur in `<defs>`, Rest als `<use>`-Kopien, nur die vorderste Reihe voll geriggt (`army()` in 007 battle.py).
- `fromTo` mit `opacity: 1` im from-Teil zeigt das Element schon ab Frame 0 (immediateRender). Für "erscheint später" `tl.set(opacity 1)` + `immediateRender: false`.
- Kamerafahrt: die ganze Welt in eine `cam`-Gruppe, deren x so gerechnet wird, dass Gegner i genau zur Zeit P[i] bei der Figur ist.
- Maßstabswechsel für Winziges (006 Runde 3): eigene Szene auf Bodenhöhe (12 px/cm), Figur nur ab den Knien (`boots()` in
  `episodes/006-ronaldo-train/src/rail.py`), dasselbe Part verkleinert mit `.mini * { vector-effect: non-scaling-stroke }`,
  sonst werden die Konturen haarfein. Zeitlupe immer mit Label "SLOW MOTION" kennzeichnen.
- Score-Bug oben rechts neben dem Logo (`scorebug()` / `score(at, a, b, who)` in rail.py) trägt Runden-Formate.
- Wechselnder Text (Anzeigetafel, Zähler) immer über einen Proxy-Tween mit `onUpdate` als Funktion der Zeit setzen
  (`board([[t, text], …])` in `episodes/006-ronaldo-train/src/rail.py`), nicht mit `tl.set(el, {textContent})`.
- `svgOrigin` nicht für Elemente in verschachtelten, verschobenen Gruppen verwenden (Zeiger flog aus dem Bild). Besser `transformOrigin: "50% 100%"`.
- `build_episode.py` schneidet die Stille am Anfang und Ende jedes Stimm-Stücks ab und kürzt Satzpausen innerhalb eines Stücks
  auf ~0.22 s (Kokoro lässt 0.35–0.4 s stehen). Nur `||x||` erzeugt längere Pausen.
- Die Wort-Zeitstempel von `npx hyperframes transcribe` kommen auf **stderr**. Bis Folge 004 v1 wurden sie deshalb nicht gelesen,
  und alle Timings waren geschätzt. Seit dem Fix sind Untertitel und Cues wortgenau; 001–003 bei Gelegenheit neu bauen.
- GSAP-`y`/`x` niemals auf ein `<g>` tweenen, das selbst ein `transform="translate(...)"` trägt: GSAP übernimmt die Verschiebung als x/y
  und ein absolutes `y: 0` springt an den Bildrand. Immer `<g transform=…><g id=…>` verschachteln.
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
