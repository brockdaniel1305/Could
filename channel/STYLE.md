# COULD? – Look & Sound

Gebaut mit **HyperFrames** (HTML → Video). Hochformat 1080×1920, 30 fps.

## Layout (TikTok-sicher)

| Bereich | y (px) | Inhalt |
|---------|--------|--------|
| 0–168 | – | frei (TikTok-Statusleiste) |
| 178–240 | Header | `COULD?`-Logo links, `CASE FILE 001` rechts, Haarlinie |
| 262–598 | Fakten-Panel | Kicker (Mono, Gold) · Headline (Serif, Creme) · bis 3 Zeilen Schlüssel/Wert |
| 620–1180 | Bühne | Cartoon 984×560, abgerundet, cremefarbener Rahmen, Label `● LIVE RECONSTRUCTION`, optional Score-Bug oben rechts |
| 1196–1320 | Untertitel | Karaoke-Untertitel aus den echten Wort-Timings (Gold = aktuelles Wort) |
| ab 1330 | nur Deko | TikTok-UI (Caption, Buttons), nur "ABSURD QUESTIONS / SERIOUS ANSWERS" |

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
- Stimme: Kokoro `bm_george` (britisch, trocken), Tempo 1.08. Optional HeyGen- oder ElevenLabs-Stimme, wenn ein Zugang eingerichtet ist.
- SFX nur mit Ursache im Bild: `pop` (Badge), `whoosh` (Sprint), `impact-bass-1` (Schlag/Stempel), `ping` (Ziel erreicht). Spitze 1 Frame nach dem Bild.
- Musik: keine eingebaut (keine freie Quelle hier). Entweder `"music": {"src": "assets/music/x.mp3"}` in `narration.json` oder in der TikTok-App einen Sound drunterlegen (hilft auch der Reichweite).
