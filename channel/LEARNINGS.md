# COULD? – Lernprotokoll

Alles, was der Creator gewünscht, korrigiert oder abgelehnt hat, und was sich technisch bewährt hat.
**Jede Regel hier gilt für jede neue Folge**, sie hat Vorrang vor FORMAT.md und STYLE.md.
Neue Einträge oben in die passende Rubrik, mit Datum und Folge.

## Wünsche des Creators (verbindlich)
- 2026-11-03 · S2E02 · **Jede Folge bekommt eigene, sehr unauffällige Hintergrundmusik**, die zum Thema passt, aber nicht ablenkt.
  `narration.json` → `"music": {"theme": "flamenco" | "stadium" | "march", "volume": 0.17}`; `build_episode.py` erzeugt sie mit
  `tools/make_music.py` auf die Folgenlänge (lokal synthetisiert, keine Lizenzen). Pegel ~16 dB unter der Stimme.
- 2026-11-03 · S2E02 · **"Prime" + Zeitraum nennen**: Bei der Vorstellung einer Legende "Prime …" sagen und schreiben und die Fakten
  zeitlich einordnen (z. B. "March 2018 to August 2019: fifty Premier League games").
- 2026-11-03 · S2E02 · **Animationen nie "stumpf"**: Sekundärbewegung immer an (Atmen, Federn, Vorlehnen beim Laufen), Staub hinter
  Rennenden, Dampf/Schnauben, Comic-"BAM!" bei Zusammenstößen, Speedlines bei Angriffen. Die Kamera darf nie in eine Figur fahren
  (Snapshots der Übergänge prüfen).
- 2026-11-03 · S2E02 · **Jedes Bild ein volles Werk** (Referenzvideo): keine leeren Flächen (Himmel, Wände, Boden), Ebenen mit
  unscharfem Vordergrund, Figuren davor, detailreicher Hintergrund. Viele Nahaufnahmen, Zooms (fov-Fahrten), Untersichten,
  gekippte Winkel (`roll`), Draufsichten. **Kamera fährt nie durch Wände** (`camBounds` je Welt). Technik: Vordergrund-Pass in
  `engine.js` (alles näher als die nächste Figur wird über den Figuren unscharf gezeichnet), Dichte-Pass in der Welt
  (Wimpelketten, Hinterhäuser, Kirche, Berge, Wolken, Blumen, Lichtstrahlen, Staub).
- 2026-11-03 · S2E01 · **Untertitel bei 3D-Folgen tiefer setzen**: Bei Close-ups verdeckten sie meist den Ball (Band lag bei y 1196).
  `build_episode.py` setzt sie für `"world": true` jetzt automatisch auf y 1460 (über TikToks unterer Leiste, ~1600);
  per `"caption_top"` in narration.json änderbar. Beim Snapshot prüfen, dass Ball und Füße frei bleiben.
- 2026-11-02 · S2E01 · **3D-Folgen künftig 40–50 s**, eine Wendung weniger als S2E01 (78 s hielt absolut länger, aber nur 27 % des Videos).
  Lieber ein Gag weniger als schneller sprechen.
- 2026-11-02 · S2E01 · **Follow-Aufruf gehört in die Handlung**, nicht nur Likes/Kommentare (S2E01: 0 neue Follower). Als Gag zum Thema,
  z. B. "Follow, or Messi just walks." kurz vor dem Loop-Satz, mit sichtbarem Follow-Element im Bild.
- 2026-11-02 · S2E01 · **Aussprache von Namen prüfen.** Kokoro sagt "Real" englisch ("riel"). Lösung über `{shown|spoken}`:
  `{Real|Ray-ahl} Madrid`, `{Bernabéu|Bernabay-oo}`. Bei spanischen/französischen Namen immer eine Lautschrift-Schreibweise setzen.
- 2026-11-02 · S2E01 · **Sprecher nicht zu schnell, nie ohne Pause.** v2 (Tempo 1.1, ~3,4 Wörter/s, lange Sätze am Stück) klang stellenweise
  undeutlich. Vorbild ist die United-Folge (010): kurze Satzstücke, zwischen den Sätzen `||0.15–0.25||`, Tempo ~1.05, Ziel ~2,5 Wörter/s.
  Lieber Füllwörter streichen als schneller sprechen.
