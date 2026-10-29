# Review – 007 Could the Roman Empire stop prime Lionel Messi?

**Render:** 1080×1920, 30 fps, 106.4 s. Ton −14.5 LUFS (true peak −1.5 dB), gemessen, nicht gehört.
**Stimme:** Kokoro-Vorschau (bm_george); `narration.json` steht auf VoiceStudio `fable`. Wort-Timings echt (whisper neu gebaut).
**Sound:** 124 Soundeffekte (eigene synthetische Bibliothek `channel/kit/sfx` + HyperFrames-Bibliothek), aus Zeitplan erzeugt (`src/sfx.py`).

## Aufbau (vom Creator freigegebenes Skript, Szene 7 gekürzt)
Hook → Rom (Karte wächst aus Rom, Zähler 380,000, Schilde/Rüstung/Schwerter synchron, Ball wird mit dem Schwert angestupst)
→ Messi (1.70 m Lineal, 8 goldene Bälle, 91 Tore mit Schüssen, GOAT-Ziege, Verteidiger schauen nur zu)
→ Standoff (Schildwand, 380,000 : 1, Augen-Nahaufnahmen, Steppenläufer, Schweißtropfen, Schnürsenkel)
→ Dribbling (8 Römer, echte Tricks: Übersteiger, Täuschung, Tunnel, Drehung; jeder dreht sich und bleibt schwindlig; 9 Tage als Tag/Nacht; Domino bis zum Horizont, 0:1)
→ Testudo (Kamera auf Beinhöhe, Tunnel, Schildkröte zerfällt, 0:2) → Hadrianswall (wächst, Karte 117 km, Freistoß über die Mauer, 0:3)
→ "This is when they all realised that nobody could stop Messi" (weiße Fahne, Stempel UNSTOPPABLE.) → Pflicht-Outro.

## Geprüft
- `lint` 0 Fehler (nur Hinweise "Datei groß"), `check` ok. Snapshots an ~40 Zeitpunkten, 7 Frames aus dem MP4.

## Schwächste Stellen
- Die SFX sind synthetisch (kein echter Jubel/Pfiff aus Aufnahmen), gemessen, aber nicht gehört.
- Im Freistoß-Bild (Weitwinkel, 65 px/m) sind Messi und Ball klein.
