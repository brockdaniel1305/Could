# COULD? – TikTok-Mockumentary-Kanal

Absurde Fragen. Echte Fakten. Unsinnige Logik. Auf Englisch, im trockenen Doku-Stil.

- [`FORMAT.md`](FORMAT.md) – Format-Bibel: Aufbau, Ton, Regeln
- [`IDEAS.md`](IDEAS.md) – Episoden-Ideen
- `episodes/<nr>-<slug>/script.json` – Skript pro Folge (Szenen + Voice-over + Caption)
- `tools/render.py` – macht aus einem Skript ein fertiges 1080×1920-Video (Stimme, Grafiken, Untertitel, Sound)

## Video rendern

```bash
pip install piper-tts numpy pillow      # einmalig; ffmpeg muss installiert sein
python3 tools/render.py episodes/001-neuer-titanic/script.json
# -> episodes/001-neuer-titanic/001-neuer-titanic.mp4
```

Das Stimmmodell (`en_GB-alan-medium`) wird beim ersten Lauf nach `voices/` geladen.
Optionen: `--music song.mp3` (eigene Musik), `--no-captions`, `--out datei.mp4`.
Fotos/B-Roll: in `script.json` bei einer Szene `"image": "assets/foo.jpg"` eintragen. Das Bild bekommt automatisch einen Archiv-Sepia-Look.

Videos (`*.mp4`), Stimmmodelle und Build-Cache sind per `.gitignore` aus Git ausgeschlossen.
