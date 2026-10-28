# COULD? – Format-Bibel

**Kanal-Idee:** Englischsprachige Mockumentary-Shorts. Jede Folge stellt eine absichtlich absurde Frage
(*"Could Manuel Neuer save the Titanic?"*) und beantwortet sie mit todernstem Doku-Ton, echten Zahlen
und vollkommen unsinniger Logik. Das Ereignis läuft dabei als **Cartoon im Vollbild live mit**, die Fakten des Erzählers
fliegen als Karten in die Animation hinein und wieder hinaus.

## Der Witz in einem Satz
Absurde Frage + seriöse Fakten + streng "rationale" Rechnung = Lacher. Der Erzähler lacht **nie**, der Cartoon darf.

## Aufbau jeder Folge (immer gleich)

| # | Szene (id) | Erzähler | Cartoon (live) | Dauer |
|---|-----------|----------|----------------|-------|
| 1 | `s1-hook` | Die Frage wörtlich + "We looked at the evidence. Scientifically. And for far too long." | Beide Parteien + Gegner schon im Bild (Frame 0 = Thumbnail) | 7–9 s |
| 2 | `s2-…` SUBJECT A | Partei A trocken vorstellen, letzte Zeile = Pointe | Partei A in Aktion, Pointe wird gespielt | 12–15 s |
| 3 | `s3-…` SUBJECT B | Partei B genauso; letzte Zeile verbindet beide absurd ("None of them were icebergs.") | B tut, wofür B bekannt ist | 15–19 s |
| 4 | `s4-…` PLAN A | Naheliegend-dummer Versuch: Zahl vs. Zahl → Rechnung → Pointe | Versuch scheitert sichtbar | 13–16 s |
| 5 | `s5-…` PLAN B | Überraschend fast plausibel | Fast-Erfolg, Countdown o. ä. | 15–18 s |
| 6 | `s6-…` PLAN C | Komplett absurd | Eskalation | 13–16 s |
| 7 | `s7-verdict` | Frage wiederholen → Pause → "No." / "Yes." / "Technically." → Trostpreis → zwei Prozentwerte | Roter Stempel knallt aufs Bild | 14–17 s |
| 8 | `s8-outro` | "Who should we send next? Tell us in the comments." | Figuren winken | 4–5 s |

Ziel-Länge: **90–115 s** (über 60 s = Creator-Rewards-fähig).

## Regeln für Skripte
1. **Zahlen sind echt** oder klar als "estimated" markiert. Die Logik ist der Witz, nicht falsche Fakten.
2. **Kurze Sätze.** Punkt. Pause (`||0.5||`). Pointe. Britisches Understatement ("A busy evening, even for Neuer.").
3. **Drei Pläne mit Eskalation:** A = naheliegend-dumm, B = überraschend fast plausibel, C = komplett absurd.
4. **Running Gags des Kanals:** "We looked at the evidence…", der rote Stempel, "Chance he tries anyway: 100 %", ein Score-Bug ("ICEBERG 1 : 0 TITANIC").
5. **Respektvoll bei echten Personen:** über die bekannte Eigenschaft lachen (Torwart, Sprinter, Koch), nie über Privates. Cartoon = Karikatur, keine Fotos.
6. **Fliegende Fakten:** jede Szene beginnt mit einem Kapitel-Banner (z. B. PLAN A / The Punch). Jede Zahl des Erzählers fliegt als Karte auf ihrem Wort ins Bild und fliegt wieder hinaus, sobald die nächste kommt.
7. **Sprech-Markup:** `{1912|nineteen twelve}` (Untertitel/Stimme), `{{cue}}` (Zeitmarke für Animationen), `||0.6||` (Kunstpause).
