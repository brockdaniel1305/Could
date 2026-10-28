# COULD? – Look & Sound

Gebaut mit **HyperFrames** (HTML → Video). Hochformat 1080×1920, 30 fps.

## Layout (TikTok-sicher) – Vollbild-Animation
Die Cartoon-Animation füllt das ganze Bild (1080×1920). Es gibt **kein** Fakten-Panel und keinen Rahmen mehr.
Die Fakten sind Cartoon-Karten, die auf ihrem Wort ins Bild **hineinfliegen**, kurz landen und wieder **hinausfliegen**.

| Bereich | y (px) | Inhalt |
|---------|--------|--------|
| 0–168 | – | nur Himmel o. ä. (TikTok-Statusleiste) |
| 184–270 | oben links | kleines `COULD?`-Logo und `● LIVE RECONSTRUCTION` (Teil der Animation) |
| 300–900 | Himmel | fliegende Karten: Kapitel-Banner (`banner`) und Fakten-Karten (`card`, Varianten `gold`, `red`) |
| 700–1200 | Bühne | die Handlung (Figuren, Schiff, Eisberg) |
| 1196–1320 | Untertitel | Karaoke-Untertitel aus den echten Wort-Timings |
| ab 1330 | Unterwasserwelt / Rasen | nur Bild, kein Text (TikTok-UI): Eisberg unter Wasser, Fische, Strafraum |

- Karten kommen von links, rechts oder oben und verlassen das Bild auf dem gleichen Weg (sie kreuzen sich nie).
- Pro Moment höchstens zwei Karten. Kein Text rechts unter x 960 ab y 700 (TikTok-Buttons).

## Farben & Schrift
- Grund `#0f0e0c`, Creme `#f4efe6`, Gold `#d9a441` / `#f3c55b`, Grau `#8c8476`, Rot (Stempel) `#d6332a`.
- Headline: Playfair Display 700 (`CouldSerif`), Labels: IBM Plex Mono (`CouldMono`), Zahlen und Untertitel: Inter 900.
- Mindestgröße für lesbaren Text: 28 px.

## Cartoon
- Flache Farben, dicke dunkle Outlines `#1a1a2e` (4–6 px), runde Ecken, "kochende" Linien (Turbulenz-Filter, 12 fps).
- Figuren-Bibliothek: `channel/kit/parts/*.svg` (`python3 tools/kit.py --list`). Neue Figuren dort ablegen, damit sie wiederverwendet werden.
- Jede Erzähler-Aussage hat eine sichtbare Aktion auf ihrem Wort (Cue). Reaktionen halten, nicht sofort weiter.
- Figuren schauspielen: Vorbereitung (Ausholen), Aktion, Reaktion (Gesicht wechselt: smile → o → flat), Glieder versetzt bewegen.
- Gegner (Eisberg & Co.) bekommen ein Gesicht und reagieren selbstgefällig.

## Sound
- Stimme: **VoiceStudio** (lokal, eigenes Stimmprofil, `"provider": "voicestudio"`). Vorschau und Fallback: Kokoro `bm_george` (britisch, trocken), Tempo 1.08.
- SFX nur mit Ursache im Bild: `pop` (Badge), `whoosh` (Sprint), `impact-bass-1` (Schlag/Stempel), `ping` (Ziel erreicht). Spitze 1 Frame nach dem Bild.
- Musik: keine eingebaut (keine freie Quelle hier). Entweder `"music": {"src": "assets/music/x.mp3"}` in `narration.json` oder in der TikTok-App einen Sound drunterlegen (hilft auch der Reichweite).