- 2026-11-02 · S2E01 · **Neuer Animationsstil ab Staffel 2: 2D-Figuren vor einem echten 3D-Hintergrund** (Referenz: Cartoon mit
  gemalten 3D-Kulissen). Der Creator: "sieht deutlich besser aus". Unsere SVG-Figuren bleiben unverändert, die Welt dahinter ist Three.js
  (Stadion mit Tribünen, Fans, Flutlicht), die Kamera fährt durch den Raum, Hintergrund mit Tiefenunschärfe. Technik: `tools/world3d/`.
- 2026-11-02 · S2E01 · **Roter Faden + flüssige Kamera statt Schnittfolge.** Der Creator vermisste in v1 den roten Faden und Abwechslung
  in der Kameraführung, v1 wirkte "abgeschnitten". Deshalb: eine durchgehende Welt, Szenen als Problem → Lösung → neues Problem,
  ein Callback im Finale (Pass zu sich selbst), Kamerafahrten (Kran, Tracking, Ball-Verfolgung, Orbit, Push-in) mit weichen Übergängen,
  harte Wischer nur bei Szenenwechseln. Ruhig länger (~70 s), wenn es dafür logisch und flüssig ist.
- 2026-11-02 · S2E01 · Gags müssen im Spiel logisch sein: "Doppelpass mit der Bande" und "Schuhe binden, während Real trifft" fand
  der Creator unlogisch. Besser: echte Fußball-Mechanik überspitzen (Pass zu sich selbst, Ecke 10 gegen 1, keine Ersatzbank).
- 2026-11-02 · S2E01 · **Staffel 2 = "volle" Folgen nach Vorbild eines 400k-Like-Videos**: Textschläge "A" / "VS B" in den ersten 2 s,
  Live-Spielbericht (jeder Satz ein Ereignis, alle 1,5–2 s etwas Neues, mehrere Wendungen), volle Bilder (Tribünen mit tausenden Fans,
  Welle, Fahnen, Blitzlichter, ganze Teams mit Nummernschildern, Banden, Konfetti), 2–4 Einstellungen pro Szene (Totale, Nah, Draufsicht,
  Zoom), Sende-Anzeige (Spielstand + Minute + Ausdauerbalken), Abpfiff-Tafel mit absurden Statistiken, "Most liked comment decides
  the next case". Stil (flacher Cartoon, Zittern, Karten, LIVE RECONSTRUCTION, "Could …?") bleibt. Baukasten: `tools/stadium.py`.
  Nummerierung neu: Ordner `episodes/s02eNN-<slug>/`, id "S2E01".
