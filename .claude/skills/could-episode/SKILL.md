---
name: could-episode
description: Make a new episode of the "COULD?" TikTok mockumentary channel from a one-line idea ("Could X do Y?", "Neue Folge: …", "Idee: …"), or apply the creator's feedback to an episode and remember it. Builds the English documentary-style vertical video with HyperFrames - narrator voice, live cartoon reconstruction, facts as text, karaoke captions - renders it and records every new preference in channel/LEARNINGS.md so later episodes follow it automatically.
---

# COULD? – Folge aus einer Idee

Der Creator schreibt nur die Idee (z. B. *"Could Usain Bolt outrun a Deutsche Bahn ICE?"*). Du lieferst die fertige Folge
und lernst aus jeder Rückmeldung. Antworte dem Creator auf Deutsch; alles im Video ist Englisch.

## 0. Zuerst lesen, jedes Mal
1. `channel/LEARNINGS.md`: verbindliche Wünsche und Erfahrungen. **Hat Vorrang vor allem anderen.**
2. `channel/FORMAT.md` (Aufbau und Skriptregeln), `channel/STYLE.md` (Layout, Cartoon, Sound), `channel/IDEAS.md`.
3. Die HyperFrames-Skills (`/hyperframes`, `/hyperframes-cli`, `/media-use`) für Vertrag, Lint- und Check-Regeln.
   Die letzte Folge (`episodes/<höchste Nr>/src/`) ist die Referenz-Implementierung.

## 1. Folge anlegen
- Nummer = nächste freie Nummer in `episodes/`, Ordner `episodes/<nnn>-<slug>/` (z. B. `002-bolt-ice`).
- `FACTS.md`: jede Zahl, die im Video vorkommt, mit Quelle (WebSearch, falls verfügbar). Unsichere Zahlen heißen im Skript "estimated".
  Rechnungen (z. B. "3.5 billion footballs") nachrechnen und den Rechenweg notieren.

## 1b. Skript zur Freigabe (Pflicht, seit 007)
Zuerst `SCRIPT.md` schreiben: pro Szene Erzählertext (Englisch) + genaue Beschreibung der Animation (Deutsch), Länge, Caption,
Fakten-Check. Dem Creator im Chat schicken und **auf sein OK warten**. Erst danach `narration.json` und alles Weitere.

## 2. Skript: `narration.json`
Format wie in `episodes/001-neuer-titanic/narration.json`: `id`, `title`, `provider`, `voice`, `speed` (1.08), `caption`
(Posting-Text mit Hashtags, immer `#could`), `scenes[]` mit `id`, `text`, optional `tail` und `sfx`.
- Stimme: `"provider": "voicestudio"` mit `voice` = VoiceStudio-Profil-ID, wenn der Creator VoiceStudio nutzt (läuft nur lokal
  auf seinem Rechner, Port 3900, `VOICESTUDIO_BASE_URL` / `VOICESTUDIO_API_KEY`). Ist es nicht erreichbar, bricht
  `build_episode.py` ab: dann nicht still auf Kokoro wechseln, sondern dem Creator sagen, dass er den Build lokal startet,
  oder mit `"provider": "kokoro"`, `"voice": "bm_george"` eine Vorschau bauen und das klar sagen.
- Szenenfolge und Längen laut FORMAT.md (8 Szenen, 90–115 s).
- Letzte Szene `s8-outro` immer mit genau diesem Text: `Could you imagine another scenario that we should do next? {{c}}Write it in the comments.`
- Markup: `{shown|spoken}`, `{{cue}}` vor jedem Wort, auf dem etwas passieren soll, `||0.4||` nur für echte Pointen-Pausen
  (sparsam, sonst klingt der Erzähler abgehackt).
- Namen und Fremdwörter: neue Namen vorher mit `npx hyperframes tts` + `transcribe` testen; falsch gesprochene in
  `channel/pronunciation.json` eintragen (Lautschrift, z. B. `"Upamecano": "Oopah-mekano"`). Die Untertitel behalten die echte Schreibung.
- `sfx`: `{"name", "cue" oder "at", "offset", "volume"}` aus `channel/kit/sfx/manifest.json` (Cartoon-Bibliothek, zuerst) oder
  `.claude/skills/media-use/audio/assets/sfx/manifest.json`. SFX **sparsam und punktuell** (nur echte Ereignisse, keine Karten-Swooshes, kein synthetischer Jubel/Wind), danach `tools/thin_sfx.py` laufen lassen.
  `offset` so wählen, dass die Spitze des Sounds 1 Frame nach dem Bild liegt (Spitzen: `npx hyperframes audio <file> --json`).

Dann: `python3 tools/build_episode.py episodes/<ep>` (in der Cloud mit `--preview`, dann spricht die Kokoro-Stimme statt VoiceStudio). Das erzeugt Stimme, Wort-Timings und Cue-Zeiten (`timing.json`),
Untertitel, `index.html` und Stub-Szenen. Die Ausgabe listet die Cue-Zeiten je Szene. Gesamtlänge prüfen, sonst Text kürzen.

