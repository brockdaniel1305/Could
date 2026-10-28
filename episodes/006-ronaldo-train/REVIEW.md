# Review – 006 v2 Could Cristiano Ronaldo jump high enough to dodge a moving train?

**Warum v2:** Der Creator fand v1 langweilig, weil von Anfang an klar war, dass Ronaldo es nicht schafft.
v2 ist ein "Best of three" mit Score-Bug (CR7 : TRAINS), bei dem jede Runde anders ausgeht.

## Aufbau
Headline + "Three trains, three rounds, best of three" → Ronaldo (1.87 m, 2.56-m-Kopfball, SIUUU)
→ Runde 1 ICE: 3.9 m Dach vs. 0.7 m, 3 m zu kurz, er rettet sich auf den Bahnsteig, der Zug rauscht durch (0:1)
→ Runde 2 Intercity: Tafel +10 … +47 min → "cancelled", "A train that never arrives cannot hit you" (1:1)
→ Runde 3 Modell-ICE 1:87 auf Bodenhöhe: 4.5 cm, 1 m/s, Zeitlupen-Sprung, das Modell fährt unter ihm durch, 65 cm Luft, SIUUU (2:1)
→ Twist: das Modell hatte +3 min Verspätung, "made in Germany" → Urteil-Stempel "YES." "If the train is small enough. Or late enough."
→ Final score 2:1, SIUUU, "Please do not try this. With any train. Not even a small one." → Pflicht-Outro.

## Geprüft
- `lint` 0/0, `check` ok. Snapshots an 26 Zeitpunkten (u. a. Sprung über das Modell an 4 Zeitpunkten).
- Render 1080×1920, 114.6 s, Ton −14.8 LUFS (true peak −1.5 dB), gemessen, nicht gehört. Frames aus dem MP4 geprüft.
- Stimme: Kokoro-Vorschau, `narration.json` steht auf VoiceStudio `fable`.

## Schwächste Stellen
- Runde 3 zeigt Ronaldo nur ab den Knien (Maßstab 12 px/cm), das Modell ist klein; der Erzähler und die Karten tragen die Szene.
- Der Zug in Runde 2 erscheint nie (das ist der Witz), die Szene lebt nur von Tafel, Uhr und Schlaf-"zzZ".
