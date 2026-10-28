# Review – 001 Could Manuel Neuer save the Titanic? (v2, Vollbild)

**Render:** 1080×1920, 30 fps, 110.7 s, H.264/AAC. Ton auf −14.8 LUFS normalisiert (true peak −1.1 dB), gemessen, nicht gehört.
**Stimme in diesem Render:** Kokoro `bm_george` als Vorschau (`--preview`). `narration.json` steht auf VoiceStudio `fable`,
der finale Ton entsteht lokal mit `sh tools/make_episode.sh episodes/001-neuer-titanic`.

## Änderungen gegenüber v1 (Wunsch des Creators)
- Fakten-Panel und Rahmen entfernt: Die Animation läuft im Vollbild.
- Fakten sind Cartoon-Karten, die auf ihrem Wort hineinfliegen und wieder verschwinden. Jede Szene startet mit einem Kapitel-Banner.
- Die untere Bildhälfte zeigt die Unterwasserwelt (90 % des Eisbergs, Fische) bzw. den Strafraum, aus dem Neuer hinausläuft.

## Geprüft
- `lint` und `check`: 0 Fehler, 0 Warnungen.
- 27 Snapshots an Pointen-Zeitpunkten und 6 Frames aus dem fertigen MP4 angesehen.

## Nicht geprüft / offen
- Die VoiceStudio-Stimme selbst: Von der Cloud aus ist die App nicht erreichbar. Mit ihr ändern sich die Timings,
  `build_episode.py` und `build_all.sh` ziehen alle Animationen automatisch nach.
- Wie der Ton klingt (nur gemessen).

## Schwächste Stellen
- s6: Die Wand im Rumpf ist eine große, ruhige Fläche, solange das Wasser noch niedrig steht.
- s5: Das "!!" des Ausgucks steht am rechten Bildrand, der Ausguck selbst ist außerhalb des Bildes.
