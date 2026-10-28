# COULD? – TikTok-Mockumentary-Kanal

Absurde Fragen. Echte Fakten. Unsinnige Logik. Auf Englisch, im trockenen Doku-Stil. Das Ereignis läuft als Cartoon live mit,
die Fakten des Erzählers erscheinen daneben als Text. Gebaut mit [HyperFrames](https://hyperframes.heygen.com).

## Neue Folge
Dem Claude-Agenten einfach die Idee schreiben, z. B. *"Could Usain Bolt outrun a Deutsche Bahn ICE?"*.
Der Skill [`could-episode`](.claude/skills/could-episode/SKILL.md) macht daraus die fertige Folge und trägt jede Rückmeldung
in [`channel/LEARNINGS.md`](channel/LEARNINGS.md) ein, damit sie ab der nächsten Folge automatisch gilt.

## Aufbau
- `channel/FORMAT.md`: Aufbau jeder Folge und Skriptregeln
- `channel/STYLE.md`: Layout, Farben, Cartoon-Stil, Sound
- `channel/LEARNINGS.md`: Wünsche und Erfahrungen (Vorrang vor allem anderen)
- `channel/IDEAS.md`: Episoden-Ideen
- `channel/kit/`: Szenen-Vorlage, Untertitel, Rahmen, Schriften, Cartoon-Figuren (`parts/*.svg`)
- `episodes/<nr>-<slug>/`: ein HyperFrames-Projekt pro Folge
  - `narration.json`: Skript mit Cues, Pausen und Soundeffekten
  - `src/sN.py`: Quelle der Szenen, `compositions/`: erzeugte Szenen (in der HyperFrames-App bearbeitbar)
  - `FACTS.md`: Zahlen mit Quellen
- `tools/build_episode.py`: Stimme (Kokoro), Wort-Timings, Untertitel und Zeitleiste aus `narration.json`
- `tools/scene.py`, `tools/kit.py`: Szenen-Baukasten

## Von Hand bauen
```bash
npx skills add heygen-com/hyperframes          # einmalig (liegt schon in .claude/skills)
pip install kokoro-onnx soundfile               # Offline-Stimme
python3 tools/build_episode.py episodes/001-neuer-titanic
sh episodes/001-neuer-titanic/src/build_all.sh
cd episodes/001-neuer-titanic
npx hyperframes check
npx hyperframes preview                         # Vorschau zum Bearbeiten
npx hyperframes render --quality looks --output renders/001.mp4
```