- 2026-11-01 · Zielgruppe: **englischsprachig (UK/US), nicht Deutschland** (Zuschauer waren fast nur deutsch). Inhaltlich: internationale
  Themen (Premier League, CL, Weltstars, Weltgeschichte), keine deutschen Insider (DB, deutsche Spieler) als Hauptgag, US/UK-Stimme,
  englische Captions/Hashtags (#premierleague #football #soccer). Posting-Empfehlung an den Creator: 18–21 Uhr deutscher Zeit.
- 2026-11-01 · 012 · **Cold Open statt Banner-Einstieg** (Grund: 010/011 verlieren die meisten Zuschauer bei 0:01, Ø Watchtime ~10 s):
  Frame 0 zeigt den Höhepunkt MITTEN in der Bewegung (Domino fällt, Grätsche, Karte fliegt), großer Titel mit 3–5 Wörtern
  ("MESSI vs. 380,000 ROMANS") statt dreizeiligem Banner, Impact-Sound in Frame 0, Zähler läuft schon. Dann "Let's go back." (Rückspul-Effekt)
  und die Geschichte im Schnelldurchlauf. In den ersten 5 s alle 1–1,5 s eine Änderung. Kurzfolgen 25–35 s.
  Loop: KEIN Wisch-Übergang mehr (erstes Bild war halb schwarz → sah aus wie Laden). Stattdessen zeigt das letzte Bild (0,4 s)
  dasselbe Motiv wie Frame 0 (`scene(..., loop_out="cut")`, Vorlage `episodes/012-messi-cold/src/cold.py`).
  Kommentar-Karte als konkrete Frage ("Who should Messi dribble past next?"), Follow-Karte mit Serienhinweis ("COULD? case files").
- 2026-10-31 · alle · **Jede Folge ist ein Loop**: Der letzte Satz bleibt offen und läuft in die Frage am Anfang ("… And if anyone asks you:" /
  "So next time someone asks you:" → "Could …?"), damit Zuschauer das Ende nicht merken. Umsetzung: `"loop": true` in narration.json
  (letzte Szene endet 0,3 s nach dem letzten Wort, keine Abblende), `scene(..., loop_in=True)` in s1 (Wisch von rechts herein, kein Punch-in)
  und `scene(..., loop_out=True)` in der letzten Szene (Wisch nach links hinaus). Der Kommentar-Satz/Like-Aufruf kommt VOR den Loop-Satz.
  Ausgenommen (Wunsch): 001 Neuer, 006 Ronaldo.
- 2026-10-31 · 009/010 · **Vorschau-Stimme jetzt Adam** (Kokoro `am_adam`, `"preview_voice": "am_adam"`) statt George. Spricht schneller (~10 %).
- 2026-10-31 · 010 · Aktuelle Spieltags-Kurzfolgen (z. B. nach einer Niederlage) sind gewünscht: echte Szene des Tages als Fakt (Quelle prüfen),
  Pointe als Rechnung ("mit Martínez 2–0, mit dem Baby 1–0"). Der Witz zielt auf die Szene/das Team, nicht auf die Person.
- 2026-10-31 · 009 · **In jeder Folge ein Aufruf zu Liken und Folgen/Abonnieren, gut in die Geschichte eingebaut** (z. B. eine Figur gibt
  Daumen hoch / ein Like-Herz, und der Erzähler sagt trocken etwas wie "Even Atlantis left a like."). Dazu am Ende Karten LIKE · FOLLOW.
- 2026-10-31 · 009 · **Neues Kurzformat (< 30 s) fürs Repertoire**: Hook → Person (1 Satz Stat) → Ziel (1 Satz) → Pointe, in der es klappt
  oder lustig scheitert. Kein gesprochenes Outro; stattdessen Karten "WRITE YOUR SCENARIO IN THE COMMENTS ↓" + Like/Follow.
  Die Pointe greift die Stat aus der Vorstellung logisch wieder auf (De Bruyne findet, was niemand sieht → Atlantis).
- 2026-10-31 · 009 · Keine Witze über Opfer von Verbrechen/Völkermord (Anne-Frank-Idee abgelehnt, Alternative Atlantis gewählt).
- 2026-10-29 · 008 · **Kein Barometer/Stimmungs-Meter** unter den Untertiteln mehr (und keine Sounds dazu), "stört das Video".
  Die untere Hälfte stattdessen mit der Szene selbst füllen (Boden, Menge, Wasser …). Ersetzt die Erfahrung aus 005 (Stimmungs-Barometer).
- 2026-10-29 · 008 · Lieber **kürzer** (008: ~80 s statt 105 s) und vor allem ein **kurzes Ende**. Pointen über bekannte Eigenschaften
  der Person (Tempo, Jubel, Rolle im Verein) kommen besser an als Vertrags-/Verwaltungs-Gags ("das mit dem Vertrag finde ich komisch").
  Ein Schluss, der die Person in ihre Gegenwart zurückholt (Mbappé → Elfmeter bei Real Madrid), ist gewünscht.
- 2026-10-29 · v3/007/008 · **Soundeffekte sparsam und punktuell** (ersetzt "mehr Soundeffekte" vom selben Tag): nur auf echten Ereignissen,
  die dadurch besser werden (Schuss, Netz, Stempel, Aufprall, Pfiff, Galopp, Domino). **Keine Sounds für einfliegende Karten**
  ("durch die Häufigkeit störend"), **keine synthetischen Fan-/Jubel- oder Windgeräusche** ("klingt schlecht, wenig wahrheitsgetreu").
  Richtwert: 1-4 pro Szene, gleiche Sounds höchstens 1-2x pro Szene. Werkzeug: `tools/thin_sfx.py` (`--strict` für dichte Folgen).
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
- 2026-10-28 · ab 003 · **Jede normale Folge (nicht das Kurzformat) endet mit dem Satz: "Could you imagine another scenario that we should do next? Write it in the comments."**
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
- 2026-11-04 · S2E03 Diktator-Mbappé (44,8 s) auf **TikTok** nach ~2 h: 464 Aufrufe, 16 Likes, 0 Kommentare, 0 Shares, 1 Save,
  Ø 14,9 s (33 %), 7,2 % ganz, **7 neue Follower** (bisher bester Wert → Follow-Aufruf in der Mitte wirkt). Publikum wieder **~70 % weiblich**.
  Annahme: Fantasie-/Geschichtssettings (Pamplona, Paris 1789) + Cartoon-Stil lassen TikTok das Video als Animation/Geschichte statt
  Fußball einordnen. → Als Nächstes: Fußball-zentrierte Themen im Stadion, breite Debatten (GOAT, 1 gegen 100), die Kommentare provozieren.
- 2026-11-03 · S2E02 Van Dijk (47 s) auf **TikTok** nach ~7 h: 1.040 Aufrufe, 44 Likes (4,2 %), 0 Kommentare, 3 Shares, 5 Saves,
  Ø **13,9 s (30 %)**, 5,3 % ganz, **0 Follower**. Spitze in Stunde 2, danach Abfall. Erkenntnis: Follow-Gag ganz am Ende sehen nur ~5 %
  → Follow-/Kommentar-Aufruf früher einbauen (Mitte, nach dem ersten Höhepunkt); ohne Kommentar-Frage kommen keine Kommentare.
  **Beibehaltungs-Kurve:** Absturz von 100 % auf ~35 % in den ersten ~4 s (meiste Abbrüche bei 0:01), danach fast flach bis zum Ende.
  → Das Problem ist der Einstieg, nicht die Mitte. Erstes Bild wirkt wie eine Titelkarte (3 Zeilen Text, Figur steht still, Stiere
  klein im Hintergrund). Regel ab jetzt: Bild 1 = Action in Bewegung (Bedrohung groß im Bild), max. 3–4 Wörter Text, erster
  Kamerawechsel nach ≤ 1,5 s, Geräusch ab Frame 0.
  **Publikum:** ~60 % der Aufrufe kamen von Frauen. TikTok hat das Video vermutlich als Reise/Festival/Cartoon statt Fußball
  eingeordnet (Pamplona, Wimpel, Stiere, kein Ball im ersten Bild) – plausibler Teil der Erklärung für den Absturz bei 0:01.
  → Fußball-Signale gezielt setzen: Fußball im ersten Bild (Trikot/Ball/Stadion), Fußballbegriff in Bild 1 + erstem Satz,
  Caption beginnt mit Fußballkontext, Hashtags nischig (#premierleague #liverpoolfc #footballtiktok #epl) statt generisch (#fyp),
  Account-Signale (Fußball-Videos anschauen/kommentieren, Fußball-Accounts folgen).
- 2026-11-03 · S2E01 Short (52 s, 3D, Follow-Gag) auf **YouTube Shorts**: nach 2 h 1.260 Aufrufe, Ø Wiedergabe **0:30 (≈ 58 %)**,
  **44,8 % angesehen / 55,2 % weggewischt** (frühere Folgen ~26 % / 74 %). Bester Wert bisher: 3D-Stil + roter Faden + ~50 s funktioniert.
- 2026-11-02 · S2E01 v3 (3D-Stil, 78 s, gepostet 20:13): nach ~2 h 599 Aufrufe, Ø Wiedergabe **21,4 s** (vorher ~9–10 s),
  6,87 % ganz gesehen, 15 Likes, 3 Kommentare, 6 Shares, 3 Saves, 0 Follower. Absolute Watchtime verdoppelt, relativ (27 %) aber
  unter 010 (37 %). Offen: Wo genau springen die Leute ab (Zuschauerbindungs-Kurve)? Abendliche Postzeit scheint besser zu laufen.
  Nach ~14 h: 957 Aufrufe, Ø 24,9 s, **32 % des Videos** im Schnitt, 8,3 % ganz, 26 Likes, 4 Kommentare, 7 Shares, 4 Saves, 1 Follower.
  Verlauf: Spitze in der 1. Stunde (~330/h), nach ~4 h fast null, nach ~12 h **zweite Welle** (~90/h) – TikTok testet das Video erneut.
- 2026-11-02 · 012 Messi Cold Open (TikTok, ~4 h, gepostet 11:06): 803 Aufrufe, 44 Likes, 0 Kommentare, Ø 9,0 s von 33,5 s, ganz 7,7 %.
  YouTube Shorts: 26 % weiter angesehen / 74 % weggewischt, Ø 15 s. → Cold Open allein hat die Absprungrate NICHT verbessert.
  Verdacht: synthetische Vorschau-Stimme (wird als KI erkannt), zu viel Text im ersten Bild, Posting-Uhrzeit (11 Uhr statt 18–21 Uhr),
  Kommentarfrage erst am Ende (nur ~8 % sehen sie) → als angepinnten eigenen Kommentar posten. Nächster Test: S2E01 (voller Stil) abends.
- 2026-11-01 · 010 (TikTok, ~25 h nach Upload): 1.014 Aufrufe, 60 Likes (5,9 %), 9 Shares, 5 Saves, **0 Kommentare, 0 neue Follower**,
  Ø Wiedergabe 10,1 s von 27,5 s (37 %), ganz angeschaut 15,5 %. Folgerungen:
  → Die ersten 2–3 s entscheiden: sofort Action/Bildwitz zeigen (nicht nur Banner + stehende Figuren), Frage in < 2 s gesprochen.
  → Kommentare kommen nicht von "Write your scenario": eine konkrete, leicht zu beantwortende Frage stellen ("Who should the baby replace next?").
  → Follower: Serien-Gedanke nennen ("Part of the COULD? case files – follow for case 011").
  → Like-Rate ist gut: der eingebaute Like-Gag funktioniert.
- 2026-10-29 · TikTok: Die ersten 4 Uploads direkt nach Kontoerstellung bekamen 0 Aufrufe (Konto galt als Bot). Erstes Video danach:
  800 Aufrufe / 15 Likes nach 3 h. Neue Konten erst "aufwärmen", Uploads verteilen. Re-Uploads alter Folgen als echte neue Fassung (v3):
  neue Erzählerspur, Pflicht-Outro, neuer Einstieg (Punch-in) → `renders/<ep>-v3-final.mp4`.
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
- Zoom auf eine SVG-Gruppe um einen absoluten Punkt: `svgOrigin: "x y"` (transformOrigin in px ist relativ zur Bounding-Box, der Zoom wanderte aus dem Bild).
- Die Loop-Hülle in `scene.py` heißt `<sid>-loopcam`; eigene Gruppen nie `<sid>-cam` nennen (Kollision: ganzes Bild verschob sich, 007 musste neu gerendert werden).
- Nur der Ton geändert? Nicht neu rendern: `tools/remix_audio.py episodes/<ep> <render.mp4> <final.mp4>` mischt Stimme+SFX aus
  index.html neu (inkl. loudnorm, apad auf volle Länge) und kopiert das Bild. Dauert Sekunden statt Minuten.
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
- **3D-Welt (`tools/world3d/`, ab S2E01):** `narration.json` `"world": true` → `build_episode.py` lädt `world/world.html` statt der
  Szenen-Kompositionen. Die Folge hat `world/build.py` (Sprites aus dem Kit) und `world/director.js` (die komplette Handlung als reine
  Funktion der Zeit: Pfade `[t, x, z, ease]` – `"j"` = Sprung ohne Gleiten –, Ball-Segmente, Kamera-Shots mit `blend`/`whip`, Overlays,
  Sprechblasen). Zeiten immer aus den Cues (`c("s3.press")`). Positionen prüfen ohne Render: `node dbg.mjs <ep> <t>`.
  Render dauert ca. 35–40 s pro Videosekunde (Software-GPU), also erst Snapshots, dann einmal komplett rendern.