## 3. Szenen: `episodes/<ep>/src/sN.py` (Vollbild-Cartoon + fliegende Karten)
Jede Szene ist ein kleines Python-Skript mit `from scene import *` (`tools/scene.py`):
`scene(sid, world_svg, js, cards, extra_css="")`.
- `world_svg`: der Cartoon im Vollbild 1080×1920 aus `part("<name>", sid + "-x", WL=…)` (`python3 tools/kit.py --list`).
  Wasserlinie bzw. Boden bei etwa y 1150–1250. Die untere Hälfte füllen (z. B. `iceberg-under`, Fische, Strafraum), dort aber kein Text.
  Fehlt eine Figur oder ein Objekt, zeichne es als neues `channel/kit/parts/<name>.svg` (Kopfkommentar: Ursprung, Größe, animierbare ids).
- `cards`: `banner(sid, name, kicker, title, x, y)` für das Kapitel und `card(sid, name, label, value, x, y, kind)` für jede Zahl.
  Position im Himmel (y 300–900, x 50–900).
- `js`: `fly(name, C.in, C.out, {from: "left"|"right"|"top"})` lässt eine Karte auf ihrem Cue einfliegen und auf dem nächsten
  wieder hinaus (`null` = bleibt bis zum Schnitt). Höchstens zwei Karten gleichzeitig. Weitere Helfer: `pop`, `swap`, `blink`, `waves`, `puffs`, `R`.
- Jede Aussage des Erzählers hat eine Aktion im Cartoon auf ihrem Cue. Die Pointe bekommt eine Reaktion, die gehalten wird.
- Frame 0 (Thumbnail) zeigt schon die Frage als Banner, die Hauptfigur und den Gegner.

`sh episodes/<ep>/src/build_all.sh` schreibt `compositions/*.html`.

## 4. Prüfen
1. `cd episodes/<ep> && npx hyperframes lint` und `npx hyperframes check --json`: alle Fehler beheben, Warnungen abwägen.
2. `npx hyperframes snapshot --at <Cue-Zeiten + 0.5 s>` für jede Pointe, die Bilder ansehen (Kontaktbogen per PIL).
   Achten auf: Überdeckung von LIVE-Label oder Score-Bug, zu kleiner Text, Figuren außerhalb der Bühne, Aktionen zum falschen Wort.
3. Nach dem Render (`render --quality looks`): mit `ffprobe` die Dauer prüfen, mit `npx hyperframes audio <mp4> --json` den Ton.

## 5. Rendern und liefern
Lokal beim Creator erledigt `sh tools/make_episode.sh episodes/<ep>` alles in einem Schritt: VoiceStudio-Stimme, Szenen, Render und Lautheit.
- `npx hyperframes render --quality looks --output renders/<ep>.mp4` (dauert in der Cloud-Sandbox etwa 6 Minuten, im Hintergrund laufen lassen).
- Lautheit auf Social-Niveau bringen: `ffmpeg -i renders/<ep>.mp4 -c:v copy -af loudnorm=I=-15:TP=-1.5:LRA=11 -c:a aac -b:a 192k -movflags +faststart renders/<ep>-final.mp4`
  und mit `npx hyperframes audio … --json` nachmessen (Ziel −16 bis −14 LUFS).
- Dem Creator schicken: Video, Caption mit Hashtags und eine Kurzfassung von `REVIEW.md` (was gemessen wurde und was nicht, die schwächste Stelle).
- `channel/IDEAS.md`: Status der Folge auf ✅ setzen, neue Ideen aus dem Gespräch ergänzen.
- **Folgenarchiv aktualisieren**: `channel/overview/folgen.html` (EPISODES-Liste: Fassung, Länge, Datei, Versionen, Chat-Entscheidungen,
  Caption) und mit dem Artifact-Tool erneut veröffentlichen (gleiche Datei, gleiche URL: https://claude.ai/artifact/USAvCprTbBxbHt4EhtK62A).
- Committen und auf den Arbeitsbranch pushen. Videos, Stimmen und Builds sind per `.gitignore` ausgeschlossen.

## 6. Dazulernen (wichtig)
Jede Rückmeldung des Creators ("zu lang", "mehr Slapstick", "andere Stimme", "nie wieder X") ist eine Regel für die Zukunft:
1. In der aktuellen Folge umsetzen.
2. In `channel/LEARNINGS.md` unter "Wünsche des Creators" mit Datum und Folge eintragen, als allgemeine Regel formuliert.
3. Ist es eine Stil- oder Formatfrage, auch `FORMAT.md`, `STYLE.md` oder den Kit (`scene-template.html`, Parts, `scene.py`) anpassen,
   damit die nächste Folge es von selbst richtig macht.
4. Technische Erkenntnisse (Bug, Workaround) unter "Technik" eintragen.
5. Committen. Widerspricht eine neue Regel einer alten, die alte ersetzen und nicht beide stehen lassen.
