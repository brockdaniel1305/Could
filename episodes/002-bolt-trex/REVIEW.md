# Review – 002 Could Usain Bolt beat a T-Rex in a 100 m race?

**Render:** 1080×1920, 30 fps, 110.6 s. Ton −14.9 LUFS (true peak −1.4 dB), gemessen, nicht gehört.
**Stimme in diesem Render:** Kokoro `bm_george` (Vorschau). `narration.json` steht auf VoiceStudio `fable`; lokal `sh tools/make_episode.sh episodes/002-bolt-trex`.

## Aufbau (Wunsch des Creators)
Headline → Bolt (Lane 4) → T-Rex (Lane 5) → 0–30 m Start → 30–80 m Top Speed → 80–100 m Finish → Verdict "YES." mit Twist → Outro.

## Entscheidungen
- Stil von 001 v2 übernommen: Vollbild-Cartoon, fliegende Karten, Kapitel-Banner, Stempel, Karaoke-Untertitel.
- Das Rennen läuft nach einem Modell (Bolts Zwischenzeiten von 2009, T-Rex ~5.4 m/s, 12 m Vorsprung "nose first"), in Zeitlupe mit Rennuhr.
  Führungswechsel bei ~35 m, T-Rex bei 64 m, wenn Bolt ins Ziel kommt: alles aus dem Modell.
- Unten eine Live-Grafik (Balken 0–100 m) statt leerer Bahn.
- Headline "Could …" statt "Can …", passend zum Kanalnamen.

## Geprüft
- `lint`: 0 Fehler. `check`: 0 Fehler, 0 Warnungen. Snapshots an 24 Zeitpunkten und 8 Frames aus dem MP4.

## Schwächste Stellen
- Die Profil-Szenen (s2, s3) spielen am selben Ort wie der Hook, sie leben vom Spotlight und den Karten.
- Beim Übergang in s7 ("One problem" → "No") sind für einen Moment zwei Karten gleichzeitig unterwegs.
